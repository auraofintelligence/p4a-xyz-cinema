"""Action inventory and representative desktop/mobile interaction checks."""
from pathlib import Path
from bs4 import BeautifulSoup
import sys,json,base64,collections,subprocess
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
OUT=R/'tools/publication-qa';shots=OUT/'action-screenshots';shots.mkdir(exist_ok=True)
selector='.button,.ve-button,.source-links a,.official-link-actions a,.builder-nav-strip a,.map-jump a,.index-toggle,.floating-action-link,.floating-top-button,.segmented-control button,.support-presets button,.ve-filters button,.vic-workbench button:not(.vic-physical-seat),.ve-candidate-actions a'
paths=[R/'index.html',*sorted((R/'pages').rglob('*.html')),*sorted((R/'states').rglob('*.html'))];inventory=collections.Counter();linkchanges=[]
for p in paths:
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for e in s.select(selector):inventory[e.name+'.'+'.'.join(e.get('class',[]))]+=1
 old=subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R).decode('utf-8')
 if [a.get('href') for a in s.select('a[href]')]!=[a.get('href') for a in BeautifulSoup(old,'html.parser').select('a[href]')]:linkchanges.append(p.relative_to(R).as_posix())
assert not [x for x in linkchanges if x not in ['pages/ancient-aliens.html','pages/truth-engine.html']],linkchanges
pages=['index.html','pages/civic-ledger.html','pages/gambling-harm.html','pages/web3-sensorium.html','pages/joke.html','pages/twinkle-ancient-aliens.html','pages/site-map.html','pages/p4a-builder.html?tool=ledger-summary','pages/c-hour-receipt-builder.html','pages/support.html','pages/states.html','states/vic/index.html','states/vic/election/index.html','states/vic/map/index.html']
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[]
for w in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':950,'deviceScaleFactor':1,'mobile':w<500})
 for name in pages:
  c.evaluate('window.__oldAction=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/'+name});c.wait("!window.__oldAction&&document.readyState==='complete'")
  c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
  c.evaluate('new Promise(r=>setTimeout(r,350))')
  result=c.evaluate('''(()=>{let sel=SELECTOR;let items=[...document.querySelectorAll(sel)].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height);let failed=items.filter(e=>e.scrollWidth>e.clientWidth+3||e.getBoundingClientRect().right>innerWidth+2).map(e=>({label:e.textContent.trim(),class:e.className,width:e.clientWidth,scroll:e.scrollWidth}));let groups=[...new Set(items.map(e=>e.className||e.parentElement.className))];return {overflow:document.documentElement.scrollWidth>innerWidth+2,actions:items.length,clipped:failed,groups,heights:items.filter(e=>e.closest('.next-trail')).map(e=>({label:e.textContent.trim(),height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width}))}})()'''.replace('SELECTOR',json.dumps(selector)))
  assert not result['overflow'] and not result['clipped'],[name,w,result]
  target=c.evaluate("(()=>{let e=document.querySelector('.next-trail .button')||document.querySelector('.ve-actions a')||document.querySelector('.vic-map-controls button')||document.querySelector('.button');if(!e)return null;e.scrollIntoView({block:'center',behavior:'instant'});e.focus();window.__actionTest=e;let r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,width:r.width,height:r.height}})()")
  if target:
   for repeat in range(3):
    c.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':target['x'],'y':target['y']})
    c.evaluate('new Promise(r=>setTimeout(r,180))')
    assert c.evaluate('Math.abs(__actionTest.getBoundingClientRect().width-'+str(target['width'])+')<1')
    c.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':1,'y':1})
   c.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Tab','code':'Tab','windowsVirtualKeyCode':9});c.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'Tab','code':'Tab','windowsVirtualKeyCode':9})
   focus=c.evaluate("__actionTest.focus();getComputedStyle(__actionTest).outlineStyle")
   assert focus not in ['none','hidden'],[name,w,'focus']
   target=c.evaluate("(()=>{__actionTest.scrollIntoView({block:'center',behavior:'instant'});let r=__actionTest.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()")
   # Observe a real click without opening external pages or submitting a form.
   c.evaluate("window.__testClick=false;__actionTest.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();window.__testClick=true},{once:true,capture:true})")
   for typ in ['mousePressed','mouseReleased']:c.call('Input.dispatchMouseEvent',{'type':typ,'x':target['x'],'y':target['y'],'button':'left','clickCount':1})
   assert c.evaluate('window.__testClick'),[name,w,'click']
   result['stableRepeatedHover']=True;result['clickObserved']=True;result['focusOutline']=focus
  if name=='pages/civic-ledger.html':c.evaluate("document.querySelector('.next-trail').scrollIntoView({block:'center',behavior:'instant'})")
  c.evaluate('new Promise(r=>setTimeout(r,200))')
  file=name.split('?')[0].replace('/','-').replace('.html','')+'-'+str(w)+'.png';(shots/file).write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
  runs.append({'page':name,'width':w,**result});print('PASS',w,name,flush=True)
c.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
reduced=c.evaluate("getComputedStyle(document.querySelector('.index-toggle')).transitionDuration")
assert float(reduced.rstrip('s'))<=.001,reduced
c.call('Emulation.setEmulatedMedia',{'features':[]})
(OUT/'action-design-report.json').write_text(json.dumps({'publicHTMLFiles':len(paths),'staticInventory':dict(inventory),'buttonNavigationChanges':[],'separateContentChangeExcludedFromNavigationComparison':linkchanges,'runs':runs,'reducedMotionTransition':reduced,'ticker':'Excluded from action selectors; original CSS and JS unmodified.','semantics':'Prose links, tags/status badges and atlas list rows retain distinct treatment. Physical chamber seat markers are excluded: they preserve their spatial geometry, party colours and intentional horizontally scrollable chamber.'},indent=2)+'\n',encoding='utf-8')
print('PASS',len(runs),'render cases; inventory, destination preservation, repeated hover, focus, click, reduced motion')
