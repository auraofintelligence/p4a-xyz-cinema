from pathlib import Path
import sys,base64,json
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[];out=R/'tools/publication-qa/action-screenshots'
cases=[('pages/p4a-builder.html?tool=contribution-ledger-summary','.builder-actions'),('pages/test-store1.html','.support-presets'),('pages/states.html','.segmented-control'),('pages/site-map.html','.official-link-actions'),('states/vic/election/index.html','.ve-filters'),('pages/ancient-aliens.html','#empty-chair'),('pages/ancient-aliens.html','#traditions'),('pages/ancient-aliens.html','#australian-records')]
for w in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':950,'deviceScaleFactor':1,'mobile':w<500})
 for i,(page,sel) in enumerate(cases):
  c.evaluate('window.__oldExtra=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/'+page});c.wait("!window.__oldExtra&&document.readyState==='complete'")
  c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
  c.wait('!!document.querySelector('+json.dumps(sel)+')')
  c.evaluate('document.querySelector('+json.dumps(sel)+').scrollIntoView({block:"start",behavior:"instant"});window.scrollBy(0,-95)')
  result=c.evaluate("({overflow:document.documentElement.scrollWidth>innerWidth+2,header:document.querySelector('h1').textContent})")
  assert not result['overflow'],[page,w]
  if sel=='.support-presets':
   c.evaluate("document.querySelectorAll('.support-presets button')[1].click()")
   assert c.evaluate("document.querySelectorAll('.support-presets button')[1].classList.contains('is-active')")
   result['presetClickChangesSelection']=True
  if sel=='.builder-actions':
   result['actions']=c.evaluate("[...document.querySelectorAll('.builder-actions button')].map(e=>({text:e.textContent.trim(),height:e.getBoundingClientRect().height}))")
  if sel=='.ve-filters':
   c.evaluate("let e=document.querySelector('.ve-filters input');e.value='Jacinta';e.dispatchEvent(new Event('input',{bubbles:true}))")
   result['filterResponds']=c.evaluate("document.querySelectorAll('.ve-candidate:not([hidden])').length<20")
   assert result['filterResponds']
  # Long-label stress check restores text immediately; no destination changes.
  longlabel=c.evaluate("(()=>{let e=document.querySelector('.next-trail a')||document.querySelector('.hero-actions a')||document.querySelector('.ve-actions a');if(!e)return null;let t=e.textContent;e.textContent='Review the complete community evidence and correction record';let ok=e.scrollWidth<=e.clientWidth+2&&e.getBoundingClientRect().right<=innerWidth+2;e.textContent=t;return ok})()")
  assert longlabel is not False;result['longLabelFits']=longlabel
  if sel=='#empty-chair':
   c.evaluate("document.querySelector('#empty-chair details').open=true")
   result['expandableSourceOpens']=True
  c.evaluate('new Promise(r=>setTimeout(r,250))')
  file=('ancient' if 'ancient' in page else 'variant')+'-'+str(i)+'-'+str(w)+'.png';(out/file).write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
  runs.append({'page':page,'selector':sel,'width':w,**result});print('PASS',w,page,sel,flush=True)
(R/'tools/publication-qa/action-and-ancient-extra-report.json').write_text(json.dumps(runs,indent=2)+'\n',encoding='utf-8')
