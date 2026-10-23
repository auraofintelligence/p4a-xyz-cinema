"""Offline integration of minimal official directory facts observed in browser.

The directory independently lists each current mayor; no2024 winner is used as
current-office evidence. It does not expose a complete councillor roster. Keep
the original Redland division profiles independently sourced and unchanged.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT/'content/places/raw/council-qld-current-leaders-browser.json'
    extract=json.loads(path.read_text(encoding='utf-8'))
    canonical=json.loads((ROOT/'content/places/councils.json').read_text(encoding='utf-8'))
    places={p['id']:p for p in canonical['places']}
    if len(extract['records'])!=78 or extract['failures']:raise ValueError('Expected78verified independent directory records')
    sid='council-qld-current-leaders-browser'
    source={'id':sid,'title':'Queensland Government current local government directory: independently published mayors and official council websites',
            'url':extract['url'],'checked':extract['checked'],'sourcePageUpdated':extract['sourcePageUpdated'],
            'rawFile':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'method':extract['method'],'licence':'Minimal public professional name, role and institutional website facts. Publisher rights retained; no addresses, contacts or CEO data republished.'}
    records=[]
    for row in extract['records']:
        pid='qld-council-'+row['directoryId'];place=places[pid]
        patch={'id':pid,'sources':[sid],'officialUrl':row['website'],
               'coverageNotes':['Official council website independently published in the Queensland Government directory, checked 17 October 2026.']}
        if row['name']:
            if place['kind']!='council' or row['role']!='Mayor':raise ValueError('Unexpected directory governing role: '+pid)
            patch['representatives']=[{'name':row['name'],'role':row['role'],'profileUrl':extract['url'],'profileType':'official current-member directory roster',
                                       'website':row['website'],'sourceId':sid,'checked':extract['checked'],
                                       'status':'Independently named in the official Queensland Government directory checked 17 October 2026'}]
            patch['coverageNotes'].append('This source supplies the published mayor independently of2024 election results. Complete current councillor rosters and individual biographies remain unpopulated except where separately sourced. The page-wide16 October 2026 update is not an individual office-commencement date.')
        else:
            patch['coverageNotes'].append('The directory supplies this special body website but no mayor field. No ordinary mayor or council election is invented.')
        records.append(patch)
    parent_patches={p['id']:p for p in records}
    ward_links=0
    for ward in canonical['places']:
        if ward['jurisdiction']!='qld' or ward['kind']!='ward':continue
        # This is only the obsolete inherited institutional directory link;
        # individual Redland representative profiles remain their actual links.
        parent=parent_patches[ward['parentId']]
        if ward.get('officialUrl') not in ['https://www.localgovernment.qld.gov.au/for-councils/local-government-directory',parent['officialUrl']]:continue
        records.append({'id':ward['id'],'officialUrl':parent['officialUrl'],'sources':[sid],
                        'coverageNotes':['The inherited retired generic directory link is replaced by this division parent council\'s independently published institutional website. Individual representative profiles remain separately sourced.']})
        ward_links+=1
    result={'schemaVersion':1,'checked':extract['checked'],'sources':[source],'places':records,
            'coverage':{'councilsWithIndependentMayor':sum(bool(p.get('representatives')) for p in records),'officialBodyWebsites':len(parent_patches),'retiredInheritedWardLinksReplaced':ward_links}}
    (ROOT/'content/places/qld-current-leaders.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['coverage']))


if __name__=='__main__':main()
