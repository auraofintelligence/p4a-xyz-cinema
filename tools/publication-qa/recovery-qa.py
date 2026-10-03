"""Final file/HTTP desktop/mobile publication checks; outputs a dated report."""
import datetime,json,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/vic-qa'))
from cdp_client import CDP
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
pages={p:Links() for p in [ROOT/'index.html',*ROOT.glob('pages/*.html'),*ROOT.glob('states/**/*.html')]}
for p,parser in pages.items():parser.feed(p.read_text(encoding='utf-8'))
missing=[];count=0;fragments=0
for p,parser in pages.items():
 for href in parser.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  count+=1
  if not target.exists():missing.append([str(p.relative_to(ROOT)),href])
  # Runtime-generated fragments are checked by the browser below.
  if u.fragment and target in pages and unquote(u.fragment) in pages[target].ids:fragments+=1
assert not missing,missing
projects=json.loads((ROOT/'content/connected-projects.json').read_text(encoding='utf-8'))
reviewed=[x for x in projects['projects'] if x.get('description')];assert len(reviewed)==7
for item in reviewed:
 assert item['links'][0] in (ROOT/'pages/site-map.html').read_text(encoding='utf-8')
 for name in item['contextPages']:assert item['links'][0] in (ROOT/'pages'/name).read_text(encoding='utf-8')
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');runs=[]
def nav(url):
 c.evaluate('window.__qaOldDocument=true');c.call('Page.navigate',{'url':url});c.wait("!window.__qaOldDocument && document.readyState==='complete'")
for protocol,base in [('file',ROOT.as_uri()+'/'),('http','http://127.0.0.1:8765/')]:
 for width in [1440,390]:
  c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000 if width>500 else 844,'deviceScaleFactor':1,'mobile':width<500})
  for path in ['index.html','pages/site-map.html','pages/about.html','states/vic/index.html','states/vic/election/index.html','states/vic/map/index.html']:
   nav(base+path);c.wait('!!document.querySelector(".footer-index")')
   result=c.evaluate('''(()=>{const f=document.querySelector('.footer-index'),g=[...f.children],ys=g.map(x=>x.getBoundingClientRect().top);return {groups:g.length,columns:getComputedStyle(f).gridTemplateColumns,topAligned:innerWidth<500||Math.max(...ys)-Math.min(...ys)<2,overflow:document.documentElement.scrollWidth>innerWidth,layout:g.map(x=>getComputedStyle(x).justifyContent)}})()''')
   assert result['topAligned'] and not result['overflow'],[protocol,width,path,result]
   assert all(x=='flex-start' for x in result['layout']),result
   if path=='index.html':
    c.wait('!!document.querySelector("[data-ticker-toggle]")');c.evaluate('document.querySelector("[data-ticker-toggle]").click()');assert c.evaluate('document.querySelector("[data-issue-ticker]").classList.contains("is-paused")')
    c.evaluate('document.querySelector("[data-ticker-group] a").focus()');assert c.evaluate('document.querySelector("[data-issue-ticker]").classList.contains("has-link-focus")')
    c.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});c.wait('document.querySelector("[data-ticker-toggle]").disabled');c.call('Emulation.setEmulatedMedia',{'features':[]})
    assert c.evaluate('!!document.querySelector(\'a[href="states/vic/election/index.html"]\')')
   if path=='pages/site-map.html':
    for anchor in ['official-links-out','connected-projects']:
     assert c.evaluate('!!document.getElementById('+json.dumps(anchor)+')')
   if path=='states/vic/election/index.html':c.wait('document.querySelectorAll("[data-candidate-id]").length===482')
   runs.append({'protocol':protocol,'width':width,'path':path,**result});print(protocol,width,path,'PASS',flush=True)
  nav(base+'states/vic/map/index.html?chamber=firstpeoples');c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady');assert c.evaluate('P4A_VIC_MAP.getState().chamber || P4A_VIC_MAP.getState().layer')=='firstpeoples'
report={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':len(pages),'localLinks':count,'staticFragments':fragments,'missingLinks':missing,'reviewedProjects':len(reviewed),'browserRuns':runs}
(ROOT/'tools/publication-qa/recovery-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS',len(pages),'pages;',count,'local links;',len(runs),'browser cases; First Peoples deep links')
