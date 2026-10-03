import pathlib,json,hashlib,collections
from shapely.geometry import shape,Point,Polygon
from shapely.ops import unary_union
import sys
R=pathlib.Path(__file__).resolve().parents[2];out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'assets/maps/vic-provenance.json').read_text());fixtures=[];summary={}
for layer,expected in [('assembly',88),('council',8)]:
 raw=(R/f'assets/maps/vic-{layer}.geojson').read_bytes();assert hashlib.sha256(raw).hexdigest()==manifest['datasets'][layer]['sha256']
 features=json.loads(raw)['features'];assert len(features)==expected
 geoms=[shape(f['geometry']) for f in features]
 ids=[f"vic-{layer}-{f['properties'].get('district_code',f['properties']['region_code'])}" for f in features]
 assert len(set(ids))==expected and all(g.is_valid for g in geoms)
 vertices=0;islands=0;holes=0
 def expected_at(point):
  matches=[ids[i] for i,g in enumerate(geoms) if g.contains(point)]
  assert len(matches)<=1,(point,matches)
  return matches[0] if matches else None
 def add(point,label):fixtures.append({'layer':layer,'point':[point.x,point.y],'expected':expected_at(point),'case':label})
 for i,g in enumerate(geoms):
  add(g.representative_point(),ids[i]+' interior')
  polys=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
  for poly in polys:
   vertices+=len(poly.exterior.coords)+sum(len(h.coords) for h in poly.interiors)
   holes+=len(poly.interiors)
  # Test a separated component, including small islands, for every multipart feature.
  if len(polys)>1:
   islands+=len(polys)-1;add(min(polys,key=lambda p:p.area).representative_point(),ids[i]+' smallest component')
  for poly in polys:
   for hole in poly.interiors:
    add(Polygon(hole).representative_point(),ids[i]+' hole');break
   if poly.interiors:break
 # Boundary-adjacent samples on each side of actual shared segments.
 shared=0
 for i,g in enumerate(geoms):
  for j in range(i+1,len(geoms)):
   h=geoms[j]
   if not g.envelope.intersects(h.envelope):continue
   intersection=g.boundary.intersection(h.boundary)
   if intersection.is_empty or intersection.length<1e-6:continue
   shared+=1
   if shared>32:continue
   components=list(intersection.geoms) if hasattr(intersection,'geoms') else [intersection]
   lines=[x for x in components if x.geom_type=='LineString' and x.length>1e-6]
   if not lines:continue
   line=max(lines,key=lambda x:x.length);a=line.interpolate(.49,normalized=True);b=line.interpolate(.51,normalized=True);mid=line.interpolate(.5,normalized=True)
   dx=b.x-a.x;dy=b.y-a.y;length=(dx*dx+dy*dy)**.5
   if length:
    for sign in [-1,1]:add(Point(mid.x-sign*dy/length*1e-5,mid.y+sign*dx/length*1e-5),f'{ids[i]} / {ids[j]} shared edge {sign}')
 add(Point(144.9,-38.2),'Port Phillip water/hole');add(Point(143,-40),'outside Victoria')
 summary[layer]={'features':len(features),'vertices':vertices,'additionalComponents':islands,'holes':holes,'adjacentPairs':shared,'allValid':True,'sourceHashMatches':True}
 if layer=='assembly':assembly=features;assembly_geoms=geoms
 else:
  differences=[]
  for f,g in zip(features,geoms):
   district_union=unary_union([ag for af,ag in zip(assembly,assembly_geoms) if af['properties']['region_code']==f['properties']['region_code']])
   differences.append({'region':f['properties']['region'],'symmetricDifferenceDegreesSquared':g.symmetric_difference(district_union).area})
  summary['districtRegionAlignment']=differences
(out/'vic-picking-fixtures.json').write_text(json.dumps(fixtures,indent=2),encoding='utf-8')
(out/'geography-report.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2));print('Independent picking fixtures:',len(fixtures))
