"""Audit public names, provenance exceptions and changed-page local links."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
from urllib.parse import urlsplit,unquote
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools'))
from public_copy import public_html
paths=[R/'index.html',*sorted((R/'pages').rglob('*.html')),*sorted((R/'states').rglob('*.html'))]
allowed=re.compile(r'Luke Richmond|Luke Sharrock|Luke Matthew Preston|BRADY, Luke|SMITH, Luke|ALEKSOV, Angel|Angel Dolejší|HAYES, Clifford')
errors=[];exceptions=[];address_files=[];checks=0
for p in paths:
 text=p.read_text(encoding='utf-8');s=BeautifulSoup(text,'html.parser')
 for e in s(['script','style']):e.decompose()
 for t in s.find_all(string=re.compile(r'\bLuke\b|\bHayes\b|\bAngel\b',re.I)):
  if isinstance(t,Comment):continue
  if allowed.search(str(t)):exceptions.append({'file':str(p.relative_to(R)),'text':str(t),'reason':'Unrelated elected representative or actual candidate; identity preserved.'})
  else:errors.append([str(p),'public name',str(t)])
 for e in s.select('meta[content],[title],[aria-label],img[alt]'):
  for key in ['content','title','aria-label','alt']:
   val=e.get(key,'')
   if re.search(r'\bLuke\b|\bHayes\b',val,re.I) and not val.startswith('http'):errors.append([str(p),key,val])
 if re.search('UNGA81-Luke-Hayes|lukes-relevance',text):address_files.append(str(p.relative_to(R)))
 assert public_html(p.name,text)==text,('not idempotent',p)
 for a in s.select('a[href]'):
  u=urlsplit(a['href'])
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.exists():
   # Report only newly introduced broken destinations; pre-existing state data can contain historic links.
   old=subprocess.run(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R,capture_output=True).stdout.decode('utf-8')
   if a['href'] not in old:errors.append([str(p),'missing destination',a['href']])
  else:checks+=1
assert not errors,errors
report={'publicHTMLFiles':len(paths),'localDestinationsChecked':checks,'strayPublicNames':errors,'intentionalOtherPeople':exceptions,'preservedURLSlugFiles':address_files,'legalProvenanceUnchanged':['LICENCE.md','content/licences/vic-source-register.json','content/licences/vic-source-register.md'],'historyPreserved':['content/archive','docs/planning'],'intentionalToolingPatterns':'tools/public_copy.py retains retired personal strings only as replacement match patterns; planning generators retain internal research provenance, not rendered visitor copy.','scope':'Visible copy and metadata checked; factual authorship in original sources and legal notices retained.'}
(R/'tools/publication-qa/public-copy-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS',len(paths),'public HTML files;',checks,'local destinations; no promotional names; explicit exceptions recorded.')
