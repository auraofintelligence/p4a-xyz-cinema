"""Build the complete policy directory and site inventory from local sources."""
from pathlib import Path
from urllib.parse import urlsplit
import html,json,re
BASE=Path(__file__).resolve().parents[1]
OUT=BASE
def read(rel):
 p=OUT/rel
 return (p if p.exists() else BASE/rel).read_text(encoding='utf-8')
def write(rel,text):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def plain(text):return html.unescape(re.sub('<[^>]+>',' ',text)).strip()
e=html.escape
GROUPS=[
 ('bills','Bills and public wealth',[1,2,3,6,10,13,33,37,38,39]),
 ('work-homes','Housing, work and ownership',[4,5,26,28,31,32,40,47]),
 ('care','Health, care and family',[7,8,9,22,29,30,34,36,44,45,46]),
 ('digital','AI and digital safety',[11,12,14,23,24,25,35,49]),
 ('trust','Public trust and First Peoples',[16,17,19,27,48]),
 ('place','Place, climate and public projects',[18,21]),
 ('peace','Peace, security and open inquiry',[15,20,41,42,43])]
KEY=[
 ('c-hour','C-Hour','Recognise a verified voluntary hour of care, teaching or community work alongside ordinary money and paid work. C-Hours would have no fixed dollar equivalent and would not replace wages.','https://auraofintelligence.github.io/C-Hour-introduction/community-hours.html','braided-economy.html'),
 ('worker-mutuals','Worker mutuals','Help workers gain a shared stake in productive businesses through willing succession, patient finance, mentoring and learning as they go. Mutual Futures connects ownership with livelihoods, care and time.','https://auraofintelligence.github.io/mutual-futures/','workforce-transition.html?twinkle=workforce#policy-workforce'),
 ('sensorium','Web3 Sensorium','Build the missing middle between a household laptop and a corporate data centre: community-scale computing, sovereign data and useful models of places, services and possible futures.','web3-sensorium.html','web3-sensorium.html?twinkle=datacentres#policy-datacentres'),
 ('genesis','Aura Genesis','Explore consent-led AI reflection, digital memoirs and personal intelligence, with separate paths into civic trust, care research and creative worldbuilding.','aura-genesis.html','aura-politics.html'),
 ('truth','Truth Engine','Make public claims traceable: show sources, uncertainty, contested interpretations and visible corrections. Connect honest politics to public evidence and accountability.','truth-engine.html','truth-engine.html?twinkle=political-lies#policy-political-lies'),
 ('legal','Legal RAG','Use retrieval-augmented generation: find the relevant legal sources, explain their wording and follow the citations back. Connect Luke’s Relevance and the Legal Engine to contracts, disputes and reform design.','legal-rag.html','community-insurance.html?twinkle=insurance#policy-insurance'),
 ('republic','Cyber-Republic Simulator','Let people explore proposed constitutional and democratic changes before choosing them. Compare rules, powers and consequences through a public rehearsal that people can inspect and improve.','cyber-republic.html','constitution.html')]
def policy_href(r):return r['destination'].split('#')[0]+'?twinkle='+r['slug']+'#policy-'+r['slug']
def key_cards():
 return ''.join('<article class="rabbit-key-card" id="key-'+slug+'"><h3><a href="'+e(url,quote=True)+'">'+e(title)+'</a></h3><p>'+e(body)+'</p><div class="source-links"><a href="'+e(url,quote=True)+'">Open '+e(title)+'</a><a href="'+e(related,quote=True)+'">Related P4A policy</a></div></article>' for slug,title,body,url,related in KEY)
def card(r,group):
 projects=''.join('<li><a href="'+e(p['url'],quote=True)+'">'+e(p['title'])+'</a> — '+e(p['description'])+'</li>' for p in r['projectConnections'])
 sources=''.join('<a href="'+e(p['url'],quote=True)+'">'+e(p['title'])+'</a>' for p in r['sourceDocuments'])
 return '<article class="rabbit-solution" id="solution-'+r['slug']+'" data-policy-entry="'+r['slug']+'" data-policy-number="'+str(r['number'])+'" data-policy-category="'+group+'"><p class="eyebrow">Twinkle '+str(r['number']).zfill(2)+'</p><h3>'+e(r['policyTitle'])+'</h3><p>'+e(r['proposal'])+'</p><div class="hero-actions"><a class="button button-primary" data-solution-link href="'+e(policy_href(r),quote=True)+'">Open the solution</a><a class="button button-secondary" href="twinkle-'+r['slug']+'.html#clip">Twinkle '+str(r['number']).zfill(2)+' · video</a></div><details><summary>Connected projects and sources</summary><ul>'+projects+'</ul><div class="source-links">'+sources+'</div></details></article>'
def build():
 rows=json.loads(read('content/twinkle-policy-drafts.json'))
 assert sorted(n for _,_,numbers in GROUPS for n in numbers)==list(range(1,len(rows)+1))
 by_number={r['number']:r for r in rows}
 old=read('pages/rabbit-hole.html')
 # Preserve the previous civic journey under its own purpose and URL.
 if not (OUT/'pages/civic-pathway.html').exists() and not (BASE/'pages/civic-pathway.html').exists():
  journey=old.replace('<title>Rabbit-hole Map | P4A</title>','<title>Civic Pathway | P4A</title>').replace('<h1>The rabbit-hole campaign</h1>','<h1>The civic pathway</h1>').replace('<strong>Rabbit-hole map</strong>','<strong>Civic pathway</strong>')
  journey=journey.replace('A civic quest through','A civic pathway through')
  journey=journey.replace('<a class="button button-secondary" href="site-map.html#twinkle-series">All clips and policy rooms</a>','<a class="button button-secondary" href="rabbit-hole.html#rooms">All 49 policy solutions</a>')
  write('pages/civic-pathway.html',journey);write('content/rooms/civic-pathway.html',journey)
 head=old[:old.index('<main id="main">')]
 head=re.sub(r'<title>.*?</title>','<title>Rabbit-hole Policies | P4A</title>',head,count=1)
 head=re.sub(r'<meta name="description"[^>]*>','<meta name="description" content="All 49 Twinkle policy ideas, seven key civic systems, and direct links to deeper proposals, projects and sources.">',head,count=1)
 head=re.sub(r'<div class="site-layer-strip.*?</div>','',head,flags=re.S)
 head=re.sub(r'(?m)^[ \t]+$','',head)
 head=re.sub(r'<body[^>]*>','<body data-theme="royal" class="rabbit-policy-page">',head,count=1)
 if 'rabbit-hole-policies.css' not in head:head=head.replace('</head>','<link rel="stylesheet" href="../assets/rabbit-hole-policies.css?v=20261009-complete">\n</head>')
 footer=old[old.index('<footer class="site-footer">'):]
 footer=re.sub(r'<script src="[^" ]*rabbit-hole-policies.js[^" ]*"[^>]*></script>\s*','',footer)
 footer=footer.replace('</body>','<script src="../assets/rabbit-hole-policies.js?v=20261009-complete"></script>\n</body>')
 jumps=''.join('<a href="#policies-'+slug+'">'+e(title)+'</a>' for slug,title,_ in GROUPS)
 filters='<div class="rabbit-filter" data-policy-filters hidden><label>Find a solution<input type="search" data-policy-search placeholder="Search an idea, issue or project"></label><label>Topic<select data-policy-category-filter><option value="">All topics</option>'+''.join('<option value="'+slug+'">'+e(title)+'</option>' for slug,title,_ in GROUPS)+'</select></label><button type="button" class="button button-secondary" data-policy-reset>Show all</button></div><p class="rabbit-policy-count" role="status" aria-live="polite" data-policy-count>All '+str(len(rows))+' policy ideas</p><p data-policy-empty hidden>No matching ideas. Try another term or show all.</p>'
 groups=''.join('<section class="rabbit-policy-group" id="policies-'+slug+'" data-policy-group="'+slug+'"><h2>'+e(title)+'</h2><div class="rabbit-solution-grid">'+''.join(card(by_number[n],slug) for n in numbers)+'</div></section>' for slug,title,numbers in GROUPS)
 main='<main id="main"><section class="rabbit-policy-intro"><p class="eyebrow">Policy possibilities / Open for discussion</p><h1>Rabbit-hole policies</h1><p>All '+str(len(rows))+' Twinkle solutions, with the key systems that connect them. Open an idea to see how it could work, then follow its projects and source documents.</p><div class="hero-actions"><a class="button button-primary" href="twinkle.html">Twinkle hub</a><a class="button button-secondary" href="#rooms">All '+str(len(rows))+' solutions</a><a class="button button-secondary" href="site-map.html">Site tree</a></div></section><section class="rabbit-key-policies" id="key-policies"><h2>Key policies and civic systems</h2><div class="rabbit-key-grid">'+key_cards()+'</div></section><section id="rooms" class="rabbit-policy-directory"><h2>All '+str(len(rows))+' Twinkle solutions</h2><nav class="rabbit-topic-jumps" aria-label="Policy topic shortcuts">'+jumps+'</nav>'+filters+groups+'</section><nav class="rabbit-other-paths" aria-label="Other parts of P4A"><a href="civic-pathway.html">Civic pathway: origins, culture and organising</a><a href="architecture.html">Civic architecture</a><a href="maps.html">Geographic maps</a><a href="https://auraofintelligence.github.io/project-atlas/">Project Atlas</a></nav></main>'
 for folder in ['pages','content/rooms']:write(folder+'/rabbit-hole.html',head+main+footer)
 # Keep every published local page reachable from the site tree.
 files={'index.html'}
 for root in [BASE,OUT]:
  for folder in ['pages','states']:files.update(p.relative_to(root).as_posix() for p in (root/folder).rglob('*.html'))
 inventory=[]
 for rel in sorted(files):
  text=read(rel);m=re.search(r'<h1\b[^>]*>(.*?)</h1>',text,re.S) or re.search(r'<title>(.*?)</title>',text,re.S)
  title=' '.join(plain(m[1]).split()) if m else Path(rel).stem
  category='state-'+rel.split('/')[1] if rel.startswith('states/') else 'national'
  inventory.append({'path':rel,'title':title,'category':category})
 write('content/site-page-inventory.json',json.dumps({'purpose':'Every published local page; canonical content mirrors are not separate pages.','pages':inventory},ensure_ascii=False,indent=2)+'\n')
 branches=[]
 for category in ['national']+['state-'+s for s in ['vic','nsw','qld','sa','wa','tas','act','nt']]:
  entries=[p for p in inventory if p['category']==category]
  label='National pages and tools' if category=='national' else category.split('-')[1].upper()+' pages'
  branches.append('<details class="map-branch"><summary><strong>'+label+'</strong><small>'+str(len(entries))+' pages</small></summary><ul>'+''.join('<li><a href="'+e('../'+p['path'],quote=True)+'">'+e(p['title'])+'</a></li>' for p in entries)+'</ul></details>')
 full='<!-- site-page-inventory:start --><section class="section" id="all-site-pages"><div class="page-copy"><h2>Every page in the site</h2><p>'+str(len(inventory))+' published local pages, including the preserved civic pathway and all state rooms.</p>'+''.join(branches)+'</div></section><!-- site-page-inventory:end -->'
 tree=read('content/rooms/site-map.html')
 tree=re.sub(r'<!-- site-page-inventory:start -->.*?<!-- site-page-inventory:end -->','',tree,flags=re.S)
 tree=tree.replace('</main>',full+'</main>',1)
 tree=tree.replace('Rabbit-hole map</a><em>The deeper map: entry points, follow-through rooms, trust layers and future rooms.','Rabbit-hole policies</a><em>All 49 solutions, key civic systems, source projects and policy rooms.')
 if 'href="civic-pathway.html"' not in tree:tree=tree.replace('<li><a href="rabbit-hole.html">','<li><a href="civic-pathway.html">Civic pathway</a><em>The preserved journey through origins, culture, organising, trust and civic design.</em></li><li><a href="rabbit-hole.html">',1)
 # Retain broad room links while making their policy purpose explicit.
 unique={r['destination'].split('#')[0] for r in rows}
 rooms=[]
 for name in sorted(unique):
  text=read('pages/'+name);title=plain(re.search(r'<h1>(.*?)</h1>',text,re.S)[1])
  rooms.append('<li><a href="'+name+'">'+e(title)+'</a></li>')
 policy_branch='<details class="map-branch" id="rabbit-rooms" open><summary><span>03</span><strong>Rabbit-hole policies</strong><small>All 49 solutions and their full policy rooms.</small></summary><ul><li><a href="rabbit-hole.html#key-policies">Seven key policies and civic systems</a></li><li><a href="rabbit-hole.html#rooms">All 49 Twinkle solutions</a></li>'+''.join(rooms)+'</ul></details>'
 tree,n=re.subn(r'<details class="map-branch" id="rabbit-rooms".*?</details>',lambda _:policy_branch,tree,count=1,flags=re.S);assert n==1
 # Correct legacy escaped heading markup in existing tree labels.
 tree=re.sub(r'&lt;br\s*/?&gt;', ' ',tree)
 if 'href="#all-site-pages"' not in tree:tree=tree.replace('<a href="#official-links-out">Connected projects</a>','<a href="#official-links-out">Connected projects</a><a href="#all-site-pages">Every site page</a>')
 for folder in ['content/rooms','pages']:write(folder+'/site-map.html',tree)
 nav=read('assets/site-nav.js')
 nav=nav.replace("title: 'Rabbit-hole map', note: 'The deeper campaign map: entries, rooms, trust layers.'","title: 'Rabbit-hole policies', note: 'All 49 policy solutions, key civic systems and connected source projects.'")
 nav=nav.replace('Forty-six Twinkles','49 Twinkles').replace("Alcohol categories and the enacted draught freeze.","Beer tax, resource rent and the public return.").replace('Prevention, lawful pooling, reinsurance, local wealth.','AI legal and contract support, then mutual protection.').replace('Human adaptability and civic readiness.','Worker mutuals, C-Hours, patient capital and AI learning.')
 if "href: 'pages/civic-pathway.html'" not in nav:nav=nav.replace("{ href: 'pages/architecture.html'","{ href: 'pages/civic-pathway.html', title: 'Civic pathway', note: 'Origins, culture, organising and the broader civic journey.' },\n        { href: 'pages/architecture.html'",1)
 start='/* key-policy-navigation:start */';end='/* key-policy-navigation:end */'
 nav=re.sub(re.escape(start)+'.*?'+re.escape(end)+'\n?','',nav,flags=re.S)
 keys=[{'href':'pages/rabbit-hole.html#key-'+slug if url.startswith('https:') else 'pages/'+url,'title':title,'note':body} for slug,title,body,url,_ in KEY]
 block=start+'\n'+json.dumps({'id':'key-policies','num':'Key','label':'Key policy ideas','blurb':'The core proposals connecting the Twinkle solutions.','links':keys},ensure_ascii=False)+',\n'+end+'\n'
 nav=nav.replace("    {\n      id: 'spark',",block+"    {\n      id: 'spark',",1)
 write('assets/site-nav.js',nav)
 # Make prominent policy links visible on the homepage as well.
 home=read('index.html')
 start='<!-- key-policy-home:start -->';end='<!-- key-policy-home:end -->'
 home=re.sub(re.escape(start)+'.*?'+re.escape(end),'',home,flags=re.S)
 keylinks=start+'<nav class="source-links" aria-label="Key policy ideas">'+''.join('<a href="'+e(url if url.startswith('https:') else 'pages/'+url,quote=True)+'">'+e(title)+'</a>' for _,title,_,url,_ in KEY)+'</nav>'+end
 target='<h3>Rabbit-hole policies</h3>'
 assert target in home
 home=home.replace(target,target+keylinks,1)
 home=home.replace('Explore the broader rooms, then the connected projects behind them.','Browse all 49 solutions and the key policies, then follow their projects and sources.')
 write('index.html',home)
 js=read('assets/twinkle-navigation.js')
 js=js.replace("document.querySelectorAll('[data-policy-draft]').forEach(s=>s.hidden=true)","document.querySelectorAll('[data-policy-draft]').forEach(s=>s.hidden=false)")
 write('assets/twinkle-navigation.js',js)
 # Use one clear directory name on every public entry point and source mirror.
 for root in [BASE,OUT]:
  for folder in ['pages','states','content/rooms']:
   for p in (root/folder).rglob('*.html'):
    rel=p.relative_to(root).as_posix();text=read(rel)
    text=re.sub(r'(<a\b[^>]*href="[^"]*rabbit-hole.html(?:#[^"]*)?"[^>]*>)Rabbit-hole map(</a>)',r'\1Rabbit-hole policies\2',text)
    text=re.sub(r'(assets/site-nav.js)(?:\?[^"\s]*)?',r'\1?v=20261009-policy-directory',text)
    write(rel,text)
 home=read('index.html');home=re.sub(r'(assets/site-nav.js)(?:\?[^"\s]*)?',r'\1?v=20261009-policy-directory',home);write('index.html',home)
 return {'policySolutions':len(rows),'keyPolicies':len(KEY),'publicPages':len(inventory),'preservedJourney':'pages/civic-pathway.html'}
if __name__=='__main__':print(json.dumps(build()))
