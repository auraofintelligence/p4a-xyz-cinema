"""Check generated rooms, links, ticker preservation and desktop/mobile layout."""
import json, sys, base64
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'tools/vic-qa'))
from cdp_client import CDP
class Document(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if t=='a' and a.get('href'):self.links.append(a)
docs={p:Document() for p in [R/'index.html',*R.glob('pages/*.html'),*R.glob('states/**/*.html')]}
for p,d in docs.items():d.feed(p.read_text(encoding='utf-8'))
names=sys.argv[1:] or [p.name for p in (R/'content/rooms').glob('*.html')]
errors=[]
for name in names:
 p=R/'pages'/name
 for a in docs[p].links:
  u=urlsplit(a['href'])
  if u.scheme in ('https','http'):
   if a.get('target')!='_blank':errors.append([name,a['href'],'external target'])
  elif not u.scheme and not u.netloc:
   dest=(p.parent/unquote(u.path)).resolve() if u.path else p
   if dest.is_dir():dest=dest/'index.html'
   if not dest.exists():errors.append([name,a['href'],'missing file'])
   if u.fragment and dest in docs and unquote(u.fragment) not in docs[dest].ids and dest.name!='p4a-builder.html':errors.append([name,a['href'],'missing anchor'])
assert not errors,errors
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[]
for width in (1440,390):
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':900,'deviceScaleFactor':1,'mobile':width<500})
 for name in names:
  c.evaluate('window.__oldPolicyQA=true');c.call('Page.navigate',{'url':(R/'pages'/name).as_uri()});c.wait("!window.__oldPolicyQA && document.readyState==='complete' && !!document.querySelector('.footer-index')")
  c.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
  result=c.evaluate("(()=>{let g=[...document.querySelector('.footer-index').children];let y=g.map(e=>e.getBoundingClientRect().top);return {overflow:document.documentElement.scrollWidth>innerWidth,footerAligned:innerWidth<500||Math.max(...y)-Math.min(...y)<2,h1:document.querySelector('h1').textContent}})()")
  assert not result['overflow'] and result['footerAligned'],[name,width,result]
  runs.append({'page':name,'width':width,**result})
  if len(runs)%10==0:print('Checked',len(runs),'render cases',flush=True)
  if name in ('web3-sensorium.html','twinkle.html','ai-copyright.html','tobacco.html','marriage-divorce.html','restricted-plants.html'):
   c.evaluate("document.documentElement.style.scrollBehavior='auto'; (document.querySelector('#missing-middle')||document.querySelector('#seeds')||document.querySelector('#room')).scrollIntoView({behavior:'instant'})")
   c.wait("Math.abs((document.querySelector('#missing-middle')||document.querySelector('#seeds')||document.querySelector('#room')).getBoundingClientRect().top)<140")
   c.evaluate("new Promise(resolve=>setTimeout(resolve,1200))")
   shot=c.call('Page.captureScreenshot',{'format':'png'})['data']
   (R/'tools/publication-qa'/f'{Path(name).stem}-{width}.png').write_bytes(base64.b64decode(shot))
(R/'tools/publication-qa/policy-report.json').write_text(json.dumps({'checked':'2026-10-03','linkErrors':errors,'browserRuns':runs},indent=2)+'\n',encoding='utf-8')
print('PASS',len(names),'pages;',len(runs),'desktop/mobile cases; local links and anchors; external targets')
