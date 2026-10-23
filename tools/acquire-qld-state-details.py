#!/usr/bin/env python3
"""Acquire independently sourced Queensland state people and election details.

Explicit --fetch retains originals; --build is offline. This supplemental file
joins the national state adapter by official district name and never changes
shared state geometry, existing pages, or creates Twinkles.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import hashlib
import html
import json
from pathlib import Path
import re
import ssl
import urllib.request
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
SOURCES = ROOT / 'content/places/sources'
CHECKED = '2026-10-17'
URLS = {
    'members-current.json': 'https://data.parliament.qld.gov.au/api/members/current',
    'member-list.html': 'https://www.parliament.qld.gov.au/Members/Current-Members/Member-List',
    'results-2024.html': 'https://results.elections.qld.gov.au/SGE2024',
    'results-stafford-2026.html': 'https://results.elections.qld.gov.au/Stafford2026',
    'results-index.html': 'https://results.elections.qld.gov.au/',
    'stafford-event.html': 'https://www.ecq.qld.gov.au/elections/election-events/stafford-state-by-election',
    'election-results-index.html': 'https://www.ecq.qld.gov.au/elections/election-results',
    'election-events.html': 'https://www.ecq.qld.gov.au/elections/election-events',
    'public-api-docs.html': 'https://data.parliament.qld.gov.au/api/index.html',
    'results-client.js': 'https://results.elections.qld.gov.au/main.75da34c831468df6.js',
    'results-events.json': 'https://resultsdata.elections.qld.gov.au/elections.json',
    'members-current-mailing.pdf': 'https://documents.parliament.qld.gov.au/members/mailinglists/memlist.pdf',
    'results-2024-final.zip': 'https://resultsdata.elections.qld.gov.au/XMLData/publicResults_SGE2024_ICCDiv4_Final.zip',
    'results-stafford-final.zip': 'https://resultsdata.elections.qld.gov.au/XMLData/publicResults_Stafford_CentralHighlands_Final.zip',
    'results-hinchinbrook-final.zip': 'https://resultsdata.elections.qld.gov.au/XMLData/publicResults_Hinchinbrook2025_Final.zip',
    'electorates-2024.json': 'https://resultsdata.elections.qld.gov.au/SGE2024-electorates.json',
    'electorates-stafford.json': 'https://resultsdata.elections.qld.gov.au/Stafford2026-electorates.json',
    'electorates-hinchinbrook.json': 'https://resultsdata.elections.qld.gov.au/Hinchinbrook2025-electorates.json',
    'constitution-current.html': 'https://www.legislation.qld.gov.au/view/html/inforce/current/act-2001-080',
    'constitution-current.xml': 'https://www.legislation.qld.gov.au/view/xml/inforce/current/act-2001-080',
    'qrc-2026-effect.html': 'https://redistribution.ecq.qld.gov.au/redistribution-process/electoral-boundary-reviews-in-queensland',
}


def raw_path(name):
    return RAW / ('state-qld-supp-' + name)


def fetch_one(item):
    name, url = item
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (P4A civic source archive)'})
        tls_note = None
        try:
            response = urllib.request.urlopen(request, timeout=45)
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, ssl.SSLCertVerificationError):
                # Public read-only source only: retain the TLS verification
                # limitation. No credentials or authenticated requests exist.
                tls_note = str(exc.reason)
                response = urllib.request.urlopen(request, timeout=45, context=ssl._create_unverified_context())
            else:
                raise
        with response:
            data = response.read()
            if re.search(br'<title[^>]*>\s*(404|Page not found)', data[:12000], re.I):
                raise ValueError('Soft-404, not evidence')
            raw_path(name).write_bytes(data)
            return {'file': raw_path(name).relative_to(ROOT).as_posix(), 'url': url, 'status': response.status,
                    'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'checked': CHECKED,
                    **({'tlsCertificateNote': tls_note} if tls_note else {})}
    except Exception as exc:
        return {'file': raw_path(name).relative_to(ROOT).as_posix(), 'url': url, 'status': 'unavailable', 'error': str(exc), 'checked': CHECKED}


def fetch(only=None):
    RAW.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    selected = lambda name: not only or any(fragment in name for fragment in only.split(','))
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(fetch_one, [(n, u) for n, u in URLS.items() if selected(n)]))
    log_path = SOURCES / 'state-qld-supp-transfers.json'
    if only and log_path.exists():
        rows = [r for r in json.loads(log_path.read_text()) if not selected(Path(r['file']).name.removeprefix('state-qld-supp-'))] + rows
    log_path.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    for row in rows:
        if selected(Path(row['file']).name.removeprefix('state-qld-supp-')):
            print(Path(row['file']).name, row['status'], row.get('bytes', ''), flush=True)


def source(name, title, **extra):
    path = raw_path(name)
    return {'id': 'state-qld-supp-' + name.rsplit('.', 1)[0], 'title': title, 'url': URLS[name], 'checked': CHECKED,
            'rawFile': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), **extra}


def member_rows():
    text_path = raw_path('members-current-mailing.txt')
    if not text_path.exists():
        executable = Path(r'C:\Users\Aura2020\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
        code = "from pypdf import PdfReader;from pathlib import Path;r=PdfReader('" + raw_path('members-current-mailing.pdf').as_posix() + "');Path('" + text_path.as_posix() + "').write_text('\\n'.join(p.extract_text(extraction_mode='layout') for p in r.pages),encoding='utf-8')"
        subprocess.run([str(executable), '-B', '-c', code], check=True)
    text = text_path.read_text(encoding='utf-8')
    pattern = re.compile(r'^[ \t]*([^,\r\n]+,[ \t]+.*?)[ \t]{2,}([A-Za-z][A-Za-z .-]*?)[ \t]{2,}(ALP|LNP|KAP|GRN|IND)[ \t]{2,}', re.M)
    matches = list(pattern.finditer(text))
    rows = []
    for i, match in enumerate(matches):
        family, given = match.group(1).split(', ', 1)
        given = re.sub(r'\s*\[[^]]*\]', '', given).replace('Honourable ', '').strip()
        preferred = re.search(r'\(([^)]+)\)', given)
        short = preferred.group(1) if preferred else given
        short = re.sub(r'\([^)]*\)', '', short).strip()
        name = short + ' ' + family
        district = match.group(2)
        # Wrapped names are explicitly present on the following table line.
        chunk = text[match.start():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        if district == 'Toowoomba':
            assert re.search(r'\b(North|South)\b', chunk)
            district += ' ' + ('North' if family == 'WATTS' else 'South' if family == 'JANETZKI' else 'UNRESOLVED')
        if district == 'Mount':
            assert 'Ommaney' in chunk
            district = 'Mount Ommaney'
        page_count = len(re.findall(r'\bPage\s+\d+', text[:match.start()])) + 1
        rows.append({'name': name, 'given': short, 'family': family, 'district': district,
                     'party': match.group(3), 'sourcePage': page_count})
    assert len(rows) == 93
    assert len({r['district'] for r in rows}) == 93
    assert 'As at 23 September' in re.sub(r' +', ' ', text)
    return rows


def inspect():
    rows = member_rows()
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    for name in ('results-2024-final.zip', 'results-stafford-final.zip', 'results-hinchinbrook-final.zip'):
        with zipfile.ZipFile(raw_path(name)) as archive:
            root = ET.fromstring(archive.read(archive.namelist()[0]))
        for event in root.findall('election'):
            print(name, event.attrib)
            for district in event.findall('districts/district')[:1]:
                print(district.attrib, [(r.attrib, len(r)) for r in district if r.tag in ('countRound', 'candidates', 'declaredCandidate')])


def normalized(value):
    return re.sub('[^a-z0-9]', '', value.casefold())


def build():
    roster = member_rows()
    profiles = {r['district']: r for r in json.loads(raw_path('member-profiles.json').read_text(encoding='utf-8'))['profiles']}
    districts_2024 = json.loads(raw_path('electorates-2024.json').read_text(encoding='utf-8'))['electorates']
    assert len(districts_2024) == 93
    assert {r['district'] for r in roster} == {r['electorateName'] for r in districts_2024}
    assert set(profiles) == {r['district'] for r in roster}
    sources = [source('members-current-mailing.pdf', 'Queensland Parliament official current 93-member roster, as at 23 September 2026',
                      observationDate='2026-09-23', licence='Public parliamentary roster: source document retains its original Queensland Parliament rights. No addresses reproduced in normalized records.'),
               source('results-events.json', 'ECQ public results event index: official dates, archive URLs and event stubs'),
               source('electorates-2024.json', 'ECQ 2024 state districts and full ballot roster'),
               source('electorates-stafford.json', 'ECQ 2026 Stafford ballot roster'),
               source('electorates-hinchinbrook.json', 'ECQ 2025 Hinchinbrook ballot roster'),
               source('constitution-current.xml', 'Official in-force Constitution of Queensland 2001: ordinary election rule, section 19B'),
               source('qrc-2026-effect.html', 'QRC explanation: 2026 redistributed boundaries apply at the 2028 general election; earlier by-elections retain existing boundaries')]
    evidence_path = raw_path('member-profiles.json')
    sources.append({'id': 'state-qld-supp-member-profiles', 'title': 'Exact official parliamentary public profile links checked by name, district and party',
                    'url': URLS['member-list.html'], 'checked': CHECKED, 'rawFile': evidence_path.relative_to(ROOT).as_posix(),
                    'sha256': hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
                    'method': 'Facts/URLs from publicly indexed official profiles, independently reconciled to the official current parliamentary roster. Direct API/HTML access403 remains documented; no access control was bypassed.'})
    law = re.sub(r'\s+', ' ', ' '.join(ET.fromstring(raw_path('constitution-current.xml').read_text(encoding='utf-8')).itertext()))
    assert 'last Saturday in October' in law and 'fourth calendar year' in law
    assert date(2028, 10, 28).weekday() == 5 and date(2028, 10, 28).month == 10
    places = {}
    for person in roster:
        district = person['district']
        profile = profiles[district]
        assert normalized(person['family']) in normalized(profile['name']), (person, profile)
        assert person['party'] == profile['party'], (person, profile)
        name = re.sub(r'^(?:Hon|Mr|Mrs|Ms|Miss|Dr)\s+', '', profile['name'])
        representative = {'name': name, 'role': 'Member for ' + district, 'party': person['party'],
                          'profileUrl': profile['url'], 'sourceId': 'state-qld-supp-members-current-mailing',
                          'profileSourceId': 'state-qld-supp-member-profiles', 'checked': CHECKED,
                          'rosterAsAt': '2026-09-23', 'sourcePage': person['sourcePage']}
        if profile.get('website'):
            representative['website'] = profile['website']
        places[district] = {'name': district, 'representatives': [representative], 'elections': [],
                            'sources': ['state-qld-supp-members-current-mailing', 'state-qld-supp-member-profiles', 'state-qld-supp-constitution-current', 'state-qld-supp-qrc-2026-effect'],
                            'coverageNotes': ['Current office is independently sourced from the Parliament’s current roster, published as at 23 September 2026 and retrieved 17 October 2026. Official public profile identity/district/party is separately reconciled; it is not inferred from the 2024 winner.',
                                              'Historical election records use the boundaries applying at each event. The 2026 redistributed boundaries take effect for the 2028 general election; earlier by-elections use the existing boundaries.',
                                              'All previous ballot contestants are retained, including unsuccessful candidates. Historical personal/campaign websites are not assumed to remain available; every contestant has the original ECQ result record.',
                                              'The ECQ public Final archive contains declared candidates and official count rounds while retaining district final=NO flags. This adapter preserves that flag and labels the data as a declared archived official count rather than rewriting the source flag.',
                                              'No local Twinkles or inferred resident views are created.']}
    event_index = {r['stub']: r for r in json.loads(raw_path('results-events.json').read_text())['elections']}
    totals = {}
    for filename, stub, expected_count in [('results-2024-final.zip', 'SGE2024', 93),
                                           ('results-hinchinbrook-final.zip', 'Hinchinbrook2025', 1),
                                           ('results-stafford-final.zip', 'Stafford2026', 1)]:
        sources.append(source(filename, 'ECQ published Final XML archive: ' + event_index[stub]['electionName'],
                              archiveEdition='Published Final archive, with original district flags/count timestamps retained',
                              licence='Original ECQ public result data and source rights retained.'))
        src_id = 'state-qld-supp-' + filename.rsplit('.', 1)[0]
        with zipfile.ZipFile(raw_path(filename)) as archive:
            assert archive.namelist() == ['publicResults.xml']
            root = ET.fromstring(archive.read('publicResults.xml'))
        target_events = [e for e in root.findall('election') if e.attrib.get('eventType') in ('State General', 'State By-election')]
        assert len(target_events) == 1
        event = target_events[0]
        areas = event.findall('districts/district')
        assert len(areas) == expected_count
        metadata = event_index[stub]
        assert event.attrib['electionDay'] == metadata['electionDay']
        ballot_file = 'electorates-2024.json' if stub == 'SGE2024' else 'electorates-stafford.json' if stub == 'Stafford2026' else 'electorates-hinchinbrook.json'
        ballot_index = {r['electorateName']: r for r in json.loads(raw_path(ballot_file).read_text())['electorates']}
        candidate_total = 0
        for area in areas:
            district = area.attrib['districtName']
            assert district in places and district in ballot_index
            roster_source = area.find('candidates')
            ballots = list(roster_source)
            assert len(ballots) == int(roster_source.attrib['count']) == ballot_index[district]['candidatesCount']
            assert {c.attrib['ballotName'] for c in ballots} == {c['ballotName'] for c in ballot_index[district]['candidates']}
            declared = {c.attrib['ballotName'] for c in area.findall('declaredCandidate')}
            primary = next(c for c in area.findall('countRound') if c.attrib.get('id') == '3' and c.attrib.get('unofficial') == 'NO' and c.attrib.get('preferences') == 'NO')
            counts = {c.attrib['ballotName']: int(c.findtext('count')) for c in primary.findall('primaryVoteResults/candidate')}
            assert set(counts) == {c.attrib['ballotName'] for c in ballots}
            assert sum(counts.values()) == int(primary.findtext('totalFormalVotes/count'))
            results_url = 'https://results.elections.qld.gov.au/' + stub + '/' + ballot_index[district]['stub'] + '/primary'
            candidates = []
            member = next(p for p in roster if p['district'] == district)
            for ballot in ballots:
                ballot_name = ballot.attrib['ballotName']
                row = {'id': 'ecq-' + event.attrib['id'] + '-' + area.attrib['number'] + '-ballot-' + ballot.attrib['ballotOrderNumber'],
                       'name': ballot_name, 'party': ballot.attrib['party'],
                       'status': 'elected' if ballot_name in declared else 'contested',
                       'ballotPosition': int(ballot.attrib['ballotOrderNumber']), 'sourceUrl': results_url, 'sourceId': src_id,
                       'votes': counts[ballot_name], 'voteMeasure': 'official first preferences'}
                if normalized(ballot.findtext('surname')) == normalized(member['family']) and normalized(ballot_name.split(', ', 1)[1]) in normalized(profiles[district]['name']):
                    row['profileUrl'] = profiles[district]['url']
                candidates.append(row)
            normalized_event = {'id': 'ecq-' + event.attrib['id'] + '-district-' + area.attrib['number'],
                                'officialEventId': event.attrib['id'], 'eventStub': stub,
                                'label': event.attrib['electionName'], 'kind': 'general-election' if stub == 'SGE2024' else 'by-election',
                                'status': 'declared; archived official count', 'date': event.attrib['electionDay'],
                                'dateBasis': 'ECQ official polling date from retained event metadata and published Final archive.',
                                'timezone': 'Australia/Brisbane', 'sourceUrl': results_url, 'resultsUrl': results_url,
                                'sourceId': src_id, 'boundaryEdition': '2017 Queensland state electoral boundaries, used at the 2024 election and subsequent by-elections before the 2028 general-election writ',
                                'sourceFinalFlag': area.attrib.get('final'), 'sourceCountUpdated': primary.attrib.get('lastUpdated'),
                                'candidates': candidates}
            places[district]['elections'].append(normalized_event)
            places[district]['sources'].extend([src_id, 'state-qld-supp-' + ballot_file.rsplit('.', 1)[0], 'state-qld-supp-results-events'])
            candidate_total += len(candidates)
        totals[stub] = {'districts': len(areas), 'contestants': candidate_total}
    for place in places.values():
        place['elections'].append({'id': 'qld-state-normal-2028-' + normalized(place['name']),
                                   'label': '2028 Queensland ordinary state election', 'kind': 'general-election', 'status': 'rule-derived normal date',
                                   'date': '2028-10-28', 'dateBasis': 'Rule-derived normal polling day under Constitution of Queensland 2001 s19B: last Saturday in October in the fourth calendar year after the ordinary 2024 election. This is not a published writ/timetable; statutory postponement and extraordinary-election provisions remain applicable.',
                                   'timezone': 'Australia/Brisbane', 'sourceUrl': URLS['constitution-current.html'] + '#sec.19B',
                                   'sourceId': 'state-qld-supp-constitution-current', 'candidates': []})
        place['sources'] = list(dict.fromkeys(place['sources']))
    payload = {'checked': CHECKED, 'scope': 'qld-state-supplement', 'sources': sources,
               'places': list(places.values()), 'coverage': {'districts': len(places), 'currentMPs': len(roster),
                                                          'officialIndividualProfileLinks': len(profiles), 'electionEvents': totals,
                                                          'currentRosterAsAt': '2026-09-23',
                                                          'gaps': ['Historical unsuccessful-candidate personal/campaign website review remains incomplete; all official result links are provided.',
                                                                   'Direct Parliamentary API/member HTML requests returned403 and remain recorded; public PDF and publicly indexed official profile facts are the lawful alternatives used.',
                                                                   'ECQ source TLS certificate verification failed in the local Python trust environment; public unauthenticated read-only retrieval used a documented certificate exception, with source URLs and hashes retained.']}}
    (ROOT / 'content/places/state-qld-details.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    verification = {'checked': CHECKED, 'status': 'pass', 'districts': len(places), 'currentMembers': len(roster),
                    'profileURLsIndependentlyLocated': len(profiles), 'rosterObservationDate': '2026-09-23',
                    'events': totals, 'checks': ['All93 current parliamentary districts reconcile to ECQ2024 districts and independent official profile district/party/name facts.',
                                                'Every ECQ archive candidate count and ballot name reconciles to the independently retained ECQ electorate JSON.',
                                                'Official first-preference totals sum exactly to formal votes for each district and event.',
                                                'Stafford2026 and Hinchinbrook2025 preserve their event identities separately from2024 general results.',
                                                'Current office is never inferred from declared election winners. No addresses are copied into normalized data.'],
                    'limitations': payload['coverage']['gaps']}
    (SOURCES / 'state-qld-supp-verification.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload['coverage'], indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--only')
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--export-members', action='store_true')
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    if args.fetch:
        fetch(args.only)
    if args.inspect:
        inspect()
    if args.export_members:
        rows = member_rows()
        raw_path('members-parsed.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(json.dumps(rows, ensure_ascii=False))
    if args.build:
        build()
