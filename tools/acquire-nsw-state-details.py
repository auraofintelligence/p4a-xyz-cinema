#!/usr/bin/env python3
"""Retain public official NSW member and election sources; normalize offline.

This adapter only writes its own state-nsw-supp-* sources and supplement.
HTTP access denials are recorded and never worked around.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
SOURCES = ROOT / 'content/places/sources'
CHECKED = '2026-10-17'
URLS = {
    'members.html': 'https://www.parliament.nsw.gov.au/members-and-electorates/members-and-ministers/all-members',
    'results-2023.html': 'https://pastvtr.elections.nsw.gov.au/sg2301/la/results',
    'results-index.html': 'https://elections.nsw.gov.au/elections/past-results/state-election-results',
    'data-2023.html': 'https://www.parliament.nsw.gov.au/parliamentary-business/research-and-library/research-publications-data/2023-nsw-election-analysis-with-supplement-2025',
    'copyright-parliament.html': 'https://www.parliament.nsw.gov.au/about-parliament/copyright-and-conditions-of-use',
    'members-la-march-2026.pdf': 'https://www.parliament.nsw.gov.au/members/downloadables/PublishingImages/Pages/downloadable-lists/List%20of%20Members%20No%2047.pdf',
    'timetable-2027.html': 'https://elections.nsw.gov.au/elections/state-elections/2027-nsw-state-election',
    'results-2023.xlsx': 'https://pastvtr.elections.nsw.gov.au/SG2301/LA/state/SGE%202023%20LA%20Final%20Votes.xlsx',
    'lc-results-2023.html': 'https://pastvtr.elections.nsw.gov.au/SG2301/LC/state/fp_by_grp_and_candidate',
    'lc-check-2023.html': 'https://pastvtr.elections.nsw.gov.au/SG2301/LC/state/cc/fp_summary',
}

def discover():
    registry=raw_path('discovered-urls.json')
    urls=json.loads(registry.read_text()) if registry.exists() else {}
    p=raw_path('results-2023.html')
    if p.exists():
        for path in re.findall(r'href="([^"]+/cc/fp_summary)"',p.read_text()):
            slug=path.split('/')[3]
            urls['result-2023-'+slug+'.html']=urljoin(URLS['results-2023.html'],path)
    p=raw_path('results-index.html')
    if p.exists():
        content=p.read_text()
        for section in re.split(r'<h3[^>]*>',content):
            if not re.match(r'\s*202[45] ',section): continue
            heading=re.sub('<[^>]*>',' ',section.split('</h3>')[0])
            for link in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',section,re.S):
                url,text=link
                if not 'First Preference' in text: continue
                url=html.unescape(url)
                if 'safelinks.protection.outlook.com' in url:
                    from urllib.parse import urlparse,parse_qs
                    url=parse_qs(urlparse(url).query)['url'][0]
                slug=re.sub('[^a-z0-9]+','-',heading.lower()).strip('-')
                urls['by-'+slug+'.html']=url
    registry.write_text(json.dumps(urls,indent=2)+'\n',encoding='utf-8')
    return urls

def raw_path(name):
    return RAW / ('state-nsw-supp-' + name)

def fetch_one(item):
    name, url = item
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (P4A public civic source archive)'})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            if re.search(br'<title[^>]*>\s*(404|Page not found)', data[:12000], re.I):
                raise ValueError('Soft-404, not source evidence')
            raw_path(name).write_bytes(data)
            return {'file':raw_path(name).relative_to(ROOT).as_posix(), 'url':url,'status':response.status,
                    'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'checked':CHECKED}
    except Exception as exc:
        return {'file':raw_path(name).relative_to(ROOT).as_posix(), 'url':url,'status':'unavailable','error':str(exc),'checked':CHECKED}

def fetch(only=None):
    RAW.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    selected = lambda name: not only or any(fragment in name for fragment in only.split(','))
    available={**URLS,**(json.loads(raw_path('discovered-urls.json').read_text()) if raw_path('discovered-urls.json').exists() else {})}
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(fetch_one,[(n,u) for n,u in available.items() if selected(n)]))
    log=SOURCES/'state-nsw-supp-transfers.json'
    if only and log.exists():
        rows=[r for r in json.loads(log.read_text()) if not selected(Path(r['file']).name.removeprefix('state-nsw-supp-'))]+rows
    log.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    for row in rows:
        if selected(Path(row['file']).name.removeprefix('state-nsw-supp-')):
            print(Path(row['file']).name,row['status'],row.get('bytes',''),flush=True)

def clean(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',value))).strip()

def source(name,title,url=None,**extra):
    p=raw_path(name)
    all_urls={**URLS,**json.loads(raw_path('discovered-urls.json').read_text())}
    return {'id':'state-nsw-supp-'+name.rsplit('.',1)[0], 'title':title,
            'url':url or all_urls[name], 'checked':CHECKED,
            'rawFile':p.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**extra}

def ballot(name,url):
    content=raw_path(name).read_text(encoding='utf-8-sig')
    district=clean(re.search(r'State Electoral District of\s+([^<\r\n]+)',content).group(1))
    candidates=[]
    totals=[]
    found=False
    for table in re.findall(r'<table\b[^>]*>(.*?)</table>',content,re.S|re.I):
        if not re.search(r'<th\b[^>]*>\s*Candidate\s*</th>',table,re.I): continue
        for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S|re.I):
            cells=[clean(v) for v in re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S|re.I)]
            if not cells: continue
            if cells[0]=='TOTAL FORMAL VOTES':
                totals.append(int(cells[2].replace(',','')))
                continue
            if len(cells)<3 or not re.fullmatch(r'[\d,]+',cells[2]): continue
            candidates.append({'name':cells[0],'party':cells[1], 'status':'contested',
                               'sourceUrl':url,'votes':int(cells[2].replace(',','')),
                               'voteMeasure':'first-preference votes', 'ballotOrder':len(candidates)+1})
        found=True
        break
    assert found and candidates and len(totals)==1,(name,len(candidates),totals)
    assert sum(c['votes'] for c in candidates)==totals[0],(name,'formal vote mismatch')
    assert 'Check Count Complete' in content,(name,'incomplete check count')
    return district,candidates,totals[0]

def build():
    urls=json.loads(raw_path('discovered-urls.json').read_text())
    profiles=json.loads(raw_path('member-profiles.json').read_text())['records']
    assert len(profiles)==93
    assert len({r['district'] for r in profiles})==93
    assert len({r['profileUrl'] for r in profiles})==93
    profile_source=source('member-profiles.json','NSW Parliament: independent current public profile factual extracts',
                          URLS['members.html'], extractionMethod='Minimal name, public current district role and public profile URL facts extracted from each official profile Current positions table through publicly indexed HTML. Prior positions and biographies excluded.',
                          rightsScope='Facts and links only. No full-page, biography, photo or contact-address republication licence asserted.')
    sources=[profile_source,source('results-index.html','NSW Electoral Commission: state election and by-election history'),
             source('timetable-2027.html','NSW Electoral Commission: 2027 state election key dates')]
    timetable=raw_path('timetable-2027.html').read_text()
    assert '13 March 2027' in timetable and 'Election day' in timetable
    places={}
    for row in profiles:
        assert row['name'] and row['currentPosition']=='Member for '+row['district']
        assert row['currentPositionEvidence'].startswith(row['currentPosition']+'  |')
        member_id=row['profileUrl'].split('=')[-1]
        src={**profile_source,'id':'state-nsw-supp-profile-'+member_id,
             'title':'NSW Parliament: '+row['name']+' current public profile','url':row['profileUrl'],
             'recordDistrict':row['district']}
        sources.append(src)
        rep={'name':row['name'],'role':'Member for '+row['district']+' (Legislative Assembly)',
             'profileUrl':row['profileUrl'],'sourceId':src['id'],'checked':CHECKED}
        if row.get('website'): rep['website']=row['website']
        places[row['district']]={'name':row['district'],'representatives':[rep],'elections':[],
            'coverageNotes':['Serving member independently checked in the official parliamentary profile Current positions table; election winners are historical results, not a current-office roster. Party is omitted where a separate current affiliation source was not retained.']}
    audits=[]
    for name,url in sorted(urls.items()):
        if not name.startswith(('result-2023-','by-')): continue
        district,candidates,total=ballot(name,url)
        assert district in places,(name,district)
        src=source(name,'NSW Electoral Commission: '+district+' official first-preference check count')
        sources.append(src)
        if name.startswith('result-2023-'):
            event_id='nsw-state-2023-SG2301'
            day='2023-03-25'
            label='2023 NSW State election — '+district
            kind='general'
        else:
            event_code=url.split('/')[3]
            day={'SB2401':'2024-06-22','SB2402':'2024-10-19','SB2501':'2025-03-15','SB2502':'2025-09-13'}[event_code]
            event_id='nsw-state-'+event_code.lower()+'-'+re.sub('[^a-z0-9]+','-',district.lower())
            label=day[:4]+' '+district+' State by-election'
            kind='by-election'
        event={'id':event_id,'label':label,'kind':kind,'status':'completed; official check count complete',
               'date':day,'dateBasis':'Official NSW Electoral Commission event and final first-preference check-count reports.',
               'timezone':'Australia/Sydney','sourceUrl':URLS['results-index.html'] if kind=='by-election' else URLS['results-2023.html'],
               'resultsUrl':url,'sourceId':src['id'],'candidates':candidates,'formalVotes':total}
        places[district]['elections'].append(event)
        audits.append({'district':district,'eventId':event_id,'date':day,'candidates':len(candidates),
                       'formalVotes':total,'candidateVotesSum':sum(c['votes'] for c in candidates),'sourceFile':src['rawFile']})
    assert sum(name.startswith('result-2023-') for name in urls)==93
    assert len(audits)==99
    for place in places.values():
        place['elections'].sort(key=lambda e:e['date'],reverse=True)
        place['elections'].append({'id':'nsw-state-2027','label':'2027 NSW State election','kind':'general',
            'status':'scheduled; nominations not yet open','date':'2027-03-13',
            'dateTime':'2027-03-13T18:00:00+11:00','milestoneLabel':'election-day voting closes',
            'dateBasis':'NSW Electoral Commission publishes Saturday 13 March 2027, election-day voting 8am–6pm. Timer targets published 6pm election-day voting close in Australia/Sydney; postal receipt and other deadlines differ.',
            'timezone':'Australia/Sydney','sourceUrl':URLS['timetable-2027.html'],
            'sourceId':'state-nsw-supp-timetable-2027','candidates':[]})
    output={'schemaVersion':1,'checked':CHECKED,'scope':'nsw-state-supplement',
            'sources':sources,'places':sorted(places.values(),key=lambda p:p['name'])}
    (ROOT/'content/places/state-nsw-details.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report={'status':'pass','checked':CHECKED,'scope':'Retained NSW supplemental source transformations and factual joins only',
            'counts':{'districts':len(places),'independentCurrentMembers':len(profiles),'2023DistrictBallots':93,
                      'subsequentByElectionBallots':6,'previousContestants':sum(a['candidates'] for a in audits),
                      'scheduledGeneralElectionDate':'2027-03-13','scheduledVotingClose':'2027-03-13T18:00:00+11:00'},
            'checks':['93 distinct current official profile URLs, each with matching district in Current positions table; no Prior positions accepted.',
                      '93 2023 district reports and six later district by-election reports each parse complete candidate summary; all candidate vote sums equal published total formal votes.',
                      'All normalized vote counts are first-preference check-count votes, independently labelled.',
                      '2027 clock uses published 13 March 2027 election-day 6pm close, Sydney time.'],
            'limitations':['Public profile facts were viewed via indexed official HTML because direct archival HTTP returned403; no denial was bypassed. Minimal factual extraction is retained, not full profile text.',
                          'Current affiliation is omitted where not separately retained. Profiles may change after checked date.',
                          'This supplement covers Legislative Assembly districts. Legislative Council requires a separate statewide record.',
                          'Original official source HTML is retained locally with SHA256 provenance; packaging requires review of its separate rights.'],
            'districtEvents':audits}
    (SOURCES/'state-nsw-supp-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['counts'],indent=2))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--only')
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--discover',action='store_true')
    parser.add_argument('--inspect',action='store_true')
    args=parser.parse_args()
    if args.discover: print(json.dumps(discover(),indent=2))
    if args.fetch: fetch(args.only)
    if args.inspect:
        for name in ('results-index.html','results-2023.html'):
            print(name)
            for m in re.findall(r'href="([^"]+)"',raw_path(name).read_text()):
                if any(x in m.lower() for x in ('fp_summary','2027','xlsx','2025','2024')): print(html.unescape(m))
    if args.build: build()

if __name__=='__main__': main()
