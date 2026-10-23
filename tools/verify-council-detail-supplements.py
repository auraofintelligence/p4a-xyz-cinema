"""Check council supplement source integrity, actual canonical merge and repeatability.

This narrow offline audit does not certify page/browser acceptance or source
currentness beyond the declared snapshots. It never writes canonical data.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
FILES=['tas-council-details.json','wa-council-details.json','sa-council-ballots.json','sa-current-leaders.json','qld-council-ballots.json','qld-current-leaders.json','nt-council-details.json']


def main():
    canonical_path=ROOT/'content/places/councils.json'
    canonical=json.loads(canonical_path.read_text(encoding='utf-8'))
    places={p['id']:p for p in canonical['places']};sources={s['id']:s for s in canonical['sources']}
    issues=[];count=0;hashes={};supplement_checks=[]
    for filename in FILES:
        path=ROOT/'content/places'/filename
        if not path.exists():issues.append('Missing supplement '+filename);continue
        supplement=json.loads(path.read_text(encoding='utf-8'))
        for source in supplement['sources']:
            rel=source.get('rawFile')
            if rel and rel not in hashes:
                original=ROOT/rel
                hashes[rel]=hashlib.sha256(original.read_bytes()).hexdigest() if original.exists() else None
            if rel and hashes[rel]!=source.get('sha256'):issues.append('Source hash differs: '+source['id'])
            if sources.get(source['id'])!=source:issues.append('Canonical source differs: '+source['id'])
            count+=1
        for patch in supplement['places']:
            actual=places.get(patch['id'])
            if not actual:issues.append('Missing canonical place: '+patch['id']);continue
            if patch.get('representatives') and patch['representatives']!=actual.get('representatives'):issues.append('Canonical roster differs: '+patch['id'])
            if patch.get('governance') and patch['governance']!=actual.get('governance'):issues.append('Canonical governance differs: '+patch['id'])
            by_event={e['id']:e for e in actual.get('elections',[])}
            for event in patch.get('elections',[]):
                if by_event.get(event['id'])!=event:issues.append('Canonical contest differs: '+event['id'])
        supplement_checks.append({'file':filename,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                  'coverage':supplement.get('coverage',{}),'sourceRecords':len(supplement['sources'])})
    global_events=set()
    for place in canonical['places']:
        for person in place.get('representatives',[]):
            if person.get('sourceId') not in sources:issues.append('Unregistered current roster source: '+place['id'])
            if person.get('sourceId') in ['council-qld-2024-browser-verified-xml','council-sa-2022-candidate-and-historical-elected-master']:
                issues.append('Historic result is being used as a current roster: '+place['id'])
        for event in place.get('elections',[]):
            if event['id'] in global_events:issues.append('Duplicate global event ID: '+event['id'])
            global_events.add(event['id'])
            for candidate in event.get('candidates',[]):
                if 'votes' in candidate and not candidate.get('voteMeasure'):issues.append('Vote measure absent: '+event['id'])
    # Repeat the actual merge in an isolated in-memory copy. Save is deliberately
    # replaced, so this audit cannot race the root's page build or alter files.
    adapter=runpy.run_path(str(ROOT/'tools/acquire-council-places.py'))
    merge=adapter['merge_detail_supplements'];state=merge.__globals__
    state['data']=copy.deepcopy(canonical);state['save']=lambda:None
    merge()
    identical=state['data']==canonical
    if not identical:issues.append('A repeated supplement merge would change canonical data')
    report={'schemaVersion':1,'checked':'2026-10-17','status':'fail' if issues else 'pass',
            'canonicalSha256':hashlib.sha256(canonical_path.read_bytes()).hexdigest(),
            'checks':{'sourceRecordsChecked':count,'uniqueOriginalFilesHashed':len(hashes),'eventIdsChecked':len(global_events),
                      'canonicalPlaceCount':len(places),'repeatMergeIdentical':identical},'supplements':supplement_checks,'issues':issues,
            'limits':['Checks source hashes, supplement-to-canonical equality, independent current-roster provenance, typed votes and in-memory repeatability only.',
                      'Does not certify currentness of dated roster snapshots, complete biographies or later-event coverage, rendered pages, all links or browser acceptance.']}
    output=ROOT/'content/places/qa/council-details-validation.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checks':report['checks'],'issues':issues},ensure_ascii=True))
    raise SystemExit(bool(issues))


if __name__=='__main__':main()
