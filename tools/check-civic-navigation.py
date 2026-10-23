"""Check the national -> electorate -> council visitor route in all jurisdictions."""
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
import importlib.util
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
STATES=('act','nsw','nt','qld','sa','tas','vic','wa')

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.text=(ROOT/path).read_text(encoding='utf8');self.links=[];self.config=None;self.capture=False
        self.feed(self.text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a':self.links.append(a)
        if tag=='script' and a.get('id')=='civic-map-config':self.capture=True
    def handle_data(self,data):
        if self.capture:self.config=json.loads(data)
    def handle_endtag(self,tag):
        if tag=='script':self.capture=False
    def resolve(self,link):
        return posixpath.normpath(posixpath.join(posixpath.dirname(self.path),urlsplit(link['href']).path))

national=Page('pages/states.html')
labels=[a for a in national.links if 'state-raster-label' in a.get('class','').split()]
assert {a['data-map-state'] for a in labels}==set(STATES)
other_national=Page('pages/maps.html')
other_labels=[a for a in other_national.links if 'state-raster-label' in a.get('class','').split()]
assert {a['data-map-state'] for a in other_labels}==set(STATES)
for state in STATES:
    target=f'states/{state}/places/state/index.html'
    assert national.resolve(next(a for a in labels if a['data-map-state']==state))==target,state
    assert other_national.resolve(next(a for a in other_labels if a['data-map-state']==state))==target,state
    portal=Page(f'states/{state}/index.html')
    assert 'clone' not in portal.text.lower() and 'Tailoring notes' not in portal.text,state
    assert portal.text.index('national-place-links:start')<portal.text.index('state-summary-grid'),state
    assert any(portal.resolve(a)==target for a in portal.links),state
    for scope in ('state','councils','federal'):
        page=Page(f'states/{state}/places/{scope}/index.html')
        assert page.config and page.text.count('data-civic-map ')==1,page.path
        for next_scope in ('state','councils','federal'):
            expected=f'states/{state}/places/{next_scope}/index.html'
            assert any(page.resolve(a)==expected for a in page.links),(page.path,expected)
        assert any(page.resolve(a)=='pages/states.html' for a in page.links),page.path
        assert any(page.resolve(a)==f'states/{state}/index.html' for a in page.links),page.path
        if scope=='state':
            first=page.config['initialLayer']
            layer=next(l for l in page.config['layers'] if l['id']==first)
            assert layer['scope']=='state',(state,first)
    if state=='act':
        assert 'no separate elected councils' in portal.text
        local=Page('states/act/places/councils/index.html')
        assert 'not an invented elected council' in local.text
assert 'clone' not in national.text.lower()
assert 'Agent-ready data' not in national.text
spec=importlib.util.spec_from_file_location('national_builder',ROOT/'tools/build-national-places.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
places,_,_,_=builder.load()
local=[p for p in places if p['scope']=='councils']
def directory_targets(page):
    section=re.search(r'<section[^>]*id="directory"[^>]*>(.*?)</section>',page.text,re.S)
    assert section,page.path
    return [page.resolve({'href':href}) for href in re.findall(r'href="([^"]+)"',section.group(1))]
summary={}
for state in STATES:
    subset=[p for p in local if p['jurisdiction']==state]
    roots=[p for p in subset if not p.get('parentId')]
    page=Page(f'states/{state}/places/councils/index.html')
    targets=directory_targets(page)
    assert len(targets)==len(roots) and set(targets)=={p['url'] for p in roots},state
    assert all((ROOT/path).is_file() for path in targets),state
    # Layer switching still reaches the complete sourced records, while the
    # ordinary linked directory starts at councils and exceptional local areas.
    assert {p['id'] for p in page.config['places']}=={p['id'] for p in subset},state
    for parent in roots:
        children=[p for p in subset if p.get('parentId')==parent['id']]
        if children:
            child_targets=directory_targets(Page(parent['url']))
            assert set(child_targets)=={p['url'] for p in children},parent['id']
            for child in children:
                child_page=Page(child['url'])
                assert any(child_page.resolve(a)==parent['url'] for a in child_page.links),child['id']
    landing=Page(f'states/{state}/places/index.html')
    assert len(directory_targets(landing))==3,state
    summary[state]={'topLevel':len(roots),'childrenOnExistingParentPages':len(subset)-len(roots)}
print('PASS: 8 national targets, 8 early state entries, reciprocal maps and layered existing council/child routes: '+json.dumps(summary))
