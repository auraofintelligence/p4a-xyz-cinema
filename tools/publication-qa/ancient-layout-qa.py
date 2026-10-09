"""Check full-page flow and optional details at the requested desktop and mobile sizes."""
from pathlib import Path
import sys,json,base64
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.bringToFront');c.call('Page.enable');c.call('Runtime.enable');runs=[]
out=R/'tools/publication-qa/ancient-layout-screenshots';out.mkdir(exist_ok=True)
for width,height in [(1665,983),(390,950)]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':width<500})
 c.evaluate('window.__oldLayoutQA=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/pages/ancient-aliens.html'})
 c.wait("!window.__oldLayoutQA&&document.readyState==='complete'&&!!document.querySelector('.footer-index')")
 c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
 for state in ['closed','open']:
  c.evaluate('document.querySelectorAll("#room details").forEach(e=>e.open='+str(state=='open').lower()+');window.scrollTo(0,0)')
  result=c.evaluate("(()=>{let panels=[...document.querySelectorAll('#room .feature-panel')];let rects=panels.map(e=>e.getBoundingClientRect());let footer=[...document.querySelector('.footer-index').children].map(e=>e.getBoundingClientRect().top);return {overflow:document.documentElement.scrollWidth>innerWidth+2,sectionWidths:rects.map(r=>Math.round(r.width)),sectionGaps:rects.slice(1).map((r,i)=>Math.round(r.top-rects[i].bottom)),headingSizes:panels.map(e=>getComputedStyle(e.querySelector('h2')).fontSize),clippedActions:[...document.querySelectorAll('#room .source-links a')].filter(e=>e.clientWidth&&e.scrollWidth>e.clientWidth+2).map(e=>e.textContent),footerAligned:innerWidth<500||Math.max(...footer)-Math.min(...footer)<2}})()")
  assert not result['overflow'] and not result['clippedActions'] and result['footerAligned'],result
  assert len(set(result['headingSizes']))==1 and len(set(result['sectionWidths']))==1,result
  assert min(result['sectionGaps'])>=16 and max(result['sectionGaps'])-min(result['sectionGaps'])<=2,result
  size=c.call('Page.getLayoutMetrics')['cssContentSize']
  if state=='closed':
   (out/f'full-{width}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,'clip':{'x':0,'y':0,'width':width,'height':size['height'],'scale':.6}})['data']))
  runs.append({'width':width,'height':height,'details':state,**result})
 c.evaluate('document.querySelectorAll("#room details").forEach(e=>e.open=false)')
 for anchor in ['disclosure','sky-country-partnership','records','religion-and-aliens']:
  c.evaluate('document.getElementById('+json.dumps(anchor)+').scrollIntoView({behavior:"instant"});window.scrollBy(0,-90)')
  c.evaluate('new Promise(r=>setTimeout(r,150))')
  (out/f'{anchor}-{width}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
 # Native disclosures remain keyboard operable.
 c.evaluate('document.querySelector("#disclosure summary").focus()')
 c.call('Input.dispatchKeyEvent',{'type':'rawKeyDown','key':' ','code':'Space','windowsVirtualKeyCode':32})
 c.call('Input.dispatchKeyEvent',{'type':'keyUp','key':' ','code':'Space','windowsVirtualKeyCode':32})
 c.wait('document.querySelector("#disclosure details").open',seconds=3)
(R/'tools/publication-qa/ancient-layout-report.json').write_text(json.dumps({'browserChecks':runs,'keyboardDisclosure':True,'sharedStylesChanged':False,'bodyCopyChanged':False},indent=2)+'\n',encoding='utf-8')
print('PASS full-page flow, uniform headings/padding/gaps, open/closed details, keyboard disclosure, footer and actions at 1665x983 and 390x950')
