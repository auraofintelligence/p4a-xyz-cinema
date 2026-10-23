"""Lossless offline integration of retained ECSA and LIST originals.

Projection dependencies: pyproj 3.6.1 and pyshp 3.1.6. The local geometry
environment may be installed in ignored tmp/state-geometry-libs. No network.
"""
import gzip, hashlib, io, json, pathlib, re, sys, zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
RAW=ROOT/'content/places/raw/state'
CHECKED='2026-10-17'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def slug(value):
    import unicodedata
    return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().lower()).strip('-')

def source(d,rows,sid,title,licence=None):
    r=next(r for r in rows if r['id']==sid)
    if not any(s['id']==sid for s in d['sources']):
        d['sources'].append({**r,'title':title,'licence':licence or 'Publisher rights retained; factual results only; original research retained locally.'})
    return r

def deliver(d,features,lid,**properties):
    data=json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False,separators=(',',':')).encode()
    path=ROOT/'assets/maps/national'/(lid+'.geojson.gz')
    path.write_bytes(gzip.compress(data,mtime=0))
    layer={'id':lid,'geometryFile':path.relative_to(ROOT).as_posix(),'crs':'EPSG:4326','featureCount':len(features),'uncompressedBytes':len(data),'uncompressedSha256':hashlib.sha256(data).hexdigest(),**properties}
    d['layers']=[l for l in d['layers'] if l['id']!=lid]+[layer]
    return layer

def decode_path(value):
    # Google's encoded-polyline algorithm, exactly as used by ECSA App.js.
    ints=[];n=shift=0
    for char in value:
        b=ord(char)-63;n|=(b&31)<<shift
        if b<32:
            ints.append(~(n>>1) if n&1 else n>>1);n=shift=0
        else:shift+=5
    assert shift==0 and len(ints)%2==0
    lat=lon=0;points=[]
    for i in range(0,len(ints),2):
        lat+=ints[i];lon+=ints[i+1];points.append([lon/100000,lat/100000])
    assert len(points)>=4 and points[0]==points[-1]
    return points

def inside(point,ring):
    x,y=point;result=False
    for a,b in zip(ring,ring[1:]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
    return result

def polygons(rings):
    # Recover topology from complete rings without changing their ordering or
    # coordinates. ECSA's viewer puts every ring into one even/odd path set.
    bounds=[(min(p[0] for p in r),min(p[1] for p in r),max(p[0] for p in r),max(p[1] for p in r)) for r in rings]
    parents=[]
    areas=[abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:]))) for r in rings]
    for i,r in enumerate(rings):
        possible=[j for j,s in enumerate(rings) if j!=i and areas[j]>areas[i] and bounds[j][0]<=bounds[i][0] and bounds[j][1]<=bounds[i][1] and bounds[j][2]>=bounds[i][2] and bounds[j][3]>=bounds[i][3] and inside(r[0],s)]
        parents.append(min(possible,key=lambda j:areas[j]) if possible else None)
    def depth(i):return 0 if parents[i] is None else depth(parents[i])+1
    out=[]
    for i,r in enumerate(rings):
        if depth(i)%2==0:out.append([r]+[rings[j] for j in range(len(rings)) if parents[j]==i and depth(j)%2])
    assert sum(len(p) for p in out)==len(rings)
    return out

def sa_geography(d,rows):
    sid='state-sa-map-geometry';path=RAW/(sid+'.html')
    if not path.exists():return
    source(d,rows,sid,'ECSA official 2026 and 2022 district viewer encoded geometry','CC BY 3.0 Australia, ECSA copyright policy; Government of South Australia 2011. Third-party exceptions retained.')
    if any(r['id']=='state-sa-copyright' for r in rows):source(d,rows,'state-sa-copyright','ECSA official copyright and Creative Commons licence policy','CC BY 3.0 Australia; source policy, third-party exceptions retained.')
    geometry=read(path)
    assert len(geometry['2026'])==47
    lid='state-sa-assembly-2026';features=[]
    current={slug(p['name']):p for p in d['places'] if p['jurisdiction']=='sa'}
    valid=set()
    for item in geometry['2026']:
        key=slug(item['name']);valid.add(key);name=item['name'].title()
        rings=[decode_path(p) for p in item['paths']]
        features.append({'type':'Feature','properties':{'districtId':key,'name':name,'sourceName':item['name']},'geometry':{'type':'MultiPolygon','coordinates':polygons(rings)}})
        p=current.get(key)
        if p is None:
            p={'id':'state-sa-2026-'+key,'name':name,'slug':key,'jurisdiction':'sa','kind':'state-district','chamber':'House of Assembly','officialUrl':'https://www.ecsa.sa.gov.au/map','sources':[],'representatives':[],'elections':[],'coverageNotes':[]}
            # A newly named district is independently created; no old Frome
            # results/member/statistics or assumed successor relationship.
            template=next(x for x in d['places'] if x['jurisdiction']=='sa' and x['chamber']=='House of Assembly')
            p['elections']=[dict(e,candidates=[]) for e in template['elections']]
            d['places'].append(p)
        elif p.get('layerId'):
            p['mapRefs']=[{'layerId':p['layerId'],'featureId':p['featureId'],'boundaryEdition':p['boundaryEdition'],'status':'historical'}]
        p.update(layerId=lid,featureId=key,boundaryEdition='ECSA 2026 state election district viewer edition')
        p['sources']=list(dict.fromkeys(p['sources']+[sid]))
    for key,p in current.items():
        if p['chamber']=='House of Assembly' and key not in valid:
            p['status']='historical';p['elections']=[]
            p['sources']=list(dict.fromkeys(p['sources']+[sid,'state-sa-ha-api']))
            p['coverageNotes']=['Historical district in the retained May 2025 national layer. Absent from the official 2026 district roster. No current member or next election is assigned; current Ngadjuri is a separate place, with no assumed one-to-one correspondence.']
    deliver(d,features,lid,jurisdiction='sa',kind='state-district',name='House of Assembly districts — 2026 election',featureIdField='districtId',featureNameField='name',sourceId=sid,boundaryEdition='ECSA 2026 state election district viewer edition',nativeCrs='EPSG:4326 (official encoded viewer paths)',coordinateNote='Decoded official Google encoded-polyline paths at their original 1e-5 degree source precision, with every point and ring preserved. Containment groups holes and multipart rings without changing coordinates. This is the official viewer representation, not the legal boundary instrument.',attribution='Government of South Australia 2011 / Electoral Commission of South Australia; CC BY 3.0 Australia. Copyright exceptions and original encoded source retained.',licenceUrl='https://www.ecsa.sa.gov.au/copyright')
    old=next(l for l in d['layers'] if l['id']=='state-sa-assembly-2025')
    old['name']='House of Assembly districts — historical national May 2025 source'
    old['status']='historical'
    current_layer=next(l for l in d['layers'] if l['id']==lid)
    d['layers'].remove(current_layer)
    d['layers'].insert(d['layers'].index(old),current_layer)

def tas_council_geometry(d,rows):
    path=RAW/'state-tas-lc-official-zip.html'
    if not path.exists():return
    sid='state-tas-lc-official-zip';lid='state-tas-council-2017'
    source(d,rows,sid,'LIST full official Legislative Council division download; native EPSG:28355 shapefile','the LIST © State of Tasmania; CC BY 3.0 Australia; original source and attribution retained.')
    audit_path=ROOT/'content/places/qa/state-tas-geometry-verification.json'
    zip_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    if audit_path.exists():
        cached=read(audit_path);layer=cached.get('layer',{})
        files=[(layer.get('geometryFile'),cached.get('compressedGeometrySha256')),(layer.get('nativeGeometryFile'),cached.get('compressedNativeSha256'))]
        if cached.get('sourceZipSha256')==zip_hash and all(p and h and (ROOT/p).exists() and hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in files):
            d['layers']=[l for l in d['layers'] if l['id']!=lid]+[layer]
            for p in d['places']:
                if p['id'].startswith('state-tas-lc-'):p['layerId']=lid;p['sources']=list(dict.fromkeys(p['sources']+[sid]));p['boundaryEdition']=layer['boundaryEdition']
            print('LIST original and both cached deliveries match verified hashes',flush=True)
            return
    sys.path.insert(0,str(ROOT/'tmp/state-geometry-libs'))
    import shapefile
    from pyproj import Transformer, __version__ as proj_version
    z=zipfile.ZipFile(path);stem='list_legislative_council_divs_statewide'
    reader=shapefile.Reader(**{ext:io.BytesIO(z.read(stem+'.'+ext)) for ext in ['shp','shx','dbf']})
    projection=z.read(stem+'.prj').decode()
    transformer=Transformer.from_crs('EPSG:28355','EPSG:4326',always_xy=True)
    reverse=Transformer.from_crs('EPSG:4326','EPSG:28355',always_xy=True)
    features=[];native=[];max_error=0;point_count=ring_count=0
    for record in reader.iterShapeRecords():
        attrs=record.record.as_dict();shape=record.shape
        # pyshp's topology adapter keeps every vertex; the native delivery also
        # retains original ordered SHP rings independently for exact checking.
        starts=list(shape.parts)+[len(shape.points)]
        rings=[[list(p) for p in shape.points[a:b]] for a,b in zip(starts,starts[1:])]
        transformed=[]
        for ring in rings:
            xs,ys=zip(*ring)
            lons,lats=transformer.transform(xs,ys)
            back_x,back_y=reverse.transform(lons,lats)
            max_error=max(max_error,max(abs(a-b) for a,b in zip(xs,back_x)),max(abs(a-b) for a,b in zip(ys,back_y)))
            out=[list(p) for p in zip(lons,lats)]
            assert ring[0]==ring[-1] and out[0]==out[-1]
            transformed.append(out)
        point_count+=len(shape.points);ring_count+=len(rings)
        # ESRI SHP exterior/hole winding is authoritative here. Use pyshp's
        # topology adapter instead of testing every island against a million-
        # vertex mainland coastline; retain and verify every original ring.
        geo=shape.__geo_interface__
        native_polys=[geo['coordinates']] if geo['type']=='Polygon' else geo['coordinates']
        def key(r):return (len(r),tuple(r[0]),tuple(r[1]),tuple(r[-2]))
        index={key(r):i for i,r in enumerate(rings)}
        assert len(index)==len(rings)
        delivered=[];used=[]
        for poly in native_polys:
            out=[]
            for ring in poly:
                i=index[key(ring)]
                assert all(tuple(a)==tuple(b) for a,b in zip(ring,rings[i]))
                out.append(transformed[i]);used.append(i)
            delivered.append(out)
        assert sorted(used)==list(range(len(rings)))
        features.append({'type':'Feature','properties':attrs,'geometry':{'type':'MultiPolygon','coordinates':delivered}})
        native.append({'LEG_CNL_ID':attrs['LEG_CNL_ID'],'NAME':attrs['NAME'],'rings':rings})
        print('LIST geometry: '+attrs['NAME']+' / '+str(len(shape.points))+' retained vertices',flush=True)
    assert len(features)==15 and max_error<0.000001
    native_path=ROOT/'assets/maps/national/state-tas-council-2017-native.json.gz'
    native_bytes=json.dumps({'crs':'EPSG:28355','projectionWkt':projection,'features':native},ensure_ascii=False,separators=(',',':')).encode()
    native_path.write_bytes(gzip.compress(native_bytes,mtime=0))
    sid='state-tas-lc-official-zip'
    source(d,rows,sid,'LIST full official Legislative Council division download; native EPSG:28355 shapefile','the LIST © State of Tasmania; CC BY 3.0 Australia; original source and attribution retained.')
    lid='state-tas-council-2017'
    layer=deliver(d,features,lid,jurisdiction='tas',kind='state-region',name='Legislative Council divisions — 2017 redistribution',featureIdField='LEG_CNL_ID',featureNameField='NAME',sourceId=sid,boundaryEdition='2017 redistribution; official LIST full download, checked 17 October 2026',nativeCrs='EPSG:28355',coordinateNote='All native original SHP vertices/rings retained in companion native delivery; transformed with pyproj '+proj_version+' / PROJ from GDA94 MGA55 to geographic EPSG:4326, always_xy. No simplification/rounding/clipping. The GDA94/WGS84 display datum operation has metre-level accuracy; the map is not an eligibility instrument.',attribution='the LIST © State of Tasmania; CC BY 3.0 Australia.',nativeGeometryFile=native_path.relative_to(ROOT).as_posix(),nativeUncompressedSha256=hashlib.sha256(native_bytes).hexdigest(),sourcePointCount=point_count,sourceRingCount=ring_count,roundTripMaximumErrorMetres=max_error,transformation=transformer.description)
    for p in d['places']:
        if p['id'].startswith('state-tas-lc-'):
            p['layerId']=lid;p['sources']=list(dict.fromkeys(p['sources']+[sid]));p['boundaryEdition']=layer['boundaryEdition']
    audit={'checked':CHECKED,'scope':'All 15 official LIST Legislative Council SHP features','sourceZipSha256':zip_hash,'shapefileSha256':hashlib.sha256(z.read(stem+'.shp')).hexdigest(),'nativeCrs':'EPSG:28355','deliveredCrs':'EPSG:4326','features':len(features),'rings':ring_count,'points':point_count,'roundTripMaximumErrorMetres':max_error,'transformer':transformer.description,'nativeCoordinateRetention':'All ordered native SHP rings are retained without changes in companion nativeGeometryFile; original licensed ZIP retained locally.','layer':layer,'compressedGeometrySha256':hashlib.sha256((ROOT/layer['geometryFile']).read_bytes()).hexdigest(),'compressedNativeSha256':hashlib.sha256(native_path.read_bytes()).hexdigest(),'status':'PASS'}
    audit_path.write_text(json.dumps(audit,indent=2)+'\n',encoding='utf8')

def tas_events(d,rows):
    """Division-specific calendar and actual historical polls; no guessed day."""
    import datetime
    from bs4 import BeautifulSoup
    source(d,rows,'state-tas-lc-calendar','TEC Legislative Council six-year division election calendar')
    hist=source(d,rows,'state-tas-lc-history','TEC Legislative Council 2018-present election history and polling dates')
    calendar=BeautifulSoup((RAW/'state-tas-lc-calendar.html').read_text(encoding='utf8'),'html.parser')
    places={p['name']:p for p in d['places'] if p['id'].startswith('state-tas-lc-')}
    for p in places.values():p['elections']=[e for e in p['elections'] if not e['id'].startswith('tas-lc-')]
    for tr in calendar.select('table tr'):
        cells=tr.find_all(['th','td'],recursive=False)
        if len(cells)!=2 or not re.fullmatch(r'20\d\d',cells[0].get_text(strip=True)):continue
        year=int(cells[0].get_text(strip=True));text=cells[1].get_text(' ',strip=True)
        for name,p in places.items():
            if re.search(r'\b'+re.escape(name)+r'\b',text):
                next_year=year if year>2026 else year+6
                p['elections'].append({'id':'tas-lc-'+str(next_year)+'-'+p['slug'],'label':'Next '+name+' Legislative Council periodic election — May '+str(next_year),'kind':'periodic-election','status':'date-unannounced','date':None,'dateBasis':'Official TEC six-year calendar names May '+str(year)+'; subsequent six-year cycle where applicable. Exact polling day unannounced.','timezone':'Australia/Hobart','sourceUrl':next(r['url'] for r in rows if r['id']=='state-tas-lc-calendar'),'candidates':[]})
    soup=BeautifulSoup((RAW/'state-tas-lc-history.html').read_text(encoding='utf8'),'html.parser')
    year=date=None
    for node in soup.find_all(['h2','table']):
        text=node.get_text(' ',strip=True)
        if node.name=='h2':
            year=int(text) if re.fullmatch('20\d\d',text) else None
            continue
        if not year:continue
        match=re.search(r'Polling [Dd]ay:\s*(\d{1,2} \w+)',text)
        if match:
            date=datetime.datetime.strptime(match[1]+' '+str(year),'%d %B %Y').date().isoformat();continue
        if not date or 'Division Retiring member Elected candidate' not in text:continue
        for tr in node.select('tr'):
            cells=tr.find_all('td',recursive=False)
            if len(cells)!=3:continue
            area=cells[0].get_text(' ',strip=True);name=area.replace(' (by-election)','');p=places.get(name)
            if not p:continue
            kind='by-election' if '(by-election)' in area else 'periodic-election'
            p['elections'].append({'id':'tas-lc-'+date+'-'+p['slug'],'label':str(year)+' '+name+' Legislative Council '+('by-election' if kind=='by-election' else 'periodic election'),'kind':kind,'status':'historical','date':date,'dateBasis':'Official TEC election history; elected name alone is not a complete contestant ballot','timezone':'Australia/Hobart','sourceUrl':hist['url'],'candidates':[]})
    for p in places.values():
        p['elections'].sort(key=lambda e:(e['status']!='historical',e.get('date') or ''),reverse=True)
        p['sources']=list(dict.fromkeys(p['sources']+['state-tas-lc-calendar','state-tas-lc-history']))
        p['coverageNotes']=[x for x in p['coverageNotes'] if 'Previous periodic election' not in x]+['Division-specific six-year cycle and 2018–2026 historical polls, including by-elections, are sourced from TEC. Exact future polling days and complete historical contestant ballots remain unavailable in this adapter.']

def sa_results(d,rows):
    path=RAW/'state-sa-2026-ha-results.html'
    if not path.exists():return
    static=read(path);change=read(RAW/'state-sa-2026-ha-change.html')
    assert static['electionDate']==change['electionDate']=='2026-03-21' and len(static['districts'])==len(change['districts'])==47
    source(d,rows,'state-sa-2026-ha-results','ECSA 2026 complete House of Assembly ballot roster')
    rec=source(d,rows,'state-sa-2026-ha-change','ECSA 2026 final House of Assembly results and distribution rounds')
    changes={slug(x['districtId']):x for x in change['districts']}
    for district in static['districts']:
        key=slug(district['districtName']);p=next(p for p in d['places'] if p['jurisdiction']=='sa' and p['slug']==key)
        result=changes[key];rounds=result['finalDistribution']
        first=next((r for r in rounds if r['roundNumber']==0),None)
        candidates=[]
        for item in district['candidates']:
            c={'name':item['candidateName'],'party':item['partyName'],'status':'contested','sourceUrl':rec['url']}
            # Final official round 0 includes all original first preferences;
            # ordinaryVotes/declarationVotes can be outdated intermediate totals.
            if first:
                words=sorted(re.findall(r'\w+',item['candidateName'].lower()))
                match=[r for r in first['candidateResults'] if sorted(re.findall(r'\w+',r['candidateName'].lower()))==words]
                assert len(match)==1,(key,item['candidateName'])
                c.update(votes=match[0]['progressiveTotal'],voteMeasure='first preferences — final distribution round 0')
            candidates.append(c)
        p['elections'].insert(0,{'id':'sa-ha-2026-'+key,'label':'2026 House of Assembly election','kind':'general-election','status':'historical','date':'2026-03-21','dateBasis':'Official ECSA state election results','timezone':'Australia/Adelaide','sourceUrl':rec['url'],'resultsUrl':'https://result.ecsa.sa.gov.au/','boundaryEdition':'ECSA 2026 state election district viewer edition','resultStatus':change['electionStatus'],'resultUpdated':change['lastUpdated'],'candidates':candidates})
        p['sources']=list(dict.fromkeys(p['sources']+['state-sa-2026-ha-results',rec['id']]))
        p['coverageNotes']=[x for x in p['coverageNotes'] if 'Previous 2026 election contestants require' not in x]+['All 2026 ballot contestants retained. First preferences use official final distribution round 0, independently joined to the static ballot roster. Current members remain independently sourced from Parliament.']
    # LC aggregate party totals are not people and are never candidate rows.
    for sid in ['state-sa-2026-lc-results','state-sa-2026-lc-change']:
        source(d,rows,sid,'ECSA 2026 Legislative Council aggregate result feed; individual roster not included')
    p=next(p for p in d['places'] if p['id']=='state-sa-legislative-council-statewide')
    candidates=[];ballot_path=RAW/'state-sa-2026-lc-ballot.html'
    if ballot_path.exists():
        from bs4 import BeautifulSoup
        ballot=source(d,rows,'state-sa-2026-lc-ballot','ECSA 2026 complete Legislative Council ballot names, groups, affiliations and positions')
        soup=BeautifulSoup(ballot_path.read_text(encoding='utf8'),'html.parser')
        for tr in soup.select('table tr'):
            cells=[td.get_text(' ',strip=True) for td in tr.find_all('td',recursive=False)]
            if len(cells)!=4 or not cells[3].isdigit() or ',' not in cells[1]:continue
            candidates.append({'name':cells[1].replace('*','').strip(),'party':cells[2],'status':'contested','sourceUrl':ballot['url'],'group':cells[0],'ballotPosition':int(cells[3])})
        assert len(candidates)==48,len(candidates)
        p['sources'].append(ballot['id'])
    order_path=RAW/'state-sa-2026-lc-elected-order.html'
    if order_path.exists():
        import csv,io
        order=source(d,rows,'state-sa-2026-lc-elected-order','ECSA 2026 Legislative Council elected order, count and final vote-stage CSV')
        elected=[]
        for row in csv.DictReader(io.StringIO(order_path.read_text(encoding='utf-8-sig'))):
            rank=(row.get('Order Elected') or '').strip()
            if not rank.isdigit():continue
            name=(row['Candidate'] or '').replace('*','').strip()
            words=sorted(re.findall(r'\w+',name.lower()))
            match=[c for c in candidates if sorted(re.findall(r'\w+',c['name'].lower()))==words]
            assert len(match)==1,name
            c=match[0];count=int(row['Count Number'].replace(',',''));c['sourceUrl']=order['url']
            c.update(status='elected in this event; order '+rank+'; count '+str(count),electedOrder=int(rank),electedCount=count,resultSourceUrl=order['url'])
            stage=row['Votes'].strip()
            if stage.lower()=='quota':c['result']='elected at quota; order '+rank+'; count '+str(count)
            else:c.update(votes=int(stage.replace(',','')),voteMeasure='final count-stage vote value when elected at count '+str(count)+'; not first preferences')
            elected.append(int(rank))
        assert sorted(elected)==list(range(1,12))
        p['sources'].append(order['id'])
    lc=read(RAW/'state-sa-2026-lc-change.html')
    groups=[{'group':g['groupId'],'name':g['groupName'],'votes':g['votes'],'voteMeasure':'group first preferences — official final aggregate'} for g in lc['parties']]
    p['elections'].insert(0,{'id':'sa-lc-2026','label':'2026 Legislative Council periodic election','kind':'periodic-election','status':'historical','date':'2026-03-21','dateBasis':'Official ECSA state election result feed; 11 seats contested','timezone':'Australia/Adelaide','sourceUrl':'https://result.ecsa.sa.gov.au/','resultsUrl':'https://result.ecsa.sa.gov.au/','resultStatus':lc['electionStatus'],'resultUpdated':lc['lastUpdated'],'candidates':candidates,'groupResults':groups,'formalVotes':lc['totalFormalVotes'],'informalVotes':lc['totalInformalVotes']})
    p['sources']=list(dict.fromkeys(p['sources']+['state-sa-2026-lc-results','state-sa-2026-lc-change']))
    p['coverageNotes']=[x for x in p['coverageNotes'] if 'Previous 2026 election contestants require' not in x]+['2026 periodic election contested 11 seats; all 48 individual ballot names and affiliations are retained. Group first-preference aggregates remain explicitly separate from candidate records. Individual candidate first preferences/final transfer values await their dedicated official report; no result-stage votes are mislabeled.']

def wa_members(d):
    """Independent current office from normal-browser official roster tables."""
    path=RAW/'state-wa-current-browser-facts.json'
    if not path.exists():return
    facts=read(path)
    assert len(facts['records'])==96 and len({p['profileUrl'] for p in facts['records']})==96
    for house,tag,count in [('Legislative Assembly','la',59),('Legislative Council','lc',37)]:
        sid='state-wa-current-'+tag+'-browser-roster'
        rec=next(s for s in facts['sources'] if ('MembLA' if tag=='la' else 'MembLC') in s['url'])
        rows=[r for r in facts['records'] if r['house']==house]
        assert len(rows)==rec['records']==count
        d['sources']=[s for s in d['sources'] if s['id']!=sid]+[{'id':sid,'title':'WA Parliament current '+house+' official member table; normal browser factual extraction','url':rec['url'],'checked':facts['checked'],'rawFile':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'extractionMethod':facts['method'],'licence':'Publisher rights retained. Minimal factual names/roles/affiliations/profile links only; no contacts, portraits or full directory republished.'}]
        affected=[]
        for row in rows:
            if tag=='lc':p=next(p for p in d['places'] if p['id']=='state-wa-legislative-council-statewide')
            else:p=next(p for p in d['places'] if p['jurisdiction']=='wa' and p['chamber']==house and slug(p['name'])==slug(row['district']))
            if p['id'] not in affected:p['representatives']=[];affected.append(p['id'])
            name=re.sub(r'^(?:(?:Hon\.?|Mr|Mrs|Ms|Dr)\s+)+','',row['name']).strip()
            p['representatives'].append({'name':name,'sourceName':row['name'],'role':'Member of the '+house,'party':row['party'],'profileUrl':row['profileUrl'],'sourceId':sid,'checked':facts['checked']})
            p['sources']=list(dict.fromkeys(p['sources']+[sid]))
            p['coverageNotes']=[x for x in p['coverageNotes'] if 'Current office requires independent' not in x and 'Current member and previous' not in x and 'Current member roster' not in x]+['Current office independently verified from the Parliament current-member table in the normal public browser. Affiliation codes and official profile URLs retain the source display.']
        assert len(affected)==(59 if tag=='la' else 1)
