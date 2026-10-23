"""Scoped structural/source checks for the static Redland journey, no network."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from datetime import date
import json
import hashlib
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.ids=set();self.links=[];self.images=[];self.svg=False;self.disabled_note=False;self.clocks=[];self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:errors.append(f'Duplicate id {a["id"]}: {self.path}')
            self.ids.add(a['id'])
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
        if tag=='img':self.images.append(a)
        if tag=='svg':self.svg=True
        if tag=='fieldset' and 'data-note-fields' in a and 'disabled' in a:self.disabled_note=True
        if 'data-election-countdown' in a:self.clocks.append(a['data-election-countdown'])

# The national expansion adds other council/election routes to this tree.
# Keep this regression check bound to its actual reviewed reference contract;
# tools/verify-national-places.py verifies the new national routes separately.
reference_contract=json.loads((ROOT/'content/local/council-pattern-contract.json').read_text(encoding='utf-8'))
reference_paths=[ROOT/row['path'] for row in reference_contract['routes'] if row['path'].startswith('states/qld/councils/')]
assert reference_paths and len(reference_paths)==len(set(reference_paths)),'Invalid Redland reference route scope'
pages={p:Page(p) for p in reference_paths}
refs=0
for path,page in list(pages.items()):
    assert not page.svg,f'InlineSVG innewpage{path}'
    for img in page.images:
        assert img.get('alt') and img.get('width') and img.get('height'),f'Image metadata missing:{path}'
        assert not urlsplit(img['src']).path.endswith('.svg'),f'SVGmap:{path}'
    for target in page.links:
        u=urlsplit(target)
        if u.scheme or u.netloc:continue
        dest=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path)) if u.path else path
        dest=dest.resolve()
        refs+=1
        if dest.is_dir():dest=dest/'index.html'
        if not dest.exists():errors.append(f'Missing local target:{path.relative_to(ROOT)} -> {target}');continue
        if u.fragment and dest.suffix=='.html':
            if dest not in pages:pages[dest]=Page(dest)
            if unquote(u.fragment) not in pages[dest].ids:errors.append(f'Missing anchor:{path.relative_to(ROOT)} -> {target}')

data=json.loads((ROOT/'content/councils/redland.json').read_text(encoding='utf-8'))
records=json.loads((ROOT/'content/local/redland-connections.json').read_text(encoding='utf-8'))['records']
ids={r['id']:r for r in records}
assert len(ids)==len(records) and records,'Connection IDs must be unique and present'
# A named lyric reference must open that song, not merely the archive front door.
song_sources=json.loads((ROOT/'content/local/redland-song-links.json').read_text(encoding='utf-8'))
date.fromisoformat(song_sources['reviewed'])
assert song_sources['reviewWhen'] and song_sources['verification']
song_aliases={}
song_urls=set()
for song in song_sources['songs']:
    destination=urlsplit(song['url'])
    assert destination.scheme=='https' and destination.netloc=='auraofintelligence.github.io'
    assert re.fullmatch(r'/i-C-infinity-music-universe/songs/[^/]+/',destination.path),f'Not a direct lyric page: {song["url"]}'
    assert not destination.query and not destination.fragment
    assert song['url'] not in song_urls,f'Duplicate lyric destination: {song["title"]}'
    song_urls.add(song['url'])
    assert song['title'] and song['aliases']
    for alias in song['aliases']:
        assert alias.casefold() not in song_aliases,f'Duplicate song alias: {alias}'
        song_aliases[alias.casefold()]=song['url']
song_names=re.compile(r'(?<!\w)(?:'+'|'.join(re.escape(a) for a in sorted(song_aliases,key=len,reverse=True))+r')(?!\w)',re.IGNORECASE)
class SongReferences(HTMLParser):
    def __init__(self,text):
        super().__init__();self.anchor=None;self.references=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.anchor=dict(attrs).get('href')
    def handle_endtag(self,tag):
        if tag=='a':self.anchor=None
    def handle_data(self,text):
        for match in song_names.finditer(text):
            self.references.append((match.group(),self.anchor))
song_reference_count=0
for route in ['possibilities','explore','candidates','outcomes']:
    song_page=ROOT/f'states/qld/councils/redland/{route}/index.html'
    references=SongReferences(song_page.read_text(encoding='utf-8')).references
    assert references,f'No named lyric links in {route}'
    for title,destination in references:
        assert destination==song_aliases[title.casefold()],f'Unlinked or misdirected song in {route}: {title}'
    if route in ['possibilities','explore']:
        assert {destination for _,destination in references}==song_urls,f'Missing a reviewed song in {route}'
    song_reference_count+=len(references)

twinkles=sum(r['type']=='twinkle' for r in records)
assert twinkles>0
for record in records:
    assert set(record['trinity'])=={'cost','free','change'}
    for related in record['related']:assert related in ids,f'Missingrelated:{related}'
sources={s['id'] for s in data['sources']}
for indicator in data['indicators']:
    assert indicator['period'] and indicator['geography'] and indicator['sourceId'] in sources
for m in data['maps']:
    assert m['attribution'] and m['rights'] and m['edition'] and m['sourceUrl']
    assert (ROOT/m['image']).exists() and not m['image'].endswith('.svg')
assert data['maps'][0]['id']=='redland-divisions'
elections=json.loads((ROOT/'content/local/redland-election.json').read_text())
assert date.fromisoformat(elections['general']['date']).weekday()==5
if elections['earlyVoting']['opens'] is None:
    assert elections['earlyVoting']['closes'] is None
else:
    from datetime import datetime
    assert datetime.fromisoformat(elections['earlyVoting']['opens'])<datetime.fromisoformat(elections['earlyVoting']['closes'])
    assert elections['earlyVoting']['source'] and elections['earlyVoting']['locations']
if elections['byElection']['date']:
    date.fromisoformat(elections['byElection']['date'])
    assert elections['byElection']['source']
action=pages[ROOT/'states/qld/councils/redland/action/index.html']
assert action.disabled_note,'PrivateformmustbedisableduntilJavaScripthandlerisinstalled'
for p in ['pages/states.html','pages/maps.html']:
    text=(ROOT/p).read_text(encoding='utf-8')
    assert '<svg class="australia-state-map"' not in text
    assert 'assets/maps/australian-states-wikipedia.png' in text
for p in ['states/qld/index.html','states/qld/architecture/index.html','pages/maps.html','pages/site-map.html']:
    assert 'redland-local-route:start' in (ROOT/p).read_text(encoding='utf-8')
assert not errors,'\n'.join(errors)
qld=json.loads((ROOT/'assets/maps/qld-councils.geojson').read_text(encoding='utf-8'))
qld_source=json.loads((ROOT/'content/councils/qld-map-sources.json').read_text(encoding='utf-8'))
assert hashlib.sha256((ROOT/'assets/maps/qld-councils.geojson').read_bytes()).hexdigest()==qld_source['geometry']['sha256']
delivery=(ROOT/'assets/maps/qld-councils-data.js').read_text(encoding='utf-8').split('window.P4A_QLD_COUNCILS=',1)[1].removesuffix(';\n')
delivered=json.loads(delivery)
assert [f['geometry'] for f in delivered['features']]==[f['geometry'] for f in qld['features']],'Delivered coordinates must remain unchanged'
basemap=json.loads((ROOT/'content/councils/qld-basemap-sources.json').read_text(encoding='utf-8-sig'))
assert basemap['extent']['spatialReference']['wkid']==3857
assert hashlib.sha256((ROOT/basemap['image']).read_bytes()).hexdigest()==basemap['sha256']
assert (ROOT/basemap['image']).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
assert delivered['basemap']['extent']==basemap['extent']
assert delivered['basemap']['roads']==basemap['roads']
page_register=json.loads((ROOT/'content/history/civic-page-review-register-2026-10-17.json').read_text(encoding='utf-8'))
reference_routes={p.relative_to(ROOT).as_posix() for p in reference_paths}
registered_pages=[entry for group in page_register['pageGroups'] for entry in group['pages'] if entry['path'] in reference_routes]
assert {entry['path'] for entry in registered_pages}==reference_routes,'Every reviewed reference route needs its own dated register entry'
for entry in registered_pages:
    assert entry['lastUpdated'] and entry['reviewWhen'] and entry['label']
    assert entry['lastUpdated'] in (ROOT/entry['path']).read_text(encoding='utf-8')
assert 'Started 16 October' not in (ROOT/'states/qld/councils/redland/divisions/index.html').read_text(encoding='utf-8')
assert 'id="review-register"' in (ROOT/'states/qld/councils/redland/sources/index.html').read_text(encoding='utf-8')
division_source=json.loads((ROOT/'content/councils/redland-divisions-sources.json').read_text(encoding='utf-8-sig'))
division_raw_path=ROOT/division_source['geometry']['file']
division_raw=json.loads(division_raw_path.read_text(encoding='utf-8-sig'))
assert hashlib.sha256(division_raw_path.read_bytes()).hexdigest()==division_source['geometry']['sha256']
division_delivered=json.loads((ROOT/'assets/maps/redland-divisions-data.js').read_text(encoding='utf-8').split('window.P4A_REDLAND_DIVISIONS=',1)[1].removesuffix(';\n'))
assert [f['geometry'] for f in division_delivered['features']]==[f['geometry'] for f in division_raw['features']]
assert {int(f['properties']['lga_code']) for f in division_delivered['features']}==set(range(1,11))
overview=pages[ROOT/'states/qld/councils/redland/index.html']
overview_html=(ROOT/'states/qld/councils/redland/index.html').read_text(encoding='utf-8')
assert overview_html.count('<canvas')==1 and len(overview.images)==0,'Overview must have one interactive map, no duplicate static maps'
for record in records:
    if record['type']=='twinkle':
        assert record['summary'] and record['title'] and record.get('context') and record.get('seedStatus')
        assert len(record['summary'].split())<=30,'Twinkle spoken seed must fit one breath'
assert (ROOT/'states/qld/councils/redland/explore/index.html').read_text(encoding='utf-8').count('class="record-twinkle"')==twinkles
assert len(qld['features'])==78
assert len({str(f['properties']['lga_code']) for f in qld['features']})==78
assert sum(f['properties']['lga']=='Weipa Town' for f in qld['features'])==1
for route in ['states/qld/index.html','states/qld/councils/index.html']:
    text=(ROOT/route).read_text(encoding='utf-8')
    assert 'data-qld-council-map' in text and '<canvas' in text and 'data-council-search' in text, f'Missing interactive map in{route}'
    assert text.count('id="qld-council-map"')==1
    assert text.count('qld-council-map.js')==1
    assert text.count('qld-councils-data.js')==1
    for f in qld['features']:assert f['properties']['lga'] in text
print(json.dumps({'result':'PASS','generatedPages':19,'localReferencesChecked':refs,'records':len(records),'localTwinkles':twinkles,'mapRecords':len(data['maps']),'indicators':len(data['indicators']),'reviewedSongDestinations':len(song_urls),'directSongReferencesChecked':song_reference_count,'sourcePeriodsPreserved':True,'privateFormNoScriptGuard':True,'interactiveSourceAreas':78,'interactiveDivisions':10,'deliveryGeometryUnchanged':True,'oneOverviewMap':True,'visibleSpokenTwinkleSeeds':twinkles,'geographicBaseMap':'Quiet official pastel PNG, optional detailed roads, retained extent and hashes, EPSG:3857','newMapFormat':'Canvas geometry + original raster maps; no SVG'},indent=2))
