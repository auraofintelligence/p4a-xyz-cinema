"""Offline minimal WALGA directory roster normalization.

Use the retained legally public 2026 PDF, with its March 2026 publication
snapshot. PDFium's bounded text preserves kerning and apostrophes that the plain
text extraction loses. Full PDF, extracted columns and rendered review images
remain in raw/, excluded from public packages. This does not acquire any source,
infer current office from election winners, or infer ballot history.
"""
import hashlib
import copy
import json
from pathlib import Path
import re
import unicodedata
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
PDF = RAW / 'council-wa-directory-2026.pdf'
URL = 'https://walga.asn.au/awcontent/Web/Documents/Advocacy/The-Western-Australian-Local-Government-Directory.pdf'
CHECKED = '2026-10-17'
PANEL_STARTS = [19.84, 305.98, 624.13, 908.76]


def key(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    value = re.sub(r'^(?:city|town|shire)\s+of\s+', '', value)
    return re.sub('[^a-z0-9]', '', value)


def bounded(page, left, top, right, bottom):
    textpage = page.get_textpage()
    text = textpage.get_text_bounded(left=left, bottom=page.get_height()-bottom,
                                     right=right, top=page.get_height()-top)
    return [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines() if line.strip()]


def main():
    canonical = json.loads((ROOT / 'content/places/councils.json').read_text(encoding='utf-8'))
    parents = {key(p['name']): p for p in canonical['places']
               if p['jurisdiction'] == 'wa' and p['kind'] == 'council'}
    pdf = pdfium.PdfDocument(str(PDF))
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    sources, records, panels, exclusions, issues = [], [], [], [], []
    name_review_path = ROOT / 'content/places/sources/wa-directory-name-web-review.json'
    name_review = json.loads(name_review_path.read_text(encoding='utf-8'))
    for index in range(7, 42):
        page = pdf[index]
        for base in PANEL_STARTS:
            title = ' '.join(bounded(page, base-1, 20, base+265, 36))
            if not re.match(r'^(?:City|Town|Shire) of ', title):
                continue
            columns = [bounded(page, base-0.5+offset, 98, base+131+offset, 248)
                       for offset in [0, 133.23]]
            lines = []
            for column in columns:
                for line in column:
                    if line.startswith(('Executive Team', 'Council Statistics')):
                        break
                    lines.append(line)
                if any(line.startswith('Executive Team') for line in column):
                    break
            panels.append({'title': title, 'pdfPage': index+1, 'lines': lines})
            parent = parents.get(key(title))
            if not parent:
                exclusions.append({'title': title, 'reason': 'No canonical WA council; external-territory bodies remain out of this scope.'})
                continue
            source_id = 'council-wa-walga-2026-'+parent['featureId']
            source_url = URL+'#page='+str(index+1)
            source = {'id': source_id, 'title': 'WALGA 2026 published '+title+' roster (March2026 snapshot)',
                      'url': source_url, 'checked': CHECKED, 'asAt': '2026-03',
                      'rawFile': PDF.relative_to(ROOT).as_posix(), 'sha256': digest,
                      'licence': 'Minimal public professional name, role and website facts only. Copyrighted WALGA directory, incidental contacts and full source remain local-only.'}
            sources.append(source)
            contact = ' '.join(bounded(page, base+129, 69, base+264, 95))
            website = re.search(r'www\s*\.\s*([\w.\- ]+?)(?:\s|$)', contact.replace('. ', '.'))
            # The PDF publishes the official council site separately from the
            # roster link. Use only this public institutional URL, never contacts.
            website = 'https://www.'+re.sub(r'\s+', '', website.group(1)).rstrip('.') if website else None
            people, pending_role, ward, in_councillors = {}, None, None, False
            role_vacancies = []
            for line in lines:
                if line in ['Mayor', 'Lord Mayor', 'President', 'Deputy Mayor', 'Deputy Major', 'Deputy Lord Mayor', 'Deputy President', 'Commissioner', 'Chair Commissioner']:
                    pending_role = line
                    ward = None
                    continue
                if line in ['Councillors', 'Councilors']:
                    in_councillors = True
                    pending_role = None
                    continue
                if re.search(r'\bWard$', line):
                    ward = line
                    continue
                if line in ['Unexpired Term', 'Vacancy']:
                    issues.append({'place': parent['id'], 'line': line})
                    continue
                names = re.findall(r'(.+?)\s*\((20\d{2})\)(?:\s+|$)', line)
                if not names and (pending_role or in_councillors):
                    names = [(line, None)]
                if not names:
                    issues.append({'place': parent['id'], 'line': line})
                    continue
                for name, term in names:
                    name = name.strip()
                    original_name = name
                    alias = next((f for f in name_review['facts'] if f['placeId']==parent['id'] and f['sourceName']==name), None)
                    if alias:name = alias['name']
                    role = pending_role or 'Councillor'
                    if name.lower() == 'vacant' and pending_role:
                        role_vacancies.append('The directory lists the '+role+' leadership office as vacant. This does not create an additional councillor seat.')
                        continue
                    old = people.get(name)
                    if old:
                        if term and not old.get('termEndYear'):old['termEndYear'] = term
                        if ward:old['wardLabel'] = ward
                        if original_name != name:
                            old['sourceNames'] = list(dict.fromkeys(old.get('sourceNames',[])+[original_name]))
                            old['nameNote'] = 'Exact directory name discrepancy reconciled against the published leadership row and the official council source; no fuzzy merge.'
                        continue
                    record = {'name': name, 'role': role, 'profileUrl': source_url,
                              'profileType': 'official published WALGA roster',
                              'status': 'Published WALGA roster as at March2026; subsequent changes unverified',
                              'sourceId': source_id, 'checked': CHECKED, 'asAt': '2026-03'}
                    if website:record['website'] = website
                    if term:record['termEndYear'] = term
                    if ward:record['wardLabel'] = ward
                    people[name] = record
                pending_role = None
            notes = ['Names and professional roles come independently from the WALGA 2026 directory, which states its information is up-to-date as of March2026. Checking the retained source on 17 October 2026 does not establish subsequent currentness. Individual biographies and later vacancies/replacements are not reconciled.',
                     'Previous2025 local-election contestant ballots remain unintegrated; no historical winner is inferred to hold current office.']
            notes += role_vacancies
            corrections = {('wa-council-57490', 'Lorna Buchan'): ('President', 'Mayor'),
                           ('wa-council-58050', 'Charlie Zannino'): ('Deputy Major', 'Deputy Mayor')}
            for (place_id, name), (printed, correct) in corrections.items():
                if parent['id'] != place_id:
                    continue
                person = people[name]
                if person['role'] != printed:
                    raise ValueError('Printed leadership label changed; review correction: '+place_id)
                review_path = ROOT / 'content/places/sources/wa-directory-role-web-review.json'
                review = json.loads(review_path.read_text(encoding='utf-8'))
                fact = next(r for r in review['facts'] if r['placeId']==place_id)
                review_id = 'council-wa-role-review-'+parent['featureId']
                sources.append({'id': review_id, 'title': 'Official council correction of WALGA printed leadership label: '+name,
                                'url': fact['url'], 'checked': CHECKED, 'rawFile': review_path.relative_to(ROOT).as_posix(),
                                'sha256': hashlib.sha256(review_path.read_bytes()).hexdigest(),
                                'licence': 'Minimal professional name and role facts only; publisher rights retained.'})
                person.update(role=correct, sourceRole=printed, additionalSourceIds=[review_id],
                              roleNote='The directory prints '+printed+'; the official council source independently confirms '+correct+'.')
                if fact.get('profileUrl'):
                    person['profileUrl'] = fact['profileUrl']
                    person['profileType'] = 'official individual council profile'
                notes.append('The printed '+printed+' leadership label for '+name+' is corrected to '+correct+' using the official council source checked 17 October 2026.')
            record = {'id': parent['id'], 'representatives': list(people.values()), 'sources': [source_id], 'coverageNotes': notes}
            record['sources'] += [s['id'] for s in sources if s['id']=='council-wa-role-review-'+parent['featureId']]
            alias_fact = next((f for f in name_review['facts'] if f['placeId']==parent['id']),None)
            if alias_fact:
                review_id = 'council-wa-name-review-'+parent['featureId']
                sources.append({'id': review_id, 'title': 'Official council verification of exact directory name discrepancy',
                                'url': alias_fact['url'], 'checked': CHECKED,
                                'rawFile': name_review_path.relative_to(ROOT).as_posix(),
                                'sha256': hashlib.sha256(name_review_path.read_bytes()).hexdigest(),
                                'licence': 'Minimal public professional name facts; publisher rights retained.'})
                record['sources'].append(review_id)
                people[alias_fact['name']].setdefault('additionalSourceIds',[]).append(review_id)
            override = name_review['currentRosterOverride']
            if parent['id']==override['placeId']:
                review_id = 'council-wa-current-roster-'+parent['featureId']
                sources.append({'id': review_id, 'title': 'Coolgardie official current member directory checked 17 October 2026',
                                'url': override['url'], 'checked': CHECKED, 'rawFile': name_review_path.relative_to(ROOT).as_posix(),
                                'sha256': hashlib.sha256(name_review_path.read_bytes()).hexdigest(),
                                'licence': 'Minimal public professional names and roles; publisher rights retained.'})
                record['sources'].append(review_id)
                record['rosterHistory'] = [{'asAt':'2026-03','sourceId':source_id,'representatives':record['representatives']}]
                record['representatives'] = [{**r, 'sourceId':review_id, 'checked':CHECKED,
                                              'profileUrl':r.get('profileUrl',override['url']),
                                              'profileType':'official individual profile' if r.get('profileUrl') else 'official current-member roster',
                                              'status':'Named in official council directory checked 17 October 2026'} for r in override['people']]
                record['coverageNotes'].append(override['notes'])
            if website:record['officialUrl'] = website
            records.append(record)
    (RAW / 'council-wa-directory-roster-columns.json').write_text(json.dumps(panels, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    found = {r['id'] for r in records}
    missing = [p['id'] for p in parents.values() if p['id'] not in found]
    if missing or issues:
        print(json.dumps({'missing': missing, 'issues': issues, 'records': len(records), 'exclusions': exclusions}, ensure_ascii=True, indent=2))
        raise ValueError('Directory parsing needs explicit source reconciliation; no public supplement written')
    parent_records = {record['id']: record for record in records}
    ward_records, ward_joins = [], []
    for ward in canonical['places']:
        if ward['jurisdiction']!='wa' or ward['kind']!='ward':
            continue
        parent_record = parent_records[ward['parentId']]
        matches = [person for person in parent_record['representatives']
                   if person.get('wardLabel') and key(person['wardLabel'])==key(ward['name'])]
        # Both official parent identity and the full explicit ward label must
        # agree. Similar labels, administrative contexts and council-wide mayors
        # do not get projected. A repeated same-parent ward label is ambiguous.
        siblings = [p for p in canonical['places'] if p.get('parentId')==ward['parentId'] and p['kind']=='ward' and key(p['name'])==key(ward['name'])]
        if len(siblings)!=1:
            raise ValueError('Ambiguous exact WA ward label: '+ward['id'])
        if not matches:
            continue
        ward_records.append({'id':ward['id'],'representatives':copy.deepcopy(matches),'sources':parent_record['sources'],
                             'coverageNotes':['Named ward members are projected only from an explicit WALGA published ward label with one exact parent-and-full-label match. The roster remains the declared March 2026 snapshot; subsequent replacements and individual profiles require separate review.']})
        ward_joins.append({'wardId':ward['id'],'parentId':ward['parentId'],'sourceWardLabels':sorted({p['wardLabel'] for p in matches}),'representativeRecords':len(matches)})
    supplement = {'schemaVersion': 1, 'checked': CHECKED, 'sources': sources, 'places': records+ward_records,
                  'checks': {'sourceSha256': digest, 'pdfPagesRead': '8-42', 'exclusions': exclusions,'exactWardJoins':ward_joins},
                  'coverage': {'councils': len(records), 'parentRepresentativeRecords':sum(len(p['representatives']) for p in records),
                               'wardsWithExactRosterJoin':len(ward_records),'wardRepresentativeRecords':sum(len(p['representatives']) for p in ward_records),
                               'representativeRecords':sum(len(p['representatives']) for p in records+ward_records)}}
    (ROOT / 'content/places/wa-council-details.json').write_text(json.dumps(supplement, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(supplement['coverage']))


if __name__ == '__main__':
    main()
