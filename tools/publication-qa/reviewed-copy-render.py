"""Exercise expanded preserved seeds and capture representative approved copy."""
from pathlib import Path
import base64,json,sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/vic-qa'))
from cdp_client import CDP
seeds=json.loads((R/'content/twinkle-earlier-seeds.json').read_text(encoding='utf-8'))
rooms=sorted({x['destination'] for x in seeds})
twinkles=['twinkle-power.html','twinkle-gender-pay-gap.html','twinkle-ancient-aliens.html','twinkle-family-violence.html','twinkle-super-investments.html']
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[]
for width in (1440,390):
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':900,'deviceScaleFactor':1,'mobile':width<500})
 for name in rooms+twinkles:
  c.evaluate('window.__previousCopy=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/pages/'+name})
  c.wait("!window.__previousCopy&&document.readyState==='complete'&&!!document.querySelector('.footer-index')")
  c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'));document.querySelectorAll('#earlier-twinkle-seeds details').forEach(e=>e.open=true)")
  result=c.evaluate("(()=>{let y=[...document.querySelector('.footer-index').children].map(e=>e.getBoundingClientRect().top);let h=document.querySelector('.hero-content');return {overflow:document.documentElement.scrollWidth>innerWidth,footerAligned:innerWidth<500||Math.max(...y)-Math.min(...y)<2,expandedSeeds:document.querySelectorAll('#earlier-twinkle-seeds details[open]').length,heroOverflow:h.scrollHeight>h.clientHeight+2}})()")
  assert not result['overflow'] and result['footerAligned'] and not result['heroOverflow'],[name,width,result]
  if name in rooms:assert result['expandedSeeds']==sum(x['destination']==name for x in seeds),name
  runs.append({'page':name,'width':width,**result})
  if name in ['twinkle-power.html','twinkle-ancient-aliens.html','public-assets.html']:
   if name=='public-assets.html':c.evaluate("document.querySelector('#earlier-twinkle-seeds').scrollIntoView({behavior:'instant'})")
   c.evaluate('new Promise(r=>setTimeout(r,1000))')
   (R/'tools/publication-qa'/('reviewed-'+Path(name).stem+'-'+str(width)+'.png')).write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
(R/'tools/publication-qa/reviewed-copy-render-report.json').write_text(json.dumps({'checked':'2026-10-03','browserRuns':runs},indent=2)+'\n',encoding='utf-8')
print('PASS',len(runs),'HTTP desktop/mobile cases with all preserved seed details expanded')
