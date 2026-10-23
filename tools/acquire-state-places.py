"""Acquire/normalise state electoral places from retained official public sources.

Default runs only cached processing. --network acquires the selected requests;
--probe ID=URL registers an official source; --only/--plan restrict acquisition.
Geometry is never simplified, rounded, clipped, or stripped of rings.
"""
import argparse, concurrent.futures, csv, gzip, hashlib, io, json, pathlib, re, ssl, time, unicodedata, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT/'content/places/raw/state'
SOURCES = ROOT/'content/places/sources/state-requests.json'
OUT = ROOT/'content/places/state.json'
CHECKED = '2026-10-17'
SERVICE = 'https://services-ap1.arcgis.com/ypkPEy1AmwPKGNNv/ArcGIS/rest/services/State_Electoral_Polygon/FeatureServer/19'

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def browser_text(text):
    # The public browser extractor may fold multiple numbered lines together.
    text=re.sub(r'L\d+(?:@P\d+(?:-\d+)?)?: ?', '\n',text)
    return re.sub(r'\ue200cite\ue202\d+[^\w](.*?)\ue201',r'\1',text)

def fetch(rec):
    path=ROOT/rec['rawFile']
    if path.exists() and not rec.get('refresh'): return rec
    if any(code in rec.get('error','') for code in ['HTTP Error 403','HTTP Error 404','HTTP Error 500']) and not rec.get('refresh'):return rec
    try:
        req=urllib.request.Request(rec['url'],headers={'User-Agent':'P4A-civic-public-source-check/1.0 (+https://p4a.xyz)'})
        # A maintained CA bundle avoids the old default Miniconda OpenSSL store.
        import certifi
        context=ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(req,timeout=100,context=context) as response:
            data=response.read()
            rec.update(status=response.status,contentType=response.headers.get('Content-Type'),finalUrl=response.geturl())
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        rec.update(checked=CHECKED,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
        rec.pop('error',None)
        print(rec['id'],len(data),flush=True)
    except Exception as exc:
        rec['error']=str(exc);print(rec['id'],'ERROR',str(exc),flush=True)
    return rec

def bootstrap():
    d={'schemaVersion':1,'checked':CHECKED,'scope':'state','sources':[],'layers':[],'places':[]}
    provenance=read(ROOT/'assets/maps/vic-provenance.json')
    source_text=(ROOT/'content/electorates/vic.md').read_text(encoding='utf-8')
    vic=json.loads(re.search(r'```json electorate-data\s*(.*?)```',source_text,re.S).group(1))
    people=read(ROOT/'content/representatives/vic.json')
    results=read(ROOT/'content/electorates/vic-election-results.json')
    calendar=read(ROOT/'content/elections/state-election-calendar.json')
    dates={r['slug']:r for r in calendar['elections']}
    for chamber,kind,field,namefield in [('assembly','state-district','district_code','district'),('council','state-region','region_code','region')]:
        sid='state-vic-'+chamber+'-2022'
        src=provenance['datasets'][chamber]
        d['sources'].append({'id':sid,'title':'Vicmap Admin '+chamber+' official 2022 boundaries','url':src['request'],'checked':provenance['retrieved'],'licence':provenance['licence'],'rawFile':'assets/maps/'+src['file'],'sha256':src['sha256']})
        d['layers'].append({'id':sid,'jurisdiction':'vic','kind':kind,'name':'Legislative Assembly districts' if chamber=='assembly' else 'Legislative Council regions','geometryFile':'assets/maps/'+src['file'],'featureIdField':field,'featureNameField':namefield,'sourceId':sid,'boundaryEdition':provenance['boundaryEdition'],'crs':'EPSG:4326','attribution':provenance['attribution']})
        for r in vic[chamber]:
            reps=[]
            for p in people['people']:
                if p.get('areaId')==r['id'] and p.get('kind')=='mp':
                    reps.append({'name':p['name'],'role':p['role'],'party':p.get('party'),'profileUrl':p.get('profileUrl') or p.get('profile') or p['source'],'website':next(iter(p.get('websites',[])),None),'sourceId':'state-vic-members-20261002','checked':p.get('checked',people['checked'])})
            events=[]
            result=results.get(r['id'])
            if result:
                candidates=[]
                for table in result.get('tables',[]):
                    if table.get('kind')=='primary':
                        for c in table.get('rows',[]):
                            if c.get('candidate'): candidates.append({'name':c['candidate'],'party':c.get('party') or 'No affiliation published','status':'contested','sourceUrl':result['source'],'votes':c.get('votes'),'voteMeasure':'first preferences' if chamber=='assembly' else 'candidate first preferences; see official table for above/below-line treatment'})
                        break
                events.append({'id':r['id']+'-'+result['date'],'label':result['event'],'kind':'general-election','status':'historical','date':result['date'],'dateBasis':'Official historical results; original source checked '+result['retrieved'],'timezone':'Australia/Melbourne','sourceUrl':result['dateSource'],'resultsUrl':result['source'],'candidates':candidates})
            nxt=dates['vic']
            events.append({'id':'vic-state-2026','label':'2026 Victorian state election','kind':'general-election','status':'scheduled','date':nxt['date'],'dateBasis':nxt['basis']+'; calendar snapshot '+calendar['checked'],'timezone':nxt['timezone'],'sourceUrl':nxt['source'],'candidates':[]})
            d['places'].append({'id':r['id'],'name':r['name'],'slug':slug(r['name']),'jurisdiction':'vic','kind':kind,'chamber':'Legislative Assembly' if chamber=='assembly' else 'Legislative Council','layerId':sid,'featureId':r['code'],'officialUrl':r['vecUrl'],'sources':[sid,'state-vic-members-20261002','state-vic-results-20261002'],'boundaryEdition':provenance['boundaryEdition'],'representatives':reps,'elections':events,'coverageNotes':['Existing reviewed Victorian snapshot retained; member and result source checks remain 2 October 2026.']})
    d['sources'] += [{'id':'state-vic-members-20261002','title':'Existing reviewed Parliament of Victoria member contacts','url':vic['memberSource'],'checked':people['checked'],'rawFile':'content/representatives/vic.json'}, {'id':'state-vic-results-20261002','title':'Existing reviewed VEC election results','url':'https://www.vec.vic.gov.au/results/state-election-results/2022-state-election-results','checked':'2026-10-02','rawFile':'content/electorates/vic-election-results.json'}]
    return d

def registry():
    rows=read(SOURCES) if SOURCES.exists() else []
    def add(id,url,ext='json'):
        if not any(r['id']==id for r in rows):rows.append({'id':id,'url':url,'rawFile':f'content/places/raw/state/{id}.{ext}'})
    add('state-national-boundary-metadata',SERVICE+'?f=pjson')
    add('state-national-boundary-count',SERVICE+'/query?f=json&where=1%3D1&returnCountOnly=true')
    for state,pid in [('nsw','1'),('qld','3'),('sa','4'),('wa','5'),('tas','6'),('nt','7'),('act','8')]:
        params=urllib.parse.urlencode({'f':'geojson','where':"state_pid='"+pid+"'",'outFields':'*','outSR':'4326','returnGeometry':'true','orderByFields':'se_pid,se_ply_pid','resultRecordCount':'1000'})
        add('state-boundaries-'+state,SERVICE+'/query?'+params,'geojson')
    for state,pid in [('nsw','1'),('qld','3'),('sa','4'),('wa','5'),('tas','6'),('nt','7'),('act','8')]:
        for offset in [1000,2000,3000]:
            params=urllib.parse.urlencode({'f':'geojson','where':"state_pid='"+pid+"'",'outFields':'*','outSR':'4326','returnGeometry':'true','orderByFields':'se_pid,se_ply_pid','resultRecordCount':'1000','resultOffset':offset})
            add('state-boundaries-'+state+'-'+str(offset),SERVICE+'/query?'+params,'geojson')
        add('state-boundary-count-'+state,SERVICE+'/query?'+urllib.parse.urlencode({'f':'json','where':"state_pid='"+pid+"'",'returnCountOnly':'true'}))
    add('state-national-boundary-service',SERVICE.rsplit('/',1)[0]+'?f=pjson')
    attrs=RAW/'state-tas-council-attributes.html'
    if attrs.exists():
        for feature in read(attrs).get('features',[]):
            pid=feature['attributes']['LEG_CNL_ID']
            params=urllib.parse.urlencode({'where':'LEG_CNL_ID='+str(pid),'outFields':'LEG_CNL_ID,NAME,COMMENTS,UFI','returnGeometry':'true','outSR':'4326','f':'geojson'})
            add('state-tas-lc-geometry-'+str(pid),'https://services.thelist.tas.gov.au/arcgis/rest/services/Public/OpenDataWFS/MapServer/27/query?'+params,'geojson')
    add('state-qld-members','https://www.parliament.qld.gov.au/Members/Current-Members','html')
    add('state-nsw-members','https://www.parliament.nsw.gov.au/members/Pages/all-members.aspx','html')
    add('state-wa-members','https://www.parliament.wa.gov.au/Parliament/Memblist.nsf/WAllMembers','html')
    add('state-sa-members','https://www.parliament.sa.gov.au/en/House-of-Assembly/Members','html')
    add('state-tas-members','https://www.parliament.tas.gov.au/house-of-assembly/currentmembers','html')
    add('state-act-members','https://www.parliament.act.gov.au/members','html')
    add('state-nt-members','https://parliament.nt.gov.au/members/13th-assembly','html')
    write(SOURCES,rows);return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--network',action='store_true');parser.add_argument('--probe',action='append',default=[]);parser.add_argument('--only',action='append',default=[],help='Acquire only these registered source IDs; repeat for a consolidated set.');parser.add_argument('--plan',help='Reviewed JSON source plan of {id,url}; restricts acquisition to that consolidated set.');parser.add_argument('--acquire-only',action='store_true',help='Retain requested sources without rewriting canonical state data.');args=parser.parse_args()
    rows=registry()
    if args.plan:
        planned=read(ROOT/args.plan)
        args.probe.extend(r['id']+'='+r['url'] for r in planned)
        args.only.extend(r['id'] for r in planned)
    for probe in args.probe:
        id,url=probe.split('=',1)
        old=next((r for r in rows if r['id']==id),None)
        if old:
            if old['url']!=url:old.pop('error',None)
            old.update(url=url)
        else: rows.append({'id':id,'url':url,'rawFile':f'content/places/raw/state/{id}.html'})
    if args.network:
        selected=[r for r in rows if not args.only or r['id'] in args.only]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: fetched={r['id']:r for r in pool.map(fetch,selected)}
        rows=[fetched.get(r['id'],r) for r in rows]
        # Public member profile URLs are taken from the official current roster,
        # never guessed from names. Pictures and private contact details omitted.
        from bs4 import BeautifulSoup
        known={r['url'] for r in rows};additional=[]
        for roster in ([] if args.only else ['state-tas-members','state-tas-council-members']):
            rec=next((r for r in rows if r['id']==roster),None)
            if not rec or not (ROOT/rec['rawFile']).exists():continue
            soup=BeautifulSoup((ROOT/rec['rawFile']).read_text(encoding='utf-8'),'html.parser')
            for a in soup.select('a[href]'):
                url=a['href']
                if re.search(r'/(house-of-assembly/currentmembers|legislative-council/members)/[^/?#]+$',url) and url not in known:
                    known.add(url);id='state-tas-profile-'+slug(url.rsplit('/',1)[-1]);additional.append({'id':id,'url':url,'rawFile':f'content/places/raw/state/{id}.html'})
        if additional:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows+=list(pool.map(fetch,additional))
    write(SOURCES,rows)
    if args.acquire_only:return
    d=bootstrap();normalise(d,rows);print('Cached national layers normalized',flush=True)
    from state_place_supplements import sa_geography, tas_council_geometry, sa_results, tas_events, wa_members
    sa_geography(d,rows);print('SA current geometry integrated',flush=True)
    enrich(d,rows);print('Cached rosters/ballots integrated',flush=True)
    tas_council_geometry(d,rows);print('TAS native Council geometry integrated',flush=True)
    tas_events(d,rows)
    sa_results(d,rows);print('SA 2026 ballots/results integrated',flush=True)
    wa_members(d)
    from state_history_supplement import apply as apply_histories
    apply_histories(d,rows)
    write(OUT,d)
    print(json.dumps({'places':len(d['places']),'layers':len(d['layers']),'sources':len(d['sources'])}))

def normalise(d,rows):
    calendar=read(ROOT/'content/elections/state-election-calendar.json')
    dates={r['slug']:r for r in calendar['elections']}
    authorities={'nsw':'https://elections.nsw.gov.au','qld':'https://www.ecq.qld.gov.au','sa':'https://www.ecsa.sa.gov.au','wa':'https://www.elections.wa.gov.au','tas':'https://www.tec.tas.gov.au','nt':'https://ntec.nt.gov.au','act':'https://www.elections.act.gov.au'}
    for state in ['nsw','qld','sa','wa','tas','nt','act']:
        applicable=[r for r in rows if r['id']=='state-boundaries-'+state or r['id'].startswith('state-boundaries-'+state+'-')]
        groups={}
        for rec in applicable:
            path=ROOT/rec['rawFile']
            if not path.exists():continue
            raw=read(path)
            for f in raw.get('features',[]):
                props=f['properties'];groups.setdefault((props['secl_code'],props['se_pid']),[]).append(f)
            if raw.get('features'):d['sources'].append({**rec,'title':'Digital Atlas of Australia / Geoscape '+state.upper()+' electoral boundary source','licence':'CC BY 4.0; source-specific Geoscape attributions retained'})
        for cls in sorted(set(k[0] for k in groups)):
            upper=cls=='3';kind='state-region' if upper else 'state-district'
            lid='state-'+state+('-council' if upper else '-assembly')+'-2025'
            sid='state-boundaries-'+state
            features=[]
            for (_,pid),parts in sorted(groups.items()):
                if _!=cls:continue
                first=parts[0]['properties'];name=first['name'].title();name=name.replace('Mcc','McC')
                polys=[]
                for p in parts:
                    geom=p['geometry']
                    polys.extend([geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates'])
                features.append({'type':'Feature','properties':{'se_pid':pid,'name':name,'secl_code':cls,'sourcePolygonIds':[p['properties']['se_ply_pid'] for p in parts]},'geometry':{'type':'MultiPolygon','coordinates':polys}})
                membernotes=['Current member roster and previous contestant reconciliation are awaiting the jurisdiction source adapter.']
                if state=='wa':membernotes.append('Western Australia has one statewide Legislative Council electorate from the 2025 election; former six regions are historical.')
                dt=dates[state]
                events=[{'id':state+'-next-state-general','label':'Next ordinary '+state.upper()+' state/territory election','kind':'general-election','status':'scheduled' if dt['date'] else 'date-unannounced','date':dt['date'],'dateBasis':dt['basis']+'; source calendar checked '+calendar['checked'],'timezone':dt['timezone'],'sourceUrl':dt['source'],'candidates':[]}]
                if upper and state=='tas':events=[];membernotes.append('Tasmanian Legislative Council divisions elect members on their individual six-year periodic cycle; no shared House general-election date applies.')
                d['places'].append({'id':'state-'+state+'-'+pid.lower(),'name':name,'slug':slug(name),'jurisdiction':state,'kind':kind,'chamber':'Legislative Council' if upper else ('House of Assembly' if state in ['tas','sa'] else 'Legislative Assembly'),'layerId':lid,'featureId':pid,'officialUrl':authorities[state],'sources':[sid],'boundaryEdition':'Geoscape / Digital Atlas of Australia May 2025 source edition','representatives':[],'elections':events,'coverageNotes':membernotes})
            geometry={'type':'FeatureCollection','features':features}
            data=json.dumps(geometry,ensure_ascii=False,separators=(',',':')).encode('utf-8')
            dest=ROOT/'assets/maps/national'/('state-'+state+('-council' if upper else '-assembly')+'-2025.geojson.gz')
            dest.parent.mkdir(parents=True,exist_ok=True)
            prior=dest.read_bytes() if dest.exists() else None
            if prior is None or gzip.decompress(prior)!=data:dest.write_bytes(gzip.compress(data,mtime=0))
            d['layers'].append({'id':lid,'jurisdiction':state,'kind':kind,'name':'Legislative Council divisions' if upper else ('House of Assembly divisions' if state in ['tas','sa'] else 'Legislative Assembly districts'),'geometryFile':str(dest.relative_to(ROOT)).replace('\\','/'),'featureIdField':'se_pid','featureNameField':'name','sourceId':sid,'boundaryEdition':'Geoscape / Digital Atlas of Australia May 2025 source edition','crs':'EPSG:4326','nativeCrs':'EPSG:7844','coordinateNote':'Official ArcGIS query returns EPSG:4326; no coordinate precision setting, quantisation or simplification applied. Polygon parts grouped by persistent electorate identifier with every coordinate and ring retained. Source itself is an aggregated representation, not a legal boundary instrument.','attribution':'Incorporates or developed using Administrative Boundaries © Geoscape Australia licensed by the Commonwealth of Australia under CC BY 4.0. Geoscience Australia Digital Atlas of Australia.','featureCount':len(features),'uncompressedSha256':hashlib.sha256(data).hexdigest(),'uncompressedBytes':len(data)})
    supplement=ROOT/'content/places/state-qld-details.json'
    if supplement.exists():
        extra=read(supplement);d['sources'].extend(extra.get('sources',[]));indexed={slug(p['name']):p for p in extra.get('places',[])}
        for p in d['places']:
            if p['jurisdiction']=='qld' and p['slug'] in indexed:
                s=indexed[p['slug']]
                for key in ['representatives','elections','coverageNotes']:p[key]=s.get(key,p[key])
                p['sources']=list(dict.fromkeys(p['sources']+s.get('sources',[])))

def enrich(d,rows):
    from bs4 import BeautifulSoup
    registry={r['id']:r for r in rows}
    def source(id,title=None):
        rec=registry[id]
        if not any(s['id']==id for s in d['sources']):d['sources'].append({**rec,'title':title or id.replace('-',' '),'licence':'Publisher rights retained; factual names/roles/results only. No portraits copied.'})
        return rec
    def soup(id):
        r=registry.get(id)
        return BeautifulSoup((ROOT/r['rawFile']).read_text(encoding='utf-8'),'html.parser') if r and (ROOT/r['rawFile']).exists() else None
    def place(state,name,chamber=None):
        return next((p for p in d['places'] if p['jurisdiction']==state and slug(p['name'])==slug(name) and (not chamber or p['chamber']==chamber)),None)
    def event(p,id,date,url,candidates,kind='general-election'):
        p['elections'].insert(0,{'id':id,'label':date[:4]+' '+p['chamber']+' '+('election' if kind=='general-election' else kind),'kind':kind,'status':'historical','date':date,'dateBasis':'Official election results / parliamentary record','timezone':{'sa':'Australia/Adelaide','tas':'Australia/Hobart','nt':'Australia/Darwin','act':'Australia/Sydney','wa':'Australia/Perth','nsw':'Australia/Sydney'}[p['jurisdiction']],'sourceUrl':url,'resultsUrl':url,'candidates':candidates})
    # Three actual statewide upper-house electorates; no lower-house duplicate map.
    for st,title,url,n in [('nsw','New South Wales','https://www.parliament.nsw.gov.au/members-and-electorates',42),('sa','South Australia','https://www.parliament.sa.gov.au/Members/Members-Home',22),('wa','Western Australia','https://www.elections.wa.gov.au/elections/state',37)]:
        sid='state-'+st+'-upper-house-structure'
        d['sources'].append({'id':sid,'title':title+' Legislative Council structure','url':url,'checked':CHECKED,'licence':'Publisher rights retained; linked factual institutional context.'})
        dt=next(r for r in read(ROOT/'content/elections/state-election-calendar.json')['elections'] if r['slug']==st)
        p={'id':'state-'+st+'-legislative-council-statewide','name':title+' Legislative Council','slug':'legislative-council','jurisdiction':st,'kind':'statewide-upper-house','chamber':'Legislative Council','officialUrl':url,'sources':[sid],'representatives':[],'elections':[{'id':st+'-next-lc-periodic','label':'Next '+title+' Legislative Council '+('election' if st=='wa' else 'periodic election'),'kind':'general-election' if st=='wa' else 'periodic-election','status':'scheduled','date':dt['date'],'dateBasis':dt['basis']+'; existing source calendar checked 2 October 2026','timezone':dt['timezone'],'sourceUrl':dt['source'],'candidates':[]}],'coverageNotes':[str(n)+' current Legislative Council seats represent the whole state. '+('All 37 elected from one statewide electorate from 2025; the former six regions remain historical.' if st=='wa' else 'Half the chamber is elected at each ordinary state election; casual vacancies follow the actual statutory replacement process.')+' No fictional regional boundary layer is drawn.','Current member and previous contestant reconciliation pending source adapter.']}
        d['places'].append(p)
    # All 15 real Tasmanian Council constituencies, distinct from House divisions.
    attrs=RAW/'state-tas-council-attributes.html'
    if attrs.exists():
        sid='state-tas-council-attributes';rec=source(sid,'LIST current Legislative Council divisions / 2017 redistribution attributes')
        features=[]
        for row in read(attrs)['features']:
            a=row['attributes'];pid=a['LEG_CNL_ID'];georec=registry.get('state-tas-lc-geometry-'+str(pid));g=None
            if georec and (ROOT/georec['rawFile']).exists():
                raw=read(ROOT/georec['rawFile']);features.extend(raw.get('features',[]))
            d['places'].append({'id':'state-tas-lc-'+str(pid),'name':a['NAME'],'slug':slug(a['NAME']),'jurisdiction':'tas','kind':'state-region','chamber':'Legislative Council','featureId':pid,'officialUrl':'https://www.tec.tas.gov.au/legislative-council/Maps_LegislativeCouncil.html#'+a['NAME'],'sources':[sid],'boundaryEdition':a['COMMENTS'],'representatives':[],'elections':[],'coverageNotes':['Single-member Legislative Council division. Six-year periodic election cycles are division-specific; House of Assembly dates do not apply.','Previous periodic election candidate reconciliation pending.']})
        if len(features)==15:
            data=json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False,separators=(',',':')).encode('utf-8');dest=ROOT/'assets/maps/national/state-tas-council-2017.geojson.gz';dest.write_bytes(gzip.compress(data,mtime=0));lid='state-tas-council-2017'
            d['layers'].append({'id':lid,'jurisdiction':'tas','kind':'state-region','name':'Legislative Council divisions','geometryFile':str(dest.relative_to(ROOT)).replace('\\','/'),'featureIdField':'LEG_CNL_ID','featureNameField':'NAME','sourceId':sid,'boundaryEdition':'2017 redistribution (source feature COMMENTS; metadata description retains outdated 2008 text)','crs':'EPSG:4326','attribution':'the LIST © State of Tasmania; CC BY 3.0 Australia. Official ArcGIS EPSG:4326 output, every ring and coordinate retained.','featureCount':15,'uncompressedSha256':hashlib.sha256(data).hexdigest(),'uncompressedBytes':len(data)})
            for p in d['places']:
                if p['id'].startswith('state-tas-lc-'):p['layerId']=lid
            for r in rows:
                if r['id'].startswith('state-tas-lc-geometry-') and (ROOT/r['rawFile']).exists():source(r['id'],'LIST Legislative Council original unsimplified feature response')
    # The current ACT roster explicitly records the 2026 countback and affiliation.
    s=soup('state-act-current')
    if s:
        rec=source('state-act-current','ACT Legislative Assembly current members; 2026 changes stated independently of 2024 results')
        for tr in s.select('table tbody tr'):
            tds=tr.find_all('td',recursive=False)
            if len(tds)!=4:continue
            a=tds[0].find('a',href=True);p=place('act',tds[1].get_text(' ',strip=True))
            if not a or not p:continue
            website=next((x['href'] for x in tds[3].select('a[href]') if x['href'].startswith('http')),None)
            p['representatives'].append({'name':a.get_text(' ',strip=True),'role':'Member of the Legislative Assembly','party':tds[2].get_text(' ',strip=True).replace('⬤','').strip(),'profileUrl':a['href'],'website':website,'sourceId':rec['id'],'checked':CHECKED})
            p['sources'].append(rec['id'])
        s=soup('state-act-brindabella-results')
        if s:
            rec=source('state-act-brindabella-results','Elections ACT 2024 complete first preferences, all five electorates in one source document')
            for name,table in zip(['Brindabella','Ginninderra','Kurrajong','Murrumbidgee','Yerrabi'],s.select('table.electorate-results-table')):
                candidates=[];party=None
                for tr in table.select('tr'):
                    if 'group-heading' in tr.get('class',[]):party=tr.find('a').get_text(' ',strip=True) if tr.find('a') else tr.find('td').get_text(' ',strip=True)
                    if 'data-row' in tr.get('class',[]):
                        cells=tr.find_all('td',recursive=False)
                        if len(cells)==4:
                            candidates.append({'name':cells[0].get_text(' ',strip=True),'party':party,'status':'contested','sourceUrl':rec['url'],'votes':int(cells[1].get_text(strip=True).replace(',','')),'voteMeasure':'first preferences'})
                p=place('act',name);event(p,'act-2024-'+slug(name),'2024-10-19',rec['url'],candidates);p['sources'].append(rec['id'])
                p['coverageNotes']=['Five members elected by Hare-Clark. Current roster checked independently from historical results; Leanne Castley is currently Independent, and Rebecca Vassarotti replaced Shane Rattenbury by countback in June 2026.','2024 contestant first preference roster complete; historical ballot affiliations retained.']
        p=place('act','Kurrajong')
        if p:event(p,'act-kurrajong-countback-2026','2026-06-04',registry['state-act-current']['url'],[],kind='countback');p['coverageNotes'].append('The June 2026 countback is separately identified; its consenting contestant roster and transfer values require a dedicated official countback source refresh.')
    # SA public contact service is configured by its own official contact app.
    for key,chamber in [('state-sa-ha-api','House of Assembly'),('state-sa-lc-api','Legislative Council')]:
        rec=registry.get(key)
        if not rec or not (ROOT/rec['rawFile']).exists():continue
        source(key,'Parliament of South Australia current '+chamber+' member contact API')
        for member in read(ROOT/rec['rawFile']).get('memberContacts',[]):
            p=place('sa',member.get('electorateName','')) if chamber=='House of Assembly' else next(p for p in d['places'] if p['id']=='state-sa-legislative-council-statewide')
            if not p:continue
            name=(member.get('preferredName')or member['firstName']).strip()+' '+member['lastName'].strip()
            p['representatives'].append({'name':name,'role':chamber+' member','party':member['politicalPartyName'],'profileUrl':'https://www.parliament.sa.gov.au/Search/Member?type=member&id='+str(member['pmId']),'sourceId':key,'checked':CHECKED})
            p['sources']=list(dict.fromkeys(p['sources']+[key]));p['coverageNotes']=[x for x in p['coverageNotes'] if 'roster and previous contestant' not in x and 'Current member and previous' not in x]+['Current office independently verified using the official 56th Parliament contact API. Previous 2026 election contestants require official result adapter reconciliation.']
    # TAS current official profiles link every member to their actual electorate.
    for chamber,rosterid in [('House of Assembly','state-tas-members'),('Legislative Council','state-tas-council-members')]:
        roster=soup(rosterid)
        if not roster:continue
        names={a['href']:re.sub(r'^The Honourable\s+','',a.get_text(' ',strip=True)) for a in (roster.find('main')or roster).select('a[href]')}
        for r in rows:
            if not r['id'].startswith('state-tas-profile-') or r['url'] not in names or not (ROOT/r['rawFile']).exists():continue
            ss=soup(r['id']);main=ss.find('main')or ss;text=main.get_text(' ',strip=True)
            m=re.search(r'(Liberal|Labor|Independent|Tasmanian Greens|Greens|Green|Shooters[^.]*?)?\s+member for\s+(.+?)\s+First elected',text,re.I)
            if not m:continue
            p=place('tas',m[2].strip(),chamber)
            if not p:continue
            source(r['id'],'Parliament of Tasmania current profile: '+names[r['url']]);website=next((a['href'] for a in main.select('a[href]') if a.get_text(' ',strip=True)=='Members website'),None)
            p['representatives'].append({'name':names[r['url']],'role':chamber+' member','party':m[1] or 'Affiliation not published on current profile','profileUrl':r['url'],'website':website,'sourceId':r['id'],'checked':CHECKED});p['sources'].append(r['id']);p['coverageNotes']=[x for x in p['coverageNotes'] if 'Current member roster' not in x]
    # TAS lower-house 2025 first-preference totals are read from the official
    # workbook, with candidate affiliation independently from the ballot roster.
    path=RAW/'state-tas-2025-firstprefs.html'
    if path.exists():
        from openpyxl import load_workbook
        book=load_workbook(io.BytesIO(path.read_bytes()),read_only=True,data_only=True)
        rec=source('state-tas-2025-firstprefs','TEC 2025 House of Assembly first preferences by polling place workbook')
        for sheet in book:
            p=place('tas',sheet.title,'House of Assembly');ss=soup('state-tas-'+slug(sheet.title)+'-candidates');affiliations={};party=None
            if ss:
                ballot=source('state-tas-'+slug(sheet.title)+'-candidates','TEC 2025 '+sheet.title+' official ballot candidate roster')
                for node in ss.find_all(['h3','h4','td','p','strong']):
                    text=node.get_text(' ',strip=True)
                    if node.name=='h3':party=text
                    if node.name=='strong' and ',' in text and re.match(r'^[A-Za-z][A-Za-z’\' -]+,\s*\w',text) and len(text)<90:affiliations[slug(text)]=party
            candidates=[]
            for n,row in enumerate(sheet.values,1):
                name=row[0]
                if n<3 or not isinstance(name,str) or ',' not in name or not isinstance(row[-1],(int,float)):continue
                # Party headings also contain commas; accept only names on the
                # independently retained official ballot, never group totals.
                if slug(name) not in affiliations:
                    if name.strip()=='Shooters, Fishers, Farmers TAS':continue
                    raise ValueError('Workbook name absent from official ballot: '+sheet.title+' / '+name)
                candidate={'name':name,'status':'contested','sourceUrl':rec['url'],'votes':row[-1],'voteMeasure':'first preferences','sourceCell':sheet.title+'!'+str(n)}
                if affiliations.get(slug(name)):candidate['party']=affiliations[slug(name)]
                candidates.append(candidate)
            assert {slug(c['name']) for c in candidates}==set(affiliations),(sheet.title,'ballot/workbook mismatch')
            event(p,'tas-ha-2025-'+slug(sheet.title),'2025-07-19',rec['url'],candidates)
            p['sources'].append(rec['id']);p['coverageNotes']=['Seven members elected by Hare-Clark; current parliamentary profiles checked independently from the historical ballot.','All 2025 contestant first preference totals transcribed from the official workbook; party/group labels retain the ballot roster.']
    # WAEC public production endpoints publish the complete historical ballot.
    for key,field in [('state-wa-la-candidates','LACandidateSurname'),('state-wa-lc-candidates','LCCandidateParty')]:
        rec=registry.get(key)
        if not rec or not (ROOT/rec['rawFile']).exists():continue
        source(key,'WA Electoral Commission 2025 complete '+('Assembly' if 'la-' in key else 'Council')+' candidate roster')
        dataset=read(ROOT/rec['rawFile']);byarea={}
        for candidate in dataset.get(field,[]):
            area=candidate['ELECTORATE_NAME'];byarea.setdefault(area,[]).append({'name':candidate['BALLOT_PAPER_NAME'],'party':candidate.get('PARTY_AFFILIATION')or candidate.get('Party')or 'Independent / no party label','status':'contested','sourceUrl':rec['url']})
        for name,candidates in byarea.items():
            p=place('wa',name) if field=='LACandidateSurname' else next(p for p in d['places'] if p['id']=='state-wa-legislative-council-statewide')
            if p:
                event(p,'wa-2025-'+p['slug'],'2025-03-08',rec['url'],candidates);p['sources'].append(key)
                p['coverageNotes']=[x for x in p['coverageNotes'] if 'roster and previous contestant' not in x]+['All 2025 ballot contestants retained from the official WAEC public results service. Current office requires independent parliamentary membership verification.']
    # Browser-accessible public NT primary sources are retained as extracted
    # snapshots, clearly distinguished from original downloaded source bytes.
    path=RAW/'state-nt-individual-profiles-browser-extract.txt'
    if path.exists():
        text=path.read_text(encoding='utf-8');sid='state-nt-current-profiles-browser'
        d['sources'].append({'id':sid,'title':'NT Parliament public current member profiles, browser extracted snapshots','url':'https://parliament.nt.gov.au/members/by-name','checked':CHECKED,'rawFile':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'licence':'Publisher copyright retained; local research extraction, not original bytes for redistribution.'})
        for segment in text.split('--------------------------------------------------------------------------------'):
            url=re.search(r'\((https://parliament.nt.gov.au/members/by-name/[^)]+)\)',segment)
            if not url:continue
            body=browser_text(segment)
            name=re.search(r'(?m)^# (.+)',body);area=re.search(r'(?m)^Electorate\s*\|\s*(.+)',body);party=re.search(r'(?m)^Party\s*\|\s*(.+)',body)
            if not name or not area or not party:continue
            p=place('nt',area[1].strip())
            if p:
                name=re.sub(r'^Hon\s+','',name[1]).strip();p['representatives']=[{'name':name,'role':'Member of the Legislative Assembly','party':party[1].strip(),'profileUrl':url[1],'sourceId':sid,'checked':CHECKED}];p['sources'].append(sid)
                p['coverageNotes']=['Current parliamentary member profile independently checked against the official September 2026 member roster. Historical election winners are not used to infer current office.']
    path=RAW/'state-nt-results-browser-extract.txt'
    if path.exists():
        sid='state-nt-2024-results-browser';url='https://ntec.nt.gov.au/elections/past-elections/legislative-assembly/2024-territory-election/results'
        d['sources'].append({'id':sid,'title':'NTEC complete 2024 primary election results, browser extraction','url':url,'checked':CHECKED,'rawFile':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'licence':'Publisher copyright retained; local research extraction, normalized public result facts only.'})
        text=browser_text(path.read_text(encoding='utf-8'))
        for name,body in re.findall(r'(?m)^## ([^\n]+)\n(.*?)(?=^## |\Z)',text,re.S):
            p=place('nt',name.strip())
            if not p or '### Primary votes:' not in body:continue
            primary=body.split('### Primary votes:',1)[1].split('Updated:',1)[0];candidates=[]
            for nm,party,votes in re.findall(r'(?m)^([^|\n]+?) \(([^)]+)\)\s*\|\s*([\d,]+)\s*$',primary):
                candidates.append({'name':nm.strip(),'party':party,'status':'contested','sourceUrl':url,'votes':int(votes.replace(',','')),'voteMeasure':'first preferences'})
            event(p,'nt-2024-'+p['slug'],'2024-08-24',url,candidates);p['sources'].append(sid)
    path=RAW/'state-nt-members-browser-extract.txt'
    profiles=RAW/'state-nt-individual-profiles-browser-extract.txt'
    if path.exists() and profiles.exists():
        sid='state-nt-current-roster-20260918';url='https://parliament.nt.gov.au/members/MASTER-15th-Legislative-Assembly-List-of-Members-for-webpage-May-2026.pdf'
        d['sources'].append({'id':sid,'title':'NT Parliament current 15th Assembly member roster, dated 18 September 2026 (filename retains May)','url':url,'checked':CHECKED,'observationDate':'2026-09-18','rawFile':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'licence':'Publisher copyright retained; local research extraction, normalized factual roster only.'})
        links=[]
        for part in profiles.read_text(encoding='utf-8').split('--------------------------------------------------------------------------------'):
            m=re.search(r'^\s*(.*?)\s+[–-].*?\((https://parliament.nt.gov.au/members/by-name/[^)]+)\)',part,re.S)
            if m:links.append((re.sub(r'^Hon\s+','',m[1]).strip(),m[2]))
        text=' '.join(browser_text(path.read_text(encoding='utf-8')).split())
        blocks=re.split(r'(?=\b\d{1,2}\.\s+(?:Mr|Ms|Mrs|Hon|Dr)\s+)',text)
        for block in blocks:
            m=re.match(r'\d{1,2}\.\s+(?:Mr|Ms|Mrs|Hon|Dr)\s+(.+?)\s+MLA\b',block)
            if not m:continue
            for p in [p for p in d['places'] if p['jurisdiction']=='nt']:
                area=re.search(r'\b'+re.escape(p['name'])+r'\s+(Country Liberal Party|Territory Labor Party|Independent|NT Greens)\b',block,re.I)
                if not area:continue
                # The roster uses straight apostrophes while public profiles
                # use U+2019. Compare punctuation-free surnames, exact otherwise.
                surname=re.sub(r'[^a-z]','',m[1].split()[-1].lower());link=next(((nm,u) for nm,u in links if surname==re.sub(r'[^a-z]','',nm.split()[-1].lower())),None)
                if not link:continue
                p['representatives']=[{'name':link[0],'role':'Member of the Legislative Assembly','party':area[1],'profileUrl':link[1],'sourceId':sid,'checked':CHECKED}];p['sources'].append(sid)
                p['coverageNotes']=['Current office independently verified from the 18 September 2026 parliamentary member list, with actual individual public profile links resolved from the official current member directory.','2024 historical contestant roster complete. Later Nightcliff and Mulka by-election/replacement histories require separate official event source reconciliation.']
    for p in d['places']:p['sources']=list(dict.fromkeys(p['sources']))
    nsw=ROOT/'content/places/state-nsw-details.json'
    if nsw.exists():
        supplement=read(nsw);d['sources'].extend(supplement['sources'])
        for s in supplement['places']:
            p=next((p for p in d['places'] if p['id']==s.get('id')),None) or place('nsw',s['name'])
            if p:
                for key in ['representatives','elections','coverageNotes']:p[key]=s.get(key,p[key])
                p['sources']=list(dict.fromkeys(p['sources']+s.get('sources',[])))
    nsw_lc=ROOT/'content/places/state-nsw-lc-details.json'
    if nsw_lc.exists():
        supplement=read(nsw_lc);d['sources'].extend(supplement['sources'])
        p=next(p for p in d['places'] if p['id']=='state-nsw-legislative-council-statewide')
        s=next(s for s in supplement['places'] if s['kind']=='statewide-upper-house')
        p['representatives']=s['representatives'];p['coverageNotes']=s['coverageNotes']
        historical=s['elections']
        ids={e['id'] for e in historical};p['elections']=historical+[e for e in p['elections'] if e['id'] not in ids]
        p['sources']=list(dict.fromkeys(p['sources']+[r['id'] for r in supplement['sources']]))
        # Same NSWEC polling close applies to both chambers; keep the date-only
        # calendar key distinct from its explicitly offset-bearing deadline.
        assembly=next((x for x in d['places'] if x['jurisdiction']=='nsw' and x['chamber']=='Legislative Assembly'),None)
        upcoming=next((e for e in assembly['elections'] if (e.get('date') or '')>'2026-10-17'),None) if assembly else None
        if upcoming:
            for e in p['elections']:
                if e.get('id')=='nsw-next-lc-periodic':
                    for key in ['date','dateTime','milestoneLabel','dateBasis','timezone','sourceUrl']:
                        if key in upcoming:e[key]=upcoming[key]
    # Rights are source-specific: complete pages, scripts, and PDF snapshots are
    # local research material until explicit republication rights are established.
    permitted=[];local=[]
    for row in rows:
        if not (ROOT/row['rawFile']).exists():continue
        (permitted if row['id'].startswith(('state-boundaries-','state-boundary-count-','state-national-boundary-','state-tas-lc-geometry-','state-tas-lc-native-','state-tas-council-attributes','state-tas-council-metadata')) else local).append(row['rawFile'])
    local += [str(p.relative_to(ROOT)).replace('\\','/') for p in RAW.glob('*browser-extract.txt')]
    local += [str(p.relative_to(ROOT)).replace('\\','/') for pattern in ['*facts.json','*browser-results.json'] for p in RAW.glob(pattern)]
    write(ROOT/'content/places/sources/state-source-rights.json',{'checked':CHECKED,'publicSourceGeometry':permitted,'localOnlyResearchSnapshots':sorted(set(local)),'policy':'Publicly accessible does not establish a right to republish complete copyrighted source documents. Publish normalized factual records and links; retain full documents locally. No portraits copied. Geoscape CC BY 4.0 / LIST CC BY 3.0 geometry keeps its attribution and unmodified source bytes. SA viewer encoded geometry is delivered with ECSA CC BY 3.0 Australia attribution and retained copyright policy; the original response remains in local-only raw research. LIST native and transformed deliveries retain CC BY 3.0 Australia attribution.'})

if __name__=='__main__':main()
