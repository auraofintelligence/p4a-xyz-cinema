from cdp_client import CDP
import json,pathlib,time,base64
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');c.call('Network.setBlockedURLs',{'urls':[]})
c.call('Page.navigate',{'url':'about:blank'});c.wait("location.href==='about:blank' && document.readyState==='complete'");c.events=[]
def ev(s):return c.evaluate(s)
def navigate(url):
 ev('window.__qaOldDocument=true');c.call('Page.navigate',{'url':url});c.wait("!window.__qaOldDocument && document.readyState==='complete'");c.call('Page.resetNavigationHistory')
def screenshot(name):pathlib.Path(__file__).resolve().parent.joinpath(''+name+'.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
checks=[]
for width in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1100 if width>500 else 844,'deviceScaleFactor':1,'mobile':width<500});navigate((pathlib.Path(__file__).resolve().parents[2]/'states/vic/map/index.html').as_uri()+'?chamber=lga&electorate=vic-lga-339&mode=governance&section=area&visual='+str(width));c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && !!document.querySelector("#vic-tab-area")')
 ev("document.querySelector('[data-electorate-profile]').scrollIntoView({behavior:'instant'})");time.sleep(.4);screenshot('profile-'+str(width))
 contrast=ev('''(()=>{const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number),lum=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);const out=[];for(const n of document.querySelectorAll('[data-electorate-profile] h3,[data-electorate-profile] a,[aria-selected=true]')){if(!n.getClientRects().length)continue;let bg=[0,0,0,0],p=n;while(p&&(!bg.length||bg[3]===0)){bg=rgb(getComputedStyle(p).backgroundColor);p=p.parentElement;}const fg=rgb(getComputedStyle(n).color);const a=lum(fg),b=lum(bg);out.push({label:n.textContent.slice(0,60),foreground:fg,background:bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)});}return out;})()''')
 assert contrast and min(x['ratio'] for x in contrast)>=4.5,contrast
 ev("document.querySelector('[data-profile-tab=representatives]').click();document.querySelector('[data-electorate-profile] [data-person]').focus();document.querySelector('[data-electorate-profile] [data-person]').click()")
 c.wait('document.querySelector("dialog").open');screenshot('person-'+str(width));assert ev('document.querySelector("dialog").scrollWidth<=document.querySelector("dialog").clientWidth+1')
 ev("document.querySelector('.vic-dialog-close').click()");assert ev('document.activeElement.matches("[data-person]")')
 ev('history.back()');c.wait('document.querySelector("dialog").open');ev('history.back()');c.wait('!document.querySelector("dialog").open');assert ev('document.activeElement.matches("[data-person]")')
 # Direct representative URL opens a labelled modal without changing the selected council.
 u=ev('(()=>{const u=new URL(location.href);u.searchParams.set("person",P4A_VIC_PEOPLE.people.find(p=>p.areaId==="vic-lga-339").id);return u.href})()');navigate(u);c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && document.querySelector("dialog").open');assert ev('P4A_VIC_MAP.getState().selected')=='vic-lga-339';ev("document.querySelector('.vic-dialog-close').click()")
 for chamber in ['assembly','council']:
  ev("document.querySelector('[data-parliament-chamber]').value="+json.dumps(chamber)+";document.querySelector('[data-parliament-chamber]').dispatchEvent(new Event('change'));document.querySelector('.vic-room-scroll').scrollIntoView({behavior:'instant'})");time.sleep(.2);screenshot(chamber+'-seating-'+str(width))
  overlaps=ev('''(()=>{const seats=[...document.querySelectorAll('.vic-physical-seat')].map(n=>({id:n.dataset.seat,r:n.getBoundingClientRect()})),bad=[];for(let i=0;i<seats.length;i++)for(let j=i+1;j<seats.length;j++){const a=seats[i],b=seats[j];if(Math.min(a.r.right,b.r.right)-Math.max(a.r.left,b.r.left)>2&&Math.min(a.r.bottom,b.r.bottom)-Math.max(a.r.top,b.r.top)>2)bad.push([a.id,b.id]);}return bad;})()''');assert not overlaps,overlaps
 assert ev('document.documentElement.scrollWidth<=innerWidth+1')
 checks.append({'width':width,'goldContrastMinimum':min(x['ratio'] for x in contrast),'modalNoOverflow':True,'closeAndHistoryFocus':True,'personDeepLink':True,'physicalSeatButtonsDoNotOverlap':True})
print('Visual/accessibility',json.dumps(checks),flush=True)
# Cold mobile HTTP: measure the complete page and exact geometry, not cached assets.
c.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':2,'mobile':True});c.call('Network.setCacheDisabled',{'cacheDisabled':True});c.call('Network.emulateNetworkConditions',{'offline':False,'latency':80,'downloadThroughput':1250000,'uploadThroughput':1250000,'connectionType':'cellular4g'})
performance=[]
for layer in ['assembly','firstpeoples']:
 start=time.perf_counter();navigate('http://127.0.0.1:8766/states/vic/map/?chamber='+layer+'&recognition=rap,rsa&perf='+str(time.time()));c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().layer==='+json.dumps(layer),90)
 result=ev('({loadMs:performance.now(),navigation:performance.getEntriesByType("navigation").map(x=>({bytes:x.transferSize,duration:x.duration})),resources:performance.getEntriesByType("resource").map(r=>({url:r.name.split("/").pop(),bytes:r.transferSize,encoded:r.encodedBodySize,duration:r.duration}))})');result['wallSeconds']=time.perf_counter()-start;result['layer']=layer;result['pickerTiming']=ev('(()=>{const a=[];for(let i=0;i<100;i++){const t=performance.now();P4A_VIC_MAP.pickAllLonLat(144.95,-37.76);a.push(performance.now()-t);}a.sort((a,b)=>a-b);return {p50Ms:a[50],p95Ms:a[95],maxMs:a[99]}})()');result['totalTransferBytes']=sum(x['bytes'] for x in result['resources']+result['navigation']);performance.append(result);print('Performance',layer,result['wallSeconds'],result['totalTransferBytes'],flush=True)
c.call('Network.emulateNetworkConditions',{'offline':False,'latency':0,'downloadThroughput':-1,'uploadThroughput':-1});c.call('Network.setCacheDisabled',{'cacheDisabled':False})
errors=[x for x in c.events if x.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
pathlib.Path(__file__).resolve().parent.joinpath('visual-accessibility-report.json').write_text(json.dumps(checks,indent=2));pathlib.Path(__file__).resolve().parent.joinpath('performance-complete.json').write_text(json.dumps({'conditions':'Cold cache, mobile 390x844 DPR2, 10Mbps, 80ms latency; local Python HTTP server; isolated headless Edge with hardware acceleration disabled. Includes HTML transfer. Not a production or real-device benchmark.','results':performance},indent=2))
