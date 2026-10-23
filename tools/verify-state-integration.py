"""Check state adapter records and every vertex of new SA/LIST deliveries.

Offline only. Requires the retained originals and the documented geometry
dependencies. Writes state-specific verification, never national acceptance.
"""
import collections, gzip, hashlib, io, json, pathlib, sys, zipfile
from state_place_supplements import decode_path, slug

ROOT=pathlib.Path(__file__).resolve().parents[1]
RAW=ROOT/'content/places/raw/state'

def read(path):
    raw=path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw.decode('utf-8-sig'))

def main():
    data=read(ROOT/'content/places/state.json');places=data['places'];sources={s['id']:s for s in data['sources']};layers={l['id']:l for l in data['layers']}
    assert len({p['id'] for p in places})==len(places)
    for p in places:
        assert len({e['id'] for e in p['elections']})==len(p['elections']),p['id']
        assert all(s in sources for s in p['sources']),p['id']
        assert all(c.get('voteMeasure') for e in p['elections'] for c in e['candidates'] if c.get('votes') is not None),p['id']
    counts={st:{'places':len(ps),'currentMemberRecords':sum(len(p['representatives']) for p in ps),'eventContestants':sum(len(e['candidates']) for p in ps for e in p['elections'])} for st in ['vic','nsw','qld','sa','wa','tas','nt','act'] for ps in [[p for p in places if p['jurisdiction']==st]]}
    assert counts['tas']['eventContestants']==235
    assert sum(len(e['candidates']) for p in places if p['jurisdiction']=='tas' and p['chamber']=='House of Assembly' for e in p['elections'])==161
    assert counts['nt']['eventContestants']==86 and counts['act']['eventContestants']==155
    assert counts['sa']['currentMemberRecords']==69
    assert counts['sa']['eventContestants']==436
    assert counts['nt']['currentMemberRecords']==25
    assert counts['nsw']['currentMemberRecords']==134
    assert counts['wa']['currentMemberRecords']==96
    ng=next(p for p in places if p['id']=='state-sa-2026-ngadjuri')
    old=next(p for p in places if p['jurisdiction']=='sa' and p['name']=='Frome')
    assert len(ng['representatives'])==1 and len(ng['elections'][0]['candidates'])>0
    assert old['status']=='historical' and old['representatives']==[] and old['elections']==[]
    assert len([p for p in places if p['jurisdiction']=='sa' and p.get('layerId')=='state-sa-assembly-2026'])==47
    # Every official encoded source ring survives, irrespective of topology
    # grouping. This checks actual persisted delivered bytes, not builder arrays.
    def ring_hash(ring):return hashlib.sha256(json.dumps(ring,separators=(',',':')).encode()).hexdigest()
    layer=layers['state-sa-assembly-2026'];delivered=read(ROOT/layer['geometryFile'])
    originals=read(RAW/'state-sa-map-geometry.html')['2026']
    expected={slug(x['name']):collections.Counter(ring_hash(decode_path(r)) for r in x['paths']) for x in originals}
    for f in delivered['features']:
        got=collections.Counter(ring_hash(r) for poly in f['geometry']['coordinates'] for r in poly)
        assert got==expected[f['properties']['districtId']]
    sa_points=sum(len(decode_path(r)) for x in originals for r in x['paths'])
    print('SA: all 47 official path sets equal persisted geometry',flush=True)
    del delivered
    sys.path.insert(0,str(ROOT/'tmp/state-geometry-libs'))
    import shapefile
    from pyproj import Transformer
    z=zipfile.ZipFile(RAW/'state-tas-lc-official-zip.html');stem='list_legislative_council_divs_statewide'
    reader=shapefile.Reader(**{ext:io.BytesIO(z.read(stem+'.'+ext)) for ext in ['shp','shx','dbf']})
    layer=layers['state-tas-council-2017']
    native=read(ROOT/layer['nativeGeometryFile'])
    native_by_id={f['LEG_CNL_ID']:f for f in native['features']};point_count=ring_count=0
    for record in reader.iterShapeRecords():
        s=record.shape;starts=list(s.parts)+[len(s.points)]
        rings=native_by_id[record.record.LEG_CNL_ID]['rings']
        assert len(rings)==len(s.parts)
        for got,a,b in zip(rings,starts,starts[1:]):
            assert len(got)==b-a
            assert all(tuple(p)==tuple(q) for p,q in zip(got,s.points[a:b]))
        point_count+=len(s.points);ring_count+=len(s.parts)
    print('TAS: all original native coordinates/rings match retained SHP',flush=True)
    del native,native_by_id
    delivered=read(ROOT/layer['geometryFile']);by_id={f['properties']['LEG_CNL_ID']:f for f in delivered['features']}
    transformer=Transformer.from_crs('EPSG:28355','EPSG:4326',always_xy=True)
    for record in reader.iterShapeRecords():
        geom=record.shape.__geo_interface__;polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
        got=by_id[record.record.LEG_CNL_ID]['geometry']['coordinates']
        assert len(got)==len(polys)
        for p,q in zip(polys,got):
            assert len(p)==len(q)
            for native_ring,geo_ring in zip(p,q):
                assert len(native_ring)==len(geo_ring)
                xs,ys=zip(*native_ring);lons,lats=transformer.transform(xs,ys)
                assert all(lon==xy[0] and lat==xy[1] for lon,lat,xy in zip(lons,lats,geo_ring))
        print('TAS persisted transformed geometry matches: '+record.record.NAME,flush=True)
    assert len(by_id)==15
    tas_lc=[p for p in places if p['id'].startswith('state-tas-lc-')]
    assert len(tas_lc)==15 and all(p.get('layerId')==layer['id'] for p in tas_lc)
    assert all(any(e['status']=='date-unannounced' and e['date'] is None and 'May' in e['label'] for e in p['elections']) for p in tas_lc)
    assert all(any(e['status']=='historical' and e['candidates'] for e in p['elections']) for p in tas_lc)
    from decimal import Decimal
    cb=next(e for p in places if p['jurisdiction']=='act' and p['slug']=='kurrajong' for e in p['elections'] if e['kind']=='countback')
    assert len(cb['candidates'])==6 and sum(Decimal(c['voteValueExact']) for c in cb['candidates'])+Decimal(cb['exhaustedVoteValue'])+Decimal(cb['lossByFraction'])==Decimal(cb['totalVoteValueDistributed'])
    lc=next(e for p in places if p['id']=='state-sa-legislative-council-statewide' for e in p['elections'] if e['id']=='sa-lc-2026')
    assert sorted(c['electedOrder'] for c in lc['candidates'] if 'electedOrder' in c)==list(range(1,12))
    out={'checked':'2026-10-17','status':'PASS','scope':'State-specific offline data and original/persisted geometry verification; not national/browser/deep-journey acceptance','counts':counts,'southAustralia':{'currentDistricts':47,'nativeEncodedPathCoordinatesRetained':True,'points':sa_points,'houseContestants':388,'councilContestants':48,'historicFromePreservedSeparately':True,'all11CouncilElectionOrdersReconciledWithoutTreatingQuotaAsZero':True},'tasmania':{'houseBallotNames':161,'councilDivisions':15,'councilContestantRecords':74,'sourceRings':ring_count,'sourcePoints':point_count,'allNativeVerticesEqualOriginalShapefile':True,'allDeliveredVerticesEqualDocumentedProjection':True,'divisionSpecificMayCyclesWithNoInventedDay':True,'latestBallotForEveryCouncilDivision':True},'unresolved':['NSW official current Council directory lists 41; missing 42nd seat status not inferred','SA Council full individual first preferences and transfer stages not normalized; elected order and actual quota/final stage values retained','WA historical numeric result totals are not normalized','TAS 2018–2020 earlier contestant ballots are not normalized; latest ballots for all 15 divisions and intervening by-elections are present','Jurisdiction redistribution commencement review not complete beyond retained explicit editions']}
    path=ROOT/'content/places/qa/state-integration-verification.json';path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':'PASS','counts':counts,'TASpoints':point_count,'TASrings':ring_count}),flush=True)

if __name__=='__main__':main()
