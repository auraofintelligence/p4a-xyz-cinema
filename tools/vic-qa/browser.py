from cdp_client import CDP
import pathlib,json,base64,time
import sys
out=pathlib.Path(sys.argv[1]);c=CDP();c.call('Page.enable');c.call('Runtime.enable');results={}
c.call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1100,'deviceScaleFactor':1,'mobile':False})
c.call('Page.navigate',{'url':'http://127.0.0.1:8765/states/vic/map/'})
c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().count===88')
fixtures=json.loads((out/'vic-picking-fixtures.json').read_text())
def ev(s):return c.evaluate(s)
def screenshot(name):
 (out/name).write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
def check_picks(layer):
 points=[f for f in fixtures if f['layer']==layer]
 failures=ev('('+json.dumps(points)+').map(f=>({...f,actual:P4A_VIC_MAP.pickLonLat(...f.point)})).filter(f=>f.actual!==f.expected)')
 assert not failures,failures[:8]
 return len(points)
results['assemblyPicking']=check_picks('assembly')
ev('document.querySelector("[data-map-layer=council]").click()');c.wait('P4A_VIC_MAP.getState().count===8')
results['councilPicking']=check_picks('council')
ev('document.querySelector("[data-map-layer=assembly]").click()');c.wait('P4A_VIC_MAP.getState().count===88')
# Search and a real keyboard Enter activation preserve focus after the list refresh.
ev('var search=document.querySelector("[data-electorate-search]");search.value="Brunswick";search.dispatchEvent(new Event("input"));document.querySelector("[data-electorate-list] button").focus()')
c.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Enter','code':'Enter','windowsVirtualKeyCode':13,'text':'\r','unmodifiedText':'\r'});c.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
c.wait('P4A_VIC_MAP.getState().selected')
results['keyboardSelection']=ev('({selected:P4A_VIC_MAP.getState().selected,focus:document.activeElement.dataset.electorate,vacant:document.querySelector("[data-electorate-profile]").textContent.includes("Vacant seat")})')
assert results['keyboardSelection']['focus']==results['keyboardSelection']['selected'] and results['keyboardSelection']['vacant']
results['zoomedPicking']=check_picks('assembly')
# Real mouse hover/click at a known interior, after fitting the selected electorate.
selected=results['keyboardSelection']['selected'];point=next(f['point'] for f in fixtures if f['expected']==selected and f['case'].endswith('interior'))
ev('document.querySelector(".vic-map-stage").scrollIntoView({block:"center"})')
xy=ev('(()=>{const p=P4A_VIC_MAP.screenPoint(...'+json.dumps(point)+');const r=document.querySelector("[data-map-interaction]").getBoundingClientRect();return {x:p[0]+r.left,y:p[1]+r.top}})()')
c.call('Input.dispatchMouseEvent',{'type':'mouseMoved',**xy});c.wait('P4A_VIC_MAP.getState().hovered==='+json.dumps(selected))
results['realMouseHover']=True
c.call('Input.dispatchMouseEvent',{'type':'mousePressed','button':'left','clickCount':1,**xy});c.call('Input.dispatchMouseEvent',{'type':'mouseReleased','button':'left','clickCount':1,**xy})
assert ev('P4A_VIC_MAP.getState().selected')==selected
# Return to whole state, then fit a rural/island district for an additional pointer test.
ev('search.value="Bass";search.dispatchEvent(new Event("input"));document.querySelector("[data-electorate-list] button").click()')
time.sleep(.3);results['ruralSelected']=ev('document.querySelector("[data-electorate-profile] h2").textContent');assert results['ruralSelected']=='Bass'
results['ruralZoomPicking']=check_picks('assembly')
ev('document.querySelector("[data-map-reset]").click();search.value="";search.dispatchEvent(new Event("input"));window.scrollTo(0,0)');time.sleep(.4)
screenshot('victoria-desktop.png')
# Fit metropolitan district and include its detail panel in a second image.
ev('search.value="Brunswick";search.dispatchEvent(new Event("input"));document.querySelector("[data-electorate-list] button").click();window.scrollTo(0,450)');time.sleep(.3)
screenshot('victoria-selected.png')
# Device-pixel ratio, mobile layout and actual touch input.
c.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':2,'mobile':True});c.call('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5})
ev('document.querySelector("[data-map-reset]").click();window.scrollTo(0,0)');time.sleep(.4)
results['mobileNoOverflow']=ev('document.documentElement.scrollWidth<=window.innerWidth');assert results['mobileNoOverflow']
results['mobileDprPicking']=check_picks('assembly')
ev('search.value="Brunswick";search.dispatchEvent(new Event("input"));document.querySelector("[data-electorate-list] button").click();document.querySelector(".vic-map-stage").scrollIntoView({block:"center"})');time.sleep(.3)
xy=ev('(()=>{const p=P4A_VIC_MAP.screenPoint(...'+json.dumps(point)+');const r=document.querySelector("[data-map-interaction]").getBoundingClientRect();return {x:p[0]+r.left,y:p[1]+r.top}})()')
c.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[dict(xy,id=1)]});c.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});assert ev('P4A_VIC_MAP.getState().selected')==selected
before=ev('P4A_VIC_MAP.getState().transform.scale')
cx,cy=xy['x'],xy['y']
c.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx-20,'y':cy,'id':1},{'x':cx+20,'y':cy,'id':2}]})
c.call('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx-45,'y':cy,'id':1},{'x':cx+45,'y':cy,'id':2}]})
c.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
after=ev('P4A_VIC_MAP.getState().transform.scale');results['pinchZoom']=after>before;assert results['pinchZoom']
ev('document.querySelector("[data-map-reset]").click();window.scrollTo(0,0)');time.sleep(.4);screenshot('victoria-mobile.png')
results['touchSelection']=True
results['calendarDays']=ev('P4A_VIC_GEOMETRY.daysUntil("2026-11-28T08:00:00+11:00","2026-10-02T12:00:00+10:00")');assert results['calendarDays']==57
results['runtimeErrors']=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];assert not results['runtimeErrors']
(out/'browser-report.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
