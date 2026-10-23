"""Offline normalization of the independently browser-downloaded ECQ2024 XML.

Do not use the previously TLS-excepted ballot JSON. The archive was reacquired
through the visible official public results application's ordinary download. Only
local election622 is parsed; state by-elections and venue details are excluded.
"""
import hashlib
import json
from pathlib import Path
import re
import runpy
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-10-17'


def main():
    proof_path=ROOT/'content/places/sources/qld-2024-browser-acquisition.json'
    proof=json.loads(proof_path.read_text(encoding='utf-8'))
    path=ROOT/proof['rawFile']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=proof['sha256']:raise ValueError('Independently downloaded archive changed')
    canonical=json.loads((ROOT/'content/places/councils.json').read_text(encoding='utf-8'))
    namekey=runpy.run_path(str(ROOT/'tools/acquire-council-places.py'))['namekey']
    parents={namekey(p['name']):p for p in canonical['places'] if p['jurisdiction']=='qld' and p['kind']=='council'}
    root=ET.fromstring(zipfile.ZipFile(path).read('publicResults.xml'))
    election=next(e for e in root.findall('election') if e.get('id')=='622')
    sid='council-qld-2024-browser-verified-xml'
    sources=[{'id':sid,'title':'ECQ2024 local election archive independently downloaded through official public browser interface',
              'url':proof['sourcePage'],'checked':CHECKED,'rawFile':path.relative_to(ROOT).as_posix(),'sha256':proof['sha256'],
              'published':election.findtext('generationDateTime'),'licence':'Minimal event-specific names, declared historical outcomes and typed vote facts. Full copyrighted archive and incidental venue/address data remain local-only.'},
             {'id':sid+'-acquisition','title':'Independent official-browser archive acquisition and retained hash',
              'url':proof['sourcePage'],'checked':CHECKED,'rawFile':proof_path.relative_to(ROOT).as_posix(),
              'sha256':hashlib.sha256(proof_path.read_bytes()).hexdigest(),'licence':'Minimal source acquisition facts.'}]
    sources.append({'id':sid+'-tsirc-postponement','title':'Official14 March 2024 Gazette changes Torres Strait Island Regional Council polling day to 23March',
                    'url':proof['postponedPoll']['url'],'checked':CHECKED,'published':proof['postponedPoll']['published'],
                    'rawFile':proof_path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(proof_path.read_bytes()).hexdigest(),
                    'licence':'Minimal official election-calendar fact. Full Gazette publisher rights retained.'})
    patches={};checks=[];total_candidates=0;total_contests=0;official_counts=0;no_counts=0;ward_count=0
    for lga in election.findall('lga'):
        parent=parents[namekey(lga.get('electorateName'))]
        patch=patches.setdefault(parent['id'],{'id':parent['id'],'sources':[s['id'] for s in sources],'elections':[],
            'coverageNotes':['All 2024 local-election ballot names and historical declarations are independently sourced from the ECQ archive downloaded via its official public browser interface. These2024 outcomes do not establish current office; later by-elections/replacements remain separate.']})
        for contest in lga.findall('contest'):
            is_mayor=contest.get('contestType')=='mayor'
            units=[contest] if is_mayor else contest.findall('districts/district')
            for unit in units:
                title='Mayor' if is_mayor else unit.get('districtName')
                code=lga.get('areaCode') if is_mayor else lga.get('areaCode')+str(unit.get('number')).zfill(2)
                event_url='https://results.elections.qld.gov.au/2024QLGE/'+code
                declared={int(c.get('ballotOrderNumber')) for c in unit.findall('declaredCandidate')}
                ballot=unit.find('candidates');entries=ballot.findall('candidate')
                if len(entries)!=int(ballot.get('count')):raise ValueError('XML candidate count mismatch: '+code)
                round=next((r for r in unit.findall('countRound') if r.get('countName')=='Official First Preference Count' and r.get('unofficial')=='NO'),None)
                votes={int(c.get('ballotOrderNumber')):int(c.findtext('count')) for c in round.findall('primaryVoteResults/candidate')} if round is not None else {}
                system=lga.get('votingSystemMayor') if is_mayor else unit.get('votingSystem')
                candidates=[]
                for entry in entries:
                    order=int(entry.get('ballotOrderNumber'))
                    candidate={'name':entry.get('ballotName'),'ballotOrder':order,'status':'declared elected in this2024 event' if order in declared else 'contested this2024 event',
                               'contest':title,'sourceId':sid,'sourceUrl':event_url,'profileUrl':event_url}
                    if entry.get('party'):candidate['party']=entry.get('party')
                    if order in votes:
                        candidate.update(votes=votes[order],voteMeasure='candidate votes in multi-member first-past-the-post contest; multiple votes per formal ballot' if system=='First Past the Post' else 'first preference votes')
                    candidates.append(candidate)
                if round is not None:
                    if len(votes)!=len(entries):raise ValueError('Official count candidate coverage mismatch: '+code)
                    formal=int(round.findtext('totalFormalVotes/count'))
                    if sum(votes.values())!=formal:raise ValueError('Official candidate vote total differs from formal votes: '+code)
                    checks.append({'eventCode':code,'candidateCount':len(entries),'voteTotal':sum(votes.values()),'formalVotes':formal,'sourceId':sid})
                    official_counts+=1
                else:
                    no_counts+=1
                event={'id':parent['id']+'-ordinary-2024-'+code,'label':'2024 '+lga.get('electorateName')+' — '+title,
                       'kind':'ordinary','status':'historical','date':'2024-03-16','timezone':'Australia/Brisbane','milestoneLabel':'ordinary election day',
                       'dateBasis':'ECQ2024 local ordinary election archive; jurisdiction ordinary day16 March 2024. Any council-specific postponed polling day requires its own notice. First preferences are only the expressly official count; no count is invented where absent.',
                       'sourceUrl':event_url,'resultsUrl':event_url,'candidates':candidates,'votingSystem':system,
                       'boundaryEdition':'2024 local election arrangement; later boundary editions and current roles remain separate.'}
                if round is None:event['sourceNote']='The archive lists ballot candidates and declarations but supplies no official first-preference count for this contest. No vote values are invented.'
                if 'Torres Strait Island' in lga.get('electorateName'):
                    event['date']=proof['postponedPoll']['date']
                    event['dateBasis']='Official14 March 2024 Gazette changes the Torres Strait Island Regional Council polling day from 16March to 23 March 2024 because weather prevented mobile polling; the jurisdiction date is not copied into these events.'
                    event['calendarSourceUrl']=proof['postponedPoll']['url']
                patch['elections'].append(event)
                total_contests+=1;total_candidates+=len(entries)
                if not is_mayor and lga.get('electorateType')!='Council - Undivided':
                    wards=[p for p in canonical['places'] if p.get('parentId')==parent['id'] and p['kind']=='ward' and re.match(r'^Division\s+'+re.escape(str(unit.get('number')))+r'(?:\D|$)',p['name'],re.I)]
                    if len(wards)>1:raise ValueError('Ambiguous ward correspondence: '+code)
                    if wards:
                        ward=wards[0];ward_count+=1
                        patches[ward['id']]={'id':ward['id'],'sources':[s['id'] for s in sources],
                            'elections':[{**event,'id':ward['id']+'-ordinary-2024'}],
                            'coverageNotes':['The2024 councillor contest matches this council and official division number. It supplies historical ballots, not a current-office inference.']}
    if (len(election.findall('lga')),total_contests,total_candidates)!=(77,343,1422):raise ValueError('Unexpected official local election archive coverage')
    result={'schemaVersion':1,'checked':CHECKED,'sources':sources,'places':list(patches.values()),'checks':checks,
            'coverage':{'councils':77,'parentContests':total_contests,'parentContestants':total_candidates,'officialFirstPreferenceCounts':official_counts,'contestsWithoutCount':no_counts,'projectedWardContests':ward_count}}
    (ROOT/'content/places/qld-council-ballots.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['coverage']))


if __name__=='__main__':main()
