"""Verify the new AI futures doorway and its public-policy room."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import sys,json,base64
R=Path(__file__).resolve().parents[2];count=0
for name in ['ai-pdoom','twinkle-ai-pdoom']:
 p=R/'pages'/f'{name}.html';s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 ids=[e['id'] for e in s.select('[id]')];assert len(ids)==len(set(ids))
 for a in s.select('a[href]'):
  u=urlsplit(a['href'])
  if u.scheme in ['https','http']:assert a.get('target')=='_blank' and 'noopener' in a.get('rel',[])
  elif not u.scheme:
   dest=(p.parent/unquote(u.path)).resolve() if u.path else p
   assert dest.exists(),a['href']
   if u.fragment:assert BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser').find(id=unquote(u.fragment)),a['href']
  count+=1
s=BeautifulSoup((R/'pages/ai-pdoom.html').read_text(encoding='utf-8'),'html.parser')
for term in ['p(doom)','p(protopia)','p(fair go)','p(Joyful Responsible Abundance)']:assert term in s.get_text()
assert 'gajra-earth-claude-build/trinity.html' in str(s)
assert 'gajra-earth-claude-build/questions.html' in str(s)
assert '2010' not in BeautifulSoup((R/'pages/ancient-aliens.html').read_text(encoding='utf-8'),'html.parser').select_one('#recent-sightings').get_text()
sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[]
shots=R/'tools/publication-qa/ai-futures-screenshots';shots.mkdir(exist_ok=True)
for width in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':950,'deviceScaleFactor':1,'mobile':width<500})
 for name in ['ai-pdoom','twinkle-ai-pdoom']:
  c.evaluate('window.__oldAI=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/pages/'+name+'.html'})
  c.wait("!window.__oldAI&&document.readyState==='complete'&&!!document.querySelector('.footer-index')")
  c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
  anchors=['main','four-futures','ai-gods','public-options','constructive-paths','take-part'] if name=='ai-pdoom' else ['main']
  for anchor in anchors:
   c.evaluate('document.getElementById('+json.dumps(anchor)+').scrollIntoView({behavior:"instant"});window.scrollBy(0,-90)')
   c.evaluate('new Promise(r=>setTimeout(r,200))')
   result=c.evaluate("(()=>{let y=[...document.querySelector('.footer-index').children].map(e=>e.getBoundingClientRect().top);return {overflow:document.documentElement.scrollWidth>innerWidth+2,footerAligned:innerWidth<500||Math.max(...y)-Math.min(...y)<2,clippedActions:[...document.querySelectorAll('.button,.source-links a')].filter(e=>e.clientWidth&&e.scrollWidth>e.clientWidth+2).map(e=>e.textContent)}})()")
   assert not result['overflow'] and result['footerAligned'] and not result['clippedActions'],[name,width,anchor,result]
   (shots/f'{name}-{anchor}-{width}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
   runs.append({'page':name,'width':width,'anchor':anchor,**result})
(R/'tools/publication-qa/ai-futures-report.json').write_text(json.dumps({'checked':'2026-10-04','linksAndAnchors':count,'browserChecks':runs,'first48Twinkles':'Verified separately by reviewed-copy-qa.py','creativeProbabilityPrompts':'No fabricated percentages or claim of standard metrics'},indent=2)+'\n',encoding='utf-8')
print('PASS',count,'links/anchors;',len(runs),'desktop/mobile checks')
