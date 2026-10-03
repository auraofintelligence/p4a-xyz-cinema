import pathlib,json,hashlib,subprocess,re,collections
pathlib.Path('qa').mkdir(exist_ok=True)
R=pathlib.Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((R/'content/elections/vic-2026.json').read_text(encoding='utf-8'));rows=d['candidates'];assert len(rows)==482 and len({x['id'] for x in rows})==482
assert collections.Counter(x['chamber'] for x in rows)=={'assembly':407,'council':75};assert len({x['party'] for x in rows})==14;assert sum(x['party']=='One Nation' for x in rows)==93
assert collections.Counter(x['status'] for x in rows)=={'announced':481,'preselected':1}
assert sum(bool(x['conflict']) for x in rows)==2
for name,area in [('Chloe Nicolosi','Bundoora'),('Rachel Unicomb','Broadmeadows'),('Matthew De Angelis','Sydenham')]:assert [x['electorate'] for x in rows if x['name']==name]==[area]
assert all(x.get('notes') and 'registered' in x['notes'] for x in rows if x['party']=='Socialist Alliance')
assert not any(x['name'] in ['Ali Cupper','Ron Nelson','Raymond French','Steve Manning'] for x in rows)
paths=[R/x for x in ['states/vic/index.html','states/vic/election/index.html','states/vic/map/index.html','assets/vic-election-data.js','assets/vic-people.js','assets/state-data.js','pages/states.html']];before={str(p.relative_to(R)):sha(p) for p in paths}
subprocess.run(['pwsh','-NoProfile','-File',str(R/'tools/build-state-sites.ps1'),'-StateSlug','vic','-SkipHistory'],check=True)
for tool in ['build-vic-election.py','build-vic-map.py']:subprocess.run(['python',str(R/'tools'/tool)],check=True)
after={str(p.relative_to(R)):sha(p) for p in paths};assert before==after,[(p,before[p],after[p]) for p in before if before[p]!=after[p]]
for file in ['assets/vic-election.js','assets/vic-profile-details.js','assets/site-nav.js']:subprocess.run(['node','--check',str(R/file)],check=True)
subprocess.run(['git','-C',str(R),'diff','--check'],check=True)
assert subprocess.check_output(['git','-C',str(R),'diff','--','LICENCE.md']).strip()==b''
report={'candidates':482,'assembly':407,'council':75,'affiliations':14,'announced':481,'preselected':1,'formallyNominated':0,'allJoinedToExistingAreas':True,'sourceConflictsPreserved':2,'unregisteredAffiliationCaveat':True,'reproducibleScopedBuild':True,'javascriptSyntax':'pass','gitDiffCheck':'pass','projectLicenceUnchanged':True,'generatedSha256':after,'head':subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip(),'cachedOriginMain':subprocess.check_output(['git','-C',str(R),'rev-parse','origin/main']).decode().strip(),'remoteContacted':False}
pathlib.Path('qa/election-terminal-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
