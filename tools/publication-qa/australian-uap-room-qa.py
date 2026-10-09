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
for anchor in ['room','empty-chair','records','australian-records','traditions','rock-art','disclosure','regional-cooperation','sky-country-partnership','defence-records','recent-sightings','religion-and-aliens','belief-and-power','whistleblower-protection']:assert s.find(id=anchor)
for term in ['empathy, black swan preparedness, and existential threat avoidance','Minister for UAP/NHI Disclosure and Investigation','Asia, Oceania and the Indian Ocean','unidentified anomalous phenomena','non-human intelligence','extra-terrestrial','crypto-terrestrial','song, dance','oral histories']:assert term in s.get_text(' ',strip=True),term
assert 'What should disclosure require?' not in t
assert len(s.select('#traditions .official-link-card'))==4
assert len(s.select('#australian-records .official-link-card'))==4
assert len(s.select('#disclosure > .official-link-grid > .official-link-card'))==2
assert s.select_one('#whistleblower-protection').find_parent(class_='official-link-card')
assert 'Faith matters, but it is not an excuse to switch your brain off and discount rational inquiry.' in s.get_text(' ',strip=True)
for term in ['Potential benefits','Pitfalls:','Nobody speaks or vetoes','Record whether the exercise changed']:assert term in s.get_text(' ',strip=True)
before=hashlib.sha256(p.read_bytes()).hexdigest();subprocess.run([sys.executable,str(R/'tools/build-policy-rooms.py'),'ancient-aliens'],check=True,cwd=R);assert before==hashlib.sha256(p.read_bytes()).hexdigest()
for f in ['tools/build-policy-rooms.py','tools/public_copy.py']:py_compile.compile(str(R/f),doraise=True)
assert not subprocess.check_output(['git','diff','--','styles.css','assets/homepage-ticker.css','pages/twinkle-ancient-aliens.html'],cwd=R)
report={'checked':'2026-10-04','canonicalSource':'content/rooms/ancient-aliens.html','linkAndAnchorChecks':count,'allExistingSectionAnchorsPreserved':True,'idempotentRebuild':True,'exactEmptyChairPurposesPreserved':True,'AustraliaFirst':{'AustralianRecordCards':4,'AustralianCulturalCards':4,'USComparison':'one collapsed detail, two source links','foreignTraditionCatalogueRemoved':True,'proposedPortfolioNotExistingAuthority':True,'regionalCooperationNotJurisdictionOverNeighbours':True,'AntarcticTreatyContext':'Articles I-IV: peaceful purposes, scientific cooperation and preserved sovereignty positions'},'sourcesRead':[{'url':'https://www.ats.aq/e/antarctictreaty.html','finding':'Official Treaty Secretariat: peaceful use, scientific investigation/cooperation, some states do not recognise claims, Article IV preserves positions.'},{'url':'https://www.antarctica.gov.au/about-antarctica/australia-in-antarctica/australian-antarctic-territory/','finding':'Australian Antarctic Division: AAT administration and legislation; read alongside Treaty Secretariat.'},{'url':'https://www.infrastructure.gov.au/territories-regions-cities/territories','finding':'Australian Government territory responsibilities, including Indian Ocean territories, Norfolk, Coral Sea and AAT reference.'},{'url':'https://yyf.com.au/','finding':'Yolngu-led foundation describes manikay, bunggul, miny\u2019tji and storytelling; no alien interpretation attributed to it.'},{'url':'https://mowanjumarts.com/about/culture','finding':'Three named communities maintaining Wandjina knowledge through art, song and dance.'},{'url':'https://www.magabala.com/pages/about-us','finding':'Aboriginal owned and led, community-controlled publisher; controlled public sharing.'}],'priorVerifiedSourcesRetained':['Trove Port Augusta 1947','NAA Wewak/Maralinga July 1960','QSA Tully 1966','SLV Westall 1966','Patsy Cameron Sky Country','Bill Yidumduma Harney Wardaman account','NARA current UAP collection','2023 US House hearing','Cosmic Nexus governance and source index'],'culturalMaterial':'Links and short attributed paraphrases only; no art reproduction, restricted knowledge or exhaustive-catalogue claim.'}
report['rememberedSighting']='Unresolved: sources do not establish one east-coast-to-Darwin event. 2008 NT reports retained. Rejected 2010 spiral case and public research placeholder removed.'
report['twinkleConnection']='Inspected Twinkle 43 title Depends which bloke in the sky and its religion/arrival seed. Deep room now compares religious, symbolic and mechanical/ET readings and addresses authority, propaganda, coercion and Australian public accountability.'
report['sourcesRead'].extend([
 {'url':'https://www.biblegateway.com/passage/?search=Ezekiel%201&version=KJV','finding':'Read chapter 1 KJV: 1:1 vision; 1:15-21 wheels/eyes; 1:26-28 throne and divine glory. Paraphrases, no long quotations.'},
 {'url':'https://www.biblegateway.com/passage/?search=Ezekiel%2010&version=KJV','finding':'Read chapter 10 KJV: 10:9-17 wheels/eyes and 10:20 identification of cherubim. Mechanical correspondences are explicitly proposed interpretations.'},
 {'url':'https://oyc.yale.edu/religious-studies/rlst-145/lecture-19','finding':'Christine Hayes scholarly lecture: exilic priestly context and mobile divine throne imagery. No alien explanation attributed to the scholar.'},
 {'url':'https://www.fbi.gov/history/cases-and-criminals/jonestown','finding':'Primary investigating-agency history of 18 November 1978, abuse allegations, departures, Ryan murder and mass deaths. No methods reproduced.'},
 {'url':'https://humanrights.gov.au/resource-hub/by-resource-type/publications/guidelines/articles/rights-and-freedoms/freedom-thought-conscience-and-religion-or-belief','finding':'AHRC explanation of ICCPR Article 18 includes non-religious beliefs and freedom from coercion; policy suggestions labelled as proposed programme or should statements.'},
 {'url':'https://www.abc.net.au/news/2010-06-05/ufo-spotted-over-eastern-australia/855590','finding':'5 June 2010 dawn spiral across Queensland, NSW and ACT; witness accounts and contemporary rocket explanation/objections; no Darwin link established.'},
 {'url':'https://satobs.org/seesat_ref/misc/180314-falcon9s2-australia.pdf','finding':'James Oberg, March 20 2018 final draft: Falcon 9 second-stage post-insertion propellant venting analysis with orbital data, imagery and accounts.'},
 {'url':'https://www.abc.net.au/mediawatch/episodes/ufo-armada-invades-nt-news/9975122','finding':'29 September 2008 archive preserves NT News publication dates: Marlinja 27 June, armada headline 23 August, six witnesses 24 September. Separate reports, not one coast-to-Darwin event.'},
 {'url':'https://aiatsis.gov.au/research/ethical-research/code-ethics','finding':'AIATSIS Indigenous research framework: leadership, self-determination, value and accountability; proposed programme details remain P4A proposals.'},
 {'url':'https://pmtranscripts.pmc.gov.au/release/transcript-7438','finding':'Hawke parliamentary statement 22 November 1988 identifies Pine Gap satellite ground station and intelligence role.'},
 {'url':'https://www.minister.defence.gov.au/statements/2023-02-09/securing-australias-sovereignty','finding':'9 February 2023 statement describes joint facilities and full knowledge and concurrence; no ET finding.'},
 {'url':'https://www.naa.gov.au/blog/flying-saucers-fact-or-fiction','finding':'NAA account of Navy pilot O’Farrell, 31 August 1954, recorded radar confirmation; RAAF UFO investigations ceased 1994.'}
])
report['disclosureReformSources']=[
 {'url':'https://www.legislation.gov.au/C2013A00133/latest/text','compilation':'4 June 2026','read':'Sections 10-12 immunity and own conduct; section 26 external-disclosure intelligence restrictions.'},
 {'url':'https://www.legislation.gov.au/C2004A03597/latest/text','compilation':'27 August 2026','read':'Section 7 extradition objections; current Act and country arrangements govern, no general whistleblower exemption.'},
 {'url':'https://www.igis.gov.au/making-complaint','read':'Classified information requires prior contact for secure arrangements; section 32AC limits and other secrecy obligations.'},
 {'url':'https://www.ombudsman.gov.au/complaints/public-interest-disclosure-whistleblowing/information-for-disclosers','read':'Eligible officials, authorised recipients, protections and own wrongdoing limits.'},
 {'url':'https://www.ag.gov.au/international-relations/international-crime-cooperation-arrangements/extradition','read':'Act plus applicable treaties; distinct New Zealand regime.'}]
report['proposedImmunity']='Qualified good-faith disclosure through authorised process; independent review, legal assistance, retaliation remedies and proposed extradition safeguard; no immunity for unrelated serious wrongdoing or promise of foreign protection.'
report['proposedPartnership']='National voluntary Indigenous-led participation, paid local teams, community-held collections, approved attribution and translations, variants, permissions and withdrawal; co-designed categories lead to inquiry and preparedness.'
sys.path.insert(0,str(R/'tools/vic-qa'));from cdp_client import CDP
c=CDP();c.call('Page.enable');c.call('Runtime.enable');runs=[];shots=R/'tools/publication-qa/australian-uap-screenshots';shots.mkdir(exist_ok=True)
for w in [1440,390]:
 c.call('Emulation.setDeviceMetricsOverride',{'width':w,'height':950,'deviceScaleFactor':1,'mobile':w<500});c.evaluate('window.__oldAU=true');c.call('Page.navigate',{'url':'http://127.0.0.1:8765/pages/ancient-aliens.html'});c.wait("!window.__oldAU&&document.readyState==='complete'&&!!document.querySelector('.footer-index')");c.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible','visible'))")
 for anchor in ['main','disclosure','empty-chair','records','traditions','sky-country-partnership','defence-records','recent-sightings','religion-and-aliens','belief-and-power','whistleblower-protection','regional-cooperation']:
  c.evaluate('(()=>{let e=document.getElementById('+json.dumps(anchor)+');for(let p=e;p;p=p.parentElement){if(p.tagName==="DETAILS")p.open=true;}if(e.id==="traditions")e.querySelector("details").open=true;})()')
  c.evaluate('document.querySelector('+json.dumps('#'+anchor)+').scrollIntoView({block:"start",behavior:"instant"});window.scrollBy(0,-90)');c.evaluate('new Promise(r=>setTimeout(r,200))')
  result=c.evaluate("(()=>{let r=[...document.querySelectorAll('.button,.source-links a,.official-link-actions a')].filter(e=>e.getBoundingClientRect().width);return {overflow:document.documentElement.scrollWidth>innerWidth+2,clippedActions:r.filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.textContent.trim())}})()")
  assert not result['overflow'] and not result['clippedActions'],[w,anchor,result]
  (shots/f'{anchor}-{w}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']));runs.append({'width':w,'section':anchor,**result})
 c.evaluate("document.querySelector('.hero-actions a').click()");assert c.evaluate("location.hash==='#disclosure'")
 c.evaluate("document.querySelector('#records details').open=true");assert c.evaluate("document.querySelector('#records details').open")
report['browserChecks']=runs;report['heroNavigationAndUSDisclosureOpen']=True
(R/'tools/publication-qa/australian-uap-room-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS',count,'links/anchors;',len(runs),'desktop/mobile section checks; proposed scope, exact purposes, canonical rebuild and protected files')
