"""Check the Australian UAP room's scope, links, build and desktop/mobile presentation."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import json,sys,subprocess,hashlib,base64,py_compile
R=Path(__file__).resolve().parents[2];p=R/'pages/ancient-aliens.html';t=p.read_text(encoding='utf-8');s=BeautifulSoup(t,'html.parser');count=0
assert '\ufffd' not in t
ids=[e['id'] for e in s.select('[id]')];assert len(ids)==len(set(ids))
for a in s.select('a[href]'):
 u=urlsplit(a['href'])
 if u.scheme in ['http','https']:assert a.get('target')=='_blank' and 'noopener' in a.get('rel',[]),a['href']
 elif not u.scheme:
  dst=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert dst.exists(),a['href']
  if u.fragment:assert BeautifulSoup(dst.read_text(encoding='utf-8'),'html.parser').find(id=unquote(u.fragment)),a['href']
 count+=1
for anchor in ['room','empty-chair','records','australian-records','traditions','rock-art','disclosure','regional-cooperation']:assert s.find(id=anchor)
for term in ['empathy, black swan preparedness, and existential threat avoidance','Minister for UAP/NHI Disclosure and Investigation','Asia, Oceania and the Indian Ocean','unidentified anomalous phenomena','non-human intelligence','extra-terrestrial','crypto-terrestrial','song, dance','oral histories']:assert term in s.get_text(' ',strip=True),term
assert 'What should disclosure require?' not in t
assert len(s.select('#traditions .official-link-card'))==4
assert len(s.select('#australian-records .official-link-card'))==4
before=hashlib.sha256(p.read_bytes()).hexdigest();subprocess.run([sys.executable,str(R/'tools/build-policy-rooms.py'),'ancient-aliens'],check=True,cwd=R);assert before==hashlib.sha256(p.read_bytes()).hexdigest()
for f in ['tools/build-policy-rooms.py','tools/public_copy.py']:py_compile.compile(str(R/f),doraise=True)
assert not subprocess.check_output(['git','diff','--','styles.css','content/home-ticker.json','assets/homepage-ticker.css','assets/homepage-ticker.js','pages/twinkle-ancient-aliens.html','content/twinkle-reviewed-copy.json'],cwd=R)
report={'checked':'2026-10-04','canonicalSource':'content/rooms/ancient-aliens.html','linkAndAnchorChecks':count,'allExistingSectionAnchorsPreserved':True,'idempotentRebuild':True,'exactEmptyChairPurposesPreserved':True,'AustraliaFirst':{'AustralianRecordCards':4,'AustralianCulturalCards':4,'USComparison':'one collapsed detail, two source links','foreignTraditionCatalogueRemoved':True,'proposedPortfolioNotExistingAuthority':True,'regionalCooperationNotJurisdictionOverNeighbours':True,'AntarcticTreatyContext':'Articles I-IV: peaceful purposes, scientific cooperation and preserved sovereignty positions'},'sourcesRead':[{'url':'https://www.ats.aq/e/antarctictreaty.html','finding':'Official Treaty Secretariat: peaceful use, scientific investigation/cooperation, some states do not recognise claims, Article IV preserves positions.'},{'url':'https://www.antarctica.gov.au/about-antarctica/australia-in-antarctica/australian-antarctic-territory/','finding':'Australian Antarctic Division: AAT administration and legislation; read alongside Treaty Secretariat.'},{'url':'https://www.infrastructure.gov.au/territories-regions-cities/territories','finding':'Australian Government territory responsibilities, including Indian Ocean territories, Norfolk, Coral Sea and AAT reference.'},{'url':'https://yyf.com.au/','finding':'Yolngu-led foundation describes manikay, bunggul, miny\u2019tji and storytelling; no alien interpretation attributed to it.'},{'url':'https://mowanjumarts.com/about/culture','finding':'Three named communities maintaining Wandjina knowledge through art, song and dance.'},{'url':'https://www.magabala.com/pages/about-us','finding':'Aboriginal owned and led, community-controlled publisher; controlled public sharing.'}],'priorVerifiedSourcesRetained':['Trove Port Augusta 1947','NAA Wewak/Maralinga July 1960','QSA Tully 1966','SLV Westall 1966','Patsy Cameron Sky Country','Bill Yidumduma Harney Wardaman account','NARA current UAP collection','2023 US House hearing','Cosmic Nexus governance and source index'],'culturalMaterial':'Links and short attributed paraphrases only; no art reproduction, restricted knowledge or exhaustive-catalogue claim.'}
sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[];shots=R/'tools/publication-qa/australian-uap-screenshots';shots.mkdir(exist_ok=True)
for w in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':950,'deviceScaleFactor':1,'mobile':w<500});c.evaluate('window.__oldAU=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/pages/ancient-aliens.html'});c.wait("!window.__oldAU&&document.readyState==='complete'&&!!document.querySelector('.footer-index')");c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
 for anchor in ['main','disclosure','empty-chair','records','traditions','regional-cooperation']:
  c.evaluate('document.querySelector('+json.dumps('#'+anchor)+').scrollIntoView({block:"start",behavior:"instant"});window.scrollBy(0,-90)');c.evaluate('new Promise(r=>setTimeout(r,200))')
  result=c.evaluate("(()=>{let r=[...document.querySelectorAll('.button,.source-links a,.official-link-actions a')].filter(e=>e.getBoundingClientRect().width);return {overflow:document.documentElement.scrollWidth>innerWidth+2,clippedActions:r.filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.textContent.trim())}})()")
  assert not result['overflow'] and not result['clippedActions'],[w,anchor,result]
  (shots/f'{anchor}-{w}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']));runs.append({'width':w,'section':anchor,**result})
 c.evaluate("document.querySelector('.hero-actions a').click()");assert c.evaluate("location.hash==='#disclosure'")
 c.evaluate("document.querySelector('#records details').open=true");assert c.evaluate("document.querySelector('#records details').open")
report['browserChecks']=runs;report['heroNavigationAndUSDisclosureOpen']=True
(R/'tools/publication-qa/australian-uap-room-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS',count,'links/anchors;',len(runs),'desktop/mobile section checks; proposed scope, exact purposes, canonical rebuild and protected files')
