"""Acquire public TEC Tasmanian council rosters and event-specific ballot facts.

Original pages stay in the local-only research cache; public output is minimal
professional/election facts with source dates and links. TLS checks stay enabled.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import unicodedata
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
CHECKED = '2026-10-17'
MYREPS = 'https://www.tec.tas.gov.au/services/MyReps/Index.php'
RESULTS = 'https://www.tec.tas.gov.au/local-government/elections-2022/results/index.html'


def normal(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub('[^a-z0-9]', '', re.sub(r'\([^)]*\)|\bcity\b|\bcouncil\b', '', value))


def normalize(requests, roster_links):
    places = json.loads((ROOT / 'content/places/councils.json').read_text(encoding='utf-8'))['places']
    parents = {normal(p['name']): p for p in places if p['jurisdiction'] == 'tas' and p['kind'] == 'council'}
    result_sources, records, checks = [], [], []
    by_label = {normal(label): url for label, url in roster_links}
    for key, parent in parents.items():
        url = by_label[key]
        code = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['LGDivision'][0]
        path = RAW / ('tas-council-supp-roster-' + code + '.html')
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        source_id = 'council-tas-my-reps-' + code
        result_sources.append({'id': source_id, 'title': 'TEC MyReps: current ' + parent['name'] + ' council roster (source updated 31 July 2026)', 'url': url, 'checked': CHECKED, 'asAt': '2026-07-31', 'rawFile': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'licence': 'Minimal public professional role/name/link facts extracted. Full source page remains local-only; publisher rights retained.'})
        people = {}
        expected = None
        leadership = []
        coverage_notes = []
        for row in soup.select('div.row'):
            heading = row.find('p', class_='myreps', recursive=False)
            if not heading:
                continue
            role = heading.get_text(' ', strip=True)
            if not any(word in role.lower() for word in ('mayor', 'councillor', 'commissioner')):
                continue
            is_seat_row = 'councillors' in role.lower()
            if is_seat_row:
                count = re.search(r'\d+', role)
                if count:
                    expected = int(count.group())
            for anchor in row.select('div.column a[href]'):
                name = anchor.get_text(' ', strip=True)
                if not name:
                    continue
                # Leadership is a role held within the councillor roster, not an
                # additional seat. In particular a vacant mayoral office must not
                # create an extra councillor vacancy.
                if not is_seat_row:
                    leadership.append((role, name))
                    continue
                original_name = name
                if code == '1801' and name == 'Christians Street':
                    name = 'Christian Street'
                if 'vacan' in name.lower():
                    vacancy = sum('Vacant' in p['name'] for p in people.values()) + 1
                    people['vacancy-' + str(vacancy)] = {'name': 'Vacant councillor position ' + str(vacancy), 'role': 'Councillor vacancy', 'profileUrl': url, 'profileType': 'official current-member roster', 'status': 'Vacant in TEC roster as at31 July 2026: ' + name, 'checked': CHECKED, 'asAt': '2026-07-31', 'sourceId': source_id}
                    continue
                if name not in people:
                    people[name] = {'name': name, 'role': role if 'councillor' not in role.lower() else 'Councillor', 'profileUrl': url, 'website': anchor['href'], 'profileType': 'official current-member roster', 'status': 'TEC current-office roster as at 31 July 2026', 'checked': CHECKED, 'asAt': '2026-07-31', 'sourceId': source_id}
                    if original_name != name:
                        people[name]['sourceName'] = original_name
                        people[name]['nameNote'] = 'TEC councillor row spells Christians Street; its deputy-mayor row and independently published Kingborough Council notice identify Christian Street.'
        for role, name in leadership:
            if 'vacan' in name.lower():
                coverage_notes.append('TEC MyReps lists the ' + role + ' office as vacant as at 31 July 2026: ' + name + ' This leadership vacancy is not an additional councillor seat.')
            elif name not in people:
                raise ValueError('Leadership role has no independently listed councillor seat: ' + parent['name'] + ': ' + name)
            else:
                people[name]['role'] = role
        if code == '1801':
            review_path = ROOT / 'content/places/sources/tas-kingborough-roster-web-review.json'
            review = json.loads(review_path.read_text(encoding='utf-8'))
            review_id = 'council-tas-kingborough-role-review'
            result_sources.append({'id': review_id, 'title': 'Kingborough Council independently published Christian Street name and acting-mayor role', 'url': review['url'], 'checked': CHECKED, 'published': review['published'], 'rawFile': review_path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(review_path.read_bytes()).hexdigest(), 'licence': 'Minimal public professional name and role facts; publisher rights retained.'})
            people['Christian Street']['role'] = 'Deputy Mayor (TEC roster); Acting Mayor (council notice)'
            people['Christian Street']['additionalSourceIds'] = [review_id]
            coverage_notes.append('Kingborough Council notice published 19 June 2026 independently names Acting Mayor Christian Street. Only this explicitly supported TEC spelling discrepancy is corrected; no fuzzy person merging is applied.')
        if not people or (expected is not None and len(people) != expected):
            raise ValueError('Current roster reconciliation failed: ' + parent['name'] + ': ' + str((len(people), expected)))
        events = []
        result_page = next((r for r in requests if r.get('label') and normal(r['label']) == key and '/elections-2022/results/' in r.get('url', '')), None)
        if not result_page:
            # Reuse the separate council adapter's retained original pages.
            result_index = BeautifulSoup((RAW / 'tas-council-supp-results-index.html').read_text(encoding='utf-8'), 'html.parser')
            anchor = next(a for a in result_index.find_all('a', href=True) if normal(a.get_text(' ', strip=True)) == key)
            result_url = urllib.parse.urljoin(RESULTS, anchor['href'])
            result_path = RAW / ('council-tas-2022-' + anchor['href'].split('/')[0] + '.html')
        else:
            result_url, result_path = result_page['url'], ROOT / result_page['rawFile']
        main = result_path.read_text(encoding='utf-8')
        main_soup = BeautifulSoup(main, 'html.parser')
        fragments = [node['w3-include-html'] for node in main_soup.find_all(attrs={'w3-include-html': True})]
        for fragment in fragments:
            if '/elections-2022/results/' not in fragment:
                continue
            fragment_url = urllib.parse.urljoin(result_url, fragment)
            fragment_path = RAW / ('council-tas-2022-fragment-' + urllib.parse.urlsplit(fragment_url).path.replace('/', '-').strip('-'))
            source = BeautifulSoup(fragment_path.read_text(encoding='utf-8'), 'html.parser')
            title = source.find(['h1', 'h2', 'h3', 'h4'])
            title = title.get_text(' ', strip=True) if title else fragment_url.rsplit('/', 1)[-1]
            source_id = 'council-tas-2022-' + parent['id'] + '-' + fragment_url.rsplit('/', 1)[-1].removesuffix('.html')
            result_sources.append({'id': source_id, 'title': 'TEC final 2022 ' + parent['name'] + ' ' + title + ' results', 'url': fragment_url, 'checked': CHECKED, 'rawFile': fragment_path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(fragment_path.read_bytes()).hexdigest(), 'licence': 'Minimal public election-result facts extracted. Full source page remains local-only; publisher rights retained.'})
            elected, excluded = set(), set()
            candidates = []
            for table in source.find_all('table'):
                rows = table.find_all('tr')
                if not rows:
                    continue
                headers = rows[0].get_text(' ', strip=True).lower()
                first_count = next((r for r in rows[1:] if re.search(r'count\s*1.*first preferences', r.get_text(' ', strip=True), re.I)), None)
                if first_count:
                    header_cells, vote_cells = rows[0].find_all(['th', 'td']), first_count.find_all(['th', 'td'])
                    for pos, cell in enumerate(header_cells):
                        name_cell = cell.find(class_='candidate-name-dist')
                        if name_cell and pos < len(vote_cells):
                            name = name_cell.get_text(' ', strip=True)
                            votes = vote_cells[pos].get_text(' ', strip=True).replace(',', '')
                            if ',' in name and votes.isdigit():
                                candidates.append({'name': name, 'status': 'contested this 2022 event', 'votes': int(votes), 'voteMeasure': 'first preferences', 'contest': title, 'sourceId': source_id, 'sourceUrl': fragment_url, 'profileUrl': result_url})
                if 'elected candidates' in headers and 'excluded candidates' in headers:
                    for row in rows[1:]:
                        cells = row.find_all(['th', 'td'])
                        if len(cells) >= 2:
                            elected.add(cells[0].get_text(' ', strip=True))
                            excluded.add(cells[1].get_text(' ', strip=True))
                if 'candidate' in headers and 'votes' in headers and 'percent' in headers:
                    for row in rows[1:]:
                        cells = row.find_all(['th', 'td'])
                        if len(cells) < 2 or not cells[0].get('class') or 'candidate-name' not in cells[0].get('class'):
                            continue
                        name, votes = cells[0].get_text(' ', strip=True), cells[1].get_text(' ', strip=True).replace(',', '')
                        if ',' not in name or not votes.isdigit():
                            continue
                        candidates.append({'name': name, 'status': 'elected in this 2022 contest' if name in elected else 'contested this 2022 event', 'votes': int(votes), 'voteMeasure': 'first preferences', 'contest': title, 'sourceId': source_id, 'sourceUrl': fragment_url, 'profileUrl': result_url})
            text = source.get_text(' ', strip=True)
            match = re.search(r'(\d+)\s+candidates?', text, re.I)
            if not candidates and 'unopposed' in text.lower():
                # The official unopposed names are handled separately after inspection.
                checks.append({'place': parent['id'], 'contest': title, 'status': 'unopposed source needs explicit name extraction', 'url': fragment_url})
            elif not candidates or (match and len(candidates) != int(match.group(1))):
                raise ValueError('Ballot reconciliation failed: ' + parent['name'] + ' ' + title + ': ' + str((len(candidates), match.group(1) if match else None)))
            events.append({'id': source_id, 'label': '2022 ' + parent['name'] + ' ' + title + ' election', 'kind': 'ordinary-' + title.lower().replace(' ', '-'), 'status': 'final', 'date': '2022-10-25', 'dateTime': '2022-10-25T14:00:00+11:00', 'milestoneLabel': 'postal voting closes', 'dateBasis': 'TEC official2022 postal election: poll closed 2pm25October2022. Candidate/result facts are final for this specific contest, not current office.', 'timezone': 'Australia/Hobart', 'sourceUrl': fragment_url, 'resultsUrl': result_url, 'candidates': candidates})
        for section_id, title in [('mayor', 'Mayor'), ('deputy-mayor', 'Deputy Mayor'), ('councillor', 'Councillor')]:
            section = main_soup.find(id=section_id)
            if not section or 'elected unopposed' not in section.get_text(' ', strip=True).lower():
                continue
            names = [node.get_text(' ', strip=True) for node in section.find_all('strong') if ',' in node.get_text(' ', strip=True)]
            if not names:
                raise ValueError('Unopposed result has no explicit candidate: ' + parent['name'])
            source_id = 'council-tas-2022-' + parent['id'] + '-' + section_id + '-unopposed'
            result_sources.append({'id': source_id, 'title': 'TEC 2022 ' + parent['name'] + ' unopposed ' + title + ' declaration', 'url': result_url + '#' + section_id, 'checked': CHECKED, 'rawFile': result_path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(result_path.read_bytes()).hexdigest(), 'licence': 'Minimal public election-result facts extracted; full page local-only.'})
            events.append({'id': source_id, 'label': '2022 ' + parent['name'] + ' ' + title + ' election', 'kind': 'ordinary-' + section_id, 'status': 'final-unopposed', 'date': '2022-10-25', 'dateTime': '2022-10-25T14:00:00+11:00', 'milestoneLabel': 'postal voting closes', 'dateBasis': 'TEC ordinary2022 postal election context; this specific office was declared elected unopposed and no vote count is invented.', 'timezone': 'Australia/Hobart', 'sourceUrl': result_url + '#' + section_id, 'resultsUrl': result_url, 'candidates': [{'name': name, 'status': 'elected unopposed in this2022 contest', 'contest': title, 'sourceId': source_id, 'sourceUrl': result_url + '#' + section_id, 'profileUrl': result_url} for name in names]})
        if len(events) != 3:
            raise ValueError('Expected independently sourced mayor/deputy/councillor contests: ' + parent['name'] + ': ' + str(len(events)))
        records.append({'id': parent['id'], 'representatives': list(people.values()), 'elections': events, 'coverageNotes': coverage_notes, 'sources': [s['id'] for s in result_sources if s['id'] == 'council-tas-my-reps-' + code or s['id'].startswith('council-tas-2022-' + parent['id'] + '-') or (code == '1801' and s['id'] == 'council-tas-kingborough-role-review')]})
    result = {'schemaVersion': 1, 'checked': CHECKED, 'sources': result_sources, 'places': records, 'checks': checks, 'coverage': {'councils': len(records), 'representativeRecords': sum(len(p['representatives']) for p in records), 'events': sum(len(p['elections']) for p in records), 'contestantRecords': sum(len(e['candidates']) for p in records for e in p['elections'])}}
    (ROOT / 'content/places/tas-council-details.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['coverage']))


def fetch(url, suffix, acquire):
    path = RAW / ('tas-council-supp-' + suffix)
    if not path.is_file():
        if not acquire:
            raise ValueError('Missing local research cache: ' + str(path))
        request = urllib.request.Request(url, headers={'User-Agent': 'P4A public civic atlas research/1.0'})
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        with opener.open(request, timeout=65) as response:
            content = response.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquire', action='store_true')
    args = parser.parse_args()
    requests = []
    for url, name in [(MYREPS, 'myreps.html'), (RESULTS, 'results-index.html')]:
        path = fetch(url, name, args.acquire)
        requests.append({'url': url, 'rawFile': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    index = BeautifulSoup((RAW / 'tas-council-supp-results-index.html').read_text(encoding='utf-8'), 'html.parser')
    links = []
    for anchor in index.find_all('a', href=True):
        url = urllib.parse.urljoin(RESULTS, anchor['href'])
        if '/elections-2022/results/' in url and url != RESULTS and anchor['href'].count('/') == 1 and url.endswith('/index.html'):
            links.append((anchor.get_text(' ', strip=True), url))
    links = list(dict.fromkeys(links))
    roster_index = BeautifulSoup((RAW / 'tas-council-supp-myreps.html').read_text(encoding='utf-8'), 'html.parser')
    roster_links = [(option.get_text(' ', strip=True), urllib.parse.urljoin(MYREPS, 'Process.php') + '?' + urllib.parse.urlencode({'LGDivision': option['value'], 'LGGo': 'Go'})) for option in roster_index.select('select[name=LGDivision] option')]

    def download(row):
        label, url = row
        name = ('roster-' + urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['LGDivision'][0] + '.html') if 'Process.php' in url else 'result-' + url.rstrip('/').split('/')[-2] + '.html'
        try:
            path = fetch(url, name, args.acquire)
            return {'label': label, 'url': url, 'rawFile': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        except Exception as exc:
            return {'label': label, 'url': url, 'error': str(exc)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        requests.extend(pool.map(download, roster_links))
    report = {'schemaVersion': 1, 'checked': CHECKED, 'originalsLocalOnly': True, 'requests': requests}
    (ROOT / 'content/places/sources/tas-council-acquisition.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'resultPages': len(links), 'requests': len(requests), 'failed': [x for x in requests if x.get('error')]}))
    normalize(requests, roster_links)


if __name__ == '__main__':
    main()
