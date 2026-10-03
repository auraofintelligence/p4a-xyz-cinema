from cdp_client import CDP
import pathlib,json
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');c.call('Network.setBlockedURLs',{'urls':[]});report=[]
original_wait=c.wait
def checked_wait(expression,seconds=45):
 try:return original_wait(expression,seconds)
 except Exception:
  print('FAILURE',json.dumps(c.evaluate("({url:location.href,state:window.P4A_VIC_MAP?.getState(),message:document.querySelector('[data-map-message]')?.textContent,rect:document.querySelector('.vic-map-stage')?.getBoundingClientRect().toJSON(),viewport:[innerWidth,innerHeight]})")),flush=True)
  print(json.dumps([x for x in c.events if x.get('method')=='Runtime.exceptionThrown']),flush=True)
  raise
c.wait=checked_wait
def ev(s):return c.evaluate(s)
def navigate(url):
 ev('window.__qaOldDocument=true');c.call('Page.navigate',{'url':url});c.wait("!window.__qaOldDocument && document.readyState==='complete'")
aligned='''(()=>{const r=document.querySelector('.vic-map-stage').getBoundingClientRect();let top=0;for(const n of document.querySelectorAll('.site-header,.site-layer-strip')){const s=getComputedStyle(n),b=n.getBoundingClientRect();if(['sticky','fixed'].includes(s.position)&&b.top<150&&b.bottom>0)top=Math.max(top,b.bottom);}return Math.abs(r.top-top-12)<3;})()'''
for protocol,url in [('file',(pathlib.Path(__file__).resolve().parents[2]/'states/vic/map/index.html').as_uri()),('http','http://127.0.0.1:8766/states/vic/map/')]:
 for width in [1440,390]:
  print(protocol,width,flush=True)
  c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000 if width>500 else 844,'deviceScaleFactor':1 if width>500 else 2,'mobile':width<500});navigate(url+'?chamber=lga');c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady');c.wait(aligned)
  ident=ev('P4A_VIC_ELECTORATES.lga.find(r=>r.name.includes("Macedon Ranges")).id');ev('document.querySelector(\'[data-electorate="'+ident+'"]\').click()');c.wait(aligned)
  ev("document.querySelector('[data-electorate-profile]').scrollIntoView({behavior:'instant'});document.querySelector('[data-local-wards]').click()");c.wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count===3');c.wait(aligned)
  ev("document.querySelector('[data-electorate-list] button').click()");c.wait(aligned);ward=ev('P4A_VIC_MAP.getState().selected')
  ev("document.querySelector('[data-electorate-search]').value='zzzz';document.querySelector('[data-electorate-search]').dispatchEvent(new Event('input'));document.querySelector('[data-map-reset]').click();document.querySelector('[data-map-reset]').click()");c.wait(aligned)
  state=ev('P4A_VIC_MAP.getState()');assert state['count']==467 and state['localScope'] is None and state['selected']==ward and state['viewMode']=='state',state
  assert ev("document.querySelector('[data-electorate-search]').value==='' && document.querySelectorAll('[data-electorate-list] button').length===467")
  assert ev('(()=>{const s=P4A_VIC_MAP.getState(),b=s.stateBounds,t=s.transform,r=document.querySelector(".vic-map-stage");return b[0]*t.scale+t.x>=29&&b[2]*t.scale+t.x<=r.clientWidth-29&&b[1]*t.scale+t.y>=30&&b[3]*t.scale+t.y<=r.clientHeight-30})()')
  urlstate=ev('location.href');navigate(urlstate);c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count===467');c.wait(aligned);assert ev('P4A_VIC_MAP.getState().viewMode')=='state'
  for layer,count in [('assembly',88),('council',8),('lga',87)]:
   ev('document.querySelector("[data-map-layer='+layer+']").click();document.querySelector("[data-map-reset]").click()');c.wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count==='+str(count));c.wait(aligned);assert ev('P4A_VIC_MAP.getState().viewMode')=='state'
   ev("document.querySelector('[data-electorate-list] button').click()");c.wait(aligned);selected=ev('P4A_VIC_MAP.getState().selected');ev("document.querySelector('[data-map-reset]').click()");c.wait(aligned);assert ev('P4A_VIC_MAP.getState().selected')==selected
  # Individual ward deep link, stale hash removal, and browser history restoration.
  navigate(url+'?chamber=ward&electorate='+ward+'&council='+ident);c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().selected==='+json.dumps(ward));c.wait(aligned)
  ev("document.querySelector('[data-electorate-profile] a[href^=\"?chamber=lga\"]').click()");c.wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().layer==="lga"');c.wait(aligned);ev('history.back()');c.wait('P4A_VIC_MAP.getState().selected==='+json.dumps(ward));c.wait(aligned)
  ev("document.querySelector('[data-map-interaction]').focus({preventScroll:true})");c.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Home','code':'Home'});c.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'Home','code':'Home'});c.wait('P4A_VIC_MAP.getState().viewMode==="state" && P4A_VIC_MAP.getState().count===467');c.wait(aligned)
  report.append({'protocol':protocol,'width':width,'wardDrilldownAligned':True,'individualWardAligned':True,'resetScopeAndFilter':True,'resetPreservesSelection':True,'statewideExtent':True,'resetDuringLoad':True,'repeatedReset':True,'reloadAndBack':True,'keyboardHome':True})
errors=[x for x in c.events if x.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
pathlib.Path(__file__).resolve().parent.joinpath('map-navigation-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
