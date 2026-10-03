"""Read-only integrity checks. Run with Python; no packages or network required."""
import pathlib,json,re,hashlib,collections,subprocess
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_source(path,tag):
 return json.loads(re.search(r'```json '+tag+r'\s*(.*?)```',(ROOT/path).read_text(encoding='utf-8'),re.S).group(1))
def main():
 data=load_source('content/electorates/vic.md','electorate-data');state=load_source('content/states/vic.md','state-data')
 manifest=json.loads((ROOT/'assets/maps/vic-provenance.json').read_text())
 for layer,count,members in [('assembly',88,87),('council',8,40)]:
  raw=(ROOT/f'assets/maps/vic-{layer}.geojson').read_bytes();geometry=json.loads(raw)
  assert hashlib.sha256(raw).hexdigest()==manifest['datasets'][layer]['sha256']
  assert len(geometry['features'])==len(data[layer])==count
  assert sum(len(r['members']) for r in data[layer])==members
  ids={f"vic-{layer}-{f['properties'].get('district_code',f['properties']['region_code'])}" for f in geometry['features']}
  assert ids=={r['id'] for r in data[layer]}
 assert [r['name'] for r in data['assembly'] if r['vacancy']]==['Brunswick']
 assert all(len(r['districts'])==11 for r in data['council'])
 assert state['government']['leader']=='Ben Carroll' and state['researchTimezone']=='Australia/Melbourne'
 assert sum(r['seats'] for r in state['chambers'][0]['composition'])==88
 assert sum(r['seats'] for r in state['chambers'][1]['composition'])==40
 browser_data=json.loads((ROOT/'assets/state-data.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
 for record in browser_data:
  authored=load_source(f"content/states/{record['slug']}.md",'state-data')
  assert {k:v for k,v in record.items() if k!='sourceMarkdown'}==authored,record['slug']
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.paths=[]
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ['href','src'] and v:self.paths.append(v)
 files=['states/vic/index.html','states/vic/architecture/index.html','states/vic/constitution/index.html','states/vic/map/index.html','pages/states.html','pages/site-map.html']
 for name in files:
  page=ROOT/name;s=page.read_text(encoding='utf-8');assert s.count('assets/site-nav.js')==1,name
  assert 'data-menu-toggle' in s and 'data-nav-toggle' not in s,name
  assert '&#226;' not in s and 'â€' not in s,name
  links=Links();links.feed(s)
  for href in links.paths:
   u=urlsplit(href)
   if u.scheme or u.netloc or not u.path:continue
   assert (page.parent/unquote(u.path)).resolve().exists(),(name,href)
  if name in ['states/vic/index.html','pages/states.html']:
   for date in re.findall(r'data-(?:election-date|countdown)="([^"]+)"',s):assert re.match(r'\d{4}-\d\d-\d\dT',date),date
  if name=='states/vic/architecture/index.html':assert 'Local councils first' in s and 'data-map-layer-choice="councils"' in s
 map_html=(ROOT/'states/vic/map/index.html').read_text(encoding='utf-8')
 assert map_html.count('class="vic-record"')==96
 assert '2021 Census' in map_html and '2022 boundaries' in map_html and '2026 candidate list' in map_html
 geometry_js=ROOT/'assets/vic-map-geometry.js'
 js='''const assert=require('assert');const g=require(process.argv[1]);
 assert.equal(g.daysUntil('2026-11-28T08:00:00+11:00','2026-10-02T00:01:00+10:00'),57);
 assert.equal(g.daysUntil('2026-11-28T08:00:00+11:00','2026-10-02T23:59:00+10:00'),57);
 assert.equal(g.daysUntil('2026-11-28T08:00:00+11:00','2026-10-04T03:01:00+11:00'),55);
 assert.equal(g.daysUntil('2026-11-28T08:00:00+11:00','2026-11-28T00:01:00+11:00'),0);
 const p={type:'Polygon',coordinates:[[[0,0],[4,0],[4,4],[0,4],[0,0]],[[1,1],[3,1],[3,3],[1,3],[1,1]]]};
 assert(g.contains([.5,.5],p));assert(!g.contains([2,2],p));assert(!g.contains([5,5],p));
 const m={type:'MultiPolygon',coordinates:[p.coordinates,[[[8,8],[9,8],[9,9],[8,9],[8,8]]]]};assert(g.contains([8.5,8.5],m));
 console.log('Calendar/DST, holes and multipart checks passed.');'''
 subprocess.run(['node','-e',js,str(geometry_js)],check=True)
 print('PASS: 96 geometry joins, 127 members + one vacancy, source hashes, all state source/generated parity, current navigation, local links, ISO dates, 96 no-JS records.')
if __name__=='__main__':main()
