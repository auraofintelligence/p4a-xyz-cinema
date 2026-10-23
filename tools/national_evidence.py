"""Deterministic national evidence snapshots, with local research kept optional.

collect_fingerprints(root) returns sorted path/SHA256/byte rows. Missing sources
under the retention register's local-only prefixes have missing=True; a known
publisher/source hash is retained but never represented as a fresh byte check.
verify_fingerprints(root, rows) returns errors, checked and absentLocalOnly.
require_current_evidence also checks snapshot completeness and browser fixtures.
Reports are deliberately not included in their own snapshots. This module never
writes files, invokes a browser, fetches sources or changes the Git index.
"""
from __future__ import annotations
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit

JURISDICTIONS=('act','nsw','nt','qld','sa','tas','vic','wa')
SCOPES=('councils','state','federal')
BASE_FILES=(
    '.gitattributes',
    'content/places/councils.json','content/places/state.json','content/places/federal.json',
    'content/places/route-registry.json','content/places/geometry-delivery.json',
    'content/places/source-retention.json','content/places/sources/national-basemap.json',
    'assets/civic-places.js','assets/civic-places.css','tools/build-national-places.py',
    'tools/verify-national-places.py','tools/national_evidence.py',
    'tools/build-national-contracts.py','tools/verify-place-contracts.py',
)
BROWSER_CODE_FILES=('assets/civic-places.js','assets/civic-places.css','tools/build-national-places.py')

def _read(root,path):
    return json.loads((root/path).read_text(encoding='utf-8-sig'))

def _name(value):
    value=str(value).replace('\\','/')
    if value.startswith('/') or re.match(r'^[A-Za-z]:',value):raise ValueError('Evidence path must be repository-relative: '+value)
    value=posixpath.normpath(value)
    if value in ('','.','..') or value.startswith('../'):raise ValueError('Evidence path escapes repository: '+value)
    return value

def _path(root,name):
    name=_name(name);path=root/name
    if not path.resolve().is_relative_to(root.resolve()):raise ValueError('Evidence path resolves outside repository: '+name)
    return path

def _digest(path):
    digest=hashlib.sha256();size=0
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(4*1024*1024),b''):digest.update(chunk);size+=len(chunk)
    return digest.hexdigest(),size

def _retention(root):
    data=_read(root,'content/places/source-retention.json')
    prefixes=tuple(_name(p).rstrip('/')+'/' for p in data.get('localOnlyPathPrefixes',[]))
    return prefixes,{_name(p) for p in data.get('localOnlyFiles',[])}

def _local(reference,page):
    parsed=urlsplit(reference)
    if parsed.scheme not in ('','http','https') or (parsed.netloc and parsed.netloc.lower() not in ('p4a.xyz','www.p4a.xyz')):return None
    value=unquote(parsed.path).replace('\\','/')
    if not value:return None
    return _name(value.lstrip('/') if value.startswith('/') else posixpath.join(posixpath.dirname(page),value))

class _Assets(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.urls=[];self.configs=[];self._config=None
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','img','source','video','audio','iframe'):
            self.urls.extend(a[k] for k in ('src','poster') if a.get(k))
        if tag=='link' and a.get('href') and any(x in (a.get('rel') or '').split() for x in ('stylesheet','icon','preload','modulepreload')):self.urls.append(a['href'])
        if tag=='script' and a.get('id')=='civic-map-config':self._config=[]
    def handle_data(self,text):
        if self._config is not None:self._config.append(text)
    def handle_endtag(self,tag):
        if tag=='script' and self._config is not None:self.configs.append(json.loads(''.join(self._config)));self._config=None

def collect_fingerprints(root):
    root=Path(root);prefixes,excluded=_retention(root)
    required=set();optional={};visited=set();pending=[]
    def public(value):
        if not value:return
        name=_name(value)
        if name in excluded or name.startswith(prefixes):raise ValueError('Required public artifact is marked local-only: '+name)
        if name not in required:required.add(name);pending.append(name)
    def geometry(layer):
        for key in ('geometryFile','compressedFile','nativeGeometryFile'):public(layer.get(key))
    for name in BASE_FILES:public(name)
    for scope in SCOPES:
        data=_read(root,'content/places/'+scope+'.json')
        for layer in data.get('layers',[]):geometry(layer)
        for src in data.get('sources',[]):
            name=src.get('rawFile')
            if not name:continue
            name=_name(name)
            if name.startswith(prefixes):
                prior=optional.get(name);digest=src.get('sha256')
                if prior and digest and prior!=digest:raise ValueError('Conflicting source hashes for '+name)
                optional[name]=digest or prior
            elif name not in excluded:public(name)
    registry=_read(root,'content/places/route-registry.json')
    for row in registry['places']:public(row['url'])
    for layer in registry.get('layers',[]):geometry(layer)
    for layer in _read(root,'content/places/geometry-delivery.json').get('layers',[]):
        public(layer.get('source'));public(layer.get('compressed'))
    public('pages/places.html')
    for state in JURISDICTIONS:
        public('states/'+state+'/places/index.html')
        for scope in SCOPES:public('states/'+state+'/places/'+scope+'/index.html')
    public(_read(root,'content/places/sources/national-basemap.json').get('image'))
    css_url=r'''url\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|([^)'"\s][^)]*?))\s*\)'''
    while pending:
        name=pending.pop()
        if name in visited:continue
        visited.add(name);path=_path(root,name)
        if not path.is_file():raise ValueError('Missing required public evidence artifact: '+name)
        if path.suffix.lower() in ('.html','.htm'):
            page=_Assets(path.read_text(encoding='utf-8-sig'))
            for url in page.urls:
                resolved=_local(url,name)
                if resolved:public(resolved)
            for config in page.configs:
                for layer in config.get('layers',[]):geometry(layer)
                public(config.get('basemap',{}).get('image'))
        elif path.suffix.lower()=='.css':
            text=path.read_text(encoding='utf-8-sig')
            urls=[next(s for s in m.groups() if s is not None).strip() for m in re.finditer(css_url,text,re.I)]
            urls.extend(re.findall(r'@import\s+["\']([^"\']+)["\']',text,re.I))
            for url in urls:
                resolved=_local(url,name)
                if resolved:public(resolved)
    rows=[]
    for name in sorted(required|set(optional)):
        path=_path(root,name);local=name in optional
        if not path.is_file():
            if not local:raise ValueError('Missing required public evidence artifact: '+name)
            rows.append({'path':name,'optionalLocalOnly':True,'missing':True,**({'sha256':optional[name]} if optional[name] else {})});continue
        digest,size=_digest(path)
        if local and optional[name] and digest!=optional[name]:raise ValueError('Retained original differs from canonical source hash: '+name)
        rows.append({'path':name,'sha256':digest,'bytes':size,**({'optionalLocalOnly':True} if local else {})})
    return rows

def verify_fingerprints(root,rows):
    root=Path(root);prefixes,_=_retention(root);errors=[];absent=[];checked=0;seen=set()
    if not isinstance(rows,list) or not rows:return {'errors':['Evidence artifactFingerprints must be a non-empty list'],'checked':0,'absentLocalOnly':[]}
    for row in rows:
        try:
            name=_name(row['path']);path=_path(root,name)
            if name in seen:raise ValueError('Duplicate evidence fingerprint: '+name)
            seen.add(name);local=name.startswith(prefixes)
            if row.get('optionalLocalOnly') and not local:raise ValueError('Public artifact cannot be optional: '+name)
            if not path.is_file():
                if local:absent.append(name);continue
                raise ValueError('Missing required public evidence artifact: '+name)
            expected=row.get('sha256')
            if not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Existing artifact has no reviewed SHA-256: '+name)
            actual,size=_digest(path)
            if actual!=expected:raise ValueError('Stale evidence; bytes changed: '+name)
            if row.get('bytes') is not None and size!=row['bytes']:raise ValueError('Stale evidence; size changed: '+name)
            checked+=1
        except (OSError,ValueError,KeyError,TypeError) as exc:errors.append(str(exc))
    return {'errors':errors,'checked':checked,'absentLocalOnly':sorted(absent)}

def require_current_evidence(root,validation,browser):
    """Raise on stale/incomplete reports; return scoped raw-absence information."""
    root=Path(root)
    if str(validation.get('status','')).upper()!='PASS' or validation.get('mode')!='generated-pages-and-data':raise ValueError('Passing default national validation is required')
    if str(browser.get('status',browser.get('result',''))).upper()!='PASS':raise ValueError('Passing real browser review is required')
    rows=validation.get('artifactFingerprints');checked=verify_fingerprints(root,rows)
    if checked['errors']:raise ValueError('; '.join(checked['errors'][:12]))
    current=collect_fingerprints(root)
    expected={r['path'] for r in current};recorded={r['path'] for r in rows}
    if expected!=recorded:raise ValueError('National evidence artifact set changed; revalidate. Missing '+str(sorted(expected-recorded)[:8])+'; obsolete '+str(sorted(recorded-expected)[:8]))
    browser_rows=browser.get('artifactFingerprints');bcheck=verify_fingerprints(root,browser_rows)
    if bcheck['errors']:raise ValueError('Browser evidence: '+'; '.join(bcheck['errors'][:12]))
    tested=browser.get('testedPagePaths');fixtures=browser.get('fixturePaths')
    if not isinstance(tested,list) or not tested or not isinstance(fixtures,list) or not fixtures:raise ValueError('Browser report must name non-empty testedPagePaths and fixturePaths')
    browser_paths={r['path'] for r in browser_rows}
    required=set(BROWSER_CODE_FILES)|{_name(p) for p in tested+fixtures}
    if not required<=browser_paths:raise ValueError('Browser evidence missing code/page/fixture hashes: '+str(sorted(required-browser_paths)))
    if any(not _name(p).endswith(('.html','.htm')) for p in tested):raise ValueError('Browser testedPagePaths must identify delivered HTML pages')
    return {'national':checked,'browser':bcheck,'artifactCount':len(rows)}
