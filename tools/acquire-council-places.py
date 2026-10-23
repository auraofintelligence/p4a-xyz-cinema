"""Acquire and normalise the national local-government atlas, retaining exact source geometry.

Run locally with --offline to rebuild retained data; the default also acquires official sources.
No source dates in the existing Victoria/Queensland records are silently advanced.
"""
import argparse, concurrent.futures, hashlib, html, json, re, time, unicodedata, subprocess, sys
import urllib.request, urllib.parse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'content/places/raw'
OUT=ROOT/'content/places/councils.json'
SOURCES=ROOT/'content/places/sources/council-acquisition.json'
MAP=ROOT/'assets/maps/national'
CHECKED='2026-10-17'
TZ={'nsw':'Australia/Sydney','vic':'Australia/Melbourne','qld':'Australia/Brisbane','sa':'Australia/Adelaide','wa':'Australia/Perth','tas':'Australia/Hobart','nt':'Australia/Darwin','act':'Australia/Sydney','ot':'Indian/Christmas'}
STATE={'1':'nsw','2':'vic','3':'qld','4':'sa','5':'wa','6':'tas','7':'nt','8':'act','9':'ot'}
data={'schemaVersion':1,'checked':CHECKED,'scope':'councils','sources':[],'layers':[],'places':[]}
audit={'schemaVersion':1,'checked':CHECKED,'processing':'Official service geometry requested in EPSG:4326. Original responses retained. No simplification, rounding, clipping or ring removal. Per-jurisdiction subsets preserve each geometry object exactly.','requests':[],'failures':[]}

def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(obj,ensure_ascii=False,separators=(',',':')) if p.suffix=='.geojson' else json.dumps(obj,ensure_ascii=False,indent=2)
    p.write_text(text+'\n',encoding='utf-8')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def slug(v): return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',str(v)).encode('ascii','ignore').decode().lower()).strip('-')
def fetch(url,name,refresh=False):
    p=RAW/name
    if p.exists() and not refresh:return p
    if not refresh and any(x.get('url')==url for x in audit['failures']):return None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'P4A public civic atlas research/1.0','Accept':'application/json,text/html,*/*'})
            with urllib.request.urlopen(req,timeout=100) as response: b=response.read()
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
            audit['requests'].append({'url':url,'rawFile':rel(p),'sha256':sha(p),'bytes':len(b),'checked':CHECKED})
            print('Retained',name,len(b),flush=True);return p
        except Exception as exc:
            if attempt==2:
                audit['failures'].append({'url':url,'error':str(exc),'checked':CHECKED});print('Unavailable',url,str(exc),flush=True);return None
            time.sleep(1)

def verify_transport():
    import certifi
    runtime=Path(r'C:\Users\Aura2020\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
    for entry in audit.get('transportExceptions',[]):
        url=entry['url'];target=next((RAW/x['rawFile'].split('/')[-1] for x in audit['requests'] if x['url']==url),None)
        if not target:continue
        program="import urllib.request,hashlib,json,sys,ssl; u=sys.argv[1]; c=ssl.create_default_context(cafile=sys.argv[2]); b=urllib.request.urlopen(u,timeout=70,context=c).read(); print(json.dumps({'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}))"
        result=subprocess.run([str(runtime),'-B','-c',program,url,certifi.where()],capture_output=True,text=True)
        record={'url':url,'checked':CHECKED,'runtime':'BundledPython3.12','certificateValidation':'enabled','caBundle':'certifi'+certifi.__version__,'status':'verified' if result.returncode==0 else 'failed'}
        if result.returncode==0:
            record.update(json.loads(result.stdout));record['matchesRetainedBytes']=record['sha256']==sha(target)
        else:record['error']=result.stderr[-1200:]
        audit.setdefault('transportReverification',[]).append(record);print('Verified transport',url,record['status'],flush=True)
    write(SOURCES,audit)
def source(id,title,url,checked=CHECKED,path=None,**kw):
    r={'id':id,'title':title,'url':url,'checked':checked,**kw}
    if path:r.update(rawFile=rel(path),sha256=sha(path))
    if not any(x['id']==id for x in data['sources']):data['sources'].append(r)
    return id
def layer(id,j,kind,name,path,idfield,namefield,sid,edition,attribution):
    data['layers'].append({'id':id,'jurisdiction':j,'kind':kind,'name':name,'geometryFile':rel(path),'featureIdField':idfield,'featureNameField':namefield,'sourceId':sid,'boundaryEdition':edition,'crs':'EPSG:4326','attribution':attribution})
def election(j,placeid):
    config={
      'nsw':('2024-09-14','2028-09-09','https://elections.nsw.gov.au/elections/past-results/local-election-results/2024-nsw-local-government-elections','https://elections.nsw.gov.au/elections/local-government-elections'),
      'vic':('2024-10-26','2028-10-28','https://www.vec.vic.gov.au/results/council-election-results/2024-council-election-results','https://www.vec.vic.gov.au/voting/types-of-elections/local-council-elections'),
      'qld':('2024-03-16','2028-03-25','https://results.elections.qld.gov.au/QLG2024','https://www.ecq.qld.gov.au/elections'),
      'sa':('2022-11-12','2026-11-07','https://www.ecsa.sa.gov.au/elections/council-elections/past-council-election-results/2022-council-elections','https://www.ecsa.sa.gov.au/elections/council-elections'),
      'wa':('2025-10-18','2027-10-16','https://www.elections.wa.gov.au/elections/local','https://www.elections.wa.gov.au/elections/local'),
      'tas':('2022-10-25','2026-10-27','https://www.tec.tas.gov.au/local-government/elections-2022/index.html','https://www.tec.tas.gov.au/local-government/elections-2026/'),
      'nt':('2025-08-23','2029-08-25','https://ntec.nt.gov.au/elections/2025-local-government-elections','https://ntec.nt.gov.au/elections/local-government-elections')}
    if j not in config:return []
    prev,nxt,results,upcoming=config[j]
    # Future days require individually reviewed official timetables; no dates are inferred here.
    return [{'id':placeid+'-ordinary-'+prev[:4],'label':prev[:4]+' jurisdiction ordinary-election context','kind':'jurisdiction-context','status':'historical-context','date':prev,'milestoneLabel':'postal voting closed' if j in ['vic','sa','tas'] else 'ordinary election day','dateBasis':'Jurisdiction-wide context only; not a claim that this council or ward contested this event. Individual exceptions and subsequent replacements require separate verification.','timezone':TZ[j],'sourceUrl':results,'resultsUrl':results,'candidates':[]},
      {'id':placeid+'-next-ordinary','label':'Next ordinary local government election','kind':'ordinary','status':'date-not-verified','date':None,'dateBasis':'Check the official timetable for this council. No inferred countdown date.','timezone':TZ[j],'sourceUrl':upcoming,'candidates':[]}]

def initial():
    qsrc=read(ROOT/'content/councils/qld-map-sources.json');p=ROOT/qsrc['geometry']['file']
    sid=source('council-qld-boundaries',qsrc['title'],qsrc['geometry']['request'],qsrc['checked'],p,licence=qsrc['licence'])
    layer('council-qld','qld','council','Queensland local government areas',p,'lga_code','lga',sid,qsrc['boundaryEdition'],qsrc['attribution'])
    for f in read(p)['features']:
        v=f['properties'];code=str(v['lga_code']);name=v['lga'];pid='qld-council-'+code
        data['places'].append({'id':pid,'name':name,'slug':'redland' if code=='6250' else slug(name),'jurisdiction':'qld','kind':'special-local-body' if code=='7300' else 'council','layerId':'council-qld','featureId':code,'officialUrl':'https://www.localgovernment.qld.gov.au/for-councils/local-government-directory','sources':[sid],'boundaryEdition':qsrc['boundaryEdition'],'representatives':[],'elections':[] if code=='7300' else election('qld',pid),'coverageNotes':['Current individual councillor roster, personal public profiles and complete previous contestants require council-level source reconciliation.']})
    vc=read(ROOT/'content/councils/vic.json');people=read(ROOT/'content/representatives/vic.json')['people']
    sid=source('council-vic-retained','Retained Vicmap municipality and ward snapshot','https://discover.data.vic.gov.au/dataset/vicmap-admin-local-government-area-polygon',vc['retrieved'],ROOT/'content/councils/vic.json',licence='CC BY 4.0')
    for kind,field,nfield in [('lga','lga_code','lga_official_name'),('ward','pfi','ward_label')]:
        layer('council-vic-'+kind,'vic','council' if kind=='lga' else 'ward','Victoria '+kind,ROOT/('assets/maps/vic-'+kind+'.geojson'),field,nfield,sid,vc['boundarySnapshot'],'State of Victoria, Vicmap Admin, CC BY 4.0; retained 2 October 2026 snapshot.')
    for kind in ['lga','ward']:
        for r in vc[kind]:
            # Unsubdivided electoral-structure polygons are not fictional ward pages.
            if kind=='ward' and r['kind']!='WARD':
                parent=next((p for p in data['places'] if p['id']==r.get('parentId')),None)
                if parent:parent.setdefault('mapRefs',[]).append({'layerId':'council-vic-ward','featureId':str(r['code']),'boundaryEdition':vc['boundarySnapshot']})
                continue
            pid=r['id'];islocal=kind=='lga';k='council' if islocal and r['kind']=='municipality' else 'unincorporated-area' if islocal else 'ward'
            reps=[]
            for person in people:
                if person.get('areaId')==pid:
                    reps.append({'name':person['name'],'role':person.get('role','Councillor'),'party':person.get('party'),'profileUrl':person.get('source'), 'website':next(iter(person.get('websites',[])),None),'sourceId':sid,'checked':person.get('checked',vc['retrieved'])})
            if kind=='ward':
                for member in r.get('roster',r.get('members',[])):
                    if member.get('status','current')!='current':continue
                    person=next((p for p in people if p.get('areaId')==r.get('parentId') and p.get('name')==member['name']),{})
                    reps.append({'name':member['name'],'role':member.get('role','Councillor'),'profileUrl':person.get('source','https://www.vec.vic.gov.au/electoral-boundaries/local-councils'),'sourceId':sid,'checked':vc['retrieved']})
            url=r.get('source',{}).get('url','') if isinstance(r.get('source'),dict) else r.get('source','')
            if not url:url='https://www.vec.vic.gov.au/electoral-boundaries/local-councils'
            rec={'id':pid,'name':r['name'],'slug':slug(r['name']),'jurisdiction':'vic','kind':k,'layerId':'council-vic-'+kind,'featureId':str(r['code']),'officialUrl':url,'sources':[sid],'boundaryEdition':vc['boundarySnapshot'],'representatives':reps,'elections':election('vic',pid) if k!='unincorporated-area' else [],'coverageNotes':['Retained published roster checked 2 October 2026. Subsequent vacancies and by-elections require scoped review.','Previous local-election contestant roster is not yet reconciled.']}
            if r.get('parentId'):rec['parentId']=r['parentId']
            if r.get('governance'):
                rec['governance']=r['governance']
                if r['governance']!='elected-council':rec['elections']=[]
            data['places'].append(rec)
    # Original Redland division source and public councillor profile links are reused unchanged.
    rp=ROOT/'assets/maps/redlands/redland-divisions-2024.geojson'
    rd=read(ROOT/'content/local/redland-divisions.json');rs=read(ROOT/'content/councils/redland-divisions-sources.json')
    sid=source('council-redland-divisions',rs['title'],rs['geometry']['request'],rs['checked'],rp,licence=rs['licence'])
    layer('council-redland-divisions','qld','ward','Redland City electoral divisions',rp,'objectid','elect_div',sid,rs['boundaryEdition'],rs['attribution'])
    rsid=source('council-redland-profiles','Redland City Council public councillor profiles',rd['sources'][0]['url'],rd['sources'][0]['checked'],ROOT/'content/local/redland-divisions.json')
    redfeatures=read(rp)['features']
    for d in rd['divisions']:
        number=d['id'];f=next(f for f in redfeatures if int(re.search(r'\d+',f['properties']['elect_div']).group())==number)
        person=d['representative'];pid='qld-redland-division-'+str(number)
        data['places'].append({'id':pid,'name':d['label'],'slug':'division-'+str(number),'jurisdiction':'qld','kind':'ward','parentId':'qld-council-6250','layerId':'council-redland-divisions','featureId':str(f['properties']['objectid']),'officialUrl':person['url'],'sources':[sid,rsid],'boundaryEdition':rs['boundaryEdition'],'representatives':[{'name':person['name'],'role':person['role'],'profileUrl':person['url'],'sourceId':rsid,'checked':person['checked']}],'elections':election('qld',pid),'coverageNotes':['Original Redland division and published councillor listing retained. Previous contestants require ECQ result reconciliation.']})
    if not OUT.exists():save()

def retained_national():
    p=RAW/'council-abs-lga-2026.geojson'
    if not p.exists():return
    fs=read(p)['features']
    sid=source('council-abs-2026-lga','ABS ASGS Edition4 Local Government Areas2026','https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/LGA/MapServer/0',path=p,licence='CC BY 4.0',boundaryCaveat='ABS Mesh Block approximations of gazetted legal boundaries. Exact source coordinates are retained; this is statistical navigation and not a legal address determination.')
    directories={'nsw':'https://www.olg.nsw.gov.au/public/find-my-council/','sa':'https://www.lga.sa.gov.au/sa-councils/councils-listing','wa':'https://walga.asn.au/about-walga/local-government-directory','tas':'https://www.lgat.tas.gov.au/tasmanian-councils','nt':'https://nt.gov.au/community/local-councils-remote-communities-and-homelands/local-councils-and-local-authorities','act':'https://www.act.gov.au/','ot':'https://www.infrastructure.gov.au/territories-regions-cities/territories'}
    for j in ['nsw','sa','wa','tas','nt','act']:
        features=[f for f in fs if STATE.get(f['properties']['STATE_CODE_2026'])==j and f.get('geometry')]
        dest=MAP/('council-'+j+'-abs-2026.geojson');write(dest,{'type':'FeatureCollection','features':features})
        lid='council-'+j+'-abs-2026'
        layer(lid,j,'council',j.upper()+' local areas: ABS statistical boundaries',dest,'LGA_CODE_2026','LGA_NAME_2026',sid,'ASGS Edition4 LGA2026; Mesh Block approximation of gazetted areas','Australian Bureau of Statistics, ASGS Edition4, CC BY4.0. Exact statistical boundary coordinates; not legal boundaries.')
        for f in features:
            v=f['properties'];code=v['LGA_CODE_2026'];name=v['LGA_NAME_2026'];pid=j+'-council-'+code
            kind='unincorporated-area' if 'unincorporated' in name.lower() or j=='act' else 'council'
            if j=='nt' and name=='Darwin Waterfront Precinct':kind='special-local-body'
            if j=='sa' and name in ['Anangu Pitjantjatjara Yankunytjatjara','Maralinga Tjarutja']:kind='special-local-body'
            record={'id':pid,'name':name,'slug':slug(name),'jurisdiction':j,'kind':kind,'layerId':lid,'featureId':code,'officialUrl':directories[j],'sources':[sid],'boundaryEdition':'ABS ASGS Edition4 LGA2026 (statistical approximation)','representatives':[],'elections':election(j,pid) if kind=='council' else [],'coverageNotes':['ABS statistical boundary navigation retains source coordinates exactly; it is not the gazetted legal boundary or an address eligibility service.','Current individual councillor roster, verified public profiles, legal ward geometry and complete previous contestants require council-level source reconciliation.']}
            if j=='act':record['coverageNotes']=['The ACT has no separate local government councils. The Legislative Assembly performs territory and local government functions. ABS identifies this statistical area as Unincorporated ACT.']
            if j=='sa' and name=='Roxby Downs':record['elections']=[];record['governance']='administration';record['coverageNotes'].append('Roxby Downs operates under its own administration and is excluded from the periodic council election.')
            data['places'].append(record)
    state=RAW/'council-abs-state-2026.geojson'
    if state.exists():
        sf=[f for f in read(state)['features'] if f.get('geometry')]
        dest=MAP/'council-state-context.geojson';write(dest,{'type':'FeatureCollection','features':sf})
        sid=source('council-abs-2026-states','ABS ASGS Edition4 State and Territory2026','https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/STE/MapServer/0',path=state,licence='CC BY 4.0')
        layer('national-state-context','au','state','Australian states and territories',dest,'STATE_CODE_2026','STATE_NAME_2026',sid,'ABS ASGS Edition4 State/Territory2026','Australian Bureau of Statistics, ASGS Edition4, CC BY4.0. Exact original source geometry coordinates.')
    # All actual divisions in Queensland; original Redland geometries remain their existing layer.
    p=RAW/'council-qld-divisions.geojson'
    if p.exists():
        fs=read(p)['features'];sid=source('council-qld-all-divisions','Queensland current local government electoral divisions','https://spatial-gis.information.qld.gov.au/arcgis/rest/services/Boundaries/AdministrativeBoundaries/MapServer/7',path=p,licence='CC BY 4.0')
        dest=MAP/'council-qld-divisions.geojson';write(dest,{'type':'FeatureCollection','features':[f for f in fs if f['properties']['lga']!='REDLAND CITY']})
        layer('council-qld-divisions','qld','ward','Queensland local electoral divisions',dest,'objectid','elect_div',sid,'Official current service; source elect_yr retained per feature','State of Queensland2026 and Electoral Commission of Queensland2024, CC BY4.0.')
        for f in fs:
            v=f['properties']
            if v['lga']=='REDLAND CITY':continue
            parent=next((x for x in data['places'] if x['jurisdiction']=='qld' and x['kind']=='council' and x['name'].upper()==v['lga']),None)
            if not parent:audit['failures'].append({'kind':'qld-division-parent','name':v['lga']});continue
            label=v['elect_div'].title();number=re.search(r'\d+',label);local=slug(label)
            pid=parent['id']+'-'+local
            data['places'].append({'id':pid,'name':label+(' ('+v['div_name']+')' if v.get('div_name') else ''),'slug':local,'jurisdiction':'qld','kind':'ward','parentId':parent['id'],'layerId':'council-qld-divisions','featureId':str(v['objectid']),'officialUrl':parent['officialUrl'],'sources':[sid],'boundaryEdition':str(v['elect_yr'])+' election division edition; current source service','representatives':[],'elections':election('qld',pid),'coverageNotes':['Actual division geometry retained from the official current Queensland service. Councillor roster and previous election contestants still require reconciliation.']})
    save()

def acquire_context():
    pages=[
      ('https://www.dlgwv.qld.gov.au/local-government/for-the-community/local-government-directory','council-qld-directory.html'),
      ('https://www.dlgwv.qld.gov.au/local-government/for-the-community/local-government-directory/search-the-local-government-directory','council-qld-directory-search.html'),
      ('https://www.olg.nsw.gov.au/public/local-government-directory/','council-nsw-directory.html'),
      ('https://www.olg.nsw.gov.au/public/find-my-council/','council-nsw-find.html'),
      ('https://www.lga.sa.gov.au/sa-councils/councils-listing','council-sa-directory.html'),
      ('https://walga.asn.au/about-walga/local-government-directory','council-wa-directory.html'),
      ('https://www.lgat.tas.gov.au/tasmanian-councils','council-tas-directory.html'),
      ('https://www.tec.tas.gov.au/local-government/elections-2026/index.html','council-tas-2026.html'),
      ('https://www.tec.tas.gov.au/local-government/elections-2022/index.html','council-tas-2022.html'),
      ('https://www.tec.tas.gov.au/local-government/elections-2022/results/index.html','council-tas-2022-results.html'),
      ('https://www.tec.tas.gov.au/local-government/elections-2026/candidates-menu.html','council-tas-2026-candidates.html'),
      ('https://ecsa.sa.gov.au/elections/current-elections','council-sa-2027.html'),
      ('https://ecsa.sa.gov.au/parties-and-candidates/council-elections','council-sa-timetable.html'),
      ('https://www.dhud.sa.gov.au/our-department/local-govt/office-of-local-government/local-government-elections','council-sa-election-law.html'),
      ('https://results.elections.qld.gov.au/QLG2024','council-qld-results-2024.html'),
      ('https://vtr.elections.nsw.gov.au/LG2401/index','council-nsw-results-2024.html'),
      ('https://ntec.nt.gov.au/elections/2025-local-government-elections','council-nt-results-2025.html'),
      ('https://www.elections.wa.gov.au/elections/local','council-wa-elections.html'),
      ('https://walga.asn.au/your-local-government/local-government-directory','council-wa-directory-current.html'),
      ('https://walga.asn.au/awcontent/Web/Documents/Advocacy/The-Western-Australian-Local-Government-Directory.pdf','council-wa-directory-2026.pdf'),
      ('https://resultsdata.elections.qld.gov.au/2024QLGE-electorates.json','council-qld-2024-ballots.json'),
      ('https://resultsdata.elections.qld.gov.au/XMLData/publicResults_LG2024_Inala24_IpswichWest24_Final.zip','council-qld-2024-final-results.zip'),
      ('https://data.gov.au/data/api/3/action/package_show?id=geoscape-administrative-boundaries','council-geoscape-catalogue.json'),
      ('https://data.gov.au/data/api/3/action/package_search?q=wards%20Geoscape&rows=20','council-geoscape-wards-search.json'),
      ('https://services.thelist.tas.gov.au/arcgis/rest/services/Public/CadastreAndAdministrative/MapServer/4?f=pjson','council-tas-legal-metadata.json'),
      ('https://www.ecq.qld.gov.au/elections/election-events','council-qld-events.html'),
      ('https://vtr.elections.nsw.gov.au/LG2401/albury/councillor/fp-by-grp-and-candidate-by-vote-type','council-nsw-firstpref-albury.html'),
      ('https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Administrative_Boundaries_Theme/MapServer/8?f=pjson','council-nsw-legal-lga-metadata.json'),
      ('https://services.arcgis.com/fi5AzL7DTv8s5nPl/ArcGIS/rest/services?f=pjson','council-sa-arcgis-catalogue.json')]
    params=urllib.parse.urlencode({'where':'1=1','outFields':'*','outSR':'4326','returnGeometry':'true','f':'geojson'})
    pages.extend([('https://vtr.elections.nsw.gov.au/LG2401/albury/councillor','council-nsw-contest-albury-councillor.html'),('https://www.tec.tas.gov.au/local-government/elections-2022/results/hobart-city/index.html','council-tas-2022-hobart-city.html'),('https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Administrative_Boundaries_Theme/MapServer/8/query?'+params,'council-nsw-legal-lga.geojson'),('https://services.thelist.tas.gov.au/arcgis/rest/services/Public/CadastreAndAdministrative/MapServer/4/query?'+params,'council-tas-legal.geojson')])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda pair:fetch(*pair),pages))
    # VEC prior contest pages are individually linked by retained official council records.
    vc=read(ROOT/'content/councils/vic.json')
    requests=[]
    for r in vc['lga']:
        for link in r.get('historyLinks',[]):
            if link.get('label')=='2024 election results' and link.get('url'):requests.append((link['url'],'council-vic-2024-'+r['code']+'.html'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda pair:fetch(*pair),requests))
    from bs4 import BeautifulSoup
    p=RAW/'council-nsw-results-2024.html'
    if p.exists():
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        requests=[('https://vtr.elections.nsw.gov.au'+a['href'],'council-nsw-2024-'+a['href'].split('/')[-2]+'.html') for a in s.find_all('a',href=True) if re.fullmatch('/LG2401/[^/]+/results',a['href'])]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda pair:fetch(*pair),requests))
    requests=[]
    for p in RAW.glob('council-nsw-2024-*.html'):
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for a in s.find_all('a',href=True):
            href=a['href']
            if re.fullmatch('/LG2401/[^/]+/(?:[^/]+/)?(?:councillor|mayoral)',href):requests.append(('https://vtr.elections.nsw.gov.au'+href,'council-nsw-contest-'+href.replace('/','-').strip('-')+'.html'))
    p=RAW/'council-tas-2022-results.html'
    if p.exists():
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for a in s.find_all('a',href=True):
            if re.fullmatch('[a-z-]+/index.html',a['href']):requests.append(('https://www.tec.tas.gov.au/local-government/elections-2022/results/'+a['href'],'council-tas-2022-'+a['href'].split('/')[0]+'.html'))
    p=RAW/'council-tas-2022-hobart-city.html'
    if p.exists():
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for tag in s.find_all(attrs={'w3-include-html':True}):
            href=tag['w3-include-html']
            if '/results/' in href:requests.append(('https://www.tec.tas.gov.au'+href,'council-tas-2022-hobart-fragment-'+href.split('/')[-1]))
    requests=list(dict.fromkeys(requests))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda pair:fetch(*pair),requests))
    requests=[]
    for p in RAW.glob('council-nsw-contest-LG2401-*.html'):
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for a in s.find_all('a',href=True):
            if a.get_text(' ',strip=True) in ['First Preferences','First Preference Votes by Group and Candidate and by Vote Type']:
                href=a['href'];requests.append(('https://vtr.elections.nsw.gov.au'+href,'council-nsw-ballot-'+href.replace('/','-').strip('-')+'.html'))
    for p in RAW.glob('council-tas-2022-*.html'):
        if 'fragment' in p.name:continue
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for tag in s.find_all(attrs={'w3-include-html':True}):
            href=tag['w3-include-html']
            if '/results/' in href:requests.append(('https://www.tec.tas.gov.au'+href,'council-tas-2022-fragment-'+href.replace('/','-').strip('-')))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda pair:fetch(*pair),list(dict.fromkeys(requests))))
    save()

def namekey(value):
    return ' '.join(sorted(w for w in re.findall('[a-z0-9]+',unicodedata.normalize('NFKD',value).lower()) if w not in {'the','of','city','shire','council','municipality','municipal','regional','district','corporation'}))

def enrich_retained():
    from bs4 import BeautifulSoup
    p=RAW/'council-nsw-directory.html'
    if p.exists():
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        sid=source('council-nsw-olg-directory','NSW Office of Local Government published council directory','https://www.olg.nsw.gov.au/public/local-government-directory/',path=p,licence='NSW Government copyright; public factual names/roles and public council URLs extracted. Council office addresses not republished in normalized records.')
        for table in s.select('table.council_dialog'):
            row={}
            for tr in table.find_all('tr'):
                th=tr.find('th');td=tr.find('td')
                if th and td:row[th.get_text(' ',strip=True)]=td.get_text(' ',strip=True)
            name=row.get('NAME','');place=next((r for r in data['places'] if r['jurisdiction']=='nsw' and r['kind']=='council' and namekey(r['name'])==namekey(name)),None)
            if not place:continue
            if row.get('WEBSITE','').startswith('http'):place['officialUrl']=row['WEBSITE']
            place['sources'].append(sid);reps=[]
            for key,role in [('MAYOR','Mayor'),('DEPUTY_MAYOR','Deputy Mayor'),('COUNCILLORS','Councillor')]:
                for member in row.get(key,'').split(';'):
                    member=re.sub(r'^(?:Clr|Cr|Councillor)\s+','',member.strip()).strip()
                    if member and member not in ['N/A','Vacant'] and 'administrator' not in member.lower():reps.append({'name':member,'role':role,'profileUrl':'https://www.olg.nsw.gov.au/public/local-government-directory/','website':place['officialUrl'],'sourceId':sid,'checked':CHECKED,'profileType':'official published councillor directory'})
            place['representatives']=reps
            place['coverageNotes']=['Published NSW OLG directory checked 17 October 2026; not an independent verification of each councillor profile. Individual profile links and later changes require council source reconciliation.','ABS statistical geometry is exact to its source but is not a gazetted legal boundary. Previous contestants and legal ward geometry require reconciliation.']
    # Retained VEC candidate/result tables are historical contest evidence, not current office.
    vc=read(ROOT/'content/councils/vic.json')
    for r in vc['lga']:
        if r['kind']!='municipality':continue
        p=RAW/('council-vic-2024-'+r['code']+'.html')
        if not p.exists():continue
        link=next((x['url'] for x in r.get('historyLinks',[]) if x.get('label')=='2024 election results'),None)
        if not link:continue
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser');main=s.find('main') or s
        sid=source('council-vic-2024-'+r['code'],'VEC2024 '+r['name']+' declared results and contestants',link,path=p,licence='Victorian Electoral Commission copyright; factual ballot names/results extracted and source retained.')
        contests={}
        for table in main.find_all('table'):
            heading=table.find_previous('h2');area=heading.get_text(' ',strip=True) if heading else 'Council-wide'
            if area=='Navigation':continue
            area=re.sub(r'\s*\([^)]*vacanc[^)]*\)\s*$','',area).strip()
            text=table.get_text(' ',strip=True);thead=table.find('thead')
            if thead and 'First preference votes' in thead.get_text():
                entries=contests.setdefault(area,{})
                for tr in table.find_all('tr')[1:]:
                    cells=[td.get_text(' ',strip=True) for td in tr.find_all(['td','th'])]
                    if not cells or not cells[0] or cells[0]=='Candidate':continue
                    ent=entries.get(cells[0],{'name':cells[0],'status':'contested','sourceUrl':link,'profileUrl':link,'contest':area})
                    for cell in cells[1:]:
                        if re.fullmatch(r'[\d,]+',cell):ent['votes']=int(cell.replace(',',''));ent['voteMeasure']='First preference votes';break
                    entries[cells[0]]=ent
            elif 'Elected:' in text:
                entries=contests.setdefault(area,{})
                for tr in table.find_all('tr'):
                    cells=[td.get_text(' ',strip=True) for td in tr.find_all('td')]
                    if len(cells)>=2 and cells[0]=='Elected:':
                        name=re.sub(r'\s*\(Unopposed\)\s*','',cells[1]).strip();ent=entries.setdefault(name,{'name':name,'sourceUrl':link,'profileUrl':link,'contest':area})
                        ent['status']='elected-unopposed' if 'Unopposed' in cells[1] else 'elected'
        candidates=[x for c in contests.values() for x in c.values()]
        if not candidates:continue
        place=next(x for x in data['places'] if x['id']==r['id'])
        historical={'id':r['id']+'-ordinary-2024','label':'2024 '+r['name']+' election','kind':'ordinary','status':'historical','date':'2024-10-26','milestoneLabel':'ordinary election day','dateBasis':'VEC council-specific2024 election results. Date is ordinary election day; postal ballot return deadline is separate.','timezone':TZ['vic'],'sourceUrl':link,'resultsUrl':link,'candidates':candidates}
        place['elections']=[historical]+[x for x in place['elections'] if x['id']!=historical['id'] and x['status']!='historical-context'];place['sources'].append(sid)
        for ward in data['places']:
            if ward.get('parentId')==r['id']:
                c=next((c for name,c in contests.items() if namekey(name)==namekey(ward['name'])),None)
                if c:
                    ev=dict(historical);ev['id']=ward['id']+'-ordinary-2024';ev['label']='2024 '+ward['name']+' election';ev['candidates']=list(c.values());ward['elections']=[ev]+[x for x in ward['elections'] if x['id']!=ev['id'] and x['status']!='historical-context'];ward['sources'].append(sid)
    for j,filename,url,date,milestone in [('tas','council-tas-2026.html','https://www.tec.tas.gov.au/local-government/elections-2026/index.html','2026-10-27','postal voting closes'),('sa','council-sa-timetable.html','https://ecsa.sa.gov.au/parties-and-candidates/council-elections','2027-04-07','postal voting closes')]:
        p=RAW/filename
        if not p.exists():continue
        text=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser').get_text(' ',strip=True)
        if (j=='tas' and '27' in text and 'October' in text) or (j=='sa' and '7 April 2027' in text):
            sid=source('council-'+j+'-next-timetable','Official '+j.upper()+' ordinary council election timetable',url,path=p)
            for place in data['places']:
                if place['jurisdiction']!=j or place['kind']!='council' or place.get('governance')=='administration':continue
                future=next((x for x in place['elections'] if x['id'].endswith('-next-ordinary')),None)
                if not future:continue
                future.update(label=('2026' if j=='tas' else '2027')+' ordinary council election',status='announced',date=date,dateBasis='Official electoral commission timetable; postal voting closes at '+('2pm' if j=='tas' else '5pm')+' local time.',milestoneLabel=milestone,sourceUrl=url,dateTime=date+('T14:00:00+11:00' if j=='tas' else 'T17:00:00+09:30'))
                place['sources'].append(sid)
    # Representation evidence is separate from Vicmap geometry provenance.
    for r in vc['lga']:
        src=r.get('source',{});url=src.get('url') if isinstance(src,dict) else src
        if not url:continue
        sid=source('council-vic-roster-'+r['code'],'VEC published '+r['name']+' council roster',url,vc['retrieved'],ROOT/'content/councils/vic.json')
        for place in data['places']:
            if place['id']!=r['id'] and place.get('parentId')!=r['id']:continue
            for rep in place.get('representatives',[]):rep['sourceId']=sid;rep['profileType']='official published council roster'
            if place['representatives']:place['sources'].append(sid)
    # Current NSW legal geometry is distinct from the retained ABS statistical approximation.
    p=RAW/'council-nsw-legal-lga.geojson'
    if p.exists() and not any(x['id']=='council-nsw-legal' for x in data['layers']):
        fs=read(p)['features'];dest=MAP/'council-nsw-legal.geojson';write(dest,{'type':'FeatureCollection','features':fs})
        sid=source('council-nsw-legal-boundaries','NSW Spatial Services LocalGovernmentArea boundary service','https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Administrative_Boundaries_Theme/MapServer/8',path=p,licence='NSW Spatial Services source rights retained; no additional licence is granted by P4A.')
        layer('council-nsw-legal','nsw','council','NSW official local government boundaries',dest,'rid','lganame',sid,'Current NSW Spatial Services service snapshot17 October 2026','NSW Government, Spatial Services. Original service geometries retained without simplification or rounding.')
        for f in fs:
            v=f['properties'];unincorp=v['lganame'].startswith('UNINCORPORATED')
            place=next((r for r in data['places'] if r['jurisdiction']=='nsw' and (r['kind']=='unincorporated-area' if unincorp else namekey(r['name'])==namekey(v['lganame']))),None)
            if not place:audit['failures'].append({'kind':'nsw-legal-join','name':v['lganame']});continue
            if place['layerId']!='council-nsw-legal':
                place.setdefault('mapRefs',[]).append({'layerId':place['layerId'],'featureId':place['featureId'],'boundaryEdition':place['boundaryEdition']})
                place.update(layerId='council-nsw-legal',featureId=str(v['rid']),boundaryEdition='NSW Spatial Services current legal local government service snapshot17 October 2026')
                place['sources'].append(sid)
            else:place.setdefault('mapRefs',[]).append({'layerId':'council-nsw-legal','featureId':str(v['rid']),'boundaryEdition':'NSW current local government boundary service'})
    p=RAW/'council-qld-events.html'
    if p.exists():
        text=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser').get_text(' ',strip=True)
        if 'last Saturday in March' in text:
            sid=source('council-qld-election-rule','ECQ local government ordinary-election timing rule','https://www.ecq.qld.gov.au/elections/election-events',path=p)
            for place in data['places']:
                if place['jurisdiction']!='qld' or place['kind'] not in ['council','ward']:continue
                future=next((x for x in place['elections'] if x['id'].endswith('-next-ordinary')),None)
                if future:future.update(date='2028-03-25',status='scheduled',dateBasis='ECQ rule: four-year ordinary cycle, last Saturday in March, subject to regulation and the official timetable. Countdown reaches start of local date; no polling opening time is implied.',sourceUrl='https://www.ecq.qld.gov.au/elections/election-events',milestoneLabel='scheduled ordinary election day')
                place['sources'].append(sid)
    save()

def normalise_nsw_ballots():
    from bs4 import BeautifulSoup
    index=RAW/'council-nsw-results-2024.html'
    if not index.exists():return
    soup=BeautifulSoup(index.read_text(encoding='utf-8'),'html.parser');names={}
    for a in soup.find_all('a',href=True):
        if re.fullmatch('/LG2401/[^/]+/results',a['href']):names[a['href'].split('/')[2]]=a.get_text(' ',strip=True)
    for p in RAW.glob('council-nsw-contest-LG2401-*.html'):
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        profile=next((a['href'] for a in s.find_all('a',href=True) if '/councils/' in a['href']),None)
        if not profile:continue
        councilslug=profile.rstrip('/').split('/')[-1];name=names.get(councilslug,councilslug.replace('-',' '))
        place=next((x for x in data['places'] if x['jurisdiction']=='nsw' and x['kind']=='council' and namekey(x['name'])==namekey(name)),None)
        if not place:continue
        urls=[a['href'] for a in s.find_all('a',href=True) if re.fullmatch('/LG2401/'+re.escape(councilslug)+'/(?:[^/]+/)?(?:councillor|mayoral)',a['href'])]
        contesturl=next((u for u in urls if p.name=='council-nsw-contest-'+u.replace('/','-').strip('-')+'.html'),None)
        if not contesturl:continue
        suffix=contesturl.split('/')[3:];contest='Mayor' if suffix[-1]=='mayoral' else 'Councillors' if len(suffix)==1 else suffix[0].replace('-',' ').title()
        link='https://vtr.elections.nsw.gov.au'+contesturl
        sid=source('council-nsw-2024-'+councilslug+'-'+slug(contest),'NSWEC2024 '+name+' '+contest+' contestants and results',link,path=p)
        elected={namekey(t.get_text(' ',strip=True)) for t in s.select('.candidate-name')};candidates=[]
        ballotlink=next((a['href'] for a in s.find_all('a',href=True) if a.get_text(' ',strip=True) in ['First Preferences','First Preference Votes by Group and Candidate and by Vote Type']),None)
        bp=RAW/('council-nsw-ballot-'+ballotlink.replace('/','-').strip('-')+'.html') if ballotlink else None
        if bp and bp.exists():
            b=BeautifulSoup(bp.read_text(encoding='utf-8'),'html.parser');table=b.find('table');party=None
            if table:
                for row in table.find_all('tr'):
                    cells=[td.get_text(' ',strip=True) for td in row.find_all('td')]
                    if not cells:continue
                    if suffix[-1]=='mayoral':
                        if len(cells)<3 or not re.fullmatch(r'[\d,]+',cells[2]) or 'TOTAL' in cells[0]:continue
                        cname=cells[0];votes=int(cells[2].replace(',',''));aff=cells[1] or None;measure='First preference votes'
                    else:
                        if 'tr-total' in row.get('class',[]):
                            if len(cells)>1 and cells[0]:party=cells[1] or None
                            continue
                        if len(cells)<5 or not cells[1] or not re.fullmatch(r'[\d,]+',cells[4]):continue
                        cname=cells[1];votes=int(cells[4].replace(',',''));aff=party;measure='Candidate first preference votes; group votes are reported separately in the original table'
                    c={'name':cname,'status':'elected' if namekey(cname) in elected else 'contested','votes':votes,'voteMeasure':measure,'contest':contest,'sourceUrl':'https://vtr.elections.nsw.gov.au'+ballotlink,'profileUrl':link}
                    if aff:c['party']=aff
                    candidates.append(c)
        elif 'UNCONTESTED' in s.get_text():
            for tag in s.select('.candidate-name'):
                candidates.append({'name':tag.get_text(' ',strip=True),'status':'elected-unopposed','contest':contest,'sourceUrl':link,'profileUrl':link})
        if not candidates:continue
        event={'id':place['id']+'-ordinary-2024-'+slug(contest),'label':'2024 '+name+' — '+contest,'kind':'ordinary','status':'historical','date':'2024-09-14','dateBasis':'NSWEC council-specific2024 ordinary election contestant/result record. Later by-elections and current roles are separate.','milestoneLabel':'ordinary election day','timezone':TZ['nsw'],'sourceUrl':link,'resultsUrl':link,'candidates':candidates}
        place['elections']=[e for e in place['elections'] if e['id']!=event['id'] and e.get('kind')!='jurisdiction-context']+[event];place['sources'].append(sid)
        for ward in data['places']:
            if ward.get('parentId')==place['id'] and namekey(ward['name'])==namekey(contest):
                ev=dict(event);ev['id']=ward['id']+'-ordinary-2024';ward['elections']=[e for e in ward.get('elections',[]) if e['id']!=ev['id'] and e.get('kind')!='jurisdiction-context']+[ev];ward['sources'].append(sid)
    save()

def qld_web_review():
    review=ROOT/'content/places/sources/council-qld-calendar-web-review.json'
    write(review,{'checked':CHECKED,'method':'Original official ECQ election-events page read with the web tool; local TLS verification failure is not bypassed.','url':'https://www.ecq.qld.gov.au/elections/election-events','facts':{'ordinaryRule':'Every four years on the last Saturday in March, subject to change by regulation.','lastOrdinaryElection':'2024-03-16','nextRuleDerivedDate':'2028-03-25','upcomingLocalByElection':{'place':'Tablelands Regional Council Division1','date':'2026-10-31'}}})
    sid=source('council-qld-election-rule-web','ECQ verified-web local ordinary election rule and current events','https://www.ecq.qld.gov.au/elections/election-events',path=review)
    for place in data['places']:
        if place['jurisdiction']!='qld' or place['kind'] not in ['council','ward']:continue
        event=next((e for e in place['elections'] if e['id'].endswith('-next-ordinary')),None)
        if event:event.update(date='2028-03-25',status='scheduled',dateBasis='ECQ four-year last-Saturday-in-March rule, subject to regulation and official timetable. Rule-derived date; countdown reaches the start of the local calendar date.',milestoneLabel='scheduled ordinary election day',sourceUrl='https://www.ecq.qld.gov.au/elections/election-events')
        place['sources'].append(sid)
    save()

def merge_detail_supplements():
    """Merge retained, independently sourced rosters and contest supplements only.

    This does not initialise places, acquire sources or change geometry. The TAS
    builder uses the 29 cached TEC MyReps responses plus the separate adapter's
    retained council-tas-2022 pages and live include fragments. Run
    acquire-tas-council-details.py without --acquire to reconcile that cache first.
    """
    by_id={p['id']:p for p in data['places']}
    for filename in ['tas-council-details.json','wa-council-details.json','sa-council-ballots.json','sa-current-leaders.json','qld-council-ballots.json','qld-current-leaders.json','nt-council-details.json']:
        path=ROOT/'content/places'/filename
        if not path.exists():continue
        supplement=read(path)
        source_ids={s['id'] for s in supplement['sources']}
        for entry in supplement['sources']:
            original=ROOT/entry['rawFile'] if entry.get('rawFile') else None
            if original and (not original.is_file() or sha(original)!=entry['sha256']):
                raise ValueError('Missing or changed retained detail source: '+str(original))
            existing=next((i for i,s in enumerate(data['sources']) if s['id']==entry['id']),None)
            if existing is None:data['sources'].append(entry)
            else:data['sources'][existing]=entry
        for patch in supplement['places']:
            place=by_id[patch['id']]
            previous=place.get('representatives',[])
            unexpected=[r for r in previous if r.get('sourceId') not in source_ids]
            if unexpected and patch.get('representatives'):
                raise ValueError('Independently sourced roster requires explicit reconciliation before replacement: '+place['id'])
            if patch.get('representatives'):place['representatives']=patch['representatives']
            if 'rosterHistory' in patch:place['rosterHistory']=patch['rosterHistory']
            for event in patch.get('elections',[]):
                place['elections']=[e for e in place.get('elections',[]) if e['id']!=event['id'] and e.get('kind')!='jurisdiction-context']+[event]
            place['sources']=list(dict.fromkeys(place.get('sources',[])+patch.get('sources',[])))
            if patch.get('officialUrl'):place['officialUrl']=patch['officialUrl']
            if patch.get('governance'):place['governance']=patch['governance']
            notes=[n for n in place.get('coverageNotes',[]) if not ('representatives' in patch and n.startswith('Current individual councillor roster, verified public profiles'))]
            notes+=patch.get('coverageNotes',[])
            if filename.startswith('tas-'):
                notes+=['Current roles come independently from the TEC MyReps roster updated 31 July 2026, checked 17 October 2026; later changes require review. Official roster links are not individual biographies.','All three 2022 office contests retain separate TEC final ballot/declaration facts. A 2022 winner is not inferred to be a current officeholder.']
            place['coverageNotes']=list(dict.fromkeys(notes))
        print('Merged retained detail supplement',filename,supplement.get('coverage',{}),flush=True)
    import runpy
    ward_adapter=ROOT/'tools/merge-council-ward-supplements.py'
    if ward_adapter.exists():
        report=runpy.run_path(str(ward_adapter))['merge'](data)
        print('Reconciled retained ward supplements',report.get('status','complete'),flush=True)
    save()

def save():
    for place in data['places']:place['sources']=list(dict.fromkeys(place.get('sources',[])))
    # Preserve the public lossless delivery paths when merging retained data.
    # Expanded originals remain optional local copies under the retention policy.
    retention=ROOT/'content/places/source-retention.json'
    local_only=set(read(retention).get('localOnlyFiles',[])) if retention.exists() else set()
    for layer in data['layers']:
        original=layer.get('geometryFile')
        if original in local_only and (ROOT/(original+'.gz')).is_file():
            layer['geometryFile']=original+'.gz'
    write(OUT,data);write(SOURCES,audit)
    print('Saved',len(data['places']),'places',len(data['layers']),'layers',flush=True)

def national():
    # Discover the currently published ABS catalogue rather than assuming an edition endpoint.
    catalog=fetch('https://geo.abs.gov.au/arcgis/rest/services?f=pjson','council-abs-services.json')
    urls=[('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/LGA/MapServer?f=pjson','council-abs-lga-2026-metadata.json'),('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/LGA/MapServer/0?f=pjson','council-abs-lga-2026-layer.json'),('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/STE/MapServer?f=pjson','council-abs-state-2026-metadata.json'),('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/STE/MapServer/0?f=pjson','council-abs-state-2026-layer.json'),('https://spatial-gis.information.qld.gov.au/arcgis/rest/services/Boundaries/AdministrativeBoundaries/MapServer/7?f=pjson','council-qld-divisions-metadata.json')]
    for u,n in urls:fetch(u,n)
    if catalog:
        c=read(catalog);print('ABS folders',c.get('folders'),flush=True)
        for folder in ['ASGS2026']:
            p=fetch('https://geo.abs.gov.au/arcgis/rest/services/'+folder+'?f=pjson','council-abs-'+folder+'-catalogue.json')
            if p:print(folder,[(x['name'],x['type']) for x in read(p).get('services',[]) if any(t in x['name'].lower() for t in ['lga','state','ste','boundary'])],flush=True)
    params=urllib.parse.urlencode({'where':'1=1','outFields':'*','outSR':'4326','returnGeometry':'true','f':'geojson'})
    queries=[('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/LGA/MapServer/0/query?'+params,'council-abs-lga-2026.geojson'),('https://geo.abs.gov.au/arcgis/rest/services/ASGS2026/STE/MapServer/0/query?'+params,'council-abs-state-2026.geojson'),('https://spatial-gis.information.qld.gov.au/arcgis/rest/services/Boundaries/AdministrativeBoundaries/MapServer/7/query?'+params,'council-qld-divisions.geojson')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(lambda pair:fetch(*pair),queries))
    for p in results:
        if p:
            d=read(p);print(p.name,'Features',len(d.get('features',[])),'First',str(d.get('features',[{}])[0].get('properties',{}))[:1500],flush=True)
    save()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');parser.add_argument('--context-only',action='store_true');parser.add_argument('--verify-transport',action='store_true');parser.add_argument('--merge-details-only',action='store_true',help='Offline: merge reconciled TAS/WA detail supplements into existing canonical places without reinitialising or acquiring.');args=parser.parse_args()
    RAW.mkdir(parents=True,exist_ok=True);MAP.mkdir(parents=True,exist_ok=True)
    if args.merge_details_only:
        data=read(OUT)
        if SOURCES.exists():audit=read(SOURCES)
        merge_detail_supplements();sys.exit(0)
    if args.verify_transport:
        audit=read(SOURCES);verify_transport();sys.exit(0)
    if args.context_only:
        data=read(OUT)
        if SOURCES.exists():audit=read(SOURCES)
    else:
        initial()
        if not args.offline:national()
        retained_national()
    if not args.offline:acquire_context()
    enrich_retained()
    normalise_nsw_ballots()
    qld_web_review()
    merge_detail_supplements()
