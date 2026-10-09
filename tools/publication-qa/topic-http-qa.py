"""HTTP smoke checks, inline visual layout and ticker pointer regression."""
import json,sys,base64
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/vic-qa'))
from cdp_client import CDP
total=json.loads((R/'content/public-topic-inventory.json').read_text())['totalTwinkles']
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[]
def nav(path):
 c.evaluate('window.__previousTopic=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/'+path});c.wait("!window.__previousTopic&&document.readyState==='complete'&&!!document.querySelector('.footer-index')")
def pointer(x,y):
 c.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':x,'y':y})
 c.call('Input.dispatchMouseEvent',{'type':'mousePressed','x':x,'y':y,'button':'left','clickCount':1})
 c.call('Input.dispatchMouseEvent',{'type':'mouseReleased','x':x,'y':y,'button':'left','clickCount':1})
for width in (1440,390):
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':900,'deviceScaleFactor':1,'mobile':width<500})
 for path in ['pages/twinkle.html','pages/twinkle-super-investments.html','pages/super-investments.html','pages/site-map.html','pages/tobacco.html','pages/marriage-divorce.html','pages/restricted-plants.html','pages/web3-sensorium.html','pages/migration-equations.html','pages/international-wars.html','pages/security-fallacies.html']:
  nav(path)
  result=c.evaluate("(()=>{let gs=[...document.querySelector('.footer-index').children],y=gs.map(e=>e.getBoundingClientRect().top);return {overflow:document.documentElement.scrollWidth>innerWidth,footerAligned:innerWidth<500||Math.max(...y)-Math.min(...y)<2,main:document.querySelectorAll('main').length,h1:document.querySelectorAll('h1').length}})()")
  assert not result['overflow'] and result['footerAligned'] and result['main']==result['h1']==1,[path,result]
  if path=='pages/twinkle.html':
   c.evaluate("document.querySelectorAll('.seed-icon').forEach(i=>i.loading='eager')")
   c.wait("[...document.querySelectorAll('.seed-icon')].every(i=>i.complete&&i.naturalWidth>0)")
   check=c.evaluate("[...document.querySelectorAll('.seed-marker')].map(m=>{let n=m.querySelector('span').getBoundingClientRect(),i=m.querySelector('.seed-icon,.olympic-rings').getBoundingClientRect();return {inline:Math.abs((n.top+n.height/2)-(i.top+i.height/2))<2,markerHeight:m.getBoundingClientRect().height}})")
   assert len(check)==total and all(x['inline'] for x in check),check
   result['inlineIcons']=total
   # Verify an actual keyboard focus target and visible focus outline.
   c.evaluate("document.querySelector('a[href=\"twinkle-olympics.html\"]').focus()")
   assert c.evaluate("document.activeElement.getAttribute('href')==='twinkle-olympics.html'")
   c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelector('a[href=\"twinkle-olympics.html\"]').scrollIntoView({behavior:'instant',block:'center'});document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
   c.evaluate("new Promise(r=>setTimeout(r,1000))")
   (R/'tools/publication-qa'/f'games-inline-{width}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
  runs.append({'path':path,'width':width,**result})
 nav('index.html');c.wait('!!document.querySelector("[data-ticker-clone]")')
 c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelector('[data-issue-ticker]').scrollIntoView({behavior:'instant',block:'center'})")
 # Hover/pointer activation must preserve the visible moving anchor's destination.
 target=c.evaluate("(()=>{let v=document.querySelector('[data-ticker-viewport]').getBoundingClientRect();let a=[...document.querySelectorAll('[data-ticker-group] a')].find(a=>{let r=a.getBoundingClientRect();return r.left>v.left+10&&r.right<v.right-10});let r=a.getBoundingClientRect();return {href:a.getAttribute('href'),x:r.left+r.width/2,y:r.top+r.height/2}})()")
 pointer(target['x'],target['y']);c.wait('location.pathname.endsWith('+json.dumps('/'+target['href'])+')')
 nav('index.html');c.wait('!!document.querySelector("[data-ticker-toggle]")');c.evaluate("document.querySelector('[data-ticker-toggle]').click()")
 assert c.evaluate("document.querySelector('[data-issue-ticker]').classList.contains('is-paused')")
 c.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]});c.wait("document.querySelector('[data-ticker-toggle]').disabled")
 assert c.evaluate("[...document.querySelectorAll('[data-ticker-clone] a')].every(a=>a.tabIndex===-1)")
 c.call('Emulation.setEmulatedMedia',{'features':[]})
 runs.append({'path':'index.html','width':width,'movingPointerLink':target['href'],'pause':True,'reducedMotion':True,'clonesNotKeyboardFocusable':True})
(R/'tools/publication-qa/topic-http-report.json').write_text(json.dumps({'checked':'2026-10-03','runs':runs},indent=2)+'\n',encoding='utf-8')
print('PASS',len(runs),'HTTP cases;',total,'inline visual checks at both widths; pointer, pause, reduced motion')
