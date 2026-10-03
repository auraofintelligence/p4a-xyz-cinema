from cdp_client import CDP
import pathlib,json,base64
pathlib.Path('qa').mkdir(exist_ok=True)
c=CDP();c.call('Page.enable');c.call('Runtime.enable');results=[]
for width in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000 if width>500 else 844,'deviceScaleFactor':1,'mobile':width<500});c.evaluate('window.__qaOldDocument=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8766/states/vic/election/index.html'});c.wait('!window.__qaOldDocument && document.readyState==="complete" && !!window.P4A_VIC_ELECTION')
 for part,selector in [('hero','.ve-hero'),('filters','.ve-filters'),('footer','.ve-footer')]:
  c.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"start",behavior:"instant"})');c.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');path=pathlib.Path('qa')/f'election-{part}-{width}.png';path.write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
  assert c.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 c.evaluate('document.querySelector("[data-candidate-search]").focus({preventScroll:true})')
 assert c.evaluate('getComputedStyle(document.activeElement).outlineStyle')!='none'
 colours=c.evaluate('({heading:getComputedStyle(document.querySelector(".ve-hero h1")).color,link:getComputedStyle(document.querySelector(".ve-candidate a")).color,footerLinks:document.querySelectorAll(".ve-footer nav a").length})')
 results.append(dict(width=width,focusVisible=True,noOverflow=True,**colours))
pathlib.Path('qa/election-visual-report.json').write_text(json.dumps(results,indent=2));print(results)
