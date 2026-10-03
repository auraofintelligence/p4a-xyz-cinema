import pathlib,json
from shapely.geometry import shape,Point
R=pathlib.Path(__file__).resolve().parents[2];features=[];fixtures=[]
for layer in ['rap','rsa']:
 d=json.loads((R/f'assets/maps/vic-{layer}.geojson').read_text(encoding='utf-8'))
 for f in d['features']:features.append((f'vic-{layer}-{f["properties"]["OBJECTID"]}',shape(f['geometry'])))
for ident,g in features:
 assert g.is_valid,ident
 p=g.representative_point();fixtures.append({'name':ident,'point':[p.x,p.y],'matches':sorted(i for i,other in features if other.contains(p))})
for ia,a in features:
 for ib,b in features:
  if ia>=ib:continue
  intersection=a.intersection(b)
  if intersection.area>1e-7:
   p=intersection.representative_point();fixtures.append({'name':ia+'/'+ib,'point':[p.x,p.y],'matches':sorted(i for i,other in features if other.contains(p))})
fixtures.append({'name':'outside','point':[140,-40],'matches':[]})
pathlib.Path(__file__).resolve().parent.joinpath('first-peoples-fixtures.json').write_text(json.dumps(fixtures,indent=2));print('Valid statutory geometries:',len(features),'independent fixtures:',len(fixtures),'overlap fixtures:',sum('/' in f['name'] for f in fixtures))
