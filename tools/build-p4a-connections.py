# Build P4A's connected Twinkle proposals without publishing anything.
from pathlib import Path
from collections import defaultdict
import html,json,re
import importlib.util
BASE=Path(__file__).resolve().parents[1]
OUT=BASE
spec=importlib.util.spec_from_file_location('followups',BASE/'tools/build-twinkle-followups.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
def read(rel):
 p=OUT/rel
 return (p if p.exists() else BASE/rel).read_text(encoding='utf-8')
def write(rel,text):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
e=html.escape
def links(r):
 items=''.join('<li><a href="'+e(p['url'],quote=True)+'">'+e(p['title'])+'</a> — '+e(p['description'])+' <a href="'+e(p['repositoryUrl'],quote=True)+'">Source repository</a></li>' for p in r['projectConnections'])
 sources=''.join('<a href="'+e(p['url'],quote=True)+'">'+e(p['title'])+'</a>' for p in r['sourceDocuments'])
 return '<div class="project-paths"><h3>Explore the connected work</h3><ul>'+items+'</ul><div class="source-links">'+sources+'</div></div>'
def section(r):
 return '<section class="section twinkle-policy-draft" id="policy-'+r['slug']+'" data-policy-draft="'+r['slug']+'"><div class="page-copy"><article class="feature-panel"><p class="eyebrow">Twinkle '+str(r['number']).zfill(2)+' / Brainstorming scenario</p><h2>'+e(r['policyTitle'])+'</h2><p class="policy-fix">'+e(r['proposal'])+'</p><p>'+e(r['introduction'])+'</p>'+links(r)+'<h3>How it could work</h3><ol>'+''.join('<li>'+e(x)+'</li>' for x in r['steps'])+'</ol><h3>Everyday example</h3><p>'+e(r['example'])+'</p><h3>Who could act and how it could be funded</h3><p>'+e(r['deliveryAndFunding'])+'</p><h3>Fair-go safeguards</h3><p>'+e(r['safeguards'])+'</p><h3>What would show progress</h3><p>'+e(r['measures'])+'</p><div class="source-links"><a href="twinkle-'+r['slug']+'.html#clip">Twinkle '+str(r['number']).zfill(2)+' · video</a><a href="'+r['destination'].split('#')[0]+'">Open the full room</a><a href="rabbit-hole.html">Rabbit-hole policies</a></div></article></div></section>'
def marked(text,key,block):
 start='<!-- '+key+':start -->';end='<!-- '+key+':end -->'
 text=re.sub(re.escape(start)+'.*?'+re.escape(end),'',text,flags=re.S)
 return text.replace('</main>',start+block+end+'</main>',1)
def build():
 rows=json.loads(read('content/twinkle-policy-drafts.json'))
 reg=json.loads(read('content/project-source-register.json'))
 old=json.loads((BASE/'content/twinkle-reviewed-copy.json').read_text(encoding='utf-8'))
 renderer.BASE=BASE;renderer.OUT=OUT;renderer.section=section
 renderer.build(rows)
 reviewed=[{k:r[k] for k in ('number','slug','headline','gripe','destination')} for r in rows]
 write('content/twinkle-reviewed-copy.json',json.dumps(reviewed,ensure_ascii=False,indent=2)+'\n')
 # Apply approved title/joke changes everywhere they appeared, including cards.
 replacements=[]
 for a,b in zip(old,rows):
  for field in ['headline','gripe']:
   if a[field]!=b[field]:replacements.extend([(a[field],b[field]),(e(a[field]),e(b[field]))])
 files=set(['index.html','assets/site-nav.js','pages/twinkle.html','content/rooms/twinkle.html'])
 for r in rows:
  for folder in ['pages','content/rooms']:
   files.add(folder+'/twinkle-'+r['slug']+'.html');files.add(folder+'/'+r['destination'].split('#')[0])
 for rel in files:
  text=read(rel)
  for a,b in replacements:text=text.replace(a,b)
  write(rel,text)
 groups=defaultdict(list)
 for r in rows:groups[r['destination'].split('#')[0]].append(r)
 for name,connected in groups.items():
  for folder in ['content/rooms','pages']:
   rel=folder+'/'+name;text=read(rel)
   hero=reg['roomHeroes'][name]
   hero=re.sub(r'(<div class="hero-actions">.*?)(</div>)',lambda m:m[1]+'<a class="button button-secondary" data-policy-video href="twinkle-'+connected[0]['slug']+'.html#clip">Twinkle '+str(connected[0]['number']).zfill(2)+' · video</a>'+m[2],hero,count=1,flags=re.S)
   text=re.sub(r'<div class="hero-content.*?</section>',lambda _:hero,text,count=1,flags=re.S)
   text=text.replace('id="policy-background">','id="policy-background" open>')
   text=text.replace('<summary>Evidence, sources and related ideas</summary>','<summary>Full room: ideas, tools and sources</summary>')
   text=text.replace(' New delivery arrangements here are working proposals, not statements that a pilot is operating or a reform is already law.','')
   write(rel,text)
 for r in rows:
  block='<div class="feature-panel twinkle-explainer"><p class="eyebrow">Brainstorming scenario</p><h2>'+e(r['policyTitle'])+'</h2><p>'+e(r['introduction'])+'</p><p><a class="button button-primary" href="'+r['destination'].split('#')[0]+'?twinkle='+r['slug']+'#policy-'+r['slug']+'">Explore the policy idea</a></p><details><summary>Short video script</summary><p>'+e(r['clipScript'])+'</p></details>'+links(r)+'</div>'
  for folder in ['content/rooms','pages']:
   rel=folder+'/twinkle-'+r['slug']+'.html';text=read(rel)
   text=re.sub(r'<!-- twinkle-connected:start -->.*?<!-- twinkle-connected:end -->','',text,flags=re.S)
   # One short video, then the explanation and useful next destinations.
   text=text.replace('<nav class="next-trail"','<!-- twinkle-connected:start -->'+block+'<!-- twinkle-connected:end --><nav class="next-trail"',1)
   write(rel,text)
 js=read('assets/twinkle-navigation.js')
 records=[dict(r,clip='twinkle-'+r['slug']+'.html',policy=r['destination'].split('#')[0]+'?twinkle='+r['slug']) for r in reviewed]
 js=re.sub(r'const records = .*?;\s*const panel',lambda _:'const records = '+json.dumps(records,ensure_ascii=False)+';\n const panel',js,count=1,flags=re.S)
 js=js.replace('if (!record) return;', '''if (!record) {
   document.querySelectorAll('[data-policy-draft]').forEach(s=>s.hidden=false);
   const background=document.getElementById('policy-background');if(background)background.open=true;
   const intro=document.createElement('p');intro.textContent='Twinkle doorways into this room';
   const doors=document.createElement('div');doors.className='source-links';
   records.filter(r=>r.destination.split('#')[0]===panel.dataset.twinklePolicyContext).forEach(r=>doors.append(linkDoor(r)));
   panel.replaceChildren(intro,doors);return;
 }
 const background=document.getElementById('policy-background');if(background)background.open=false;''')
 # Function declaration is hoisted above both paths.
 if 'function linkDoor(' not in js:js=js.replace(' const panel ='," function linkDoor(r){const a=document.createElement('a');a.href=r.policy+'#policy-'+r.slug;a.textContent='Twinkle '+String(r.number).padStart(2,'0')+': '+r.headline;return a;}\n const panel =",1)
 write('assets/twinkle-navigation.js',js)
 # Shared gateways explain what each project offers; Atlas supplies the wider exit.
 core=['unga','chour','queens','mutual','atlas']
 gateway='<section class="section connected-gateway" id="connected-work"><div class="page-copy"><p class="eyebrow">Keep exploring</p><h2>P4A is the front door</h2><p>These are connected policy possibilities, tools and source libraries. Follow an idea into the project behind it, then use Project Atlas to explore the wider work.</p><ul>'+''.join('<li><a href="'+reg['projects'][k]['url']+'">'+e(reg['projects'][k]['title'])+'</a> — '+e(reg['projects'][k]['description'])+'</li>' for k in core)+'</ul></div></section>'
 for rel in ['index.html','pages/twinkle.html','content/rooms/twinkle.html','pages/rabbit-hole.html']:
  write(rel,marked(read(rel),'p4a-gateway',gateway))
 home=read('index.html')
 # Keep the left hub button; replace the duplicate on the right.
 home,n=re.subn(r'(<a class="button button-secondary" href=")[^"]*(">)All 49 Twinkles</a>',r'\1pages/rabbit-hole.html#rooms\2Rabbit-hole policies</a>',home,count=1)
 if n==0:assert 'Rabbit-hole policies' in home
 home=re.sub(r'(<p class="eyebrow">// GO DEEPER</p>\s*<h[23]>).*?(</h[23]>\s*<p>).*?(</p>)',r'\1Rabbit-hole policies\2Follow the gripe into policy possibilities, useful tools and public sources. Explore the broader rooms, then the connected projects behind them.\3',home,count=1,flags=re.S|re.I)
 home=home.replace('Ready to leave the shallow end? The full campaign map: rooms, trust layers and future machinery. Twinkle is the doorway; this is the house.','Follow the gripe into policy possibilities, useful tools and public sources. Explore the broader rooms, then the connected projects behind them.')
 home=home.replace('<h3>The rabbit hole</h3>','<h3>Rabbit-hole policies</h3>')
 home=home.replace('<a class="button button-primary" href="pages/rabbit-hole.html">Open the map</a>','<a class="button button-primary" href="pages/twinkle.html">Twinkle hub</a>')
 home=home.replace('<a class="button button-secondary" href="pages/twinkle.html">See all 49 Twinkles</a>','<a class="button button-secondary" href="pages/rabbit-hole.html#rooms">Rabbit-hole policies</a>')
 write('index.html',home)
 tree=read('content/rooms/site-map.html')
 branch='<details class="map-branch" id="twinkle-series" open><summary><span>02</span><strong>49 Twinkles and their policy ideas</strong><small>Stable identities: clip → specific proposal → full room → connected projects.</small></summary><ul>'
 for r in rows:
  name=r['destination'].split('#')[0];roomtitle=html.unescape(re.search(r'<h1>(.*?)</h1>',reg['roomHeroes'][name],re.S)[1])
  branch+='<li><a href="twinkle-'+r['slug']+'.html">Twinkle '+str(r['number']).zfill(2)+': '+e(r['headline'])+'</a><div class="source-links"><a href="'+name+'?twinkle='+r['slug']+'#policy-'+r['slug']+'">'+e(r['policyTitle'])+'</a><a href="'+name+'">Full room: '+e(roomtitle)+'</a></div></li>'
 branch+='</ul></details>'
 tree,n=re.subn(r'<details class="map-branch" id="twinkle-series".*?</details>',lambda _:branch,tree,count=1,flags=re.S);assert n==1
 tree=re.sub(r'Twinkle 0[1-4] follow-through: ','',tree)
 tree=marked(tree,'p4a-gateway',gateway)
 for folder in ['content/rooms','pages']:write(folder+'/site-map.html',tree)
 css=read('assets/twinkle-navigation.css')
 css=re.sub(r'/\* connected-layout:start \*/.*?/\* connected-layout:end \*/','',css,flags=re.S)
 css=css.rstrip()+'''\n/* connected-layout:start */
.project-paths ul,.connected-gateway ul {padding-left:1.2rem;margin:.5rem 0;}
.project-paths li,.connected-gateway li {margin:.55rem 0;}
.twinkle-explainer {padding:1rem; margin:1rem 0;}
.twinkle-explainer details {margin:.6rem 0;}
.twinkle-policy-page .policy-background {padding:0 1rem;}
.twinkle-policy-page .hero-actions {flex-wrap:wrap;}
.twinkle-policy-page .page-hero,.twinkle-clip-page .page-hero {min-height:0;}
.connected-gateway {padding-block:1rem;}
.vic-early-clock {margin:.6rem 0;}
.vic-early-clock span {display:block;}
/* connected-layout:end */
'''
 css=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',css)
 write('assets/twinkle-navigation.css',css)
 # Cache token is shared by every updated entry point.
 for rel in list(files)+['pages/rabbit-hole.html','content/rooms/rabbit-hole.html','pages/site-map.html','content/rooms/site-map.html']:
  text=read(rel)
  if 'twinkle-navigation.css' not in text:text=text.replace('</head>','<link rel="stylesheet" href="'+('assets/' if rel=='index.html' else '../assets/')+'twinkle-navigation.css?v=20261009-connected">\n</head>')
  text=re.sub(r'(assets/twinkle-navigation\.(?:css|js))(?:\?[^"\s]*)?',r'\1?v=20261009-connected',text)
  write(rel,text)
 spec=importlib.util.spec_from_file_location('rabbit_policies',BASE/'tools/build-rabbit-hole-policies.py')
 policies=importlib.util.module_from_spec(spec);spec.loader.exec_module(policies)
 policies.BASE=BASE;policies.OUT=OUT;policies.build()
 return {'twinkles':len(rows),'policyRooms':len(groups),'projectConnections':sum(len(r['projectConnections']) for r in rows),'localOnly':True}
if __name__=='__main__':print(json.dumps(build()))
