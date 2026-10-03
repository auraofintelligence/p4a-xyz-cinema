import sys,os
from pathlib import Path
CHECK_DIR=Path(sys.argv[1] if len(sys.argv)>1 else "qa").resolve();CHECK_DIR.mkdir(parents=True,exist_ok=True)
from cdp_client import CDP
import json,pathlib
c=CDP();c.call('Page.enable');c.call('Runtime.enable');report={}
def ev(s):return c.evaluate(s)
for protocol in ['file','http']:
 url='file:///G:/GithubLocal-PC/p4a-xyz-cinema/states/vic/map/index.html' if protocol=='file' else 'http://127.0.0.1:8765/states/vic/map/'
 c.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':2,'mobile':True})
 c.call('Page.navigate',{'url':url});c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().count===88')
 result=ev('''(()=>{const results={sorts:[]};const field=document.querySelector('[data-electorate-sort]'),order=document.querySelector('[data-electorate-order]');for(const key of ['name','population','areaKm2','medianAge','medianWeeklyRent','medianWeeklyHouseholdIncome'])for(const direction of ['asc','desc']){field.value=key;order.value=direction;field.dispatchEvent(new Event('change'));const actual=[...document.querySelectorAll('[data-electorate-list] button')].map(b=>b.dataset.electorate);const expected=[...P4A_VIC_ELECTORATES.assembly].sort((a,b)=>key==='name'?(direction==='asc'?1:-1)*a.name.localeCompare(b.name,'en-AU'):(direction==='asc'?1:-1)*(a.sortMetrics[key]-b.sortMetrics[key])||a.name.localeCompare(b.name,'en-AU')).map(r=>r.id);if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error(key+direction);results.sorts.push(key+':'+direction);if(key!=='name'&&document.querySelectorAll('.vic-list-metric').length!==88)throw Error('Missing metric');}const a={name:'Alpha',sortMetrics:{population:5}},b={name:'Beta',sortMetrics:{population:5}},missing={name:'Aardvark',sortMetrics:{}};for(const dir of ['asc','desc'])if(P4A_VIC_MAP.compareRecords(a,b,'population',dir)>=0||P4A_VIC_MAP.compareRecords(missing,a,'population',dir)<=0)throw Error('Tie/missing handling');results.missingLastAndAlphabeticalTies=true;results.assemblySeats=document.querySelectorAll('.vic-seat').length;results.vacancies=document.querySelectorAll('.vic-seat[data-party="Vacant"]').length;results.alpSeats=document.querySelectorAll('.vic-seat[data-party="Australian Labor Party"]').length;results.fullHouseMarker=document.querySelector('[data-majority-label]').textContent;results.noOverflow=document.documentElement.scrollWidth<=innerWidth;return results;})()''')
 assert result['assemblySeats']==88 and result['vacancies']==1 and result['alpSeats']==54 and result['noOverflow'] and '45 of 88' in result['fullHouseMarker'],result
 ev("document.querySelector('[data-map-colours]').value='party';document.querySelector('[data-map-colours]').dispatchEvent(new Event('change'))")
 assert ev("P4A_VIC_MAP.getState().colourMode==='party' && document.querySelector('[data-colour-legend]').textContent.includes('Vacant')")
 ev("document.querySelector('.vic-seat').focus()")
 c.call('Input.dispatchKeyEvent',{'type':'keyDown','key':'ArrowRight','code':'ArrowRight'});c.call('Input.dispatchKeyEvent',{'type':'keyUp','key':'ArrowRight','code':'ArrowRight'})
 assert ev("document.activeElement===document.querySelectorAll('.vic-seat')[1] && document.querySelector('[data-seat-detail]').textContent.includes(document.activeElement.getAttribute('aria-label').split(';')[0])")
 ev("document.querySelector('[data-map-layer=council]').click();document.querySelector('[data-parliament-chamber]').value='council';document.querySelector('[data-parliament-chamber]').dispatchEvent(new Event('change'))")
 c.wait('P4A_VIC_MAP.getState().count===8')
 result['council']=ev('''(()=>{const select=document.querySelector('[data-electorate-sort]');return {seats:document.querySelectorAll('.vic-seat').length,alp:document.querySelectorAll('.vic-seat[data-party="Australian Labor Party"]').length,regionCards:document.querySelectorAll('.vic-region-composition').length,badges:document.querySelectorAll('.vic-region-composition .vic-party-swatch').length,compositionVisible:!document.querySelector('[data-region-composition-wrap]').hidden,disabled:[...select.options].filter(o=>o.disabled).map(o=>o.value),marker:document.querySelector('[data-majority-label]').textContent,noOverflow:document.documentElement.scrollWidth<=innerWidth};})()''')
 assert result['council']['seats']==40 and result['council']['alp']==15 and result['council']['badges']==40 and result['council']['regionCards']==8 and result['council']['compositionVisible'] and result['council']['noOverflow'] and '21 of 40' in result['council']['marker'],result
 assert set(result['council']['disabled'])=={'medianAge','medianWeeklyRent','medianWeeklyHouseholdIncome'}
 report[protocol]=result
report['exceptions']=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];assert not report['exceptions']
(CHECK_DIR/'representation-sort-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
