#!/usr/bin/env python3
"""Retain and normalize minimal official NT council details.

Default is offline. --fetch retrieves only declared public URLs with verified
TLS into the ignored local research cache; no denials are bypassed.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import ssl
import urllib.request
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw/council-nt-details'
SOURCES = ROOT / 'content/places/sources'
CHECKED = '2026-10-17'
BASE = 'https://ntec.nt.gov.au/elections/past-elections/past-local-government-elections/2025-local-government-elections'
INDEXES = {
    'nt-councils.html': 'https://nt.gov.au/community/local-councils-remote-communities-and-homelands/local-councils-and-local-authorities',
    'ntec-2025.html': BASE,
    'ntec-2025-results.html': BASE + '/results',
    'ntec-2025-candidates.html': BASE + '/list-of-candidates',
    'ntec-reports.html': 'https://ntec.nt.gov.au/elections/election-events/local-government-election-reports/local-government-election-reports',
    'lgant-councils.html': 'https://lgant.asn.au/member-councils/'
}
COUNCILS = {'alice-springs':'70200','barkly':'70420','belyuen':'70540','central-desert':'70620','coomalie':'70700','darwin':'71000','east-arnhem':'71500','groote-archipelago':'71700','katherine':'72200','litchfield':'72300','macdonnell':'72330','palmerston':'72800','roper-gulf':'73600','tiwi-islands':'74050','victoria-daly':'74550','wagait':'74560','west-arnhem':'74660','west-daly':'74680'}


def clean(value):
    return ' '.join(str(value).replace('\u00ad', '').replace('\ufeff', '').split())


def namekey(value):
    return re.sub('[^a-z0-9]', '', clean(value).lower())


def wardkey(value):
    return namekey(re.sub(r'\bWard\b', '', value, flags=re.I))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def fetch_one(item):
    name, url = item
    path = RAW / name
    try:
        if path.exists():
            raw = path.read_bytes()
            status = 'retained-cache'
        else:
            context = ssl.create_default_context()
            assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
            request = urllib.request.Request(url, headers={'User-Agent': 'P4A public civic source research/1.0'})
            with urllib.request.urlopen(request, timeout=60, context=context) as response:
                raw = response.read()
                status = response.status
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        return {'url': url, 'rawFile': path.relative_to(ROOT).as_posix(), 'checked': CHECKED, 'status': status, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'tlsVerification': 'certificate and hostname verified'}
    except Exception as exc:
        return {'url': url, 'rawFile': path.relative_to(ROOT).as_posix(), 'checked': CHECKED, 'status': 'unavailable', 'error': str(exc)}


def fetch(phase):
    items = INDEXES if phase == 'indexes' else json.loads((SOURCES / ('council-nt-' + phase + '-requests.json')).read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch_one, items.items()))
    target = SOURCES / ('council-nt-' + phase + '-transfers.json')
    if target.exists():
        prior = json.loads(target.read_text(encoding='utf-8'))
        # Never erase a retained transfer or a previous failure audit.
        for row in rows:
            same = [p for p in prior if p['url'] == row['url']]
            if not same or any(p.get('sha256') != row.get('sha256') or p['status'] != row['status'] for p in same):
                prior.append(row)
        rows = prior
    write(target, rows)
    for row in rows:
        print(Path(row['rawFile']).name, row['status'], row.get('bytes', ''), row.get('error', ''), flush=True)


def build():
    from bs4 import BeautifulSoup
    canonical = json.loads((ROOT / 'content/places/councils.json').read_text(encoding='utf-8'))
    urls = json.loads((SOURCES / 'council-nt-rosters-requests.json').read_text(encoding='utf-8'))
    transfers = json.loads((SOURCES / 'council-nt-rosters-transfers.json').read_text(encoding='utf-8'))
    sources = []
    rows = {}
    notes = {}
    roster_history = {}
    def soup(stem):
        path = RAW / (stem + '.html')
        transfer = next(r for r in transfers if r['rawFile'] == path.relative_to(ROOT).as_posix() and r.get('sha256'))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == transfer['sha256'], stem
        sid = 'council-nt-roster-' + stem
        if not any(s['id'] == sid for s in sources):
            sources.append({'id':sid, 'title':'Official NT council published roster: ' + stem.replace('-', ' ').title(), 'url':urls[stem+'.html'], 'checked':CHECKED, 'rawFile':path.relative_to(ROOT).as_posix(), 'sha256':digest, 'retention':'Original HTML stays in ignored local research cache; only public professional names, roles, ward labels and official source/profile links are normalized.'})
        return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    def add(stem, name, role='Councillor', ward=None, profile=None, source_stem=None):
        source_stem = source_stem or stem
        name = clean(name).strip().rstrip('.')
        rows.setdefault(stem, []).append({'name':name,'role':role,'profileUrl':profile or urls[source_stem+'.html'],'profileType':'official individual profile' if profile else 'official council roster','sourceId':'council-nt-roster-'+source_stem,'checked':CHECKED, **({'wardLabel':clean(ward)} if ward else {}), **({'status':'vacant'} if re.search(r'vacant|vacancy',name,re.I) else {})})
    for stem in ('alice-springs','katherine','tiwi-islands'):
        for name in soup(stem).select('.profile-manager-name'):
            card = name.parent.parent.parent
            raw_name = clean(name.get_text(' ',strip=True))
            title = re.match(r'^(Deputy Mayor|Mayor|Councillor)\s+', raw_name)
            role = title[1] if title else clean(card.select_one('.profile-manager-type').get_text(' ',strip=True))
            label = card.select_one('.profile-manager-ward')
            profile = card.find('a',href=True)
            add(stem, re.sub(r'^(Deputy Mayor|Mayor|Councillor)\s+', '', raw_name), role, re.sub(r'^Ward:\s*','',label.get_text(' ',strip=True)) if label else None, urljoin(urls[stem+'.html'],profile['href']))
    for heading in soup('barkly').select('h3.caption-title'):
        label = clean(heading.get_text(' ',strip=True))
        role = 'Mayor' if label.startswith('Mayor ') else 'Deputy Mayor' if 'Deputy Mayor' in heading.parent.get_text(' ',strip=True) else 'Councillor'
        body = heading.parent.get_text(' ',strip=True)
        ward = re.search(r'Member for ([A-Za-z ]+?)(?: &| Button|$)',body)
        link = heading.parent.find('a',href=True)
        add('barkly',re.sub(r'^(?:Mayor|Cr\.?)[ ]+', '',label),role,ward[1] if ward else None,urljoin(urls['barkly.html'],link['href']) if link and link['href']!='#' else None)
    s = soup('central-desert')
    for h in s.find_all('h3'):
        label = clean(h.get_text(' ',strip=True))
        match = re.match(r'^(.+?) (Deputy President|President|Councillor)$',label)
        if match:
            ward = h.find_previous('h2').get_text(' ',strip=True)
            if ward.endswith(' Ward'):
                add('central-desert',match[1],match[2],ward)
    text = soup('coomalie').get_text(' ',strip=True)
    for role,name in re.findall(r'(Deputy President|President|Councillor) ([A-Za-z ]+?) - Email:',text):
        add('coomalie',name,role)
    s = soup('darwin')
    for node in s.select('script,style,header,footer,nav'):
        node.decompose()
    text = s.get_text(' ',strip=True)
    for ward, names in re.findall(r'(Chan|Lyons|Richardson|Waters) Ward \1 Ward comprises.*?Your local elected members are (.*?)(?=(?:Chan|Lyons|Richardson|Waters) Ward| Elections)',text):
        # The source publishes an explicit name list; validate reviewed literals
        # below against the matching ward paragraph rather than guessing token boundaries.
        reviewed = {'Chan':['Julie Fraser','Clarence McCarthy-Grogan','Peter Pangquee'],'Lyons':['Nicole Brown','Mick Palmer','Sam Weston'],'Richardson':['Jimmy Bouhoris','Shani Carson','Edwin Joseph'],'Waters':['Kim Farrar','Sylvia Klonaris','Patrik Ralph']}[ward]
        assert clean(names) == ' '.join(reviewed), (ward,names)
        for name in reviewed:
            add('darwin',name,'Councillor',ward+' Ward')
    assert len(rows.get('darwin',[])) == 12
    mayor = soup('darwin-lord-mayor').get_text(' ',strip=True)
    assert 'Lord Mayor of Darwin, the Honourable Peter Styles' in mayor
    add('darwin','Peter Styles','Lord Mayor',profile=urls['darwin-lord-mayor.html'],source_stem='darwin-lord-mayor')
    text = clean(soup('east-arnhem').get_text(' ',strip=True))
    reviewed = {'Birr Rawarrang':['Jason Mirritjawuy','David Warraya'],'Gumurr Gattjirrk':['Lapulung Dhamarrandji','Ganygulpa Dhurrkay'],'Gumurr Marthakal':['Stephen Dhamarrandji','Evelyna Dhamarrandji','Cyril Bukulatjpi'],'Gumurr Miwatj':['Marrpalawuy Marika','Priscilla Yunupingu','Lirrpiya Mununggurr'],'Gumurr Miyarrka':['Bandi Bandi Wunungmurra','Bobby Wunungmurra']}
    assert 'President Lapulung Dhamarrandji' in text
    for ward,names in reviewed.items():
        # Source ward sections precede each explicit councillor paragraph.
        start = text.index(ward+' Ward The ')
        end = text.find('Ward The ',start+len(ward)+12)
        paragraph = text[start:end] if end!=-1 else text[start:]
        for name in names:
            assert name in paragraph,(ward,name)
            add('east-arnhem',name,'President' if name=='Lapulung Dhamarrandji' else 'Councillor',ward+' Ward')
    ward = None
    for node in soup('groote-archipelago').find_all(['h3','p']):
        value = clean(node.get_text(' ',strip=True))
        if re.fullmatch(r'(Central|East|West) Ward',value):
            ward = value
        match = re.fullmatch(r'(Deputy Mayor|Mayor|Cr) (.+)',value)
        if match and ward:
            add('groote-archipelago',match[2],match[1] if match[1]!='Cr' else 'Councillor',ward)
    for heading in soup('litchfield').find_all('h4'):
        role = clean(heading.find_previous('h3').get_text(' ',strip=True))
        if role=='Mayor' or re.fullmatch(r'(North|Central|South) Ward Councillor',role):
            add('litchfield',heading.get_text(' ',strip=True),'Mayor' if role=='Mayor' else 'Councillor',role.removesuffix(' Councillor') if role!='Mayor' else None)
    for heading in soup('macdonnell').find_all('h2'):
        label = clean(heading.get_text(' ',strip=True))
        match = re.fullmatch(r'(Deputy President|President|Councillor) (.+)',label)
        if match or label=='Vacancy':
            add('macdonnell',match[2] if match else 'Vacant seat',match[1] if match else 'Councillor',heading.find_next('h4').get_text(' ',strip=True))
    notes['macdonnell'] = ['Published roster has eleven named people and an explicit Iyarrka vacancy. Its introductory general-election date and resignation narrative are stale or inconsistent with its individual cards; the displayed roster is retained as a dated published snapshot, without asserting that every sentence is current.']
    for heading in soup('palmerston').find_all('h3'):
        match = re.fullmatch(r'(Deputy Mayor|Mayor|Councillor) (.+)',clean(heading.get_text(' ',strip=True)))
        if match:
            container = heading.find_parent(class_='views-row') or heading.parent.parent
            profile = container.find('a',href=True)
            add('palmerston',match[2],match[1],profile=urljoin(urls['palmerston.html'],profile['href']) if profile else None)
    for heading in soup('roper-gulf').find_all('h3'):
        name = clean(heading.get_text(' ',strip=True))
        role_node = heading.find_next('h4')
        if not role_node or clean(role_node.get_text(' ',strip=True)) not in ('Mayor','Deputy Mayor','Councillor'):
            continue
        para = clean(role_node.find_next('p').get_text(' ',strip=True))
        ward = re.search(r'represents the (?:\s*)(.+? Ward)',para)
        assert ward,(name,para)
        add('roper-gulf',name,role_node.get_text(' ',strip=True),ward[1])
    notes['roper-gulf'] = ['Official roster page last updated 26 August 2026; the current Yugul Mangi listings are Michelle Farrell and Olga Daniels. Earlier 2025 winners and vacancies are not used as current office evidence.']
    for heading in soup('victoria-daly').select('h4.et_pb_module_header'):
        match = re.fullmatch(r'(Deputy Mayor|Mayor|Councillor) (.+)',clean(heading.get_text(' ',strip=True)))
        if match:
            para = clean(heading.parent.get_text(' ',strip=True))
            ward = re.search(r'represents the (.+? Ward)',para)
            assert ward,para
            add('victoria-daly',match[2],match[1],ward[1])
    notes['victoria-daly'] = ['Published roster currently supplies four names, with no Milngin member listed. Do not infer an incumbent or a vacancy solely from that omission. The source describes Yvette Williams as deputy for a one-year term from 18 September 2025; that stated term has expired, so the role below is retained only as the published roster label and requires a fresh council appointment record.']
    for person in rows.get('victoria-daly',[]):
        if person['name']=='Yvette Williams':
            person['role']='Councillor'
            person['sourceRoleLabel']='Deputy Mayor (published one-year term from 18 September 2025; renewal unverified)'
    for heading in soup('west-daly').find_all('h4'):
        label = clean(heading.find_next('p').get_text(' ',strip=True)) if heading.find_next('p') else ''
        match = re.fullmatch(r'(Deputy Mayor|Mayor|Councillor) - (.+? Ward)',label)
        if match:
            add('west-daly',heading.get_text(' ',strip=True),match[1],match[2])
    expected = {'alice-springs':9,'barkly':13,'central-desert':12,'coomalie':6,'darwin':13,'east-arnhem':12,'groote-archipelago':7,'katherine':7,'litchfield':7,'macdonnell':12,'palmerston':8,'roper-gulf':13,'tiwi-islands':12,'victoria-daly':4,'west-daly':6}
    for stem,count in expected.items():
        assert len(rows.get(stem,[]))==count,(stem,len(rows.get(stem,[])),count)
        assert len({namekey(p['name']) for p in rows[stem]})==count,stem
    # Web-readable West Arnhem is a minimal factual extract, clearly distinct
    # from an original HTML download that failed certificate validation.
    review_path = SOURCES / 'council-nt-web-roster-review.json'
    if review_path.is_file():
        review = json.loads(review_path.read_text(encoding='utf-8'))
        for item in review['councils']:
            stem = item['key']
            sid = 'council-nt-roster-'+stem
            sources.append({'id':sid,'title':'Official published roster minimal web review: '+stem,'url':item['url'],'checked':CHECKED,'rawFile':review_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'verificationMethod':review['method']})
            for row in item.get('representatives',[]):
                add(stem,row['name'],row['role'],row.get('wardLabel'))
            notes[stem] = item['notes']
    later_path = SOURCES / 'council-nt-later-office-review.json'
    later = json.loads(later_path.read_text(encoding='utf-8'))
    correction = later['tiwi']
    prior = [dict(p) for p in rows['tiwi-islands']]
    vacancies = [p for p in rows['tiwi-islands'] if p.get('status')=='vacant' and wardkey(p.get('wardLabel',''))==wardkey(correction['wardLabel'])]
    assert len(vacancies)==1, vacancies
    rows['tiwi-islands'].remove(vacancies[0])
    sid = 'council-nt-tiwi-milikapiti-council-declaration-2026'
    sources.append({'id':sid,'title':'Tiwi council dated Milikapiti declaration announcement','url':correction['councilUrl'],'checked':CHECKED,'published':correction['published'],'rawFile':later_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(later_path.read_bytes()).hexdigest(),'verificationMethod':later['method']})
    rows['tiwi-islands'].append({'name':correction['name'],'role':correction['role'],'wardLabel':correction['wardLabel'],'profileUrl':correction['councilUrl'],'profileType':'official council dated announcement','sourceId':sid,'asAt':correction['published'],'checked':CHECKED})
    roster_history['tiwi-islands'] = [{'label':'Published roster snapshot with stale Milikapiti vacancy','checked':CHECKED,'sourceId':'council-nt-roster-tiwi-islands','representatives':prior,'coverageNote':'Superseded for the Milikapiti vacancy by the independently dated 19 August 2026 council declaration announcement, corroborated by NTEC. This retains what the roster page actually displayed.'}]
    notes['tiwi-islands'] = ['The roster page still displays a Milikapiti vacancy. The dated council announcement, including its full article read in the ordinary browser, independently confirms Norman James Tipiloura elected to this ward on 19 August 2026, corroborated by NTEC. Current office is recorded as at that announcement; the stale roster is retained in rosterHistory.']
    notes['victoria-daly'].append('Independent NTEC event page updated 24 August 2026 confirms the Milngin casual vacancy received zero nominations; a replacement election date was not yet announced. No current member is inferred for that ward.')
    places = []
    source_ids = {s['id'] for s in sources}
    joins = []
    for stem,reps in rows.items():
        parent = 'nt-council-'+COUNCILS[stem]
        place = {'id':parent,'jurisdiction':'nt','kind':'council','officialUrl':urls[stem+'.html'],'sources':list(dict.fromkeys(r['sourceId'] for r in reps)),'representatives':reps,'elections':[],'coverageNotes':['Dated official council roster snapshot checked 17 October 2026, independently of election results. Full original pages, contacts and biographies remain local-only. Individual profile URLs are retained where explicitly supplied; a roster link is labelled as such.']+notes.get(stem,[])}
        assert all(r['sourceId'] in source_ids for r in reps)
        if stem in roster_history:
            place['rosterHistory'] = roster_history[stem]
        places.append(place)
        for ward in [p for p in canonical['places'] if p.get('parentId')==parent and p['kind']=='ward']:
            members = [dict(r) for r in reps if r.get('wardLabel') and wardkey(r['wardLabel'])==wardkey(ward['name'])]
            if members:
                places.append({'id':ward['id'],'jurisdiction':'nt','kind':'ward','parentId':parent,'sources':list(dict.fromkeys(r['sourceId'] for r in members)),'representatives':members,'elections':[],'coverageNotes':['Current council roster explicitly identifies this ward; join uses the verified parent plus an exact punctuation/spacing-normalized ward label. A council-wide mayor is not assigned to a ward without an explicit source ward label.']+notes.get(stem,[])})
                if stem in roster_history:
                    places[-1]['rosterHistory'] = [{**snapshot,'representatives':[r for r in snapshot['representatives'] if wardkey(r.get('wardLabel',''))==wardkey(ward['name'])]} for snapshot in roster_history[stem]]
                joins.append({'parentId':parent,'wardId':ward['id'],'sourceWardLabels':sorted({r['wardLabel'] for r in members}),'representativeRecords':len(members)})
        unmatched = [r['wardLabel'] for r in reps if r.get('wardLabel') and not any(wardkey(r['wardLabel'])==wardkey(p['name']) for p in canonical['places'] if p.get('parentId')==parent)]
        assert not unmatched,(stem,unmatched)
    ballots_path = SOURCES / 'council-nt-2025-ballot-web-review.json'
    ballots = json.loads(ballots_path.read_text(encoding='utf-8'))
    assert len(ballots['contests']) == ballots['expectedContests'] == 54
    assert sum(len(c['names']) for c in ballots['contests']) == ballots['expectedCandidateRecords'] == 271
    by_id = {p['id']:p for p in places}
    all_contests = [{**c,'date':ballots['eventDate'],'kind':'ordinary','edition':'ordinary-2025','dateBasis':ballots['dateBasis'],'reviewPath':ballots_path,'method':ballots['method']} for c in ballots['contests']]
    other_path = SOURCES / 'council-nt-other-ballot-web-review.json'
    other = json.loads(other_path.read_text(encoding='utf-8'))
    # The early later-event extract retains its failed web-read audit. Its
    # seventeen provisional contexts are superseded by complete browser reads.
    later_ballots_path = SOURCES / 'council-nt-later-ballot-browser-review.json'
    later_ballots = json.loads(later_ballots_path.read_text(encoding='utf-8'))
    later_editions = {c['edition'] for c in later_ballots['events']}
    all_contests += [{'dateBasis':'Official event-specific NTEC timetable; nomination lists may include uncontested wards and do not establish voting occurred in every contest.',**c,'reviewPath':other_path,'method':other['method']} for c in other['events'] if c['edition'] not in later_editions]
    all_contests += [{**c,'reviewPath':later_ballots_path,'method':later_ballots['method']} for c in later_ballots['events']]
    for contest in all_contests:
        stem = contest['council']
        parent_id = 'nt-council-'+COUNCILS[stem]
        label = contest['label']
        assert len(contest['names']) <= contest['expectedCount']
        assert len(contest['names']) == contest['expectedCount'] or contest.get('candidateListComplete') is False
        assert len({namekey(n) for n in contest['names']}) == len(contest['names'])
        suffix = re.sub('[^a-z0-9]+','-',label.lower()).strip('-')
        sid = ('council-nt-2025-ballot-' if contest['edition']=='ordinary-2025' else 'council-nt-ballot-'+contest['edition']+'-')+stem+'-'+suffix
        review_path = contest['reviewPath']
        date_label = contest['date'] or contest['year']+' (exact election day unresolved)'
        sources.append({'id':sid,'title':'NTEC official historical nominees: '+date_label+' '+stem+' '+label,'url':contest.get('contextUrl',contest['url']),'checked':CHECKED,'rawFile':review_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'verificationMethod':contest['method'],**({'sourcePage':contest.get('page',contest.get('sourcePage'))} if contest.get('page') or contest.get('sourcePage') else {})})
        if contest.get('timetableUrl'):
            sources.append({'id':sid+'-timetable','title':'NTEC event-specific timetable: '+contest['date']+' '+stem,'url':contest['timetableUrl'],'checked':CHECKED,'rawFile':review_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'verificationMethod':contest['method']})
        if parent_id not in by_id:
            place = {'id':parent_id,'jurisdiction':'nt','kind':'council','sources':[],'elections':[],'coverageNotes':['Official event-specific historical nominees are separate from current council office; no current incumbent is inferred.']}
            by_id[parent_id] = place
            places.append(place)
        event = {'id':parent_id+'-'+contest['edition']+'-'+suffix,'label':date_label[:4]+' '+stem.replace('-',' ').title()+' — '+label,'kind':contest['kind'],'status':contest.get('status','historical'),'date':contest['date'],'dateBasis':contest['dateBasis'],'timezone':'Australia/Darwin','milestoneLabel':contest.get('milestoneLabel','election day' if contest['date'] else 'exact election day unresolved'),'sourceUrl':contest.get('contextUrl',contest['url']),'candidates':[{'name':n,'status':'official historical nominee','contest':label,'sourceUrl':contest['url'],'profileUrl':contest['url'],'profileType':'official historical nomination list'} for n in contest['names']],'coverageNotes':['Official nomination-list coverage; first-preference totals, subsequent candidacy, current affiliation and present office are not inferred. An elected outcome is included only where a separate official result is expressly cited.']+contest.get('coverageNotes',[])}
        event['nominationCoverage'] = {'officialCandidateCount':contest['expectedCount'],'retainedCandidateCount':len(contest['names']),'complete':len(contest['names'])==contest['expectedCount']}
        if contest.get('timetableUrl'):
            event['dateSourceUrl'] = contest['timetableUrl']
        if contest.get('result'):
            outcome = contest['result']
            winners = [c for c in event['candidates'] if namekey(c['name'])==namekey(outcome['name'])]
            assert len(winners)==1,outcome
            winners[0].update(status=outcome['status'],resultSourceUrl=outcome['sourceUrl'])
            event['resultsUrl'] = outcome['sourceUrl']
            sources.append({'id':sid+'-result','title':'NTEC separately declared historical result: '+contest['date']+' '+stem,'url':outcome['sourceUrl'],'checked':CHECKED,'sourceUpdated':outcome['sourceUpdated'],'rawFile':review_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'verificationMethod':contest['method']})
        parent = by_id[parent_id]
        contest_sources = [s['id'] for s in sources if s['id']==sid or s['id'].startswith(sid+'-')]
        parent['sources'] = list(dict.fromkeys(parent['sources']+contest_sources))
        parent['elections'].append(event)
        if label.endswith(' Ward'):
            wards = [w for w in canonical['places'] if w.get('parentId')==parent_id and w['kind']=='ward' and wardkey(w['name'])==wardkey(label)]
            assert len(wards)==1,(stem,label,'Exact official ward join failed')
            wid = wards[0]['id']
            if wid not in by_id:
                child = {'id':wid,'jurisdiction':'nt','kind':'ward','parentId':parent_id,'sources':[],'elections':[],'coverageNotes':['Historical ballot joins the verified council parent and exact source ward label; no current officeholder is inferred from the ballot.']}
                places.append(child)
                by_id[wid] = child
            by_id[wid]['sources'] = list(dict.fromkeys(by_id[wid]['sources']+contest_sources))
            by_id[wid]['elections'].append({**event,'id':wid+'-'+contest['edition']})
    for place in places:
        assert len({e['id'] for e in place['elections']}) == len(place['elections'])
    supplement = {'schemaVersion':1,'checked':CHECKED,'scope':'council-nt-details','sources':sources,'layers':[],'places':places}
    output = ROOT / 'content/places/nt-council-details.json'
    write(output,supplement)
    report = {'schemaVersion':1,'checked':CHECKED,'status':'pass','scope':'Retained source hashes, published roster row counts, explicit current ward joins and 2025 nomination-list reconciliation; no national page/browser claim','parentCouncilsWithRoster':len(rows),'parentRepresentativeRecords':sum(len(r) for r in rows.values()),'parentNamedPeople':sum(not re.search(r'vacant|vacancy',p['name'],re.I) for r in rows.values() for p in r),'wardRosterJoins':joins,'historical2025Contests':54,'historical2025NomineeRecordsAtParent':271,'historical2025NomineeRecordsIncludingWardContexts':sum(len(e['candidates']) for p in places for e in p['elections']),'limitations':['Belyuen published page supplies only two apparently stale names inconsistent with the 2025 ballot; no current roster is inferred.','Wagait current page describes its 2025 election winners; current office/leadership requires an independent updated roster, so winners are history only.','Victoria Daly roster omits Milngin and its published deputy term has expired; no replacement or renewed deputy is inferred.','West Arnhem roster introductory 2021 wording is stale; explicit published cards are retained as a snapshot with that conflict disclosed.','2025 nomination lists do not establish all vote totals or declared outcomes. Barkly2024, Groote2025 separate election and later supplementary/by-election ballots require independent event reconciliation.','Original downloaded HTML is local-only, with no contacts or biographies in the normalized supplement.']}
    report.update(historicalContestsAtParents=len(all_contests),historicalNomineeRecordsAtParents=sum(len(c['names']) for c in all_contests),historicalNomineeRecordsIncludingWardContexts=sum(len(e['candidates']) for p in places for e in p['elections']))
    report['historical2025NomineeRecordsIncludingWardContexts'] = sum(len(e['candidates']) for p in places for e in p['elections'] if e['date']=='2025-08-23')
    report['limitations'][-2] = 'All 336 officially counted nominee records are retained. Eleven earlier web-tool cache misses were resolved through normal browser reads. Four contested 2026 contexts have no exact polling day retained, and two failed nomination rounds have no polling date. No missing dates or result totals are inferred.'
    report.update(officialCandidateRecordsExpectedAtParents=sum(c['expectedCount'] for c in all_contests),incompleteCandidateLists=[{'council':c['council'],'ward':c['label'],'url':c['url'],'contextUrl':c.get('contextUrl'),'officialCount':c['expectedCount'],'retainedCount':len(c['names'])} for c in all_contests if len(c['names'])<c['expectedCount']],undatedHistoricalContexts=sum(c['date'] is None for c in all_contests),failedNominationRounds=sum(c.get('status')=='failed-no-nominations' for c in all_contests))
    write(SOURCES/'council-nt-details-verification.json',report)
    print(json.dumps({k:report[k] for k in ('status','parentCouncilsWithRoster','parentRepresentativeRecords','parentNamedPeople')},indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--phase', choices=('indexes', 'rosters', 'results'), default='indexes')
    args = parser.parse_args()
    if args.fetch:
        fetch(args.phase)
    else:
        build()


if __name__ == '__main__':
    main()
