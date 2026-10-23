#!/usr/bin/env python3
"""Retain legally public ward services and deliver exact queried geometry.

Only writes council-ward-supp-* files and the council ward supplement. TLS
certificate and hostname verification always remain enabled; access denials
are recorded, never bypassed.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import re
import ssl
import struct
import urllib.request
from urllib.parse import urlencode

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'content/places/raw'
SOURCES=ROOT/'content/places/sources'
MAPS=ROOT/'assets/maps/national'
CHECKED='2026-10-17'
WARD='https://services-ap1.arcgis.com/ypkPEy1AmwPKGNNv/ArcGIS/rest/services/Wards/FeatureServer'
URLS={
    'geoscape-ward-service.json':WARD+'?f=pjson',
    'geoscape-ward-layer.json':WARD+'/0?f=pjson',
    'geoscape-ward-item.json':'https://www.arcgis.com/sharing/rest/content/items/1f8666324f5c4bf883a4900c9d640a4d?f=pjson',
    'geoscape-lga-item.json':'https://www.arcgis.com/sharing/rest/content/items/9ba11864213d4df09a749f2df029627c?f=pjson',
    'nsw-ward-search.json':'https://www.arcgis.com/sharing/rest/search?'+urlencode({'q':'(wards OR "ward boundaries") AND (NSW OR "New South Wales")','num':100,'f':'json'}),
    'nsw-spatial-ward-search.json':'https://portal.spatial.nsw.gov.au/portal/sharing/rest/search?'+urlencode({'q':'wards','num':100,'f':'json'}),
    'nsw-boundary-context.html':'https://elections.nsw.gov.au/elections/how-voting-works/electoral-boundaries',
    'nsw-ballina-context.html':'https://elections.nsw.gov.au/elections/find-my-electorate/councils/ballina',
    'nsw-ec-copyright.html':'https://elections.nsw.gov.au/copyright',
    'nsw-ec-electoratemap.js':'https://elections.nsw.gov.au/assets/scripts/electoratemap.js',
    'nsw-ec-ballina.kml':'https://kml.elections.nsw.gov.au/kmlservice.asmx/getKMLRedist?colortweak=1&servertype=prod&location=LG2023/Ballina_boundary.kml',
}

def raw_path(name):return RAW/('council-ward-supp-'+name)

def urls():
    p=raw_path('discovered-urls.json')
    return {**URLS,**(json.loads(p.read_text()) if p.exists() else {})}

def fetch_one(item):
    name,url=item
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (P4A public civic geometry archive)'})
        context=ssl.create_default_context()
        assert context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname
        with urllib.request.urlopen(req,timeout=90,context=context) as response:
            data=response.read()
            if name.endswith(('.json','.geojson')):
                payload=json.loads(data)
                if payload.get('error'):raise ValueError(str(payload['error']))
            raw_path(name).write_bytes(data)
            return {'file':raw_path(name).relative_to(ROOT).as_posix(),'url':url,'checked':CHECKED,'status':response.status,
                    'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'tlsVerification':'certificate and hostname verified'}
    except Exception as exc:
        return {'file':raw_path(name).relative_to(ROOT).as_posix(),'url':url,'checked':CHECKED,'status':'unavailable','error':str(exc)}

def fetch(only=None):
    RAW.mkdir(parents=True,exist_ok=True);SOURCES.mkdir(parents=True,exist_ok=True)
    selected=lambda name:not only or any(x in name for x in only.split(','))
    with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(fetch_one,[(n,u) for n,u in urls().items() if selected(n)]))
    log=SOURCES/'council-ward-supp-transfers.json'
    if log.exists():rows=[r for r in json.loads(log.read_text()) if not selected(Path(r['file']).name.removeprefix('council-ward-supp-'))]+rows
    log.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    for row in rows:
        if selected(Path(row['file']).name.removeprefix('council-ward-supp-')):print(Path(row['file']).name,row['status'],row.get('bytes',''),flush=True)

def discover():
    p=raw_path('discovered-urls.json');more=json.loads(p.read_text()) if p.exists() else {}
    item=raw_path('geoscape-lga-item.json')
    if item.exists():
        payload=json.loads(item.read_text())
        if payload.get('url'):more['geoscape-lga-service.json']=payload['url']+'?f=pjson'
        if payload.get('url'):
            service=raw_path('geoscape-lga-service.json')
            if service.exists():
                lid=json.loads(service.read_text())['layers'][0]['id']
                more['geoscape-lga-layer.json']=payload['url']+'/'+str(lid)+'?f=pjson'
                more['geoscape-lga-attributes.json']=payload['url']+'/'+str(lid)+'/query?'+urlencode({'where':"state IN ('NT','WA')",'outFields':'lga_pid,lga_name,abb_name,state','returnDistinctValues':'true','returnGeometry':'false','f':'json','resultRecordCount':2000})
    for state in ('NT','WA'):
        for suffix,params in (
                ('ids.json',{'where':"state = '"+state+"'",'returnIdsOnly':'true','f':'json'}),
                ('native.geojson',{'where':"state = '"+state+"'",'outFields':'*','returnGeometry':'true','outSR':4283,'f':'geojson','resultRecordCount':2000,'orderByFields':'objectid'})):
            more['geoscape-'+state.lower()+'-'+suffix]=WARD+'/0/query?'+urlencode(params)
    more['nsw-ward-extent-search.json']='https://www.arcgis.com/sharing/rest/search?'+urlencode({'q':'ward AND type:"Feature Service"','bbox':'140,-38,154,-27','num':100,'sortField':'modified','sortOrder':'desc','f':'json'})
    more['nsw-ward-title-search.json']='https://www.arcgis.com/sharing/rest/search?'+urlencode({'q':'title:ward AND type:"Feature Service" AND (NSW OR Australia OR .nsw.gov.au)','num':100,'f':'json'})
    more['nsw-portal-hosted.json']='https://portal.data.nsw.gov.au/arcgis/rest/services/Hosted?f=pjson'
    more['nsw-wpc-wards-metadata.json']='https://data.wpcouncils.nsw.gov.au/api/explore/v2.1/catalog/datasets/wards'
    more['nsw-wpc-wards.geojson']='https://data.wpcouncils.nsw.gov.au/api/explore/v2.1/catalog/datasets/wards/exports/geojson'
    more['nsw-north-sydney-item.json']='https://www.arcgis.com/sharing/rest/content/items/4215aff04de6473d8c6d5916e02c1f3f?f=pjson'
    more['nsw-north-sydney-service.json']='https://services-ap1.arcgis.com/33nKDOPkQG7pavgq/arcgis/rest/services/Ward_Boundaries_Public/FeatureServer?f=pjson'
    portal=raw_path('nsw-spatial-ward-search.json')
    if portal.exists():
        for row in json.loads(portal.read_text()).get('results',[]):
            if 'Historic'in row['title'] or 'Suburb'in row['title']:continue
            more['nsw-portal-item-'+row['id']+'.json']='https://portal.spatial.nsw.gov.au/portal/sharing/rest/content/items/'+row['id']+'?f=pjson'
            more['nsw-portal-service-'+row['id']+'.json']=row['url']+'?f=pjson'
    p.write_text(json.dumps(more,indent=2)+'\n',encoding='utf-8')
    print('Discovered',len(more),'public requests')

def inspect():
    for name in ('geoscape-ward-layer.json','geoscape-lga-item.json','geoscape-ward-item.json','nsw-ward-search.json','nsw-spatial-ward-search.json'):
        p=raw_path(name)
        if not p.exists():continue
        d=json.loads(p.read_text())
        if 'results'in d:
            print(name,'total',d.get('total'))
            for r in d['results']:print(r['id'],r['title'],r.get('owner'),r.get('url'))
        else:print(name,json.dumps({k:d[k] for k in ('url','name','fields','spatialReference','licenseInfo','description','layers','copyrightText') if k in d},ensure_ascii=False)[:18000])

def source(name,title,**extra):
    path=raw_path(name)
    return {'id':'council-ward-supp-'+name.rsplit('.',1)[0],'title':title,'url':urls()[name],
            'checked':CHECKED,'rawFile':path.relative_to(ROOT).as_posix(),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**extra}

def coordinate_pairs(node):
    if isinstance(node,list) and len(node)>=2 and all(isinstance(v,(int,float)) for v in node[:2]):
        yield node[:2]
    elif isinstance(node,list):
        for child in node:yield from coordinate_pairs(child)

def name_key(value):return re.sub('[^a-z0-9]','',value.lower())

def build():
    MAPS.mkdir(parents=True,exist_ok=True)
    item=json.loads(raw_path('geoscape-ward-item.json').read_text())
    assert 'creativecommons.org/licenses/by/4.0' in item['licenseInfo']
    lga_payload=json.loads(raw_path('geoscape-lga-attributes.json').read_text())
    assert not lga_payload.get('exceededTransferLimit')
    lgas={f['attributes']['lga_pid']:f['attributes'] for f in lga_payload['features']}
    base=json.loads((ROOT/'content/places/councils.json').read_text())
    council_keys={}
    for p in base['places']:
        if p['kind']!='council' or p['jurisdiction'] not in ('nt','wa'):continue
        key=(p['jurisdiction'],name_key(p['name']))
        assert key not in council_keys,key
        council_keys[key]=p
    licence='Creative Commons Attribution 4.0 International'
    attribution='Incorporates or developed using Administrative Boundaries © Geoscape Australia licensed by the Commonwealth of Australia under Creative Commons Attribution 4.0 International licence (CC BY 4.0).'
    sources=[source('geoscape-ward-item.json','Digital Atlas of Australia: Wards source licence and live item metadata',licence=licence,licenceUrl='https://creativecommons.org/licenses/by/4.0/'),
             source('geoscape-ward-service.json','Digital Atlas of Australia: Wards service metadata',licence=licence),
             source('geoscape-ward-layer.json','Digital Atlas of Australia: native GDA94 ward layer metadata',licence=licence),
             source('geoscape-lga-item.json','Digital Atlas of Australia: Local Government Areas licence and metadata',licence=licence),
             source('geoscape-lga-attributes.json','Digital Atlas of Australia: distinct official ward-parent LGA identities',licence=licence)]
    layers=[];places=[];audit=[]
    edition='Digital Atlas live item August 2026; service description November 2025; checked 17 October 2026'
    for state in ('NT','WA'):
        j=state.lower();filename='geoscape-'+j+'-native.geojson'
        data=raw_path(filename).read_bytes();geo=json.loads(data)
        ids=json.loads(raw_path('geoscape-'+j+'-ids.json').read_text())['objectIds']
        assert len(ids)==len(set(ids))
        assert set(ids)=={f['properties']['objectid'] for f in geo['features']},(state,'truncated query')
        assert not geo.get('exceededTransferLimit')
        assert len({f['properties']['wd_ply_pid'] for f in geo['features']})==len(geo['features'])
        sid='council-ward-supp-'+filename.rsplit('.',1)[0]
        sources.extend([source(filename,state+' Digital Atlas/Geoscape exact ward polygons',licence=licence,licenceUrl='https://creativecommons.org/licenses/by/4.0/',
                               attribution=attribution,nativeCRS='EPSG:4283',boundaryEdition=edition,
                               currencyCaveat='Live ArcGIS item description says August 2026; service description still says November 2025. Neither date is silently replaced by retrieval date.'),
                        source('geoscape-'+j+'-ids.json',state+' ward full object-ID inventory',licence=licence)])
        dest=MAPS/('council-ward-supp-'+j+'.geojson')
        dest.write_bytes(data)
        compressed=gzip.compress(data,mtime=0);gz=Path(str(dest)+'.gz');gz.write_bytes(compressed)
        assert gzip.decompress(compressed)==data
        lid='council-ward-supp-'+j
        layers.append({'id':lid,'jurisdiction':j,'kind':'ward','name':state+' official ward polygons (Digital Atlas/Geoscape)',
            'geometryFile':gz.relative_to(ROOT).as_posix(),'geometryFallbackFile':dest.relative_to(ROOT).as_posix(),
            'featureIdField':'wd_ply_pid','featureNameField':'ward_name','sourceId':sid,
            'boundaryEdition':edition,'crs':'EPSG:4283','nativeCRS':'EPSG:4283',
            'coordinateNote':'Native GDA94 longitude/latitude coordinates retained exactly, including each source polygon part and ring. Browser display on a WGS84 base has approximate datum alignment; no false coordinate transformation is claimed.',
            'attribution':attribution})
        by_ward={}
        for feature in geo['features']:
            prop=feature['properties'];assert prop['state']==state
            by_ward.setdefault(prop['ward_pid'],[]).append(feature)
        parents=set();references=set()
        for ward_pid,features in sorted(by_ward.items()):
            prop=features[0]['properties']
            assert all(f['properties']['lga_pid']==prop['lga_pid'] and f['properties']['ward_name']==prop['ward_name'] for f in features)
            lga=lgas[prop['lga_pid']];assert lga['state']==state
            parent=council_keys.get((j,name_key(lga['abb_name'])))
            assert parent,(state,lga)
            parents.add(parent['id'])
            refs=[{'layerId':lid,'featureId':f['properties']['wd_ply_pid'],'boundaryEdition':edition} for f in features]
            references.update(r['featureId'] for r in refs)
            record={'id':j+'-ward-'+ward_pid,'name':prop['ward_name'],
                'slug':name_key(parent['name'])+'-'+re.sub('[^a-z0-9]+','-',prop['ward_name'].lower()).strip('-'),
                'jurisdiction':j,'kind':'ward','parentId':parent['id'],'layerId':lid,'featureId':refs[0]['featureId'],
                'officialUrl':parent['officialUrl'],'sources':[sid,'council-ward-supp-geoscape-ward-item','council-ward-supp-geoscape-lga-attributes'],
                'boundaryEdition':edition,'representatives':[],'elections':[],
                'sourceWardId':ward_pid,'sourceLgaId':prop['lga_pid'],'sourceLgaName':lga['lga_name'],
                'coverageNotes':['Actual official published ward polygons, not a generated division of the council. Native GDA94 coordinates, original polygon parts, holes and source IDs retained without simplification or rounding.',
                                 'The live source item says August 2026 while the service description still says November 2025; later ward amendments need separate official reconciliation.',
                                 'Current ward representative profiles and previous ward-contestant histories require separate official reconciliation; the geometry source does not establish current office or candidacy.']}
            if len(refs)>1:record['mapRefs']=refs[1:]
            places.append(record)
        assert references=={f['properties']['wd_ply_pid'] for f in geo['features']}
        pairs=sum(1 for f in geo['features'] for point in coordinate_pairs(f['geometry']['coordinates']))
        audit.append({'jurisdiction':j,'sourcePolygonFeatures':len(geo['features']),'distinctWards':len(by_ward),
                      'parentCouncils':len(parents),'coordinatePairs':pairs,'allSourceObjectIdsPresent':True,
                      'allSourcePartsHavePlaceRefs':True,'nativeCRS':'EPSG:4283',
                      'sourceSha256':hashlib.sha256(data).hexdigest(),'deliverySha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
                      'gzipRoundTripExactBytes':True})
    output={'schemaVersion':1,'checked':CHECKED,'scope':'council-ward-supplement','sources':sources,'layers':layers,'places':places}
    (ROOT/'content/places/council-ward-supplement.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report={'status':'pass','checked':CHECKED,'scope':'Exact service geometry delivery, rights metadata and source-ID/parent joins',
            'checks':audit,'limitations':['No current individual-office or candidate completeness claim. Council agent merges people/events separately.',
                'NSW is not covered by the Geoscape Wards product. Separately discovered NSW sources require currency and licence reconciliation before use.',
                'No source denial or TLS certificate failure was bypassed. All retained transfers used verified TLS certificates and hostnames.']}
    (SOURCES/'council-ward-supp-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--fetch',action='store_true');p.add_argument('--only');p.add_argument('--discover',action='store_true');p.add_argument('--inspect',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
    if a.discover:discover()
    if a.fetch:fetch(a.only)
    if a.inspect:inspect()
    if a.build:build()

if __name__=='__main__':main()
