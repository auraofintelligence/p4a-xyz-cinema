"""Build the human directory from actual public routes, without refreshing source dates."""
from pathlib import Path
import html, json, re, runpy

ROOT = Path(__file__).resolve().parents[1]
UPDATED = '2026-10-17'
STATE_NAMES = {'act':'Australian Capital Territory','nsw':'New South Wales','nt':'Northern Territory','qld':'Queensland','sa':'South Australia','tas':'Tasmania','vic':'Victoria','wa':'Western Australia'}
GROUPS = {
 'start': ('Start and find your bearings', 'A few useful ways into P4A.'),
 'places': ('Maps and places', 'Find your state, council or electorate. The types stay separate.'),
 'redland': ('Redlands: the local journey', 'Map, questions, possibilities, people, participation and outcomes.'),
 'divisions': ('Redlands: ten divisions', 'Choose a division for local orientation, public records and connected questions.'),
 'policies': ('Everyday questions and policy ideas', 'Explore the serious context and possible responses behind public concerns.'),
 'twinkles': ('Twinkles: one scene, one gripe, one breath', 'Short seeds into deeper questions, evidence and policy rooms.'),
 'systems': ('Systems and shared possibilities', 'How local questions connect to wider civic and economic patterns.'),
 'tools': ('Build, contribute and take part', 'Practical guides and browser-local drafting tools.'),
 'culture': ('Culture, origins and meaning', 'Stories, lyric meanings and the ideas behind the project.'),
 'support': ('Support and design', 'Support options, gear and visual experiments.'),
 'state-rooms': ('State and territory rooms', 'Portals, histories, architecture and rulebooks. Victoria also has an electorate atlas and election guide.')
}
EXPLICIT = {
 'start': ['index','about','civic-pathway','site-map'],
 'places': ['maps','states','state-history','minjerribah','treaty-atlas'],
 'systems': ['architecture','braided-economy','civic-ledger','civic-surges','constitution','cyber-republic','legal-rag','sovereignty-stack','truth-engine','web3-sensorium','purple-synthesis'],
 'tools': ['civic-twin-builders','markdown-with-ai','starter-field-kit','p4a-builder','c-hour-receipt-builder','noticeboard-contract-builder','private-civic-profile-builder'],
 'culture': ['alien-necklace-film','aura-genesis','aura-politics','joke','musicverse'],
 'support': ['colour-panel','deployment-gear','gear-store','test-store1']
}
LABELS = {
 'index.html':'Home', 'pages/site-map.html':'Site map', 'pages/maps.html':'Geographic maps',
 'pages/states.html':'States and territories', 'pages/twinkle.html':'Twinkle hub and format rules',
 'pages/rabbit-hole.html':'Policy ideas: the full directory',
 'states/vic/map/index.html':'Victoria electorate and council atlas',
 'states/vic/election/index.html':'Victoria 2026 election guide',
 'states/qld/councils/index.html':'Queensland council map and search',
 'states/qld/councils/redland/index.html':'Redlands overview and division map',
 'states/qld/councils/redland/explore/index.html':'Local questions and Twinkles',
 'states/qld/councils/redland/possibilities/index.html':'Connected systems and possibilities',
 'states/qld/councils/redland/candidates/index.html':'People, elections and public records',
 'states/qld/councils/redland/action/index.html':'Take part and plan a contribution',
 'states/qld/councils/redland/outcomes/index.html':'Outcomes: cost, freely given, change',
 'states/qld/councils/redland/sources/index.html':'Sources, dates and review register',
 'states/qld/councils/redland/divisions/index.html':'All Redlands divisions',
}
divisions = json.loads((ROOT/'content/local/redland-divisions.json').read_text(encoding='utf-8'))['divisions']
for row in divisions:
 LABELS[f"states/qld/councils/redland/divisions/{row['id']}/index.html"] = f"Division {row['id']}: {row['localities']}"

def clean(value):
 return html.unescape(re.sub('<[^>]+>', '', value)).strip()

def group(path):
 if '/redland/divisions/' in path and not path.endswith('/divisions/index.html'): return 'divisions'
 if path.startswith('states/qld/councils/redland/'): return 'redland'
 if path == 'states/qld/councils/index.html': return 'places'
 if path.startswith('states/'): return 'state-rooms'
 stem = Path(path).stem
 if stem.startswith('twinkle-') or stem == 'twinkle': return 'twinkles'
 for key, stems in EXPLICIT.items():
  if stem in stems: return key
 return 'policies'

routes = [ROOT/'index.html'] + sorted((ROOT/'pages').rglob('*.html')) + sorted((ROOT/'states').rglob('*.html'))
inventory = []
for file in routes:
 path = file.relative_to(ROOT).as_posix()
 source = file.read_text(encoding='utf-8')
 heading = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', source, re.I)
 title = re.search(r'<title>([\s\S]*?)</title>', source, re.I)
 label = LABELS.get(path, clean((heading or title).group(1)))
 inventory.append({'path':path, 'title':label, 'category': 'state-'+path.split('/')[1] if path.startswith('states/') else 'national', 'navigationGroup':group(path)})

def a(path, label, **kw):
 href = '../'+path
 return f'<a href="{html.escape(href,quote=True)}">{html.escape(label)}</a>'

def rows(key):
 selected = [row for row in inventory if row['navigationGroup'] == key]
 if key == 'divisions': selected.sort(key=lambda row:int(row['path'].split('/')[-2]))
 if key == 'redland':
  order = ['index.html','divisions/index.html','explore/index.html','possibilities/index.html','candidates/index.html','action/index.html','outcomes/index.html','sources/index.html']
  selected.sort(key=lambda row:order.index(row['path'].split('states/qld/councils/redland/')[1]))
 return selected

def directory(key, opened=False):
 title, note = GROUPS[key]
 items = rows(key)
 content = '\n'.join(f'<li data-site-page data-search="{html.escape((row["title"]+" "+row["path"]+" "+title).lower(),quote=True)}">{a(row["path"],row["title"])}</li>' for row in items)
 aliases = {'start':'main-doors','twinkles':'twinkle-series','policies':'rabbit-rooms','tools':'workbench','state-rooms':'state-layer'}
 alias = f'<span id="{aliases[key]}"></span>' if key in aliases else ''
 return f'''{alias}<details class="human-directory" id="{key}" data-site-group {'open' if opened else ''}>
 <summary><strong>{html.escape(title)}</strong><span>{len(items)} pages</span></summary>
 <p>{html.escape(note)}</p><ul>{content}</ul></details>'''

source = (ROOT/'pages/site-map.html').read_text(encoding='utf-8')
external = re.search(r'<details\b[^>]*\bid="official-links-out"[\s\S]*?</details>', source)
external_html = external.group(0) if external else ''
if external_html:
 external_html = re.sub(r'\sopen(?=[\s>])', '', external_html, count=1)
 external_html = external_html.replace('class="map-branch"','class="human-directory connected-projects"')
 external_html = re.sub(r'<summary>[\s\S]*?</summary>','<summary><strong>Connected projects</strong><span>External sites and source libraries</span></summary>',external_html,count=1)

header = re.split(r'<main\b[^>]*>',source,maxsplit=1)[0]
footer = source.split('</main>',1)[1]
header = re.sub(r'<title>.*?</title>','<title>Find your way | P4A site map</title>',header,flags=re.S)
header = re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="A readable, searchable guide to every P4A page: maps, places, Redlands, Twinkles, systems and ways to take part.">',header)
if 'assets/site-map.css' not in header:
 header = header.replace('</head>','<link rel="stylesheet" href="../assets/site-map.css?v=20261017">\n<script src="../assets/site-map.js?v=20261017" defer></script>\n</head>')

main = f'''<main id="main" class="human-site-map">
 <section class="human-map-intro">
 <p class="eyebrow">P4A · Find your way</p><h1>Where would you like to go?</h1>
 <p class="human-lead">Start with your place, a question, or an idea. Each path connects to evidence, people and ways to take part.</p>
 <p class="human-map-date">Navigation updated <time datetime="{UPDATED}">17 October 2026</time> · {len(inventory)} public pages. This date records the navigation review; facts keep their own source dates.</p>
 <div class="human-start-grid">
 <article><h2>Find my place</h2><p>Use a map, search an area, inspect it, then open its journey.</p>{a('pages/states.html','Choose a state or territory')}</article>
 <article><h2>Follow a local question</h2><p>Redlands connects ordinary experiences to systems, records and useful action.</p>{a('states/qld/councils/redland/explore/index.html','Explore Redlands questions')}</article>
 <article><h2>Explore an idea</h2><p>Twinkles open the door. The policy rooms carry the serious detail.</p>{a('pages/twinkle.html','Browse Twinkles and their meanings')}</article>
 </div>
 <nav class="human-jumps" aria-label="Site map sections"><a href="#places">Maps and places</a><a href="#redland-local-journey">Redlands journey</a><a href="#all-site-pages">Every page</a><a href="#official-links-out">Connected projects</a><a href="../states/qld/councils/redland/sources/index.html#review-register">Changes and review dates</a></nav>
 <div class="human-filter" hidden data-site-filter><label for="site-map-search">Find a page or topic</label><div><input id="site-map-search" type="search" placeholder="Try rates, housing, Victoria, legal, Division 2…" autocomplete="off"><button type="button" data-site-clear>Clear</button></div><p role="status" aria-live="polite" data-site-search-status>{len(inventory)} pages available.</p></div>
 </section>
 <section class="human-places" aria-labelledby="places-heading"><h2 id="places-heading">Places: three different public responsibilities</h2>
 <div class="human-place-grid">
 <article><h3>Councils and divisions</h3><p><strong>Built example: Redlands.</strong> Queensland’s council map selects all council areas; Redlands opens ten local divisions. Victoria also has a council atlas.</p>{a('states/qld/councils/index.html','Queensland council map')} {a('states/qld/councils/redland/index.html','Open Redlands')}</article>
 <article><h3>State and territory electorates</h3><p><strong>Atlas foundation: Victoria.</strong> Maps and data for 88 Assembly districts and eight Council regions; the deeper local journeys are still to be built.</p>{a('states/vic/map/index.html','Victoria electorate atlas')} {a('states/vic/election/index.html','Victoria election guide')}</article>
 <article><h3>Federal electorates</h3><p><strong>Context only so far.</strong> Bowman boundary material is available through Redlands. A dedicated federal atlas and electorate journeys have not been built.</p>{a('states/qld/councils/redland/sources/index.html','Bowman and overlapping boundaries')}</article>
 </div></section>
 <!-- redland-local-route:start -->
 <section id="redland-local-journey" class="human-local"><h2>Redlands: keep your thread as you explore</h2><p class="human-local-flow">Queensland → council map → Redlands → a division, question, system, person or piece of evidence → participation → outcomes.</p><p>Keep three accounts together: <strong>what it cost, what was given freely, and what changed.</strong></p>
 {directory('redland',True)}{directory('divisions')}
 </section>
 <!-- redland-local-route:end -->
 <!-- site-page-inventory:start -->
 <section id="all-site-pages" class="human-all-pages"><h2>Every page, grouped by what you want to do</h2><p>Open a group to browse. Search narrows the links; clearing it brings the groups back.</p>
 {''.join(directory(key,key=='start') for key in GROUPS if key not in ('redland','divisions'))}
 </section><!-- site-page-inventory:end -->
 {external_html}
 <details class="human-directory human-agents"><summary><strong>For contributors and agents</strong><span>Rules and review trail</span></summary><p>Separate guides preserve the same human journey without copying local laws, dates or unreviewed claims.</p><ul>
 <li>{a('docs/agents/council-journey-rules.md','Council and division rules')}</li><li>{a('docs/agents/state-electorate-journey-rules.md','State electorate rules')}</li><li>{a('docs/agents/federal-electorate-journey-rules.md','Federal electorate rules')}</li><li>{a('content/history/civic-page-review-register-2026-10-17.json','Dated page and rule review register')}</li></ul></details>
 </main>'''
rendered=header+main+footer
for target in ['pages/site-map.html','content/rooms/site-map.html']:
 (ROOT/target).write_text(rendered,encoding='utf-8')
(ROOT/'content/site-page-inventory.json').write_text(json.dumps({'purpose':'Every public HTML route in the checkout; canonical content mirrors are not separate pages. Navigation review does not refresh source facts.','navigationReviewed':UPDATED,'timezone':'Australia/Brisbane','pageCount':len(inventory),'generator':'tools/build-human-site-map.py','pages':inventory},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Built human site map: {len(inventory)} actual public routes; canonical and public pages match.')
runpy.run_path(str(ROOT/'tools/build-discovery.py'))['build']()
