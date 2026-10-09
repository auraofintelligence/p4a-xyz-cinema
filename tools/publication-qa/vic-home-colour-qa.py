"""Verify the homepage Victoria card's narrow colour correction."""
from pathlib import Path
import sys,json,base64,subprocess
R=Path(__file__).resolve().parents[2]
assert not subprocess.check_output(['git','diff','--','index.html','assets/vic-home-card.js'],cwd=R)
sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.enable');runs=[];out=R/'tools/publication-qa/vic-home-colour-screenshots';out.mkdir(exist_ok=True)
def lum(col):
 rgb=[int(col[i:i+2],16)/255 for i in [1,3,5]]
 rgb=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
 return sum(x*y for x,y in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
 x,y=sorted([lum(a),lum(b)]);return round((y+.05)/(x+.05),2)
ratios={bg:contrast('#fff5ff',bg) for bg in ['#3b1d62','#190d29']};assert min(ratios.values())>=7
for w,h in [(1665,983),(390,950)]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':w<500})
 c.evaluate('window.__oldVicColour=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/index.html'});c.wait("!window.__oldVicColour&&document.readyState==='complete'&&!!document.querySelector('[data-vic-home-value]')")
 c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelector('[data-vic-home-card]').scrollIntoView({behavior:'instant'});window.scrollBy(0,-80)")
 c.evaluate('new Promise(r=>setTimeout(r,250))')
 result=c.evaluate("(()=>{let card=document.querySelector('.vic-home-card'),value=card.querySelector('[data-vic-home-value]');return {heading:getComputedStyle(card.querySelector('h2')).color,countdown:getComputedStyle(value).color,value:value.textContent,label:card.querySelector('[data-vic-home-label]').textContent,overflow:document.documentElement.scrollWidth>innerWidth+2,clippedActions:[...card.querySelectorAll('a')].filter(e=>e.clientWidth&&e.scrollWidth>e.clientWidth+2).map(e=>e.textContent)}})()")
 assert result['heading']==result['countdown']=='rgb(255, 245, 255)' and not result['overflow'] and not result['clippedActions'],result
 assert result['value'].strip() and result['label'].strip()
 (out/f'card-{w}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']));runs.append({'width':w,**result})
(R/'tools/publication-qa/vic-home-colour-report.json').write_text(json.dumps({'checks':runs,'whiteTextContrast':ratios,'backgroundCheck':'Gradient endpoints and conservative purple-overlay blend; countdown inset is darker.','markupAndCountdownScriptUnchanged':True},indent=2)+'\n',encoding='utf-8')
print('PASS Victoria heading/countdown colours, contrast, desktop/mobile layout; unchanged markup and behaviour script')
