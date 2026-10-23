"""Read-only minimal leadership extraction from the public LGA-SA workbook.

The browser-downloaded source filename declares23 September 2026. Keep that
published snapshot distinct from checking, current-office start dates, and a
complete councillor roster. Do not publish the workbook's contact/CEO fields or
treat its ambiguous Mr/Cr title fields as evidence of an elected council role.
"""
import hashlib
import json
from pathlib import Path
import re
import runpy
import openpyxl

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-10-17'
URL='https://www.lga.sa.gov.au/__data/assets/excel_doc/0035/650879/All-Council-Database-as-at-23-September-2026.xlsx'


def main():
    path=ROOT/'content/places/raw/council-sa-current-directory-2026-09-23.xlsx'
    review_path=ROOT/'content/places/sources/sa-current-leadership-web-review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    canonical=json.loads((ROOT/'content/places/councils.json').read_text(encoding='utf-8'))
    norm=runpy.run_path(str(ROOT/'tools/normalise-sa-council-ballots.py'))['key']
    def key(value):return norm(re.sub(r'\b(?:Corporation|Town|Rural|Regional|Municipal)\b','',value,flags=re.I))
    parents={key(p['name']):p for p in canonical['places'] if p['jurisdiction']=='sa' and p['kind'] in ['council','special-local-body']}
    sid='council-sa-lga-current-leaders-2026-09-23'
    sources=[{'id':sid,'title':'LGA South Australia public council directory (declared 23 September 2026 snapshot)',
              'url':URL,'checked':CHECKED,'asAt':'2026-09-23','rawFile':path.relative_to(ROOT).as_posix(),
              'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
              'method':'Normal browser download via the visible public Central Council Contacts link; no warning or validation bypass. Only public professional names/roles and institutional website fields extracted.',
              'licence':'Minimal factual public professional names, roles and institutional links. Full copyrighted directory and incidental contacts remain local-only.'}]
    workbook=openpyxl.load_workbook(path,read_only=True,data_only=True)
    rows=list(workbook.active.values)
    if rows[0][0]!='Mayor Title' or rows[0][8]!='Organisation' or len(rows)!=70:raise ValueError('Unexpected official directory workbook structure')
    records=[];skipped=[]
    for row in rows[1:]:
        role,given,surname,council,website=row[0],row[1],row[2],row[8],row[18]
        parent=parents[key(council)]
        official='https://'+str(website).strip().removeprefix('https://').removeprefix('http://')
        patch={'id':parent['id'],'officialUrl':official,'sources':[sid],
               'coverageNotes':['Official institutional website comes from the public LGA-SA directory snapshot declared 23 September 2026, checked 17 October 2026. The full copyrighted workbook and contact details remain local-only.']}
        if role and 'Mayor' in role and parent['kind']=='council':
            name=' '.join(str(x).strip() for x in [given,surname] if x)
            person={'name':name,'role':role,'profileUrl':URL,'profileType':'official published LGA current-leader directory roster',
                    'website':official,'sourceId':sid,'checked':CHECKED,'asAt':'2026-09-23',
                    'status':'Published LGA-SA leader snapshot declared 23 September 2026; checked 17 October 2026, subsequent individual changes not fully reconciled'}
            patch['representatives']=[person]
            patch['coverageNotes'].append('Only the independently published council leader is supplied here. Complete current councillor rosters and individual profiles remain unpopulated unless separately sourced; historical2022 winners are not used as current-office evidence.')
            if parent['id']=='sa-council-40120':
                fact=review['adelaideHills'];review_id='council-sa-adelaide-hills-current-mayor-role'
                sources.append({'id':review_id,'title':'Adelaide Hills official current mayor role independently verified',
                                'url':fact['url'],'checked':CHECKED,'rawFile':review_path.relative_to(ROOT).as_posix(),
                                'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'licence':'Minimal public professional role fact.'})
                if name!=fact['name'] or role!=fact['directoryRole']:raise ValueError('Adelaide Hills directory role discrepancy changed')
                person.update(role=fact['role'],sourceRole=role,additionalSourceIds=[review_id],roleNote=fact['basis'])
                patch['sources'].append(review_id);patch['coverageNotes'].append(fact['basis'])
        else:
            skipped.append({'placeId':parent['id'],'publishedTitle':role,'reason':'Ambiguous title/special-body role is not evidence of a mayor or councillor office.'})
            patch['coverageNotes'].append('The directory title field does not establish an ordinary elected office for this body. No current representative is inferred from that field.')
        if parent['id']=='sa-council-41330':
            fact=review['cooberPedy'];review_id='council-sa-coober-pedy-administrators'
            sources.append({'id':review_id,'title':'Coober Pedy official three-person administrator roster',
                            'url':fact['url'],'checked':CHECKED,'rawFile':review_path.relative_to(ROOT).as_posix(),
                            'sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),'licence':'Minimal public professional administrator name and role facts.'})
            patch.update(governance='administration',representatives=[{**r,'sourceId':review_id,'checked':CHECKED,
                         'profileUrl':fact['url'],'profileType':'official current administrator roster','status':'Appointed administrator listed by the council, checked 17 October 2026'} for r in fact['people']],
                         elections=[{'id':parent['id']+'-next-ordinary','label':'Return to elected council: date not verified','kind':'ordinary','status':'date-not-verified','date':None,
                                     'timezone':'Australia/Adelaide','milestoneLabel':'election date not verified','dateBasis':fact['basis'],'sourceUrl':fact['url'],'candidates':[]}])
            patch['sources'].append(review_id);patch['coverageNotes'].append(fact['basis'])
        records.append(patch)
    coverage={'ordinaryCouncilRecords':sum(parents[key(r[8])]['kind']=='council' for r in rows[1:]),
              'publishedMayors':sum(bool(r.get('representatives')) and r['id']!='sa-council-41330' for r in records),
              'independentlyNamedAdministrators':3,'officialBodyWebsites':len(records)}
    result={'schemaVersion':1,'checked':CHECKED,'sources':sources,'places':records,'checks':{'excludedAmbiguousRoleFields':skipped},'coverage':coverage}
    (ROOT/'content/places/sa-current-leaders.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(coverage))


if __name__=='__main__':main()
