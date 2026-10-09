from public_punctuation import public_punctuation
from web_link_policy import external_links
"""Build the Victoria atlas from reviewed local records. No network access."""
import json, re, pathlib, html
from vic_profile_facts import facts
from vic_council_facts import facts as local_facts
from vic_first_peoples_facts import facts as recognition_facts
ROOT=pathlib.Path(__file__).resolve().parents[1]
def build():
    for source_name,global_name in [('vic','P4A_VIC_PEOPLE'),('vic-seating','P4A_VIC_SEATING')]:
        payload=json.loads((ROOT/'content/representatives'/f'{source_name}.json').read_text(encoding='utf-8'))
        if source_name=='vic':
            election=json.loads((ROOT/'content/elections/vic-2026.json').read_text(encoding='utf-8'))
            payload['candidates']=election['candidates']
            payload['areaHistory']={}
            for person in payload['people']:
                if person.get('history'):
                    payload['areaHistory'][person['areaId']]=person.pop('history')
                    person['historyKey']=person['areaId']
        (ROOT/'assets'/f'{source_name}-people.js').write_text('window.'+global_name+' = '+json.dumps(payload,ensure_ascii=False)+';\n',encoding='utf-8')
    source=(ROOT/'content/electorates/vic.md').read_text(encoding='utf-8')
    data=json.loads(re.search(r'```json electorate-data\s*(.*?)```',source,re.S).group(1))
    assert len(data['assembly'])==88 and len(data['council'])==8
    elections=json.loads((ROOT/'content/electorates/vic-election-results.json').read_text(encoding='utf-8'))
    census=json.loads((ROOT/'content/electorates/vic-census-2021.json').read_text(encoding='utf-8'))
    records=[]
    e=html.escape
    for chamber in ['assembly','council']:
        for r in data[chamber]:
            members='; '.join(f"{m['name']} ({m['party']})" for m in r['members']) or 'Vacant - Brunswick; no sitting member listed as at 2 October 2026.'
            records.append(f'<details class="vic-record" id="{e(r["id"])}"><summary>{e(r["name"])} - {"Assembly district" if chamber=="assembly" else "Council region"}</summary><p>{e(members)}</p><p>{e(r.get("regionName", "Victoria"))} · Representation checked 2 October 2026.</p><p><a href="{e(r["vecUrl"])}">VEC electorate information</a> · <a href="{e(r["resultsUrl"])}">{e(r["resultsLabel"])}</a></p>{facts(r,data,elections,census)}</details>')
    local=json.loads((ROOT/'content/councils/vic.json').read_text(encoding='utf-8'))
    for layer in ['lga','ward']:
        data[layer]=[{k:r[k] for k in ['id','code','name','kind','body','level','members','labelPoint','sortMetrics','wardIds','parentId','parentName','governance'] if k in r} for r in local[layer]]
        for r in local[layer]:
            records.append(f'<details class="vic-local-record" id="{e(r["id"])}"><summary>{e(r["name"])} - {e(r["body"])}</summary>{local_facts(r,local)}</details>')
    fp=json.loads((ROOT/'content/first-peoples/vic.json').read_text(encoding='utf-8'))
    data['firstpeoples']=[{k:r[k] for k in ['id','code','name','fullName','kind','body','level','members','sortMetrics','labelPoint']} for r in fp['records']]
    for r in fp['records']:records.append(f'<details class="vic-recognition-record" id="{e(r["id"])}"><summary>{e(r["name"])} - {e(r["body"])}</summary>{recognition_facts(r,fp)}</details>')
    # Source of shared chrome is the existing, reconciled Victoria portal.
    portal=(ROOT/'states/vic/index.html').read_text(encoding='utf-8')
    header=re.search(r'<header class="site-header">.*?</header>',portal,re.S).group(0).replace('../../','../../../')
    page=(ROOT/'tools/templates/vic-map.html').read_text(encoding='utf-8').replace('@@HEADER@@',header).replace('@@DIRECTORY@@','\n'.join(records))
    page=external_links(public_punctuation(page))
    dest=ROOT/'states/vic/map';dest.mkdir(parents=True,exist_ok=True)
    (dest/'index.html').write_text(page,encoding='utf-8')
    (ROOT/'assets/vic-electorates.js').write_text('window.P4A_VIC_ELECTORATES = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    print('Generated atlas: 96 state electorates, 79 councils + 8 unincorporated areas, 467 ward/electoral-structure records.')
if __name__=='__main__':build()
