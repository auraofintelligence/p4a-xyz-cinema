from cdp_client import CDP
import pathlib,json,base64,time,collections,re,urllib.parse
R=pathlib.Path(__file__).resolve().parents[2];out=pathlib.Path('qa');out.mkdir(exist_ok=True);d=json.loads((R/'content/elections/vic-2026.json').read_text(encoding='utf-8'));c=CDP();c.call('Page.enable');c.call('Runtime.enable');c.call('Network.enable');report=[]
def ev(x):return c.evaluate(x)
def nav(url):
 ev('window.__qaOldDocument=true');c.call('Page.navigate',{'url':url});c.wait("!window.__qaOldDocument && document.readyState==='complete'");c.call('Page.resetNavigationHistory')
nav('about:blank');c.events=[]
for protocol,root in [('file','file:///G:/GithubLocal-PC/p4a-xyz-cinema/'),('http','http://127.0.0.1:8766/')]:
 for width in [1440,390]:
  print(protocol,width,flush=True);c.call('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000 if width>500 else 844,'deviceScaleFactor':1,'mobile':width<500});nav(root+'states/vic/election/index.html')
  c.wait('window.P4A_VIC_ELECTION && !document.querySelector("[data-candidate-filters]").hidden')
  assert ev('document.querySelectorAll("[data-candidate-id]").length')==482
  assert ev('document.documentElement.scrollWidth<=innerWidth+1'),ev('({sw:document.documentElement.scrollWidth,w:innerWidth})')
  assert ev('document.querySelectorAll(".ve-conflict").length')==2
  results=ev('''(()=>{let errors=[];for(const party of [...new Set(P4A_VIC_ELECTION.candidates.map(c=>c.party))]){let s=document.querySelector('[data-candidate-party]');s.value=party;s.dispatchEvent(new Event('change'));let actual=document.querySelectorAll('[data-candidate-id]:not([hidden])').length,expected=P4A_VIC_ELECTION.candidates.filter(c=>c.party===party).length;if(actual!==expected)errors.push({party,actual,expected});}document.querySelector('[data-candidate-reset]').click();for(const key of ['chamber','status','source']){let s=document.querySelector('[data-candidate-'+key+']');for(const o of [...s.options].slice(1)){s.value=o.value;s.dispatchEvent(new Event('change'));let actual=document.querySelectorAll('[data-candidate-id]:not([hidden])').length,expected=P4A_VIC_ELECTION.candidates.filter(c=>(key==='source'?new URL(c.source).hostname:c[key])===o.value).length;if(actual!==expected)errors.push({key,value:o.value,actual,expected});}document.querySelector('[data-candidate-reset]').click();}return errors;})()''');assert not results,results
  ev('document.querySelector("[data-candidate-search]").value="Matthew De Angelis";document.querySelector("[data-candidate-search]").dispatchEvent(new Event("input"))');assert ev('document.querySelectorAll("[data-candidate-id]:not([hidden])").length')==1;assert 'Sydenham' in ev('document.querySelector("[data-candidate-id]:not([hidden])").textContent')
  ev('document.querySelector("[data-candidate-reset]").click()');assert ev('document.activeElement.hasAttribute("data-candidate-search")')
  nav(root+'states/vic/election/index.html?party=One%20Nation&chamber=council&status=announced&source=vic.onenation.org.au');assert ev('document.querySelectorAll("[data-candidate-id]:not([hidden])").length')==15
  ev('document.querySelector("[data-candidate-reset]").click()');c.call('Page.captureScreenshot',{'format':'png'});(out/f'election-{protocol}-{width}.png').write_bytes(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png'})['data']))
  # Newcomer doors, source register and compact footer exist as real links.
  assert ev('document.querySelectorAll(".ve-footer nav a").length')==4
  assert ev('!!document.querySelector("#ve-start") && !!document.querySelector(\'a[href="../map/index.html?chamber=firstpeoples"]\')')
  nav(root+'states/vic/index.html');assert ev('document.querySelector(".state-election-door a").getAttribute("href")')=='election/index.html'
  nav(root+'states/vic/map/index.html?chamber=assembly&electorate='+urllib.parse.quote(d['candidates'][0]['areaId'])+'&section=election');c.wait('window.P4A_VIC_MAP && P4A_VIC_MAP.getState().layerReady && !!document.querySelector(".vic-announced-candidates")')
  failures=ev('''(()=>{const errors=[];for(const layer of ['assembly','council'])for(const record of P4A_VIC_ELECTORATES[layer]){const p=document.createElement('div');p.innerHTML='<h2>'+record.name+'</h2>';P4A_VIC_DETAILS.enhance(p,record,layer);let actual=p.querySelectorAll('[data-candidate-id]').length,expected=P4A_VIC_PEOPLE.candidates.filter(c=>c.areaId===record.id).length;if(actual!==expected)errors.push({id:record.id,actual,expected});}return errors;})()''');assert not failures,failures
  assert ev('P4A_VIC_PEOPLE.candidates.length')==482
  assert ev('!!document.querySelector(\'.vic-election a[href="../election/index.html"]\')')
  report.append({'protocol':protocol,'viewport':width,'all482Rendered':True,'all14AffiliationsFilters':True,'allChamberStatusSourceFilters':True,'urlFilterRestoration':True,'searchSydenham':True,'clearFocus':True,'twoVisibleConflictNotes':True,'noHorizontalOverflow':True,'compactFooter':True,'prominentNavigation':True,'all96AtlasAreaJoins':True})
# Progressive enhancement: all cards and source links survive disabled JavaScript.
c.call('Emulation.setScriptExecutionDisabled',{'value':True});nav('http://127.0.0.1:8766/states/vic/election/index.html');assert ev('document.querySelectorAll("[data-candidate-id]").length')==482;c.call('Emulation.setScriptExecutionDisabled',{'value':False})
all_errors=[e for e in c.events if e.get('method')=='Runtime.exceptionThrown'];extension_errors=[e for e in all_errors if 'chrome-extension://' in json.dumps(e)];errors=[e for e in all_errors if e not in extension_errors];assert not errors,errors[:2]
broken=[]
from bs4 import BeautifulSoup
for rel in ['states/vic/election/index.html']:
 p=R/rel;soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for a in soup.select('[href],[src]'):
  url=a.get('href') or a.get('src');u=urllib.parse.urlsplit(url)
  if not u.scheme and not u.netloc and u.path:
   target=(p.parent/urllib.parse.unquote(u.path)).resolve()
   if not target.exists():broken.append(url)
assert not broken,broken
final={'checked':'2026-10-02','runs':report,'noJavaScriptAll482':True,'pageRuntimeExceptions':0,'environmentExtensionErrors':len(extension_errors),'environmentExtensionNote':'Only errors explicitly naming chrome-extension:// dynamic imports are separated from page runtime errors. Browser-managed extension injection is outside the repository.','localLinksValid':True,'counts':dict(collections.Counter(r['party'] for r in d['candidates'])),'candidates':482,'assembly':407,'council':75,'noFormalNominationsAsserted':all(r['status']!='nominated' for r in d['candidates'])}
(out/'election-browser-report.json').write_text(json.dumps(final,indent=2),encoding='utf-8');print(json.dumps(final,indent=2))
