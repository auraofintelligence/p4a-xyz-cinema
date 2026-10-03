from cdp_client import CDP
import pathlib,json,time
c=CDP();c.call('Page.enable');c.call('Runtime.enable');points=json.loads(pathlib.Path('qa/council-picking-fixtures.json').read_text());report={}
for layer,count in [('lga',87),('ward',467)]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1100,'deviceScaleFactor':1,'mobile':False});c.call('Page.navigate',{'url':'file:///G:/GithubLocal-PC/p4a-xyz-cinema/states/vic/map/index.html?chamber='+layer});c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().count==='+str(count),seconds=75)
 fixtures=[f for f in points if f['layer']==layer]
 bad=c.evaluate('('+json.dumps(fixtures)+').filter(f=>P4A_VIC_MAP.pickLonLat(...f.point)!==f.expected)');assert not bad,(layer,bad)
 report[layer]={'statewidePicking':len(fixtures)}
 c.call('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5});c.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':2,'mobile':True});c.evaluate("document.querySelector('[data-map-reset]').click()");time.sleep(.6)
 bad=c.evaluate('('+json.dumps(fixtures)+').filter(f=>P4A_VIC_MAP.pickLonLat(...f.point)!==f.expected)');assert not bad,(layer,bad);report[layer]['mobileDpr2Picking']=len(fixtures)
 # Real input at an independently generated feature-interior point.
 f=next(f for f in fixtures if f['kind']=='interior');c.evaluate('document.querySelector(\'[data-electorate="'+f['expected']+'"]\').click();document.querySelector(".vic-map-stage").scrollIntoView({block:"center",behavior:"instant"})');c.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))')
 xy=c.evaluate('(()=>{const p=P4A_VIC_MAP.screenPoint(...'+json.dumps(f['point'])+');const r=document.querySelector("[data-map-interaction]").getBoundingClientRect();return {x:p[0]+r.left,y:p[1]+r.top}})()')
 before=c.evaluate('P4A_VIC_MAP.getState()');c.call('Input.dispatchMouseEvent',{'type':'mouseMoved',**xy});after=c.evaluate('P4A_VIC_MAP.getState()');assert after['hovered']==f['expected'],{'layer':layer,'fixture':f,'xy':xy,'before':before,'after':after,'viewport':c.evaluate('({width:innerWidth,height:innerHeight,scale:visualViewport.scale,scroll:scrollY,target:document.elementFromPoint('+str(xy['x'])+','+str(xy['y'])+')?.outerHTML.slice(0,120)})')};report[layer]['realHover']=True
 before=c.evaluate('P4A_VIC_MAP.getState()');c.call('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[dict(xy,id=1)]});c.call('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});after=c.evaluate('P4A_VIC_MAP.getState()');assert after['selected']==f['expected'],{'layer':layer,'fixture':f,'xy':xy,'before':before,'after':after,'viewport':c.evaluate('({width:innerWidth,height:innerHeight,scale:visualViewport.scale,scroll:scrollY})')};report[layer]['realTouch']=True
 c.call('Emulation.setTouchEmulationEnabled',{'enabled':False})
report['exceptions']=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];assert not report['exceptions']
pathlib.Path('qa/council-picking-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
