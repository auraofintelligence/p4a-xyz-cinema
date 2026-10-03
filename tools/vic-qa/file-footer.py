import sys,os
from pathlib import Path
CHECK_DIR=Path(sys.argv[1] if len(sys.argv)>1 else "qa").resolve();CHECK_DIR.mkdir(parents=True,exist_ok=True)
from cdp_client import CDP
import json,pathlib,time
c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');report=[]
for protocol,url in [('file','file:///G:/GithubLocal-PC/p4a-xyz-cinema/states/vic/map/index.html'),('http','http://127.0.0.1:8765/states/vic/map/')]:
 for width,height in [(1440,1100),(390,844)]:
  c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':width<500});c.call('Page.navigate',{'url':url})
  c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().count===88')
  c.evaluate('document.querySelector("[data-electorate=vic-assembly-1]").click()')
  c.wait('P4A_VIC_MAP.getState().selected==="vic-assembly-1"')
  district=c.evaluate('({url:location.href,population:document.querySelector("[data-electorate-profile]").textContent.includes("74,022")})')
  c.evaluate('document.querySelector("[data-related-region]").click()');c.wait('P4A_VIC_MAP.getState().count===8 && P4A_VIC_MAP.getState().selected')
  footer=c.evaluate('(()=>{const f=document.querySelector(".vic-footer");const groups=[...f.querySelectorAll(".vic-footer-groups>section")];return {groups:groups.length,columns:new Set(groups.map(g=>Math.round(g.getBoundingClientRect().x))).size,height:Math.round(f.getBoundingClientRect().height),links:f.querySelectorAll("a").length,footerNavs:f.querySelectorAll(".footer-index").length,overflow:document.documentElement.scrollWidth>window.innerWidth}})()')
  assert footer['groups']==4 and footer['columns']==(4 if width>800 else 1 if width<=480 else 2) and footer['footerNavs']==1 and not footer['overflow'],footer
  assert district['population']
  report.append({'protocol':protocol,'width':width,'assembly':88,'council':8,'selectedPopulation':True,'footer':footer})
exceptions=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];assert not exceptions,exceptions
(CHECK_DIR/'file-footer-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
