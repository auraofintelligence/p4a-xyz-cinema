from cdp_client import CDP
import json,pathlib,time,base64
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');c.call('Network.setBlockedURLs',{'urls':[]});report=[]
c.call('Page.navigate',{'url':'about:blank'});c.wait("location.href==='about:blank' && document.readyState==='complete'");c.events=[]
def ev(s):return c.evaluate(s)
def navigate(url):
 ev('window.__qaOldDocument=true');c.call('Page.navigate',{'url':url});c.wait("!window.__qaOldDocument && document.readyState==='complete'");c.call('Page.resetNavigationHistory')
def wait(s):return c.wait(s)
fixtures=json.loads(pathlib.Path(__file__).resolve().parent.joinpath('first-peoples-fixtures.json').read_text())
for protocol,base in [('file',(pathlib.Path(__file__).resolve().parents[2]/'states/vic/map/index.html').as_uri()),('http','http://127.0.0.1:8766/states/vic/map/')]:
 for width in [1440,390]:
  print(protocol,width,flush=True);c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000 if width>500 else 844,'deviceScaleFactor':1 if width>500 else 2,'mobile':width<500});navigate(base+'?chamber=firstpeoples&recognition=rap,rsa&qa='+str(width))
  wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count===16')
  assert ev('document.documentElement.scrollWidth<=innerWidth+1')
  failures=ev('('+json.dumps(fixtures)+').filter(f=>JSON.stringify(P4A_VIC_MAP.pickAllLonLat(...f.point).sort())!==JSON.stringify(f.matches))');assert not failures,failures
  for rec in ev('P4A_VIC_ELECTORATES.firstpeoples'):
   ev('document.querySelector(\'[data-electorate="'+rec['id']+'"]\').click()');assert rec['fullName'] == ev("document.querySelector('[data-electorate-profile] h2').textContent"),rec['id']
  # Every intersecting source record is offered by a real canvas click.
  overlap=next(f for f in fixtures if len(f['matches'])>1)
  ev("document.querySelector('[data-map-reset]').click()");time.sleep(.4)
  coords=ev('(()=>{document.querySelector(".vic-map-stage").scrollIntoView({behavior:"instant"});const p=P4A_VIC_MAP.screenPoint(...'+json.dumps(overlap['point'])+'),r=document.querySelector("[data-map-interaction]").getBoundingClientRect();return [r.left+p[0],r.top+p[1]];})()')
  c.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':coords[0],'y':coords[1]});c.call('Input.dispatchMouseEvent',{'type':'mousePressed','button':'left','clickCount':1,'x':coords[0],'y':coords[1]});c.call('Input.dispatchMouseEvent',{'type':'mouseReleased','button':'left','clickCount':1,'x':coords[0],'y':coords[1]});wait('P4A_VIC_MAP.getState().pickedMatches.length>1');assert sorted(ev('P4A_VIC_MAP.getState().pickedMatches'))==overlap['matches']
  ev("document.querySelector('[data-electorate-profile] button').click()");saved=ev('location.href');assert 'matches=' in saved
  # Independent layer controls, including the empty selection.
  ev("document.querySelector('[data-recognition-layer=rap]').click()");wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count===4')
  ev("document.querySelector('[data-recognition-layer=rsa]').click()");wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().count===0');assert 'does not mean no Country' in ev("document.querySelector('[data-electorate-profile]').textContent")
  navigate(saved);wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().pickedMatches.length>1')
  # All physical positions and profile identifiers join without invented seats.
  for chamber,total in [('assembly',88),('council',40)]:
   ev("document.querySelector('[data-parliament-chamber]').value="+json.dumps(chamber)+";document.querySelector('[data-parliament-chamber]').dispatchEvent(new Event('change'))")
   assert ev("document.querySelectorAll('.vic-physical-seat').length")==total
   assert ev('(()=>{const room=P4A_VIC_SEATING['+json.dumps(chamber)+'],box=document.querySelector(".vic-physical-room").getBoundingClientRect();return room.seats.every(s=>{const r=document.querySelector("[data-seat="+s.id+"]").getBoundingClientRect();return Math.abs((r.left+r.width/2-box.left)/box.width-(s.x-room.viewBox[0])/room.viewBox[2])<.0001&&Math.abs((r.top+r.height/2-box.top)/box.height-(s.y-room.viewBox[1])/room.viewBox[3])<.0001})})()')
   ev("document.querySelector('.vic-physical-seat[data-person]:not([data-person=\"\"])').click()");assert ev('document.querySelector("dialog").open');assert 'Official information' in ev('document.querySelector("dialog").textContent');ev("document.querySelector('.vic-dialog-close').click()")
  # Representative detail and UI-only history do not change the map transform.
  ev("document.querySelector('[data-map-layer=lga]').click()");wait('P4A_VIC_MAP.getState().layerReady && P4A_VIC_MAP.getState().layer==="lga"')
  ev("document.querySelector('[data-electorate=vic-lga-339]').click();document.querySelector('[data-profile-tab=representatives]').click()")
  wait("!!document.querySelector('[data-electorate-profile] [data-person]')")
  before=ev('P4A_VIC_MAP.getState()');ev("document.querySelector('[data-electorate-profile] [data-person]').click()");person=ev("new URLSearchParams(location.search).get('person')");assert person and ev('document.querySelector("dialog").open'),'open dialog';assert ev('P4A_VIC_MAP.getState().transform')==before['transform'],('open transform',before,ev('P4A_VIC_MAP.getState()'));ev('history.back()');wait('!document.querySelector("dialog").open');assert ev('P4A_VIC_MAP.getState().selected')==before['selected'],('back selection',before,ev('P4A_VIC_MAP.getState()'));assert ev('P4A_VIC_MAP.getState().transform')==before['transform'],('back transform',before,ev('P4A_VIC_MAP.getState()'));ev('history.forward()');wait('document.querySelector("dialog").open');ev("document.querySelector('.vic-dialog-close').click()")
  # Every member and councillor has a usable dialog, including the administrators.
  checked=ev('(()=>{const errors=[];for(const p of P4A_VIC_PEOPLE.people){P4A_VIC_DETAILS.openPerson(p.id,false);if(document.getElementById("vic-person-title").textContent!==p.name||!document.querySelector("dialog [data-person-area]"))errors.push(p.id);}document.querySelector("dialog").close();return errors;})()');assert not checked,checked
  for m in ['election','governance']:
   ev("document.querySelector('[data-workbench-mode]').value="+json.dumps(m)+";document.querySelector('[data-workbench-mode]').dispatchEvent(new Event('change'))");assert ev('document.querySelector("[role=tab][aria-selected=true]").dataset.profileTab')==('election' if m=='election' else 'representatives')
  assert ev("P4A_VIC_DETAILS.suggestedMode('2026-10-02')==='election' && P4A_VIC_DETAILS.suggestedMode('2027-02-01')==='governance'")
  assert ev('document.documentElement.scrollWidth<=innerWidth+1')
  report.append({'protocol':protocol,'width':width,'recognitionInteriorAndOverlapFixtures':len(fixtures),'allRecognitionProfiles':16,'layerToggleEmptyAndPermalink':True,'physicalSeats':128,'deepPeopleProfiles':769,'uiHistoryPreservesMap':True,'seasonalModes':True,'noDocumentOverflow':True})
errors=[x for x in c.events if x.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
pathlib.Path(__file__).resolve().parent.joinpath('expanded-browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
# Local-only visual QA. No screenshots are attached or uploaded.
c.call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1100,'deviceScaleFactor':1,'mobile':False});ev("document.querySelector('[data-parliament-chamber]').value='assembly';document.querySelector('[data-parliament-chamber]').dispatchEvent(new Event('change'));document.querySelector('.vic-room-scroll').scrollIntoView({behavior:'instant'})");time.sleep(.3)
pathlib.Path(__file__).resolve().parent.joinpath('physical-seating-desktop.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
