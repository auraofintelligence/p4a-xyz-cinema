import sys,os
from pathlib import Path
CHECK_DIR=Path(sys.argv[1] if len(sys.argv)>1 else "qa").resolve();CHECK_DIR.mkdir(parents=True,exist_ok=True)
from cdp_client import CDP
import pathlib,json,time,statistics
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');c.call('Network.setCacheDisabled',{'cacheDisabled':True});out=CHECK_DIR;report={}
def ev(s):return c.evaluate(s)
def load(chamber='assembly',ident=None):
 url='http://127.0.0.1:8765/states/vic/map/?chamber='+chamber
 if ident:url+='&electorate='+ident
 c.call('Page.navigate',{'url':url});c.wait(f'window.P4A_VIC_MAP && P4A_VIC_MAP.getState().count==={88 if chamber=="assembly" else 8}')
 if ident:c.wait('P4A_VIC_MAP.getState().selected==='+json.dumps(ident))
c.call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1100,'deviceScaleFactor':1,'mobile':False});load()
report['allAssemblyProfiles']=ev('(()=>{const errors=[];for(const r of P4A_VIC_ELECTORATES.assembly){document.querySelector(`[data-electorate="${r.id}"]`).click();const p=document.querySelector("[data-electorate-profile]");if(p.querySelectorAll("[data-facts]").length!==1||p.querySelectorAll(".vic-census-metrics dd").length!==7||!p.querySelector(".vic-result-table"))errors.push(r.id);}return {checked:88,errors}})()');assert not report['allAssemblyProfiles']['errors']
ev('document.querySelector("[data-map-layer=council]").click()');c.wait('P4A_VIC_MAP.getState().count===8')
report['allCouncilProfiles']=ev('(()=>{const errors=[];for(const r of P4A_VIC_ELECTORATES.council){document.querySelector(`[data-electorate="${r.id}"]`).click();const p=document.querySelector("[data-electorate-profile]");if(p.querySelectorAll("[data-census-district]").length!==11||p.querySelectorAll(".vic-census-metrics").length!==0||!p.textContent.includes("does not publish Council-region"))errors.push(r.id);}return {checked:8,errors}})()');assert not report['allCouncilProfiles']['errors']
for ident,date in [('vic-assembly-57','28 January 2023'),('vic-assembly-55','18 November 2023'),('vic-assembly-60','02 May 2026')]:
 load('assembly',ident);text=ev('document.querySelector("[data-electorate-profile]").textContent');assert date.lstrip('0') in text,(ident,date)
report['specialElectionDates']=True
load();ev('document.querySelector("[data-electorate=vic-assembly-1]").click();document.querySelector("[data-electorate=vic-assembly-3]").click()')
ev('history.back()');c.wait('P4A_VIC_MAP.getState().selected==="vic-assembly-1"')
ev('history.forward()');c.wait('P4A_VIC_MAP.getState().selected==="vic-assembly-3"')
ev('document.querySelector("[data-related-region]").click()');c.wait('P4A_VIC_MAP.getState().layer==="council" && P4A_VIC_MAP.getState().selected==="vic-council-1"')
ev('document.querySelector("[data-electorate-profile] [data-census-district]").click()');c.wait('P4A_VIC_MAP.getState().layer==="assembly" && P4A_VIC_MAP.getState().selected')
ev('history.back()');c.wait('P4A_VIC_MAP.getState().selected==="vic-council-1"');report['backForwardAndCrossChamber']=True
link=ev('Array.from(document.querySelectorAll("[data-electorate-profile] a")).find(a=>a.textContent.includes("Permanent link")).href')
c.call('Page.navigate',{'url':link});c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().selected==="vic-council-1"');report['regionPermalinkReload']=True
c.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':2,'mobile':True});time.sleep(.2)
report['mobileCouncilNoOverflow']=ev('document.documentElement.scrollWidth<=window.innerWidth');assert report['mobileCouncilNoOverflow']
load('assembly','vic-assembly-57');report['mobileDistrictNoOverflow']=ev('document.documentElement.scrollWidth<=window.innerWidth');assert report['mobileDistrictNoOverflow']
fixtures=json.loads((out/'vic-picking-fixtures.json').read_text());report['compressedPicking']={}
for layer in ['assembly','council']:
 load(layer);points=[f for f in fixtures if f['layer']==layer]
 bad=ev('('+json.dumps(points)+').filter(f=>P4A_VIC_MAP.pickLonLat(...f.point)!==f.expected)');assert not bad,bad
 report['compressedPicking'][layer]=len(points)
load();samples=[]
for i in range(12):
 samples.append(ev('new Promise(resolve=>{const start=performance.now();document.querySelector("[data-map-zoom-'+('in' if i%2==0 else 'out')+']").click();requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(performance.now()-start)));})'))
report['zoomPaintMs']={'median':statistics.median(samples),'max':max(samples),'samples':len(samples),'condition':'Headless Edge, hardware acceleration disabled, full-resolution statewide geometry'}
c.call('Network.setBlockedURLs',{'urls':['*.vic.gz']});load();report['rawFallback']=ev('P4A_VIC_MAP.getState().count')==88
c.call('Network.setBlockedURLs',{'urls':['*.vic.gz','*.geojson']});c.call('Page.navigate',{'url':'http://127.0.0.1:8765/states/vic/map/?blocked=all'});c.wait('document.querySelector("[data-map-message]")?.textContent.includes("could not load")')
ev('document.querySelector("[data-electorate=vic-assembly-1]").click()');report['numericFactsWithoutGeometry']=ev('document.querySelector("[data-electorate-profile]").textContent.includes("74,022")');assert report['numericFactsWithoutGeometry']
c.call('Network.setBlockedURLs',{'urls':[]});c.call('Emulation.setScriptExecutionDisabled',{'value':True});c.call('Page.navigate',{'url':'http://127.0.0.1:8765/states/vic/map/?nojs=1'});time.sleep(.4)
report['noJsNumericalRecords']=ev('document.querySelectorAll(".vic-record [data-facts]").length');assert report['noJsNumericalRecords']==96
c.call('Emulation.setScriptExecutionDisabled',{'value':False})
report['runtimeExceptions']=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];assert not report['runtimeExceptions']
(out/'numeric-browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
