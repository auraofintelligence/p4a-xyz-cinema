"""Generate the reviewed static Redland example. No network access or auto-redating.

Inputs: content/councils/redland.json, content/local/redland-connections.json,
content/local/redland-election.json, content/local/redland-song-links.json.
See docs/agents/local-place-pattern.md.
"""
from pathlib import Path
import html
import json
import os
import re
from datetime import date
from qld_council_widget import widget as council_widget, assets as council_map_assets, build_delivery, build_division_delivery
from redland_division_pages import build_pages as build_division_pages
from page_review_register import render_register, write_review_notes, reviewed_page_entries

ROOT = Path(__file__).resolve().parents[1]
BASE = "states/qld/councils/redland/"
CHANGED = "2026-10-17"

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))

def e(value):
    return html.escape(str(value if value is not None else ""), quote=True)

def href(page, target):
    if target.startswith(("https://", "http://", "mailto:", "#")):
        return e(target)
    clean, mark, fragment = target.lstrip("/").partition("#")
    rel = os.path.relpath(ROOT / clean.split("?")[0], (ROOT / page).parent).replace("\\", "/")
    if "?" in clean:
        rel += "?" + clean.split("?", 1)[1]
    return e(rel + ("#" + fragment if mark else ""))

def link(page, target, label, cls=""):
    external = target.startswith(("https://", "http://"))
    return f'<a href="{href(page,target)}"' + (f' class="{cls}"' if cls else '') + (' target="_blank" rel="noopener noreferrer"' if external else '') + f'>{e(label)}</a>'

SONG_SOURCES = read('content/local/redland-song-links.json')
SONG_LINKS = {alias: song for song in SONG_SOURCES['songs'] for alias in song['aliases']}

def lyric_link(page, title):
    """Keep the editorial meaning beside a direct, reviewed lyric destination."""
    song = SONG_LINKS[title]
    return link(page, song['url'], title).replace('<a ', f'<a title="{e("Read lyrics and song context: " + song["title"])}" ', 1)

def lyric_meaning(page, meaning):
    for title in sorted(SONG_LINKS, key=len, reverse=True):
        if meaning.startswith(title + ':'):
            return lyric_link(page, title) + e(meaning[len(title):])
    raise ValueError(f'Lyric meaning needs a reviewed song link: {meaning}')

def trinity(cost, free, change):
    return '<div class="local-trinity">' + ''.join(f'<div><strong>{a}</strong><p>{e(b)}</p></div>' for a,b in [("What it cost",cost),("What was given freely",free),("What changed",change)]) + '</div>'

def shell(page, title, intro, body, active="Overview", next_step=None):
    p = lambda target: href(page,target)
    nav = [("Overview","index.html"),("Divisions","divisions/index.html"),("Explore","explore/index.html"),("Possibilities","possibilities/index.html"),("People & elections","candidates/index.html"),("Take part","action/index.html"),("Outcomes","outcomes/index.html"),("Sources & dates","sources/index.html")]
    navhtml = ''.join(link(page,BASE+path,label).replace('<a ', '<a aria-current="page" ',1) if label==active else link(page,BASE+path,label) for label,path in nav)
    if not page.startswith(BASE):
        navhtml=link(page,BASE+'index.html','Enter Redlands')+link(page,BASE+'sources/index.html','Map sources & dates')+link(page,'docs/agents/local-place-pattern.md','Build another local pattern')
    next_html = '' if not next_step else f'<div class="local-next"><p>{e(next_step[0])}</p>{link(page,BASE+next_step[1],next_step[2],"local-button primary")}</div>'
    stamp = next((row['lastUpdated'] for row in reviewed_page_entries() if row['path'] == page and page.startswith(BASE)), CHANGED)
    readable_stamp = date.fromisoformat(stamp).strftime('%d %B %Y').lstrip('0')
    result=f'''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>P4A | {e(title)}</title><meta name="description" content="{e(intro)}"><meta name="theme-color" content="#3f0f75">
<link rel="stylesheet" href="{p('styles.css')}?v=20261016-local"><link rel="stylesheet" href="{p('assets/local-council.css')}?v=20261016-local"></head>
<body data-theme="royal"><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="{p('index.html')}" aria-label="P4A home"><span class="brand-mark">P4A</span><span class="brand-text"><strong>Purple Party</strong><span>for Australia</span></span></a><nav class="site-nav" data-nav aria-label="Primary">{''.join(link(page,t,l) for t,l in [('pages/maps.html','Maps'),('pages/architecture.html','System'),('pages/twinkle.html','Twinkle'),('pages/states.html','States'),('pages/starter-field-kit.html','Start local'),('pages/deployment-gear.html','Gear')])}</nav><button class="index-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-index"><span class="index-toggle-label">Index</span></button></header>
<main id="main" class="local-main"><nav class="local-crumbs" aria-label="Local journey">{link(page,'pages/states.html','States')}<span>/</span>{link(page,'states/qld/index.html','Queensland')}<span>/</span>{link(page,'states/qld/councils/index.html','Councils')}<span>/</span>{link(page,BASE+'index.html','Redlands')}</nav>
<p class="local-kicker">A local path to joyful responsible abundance</p><h1>{e(title)}</h1><p class="local-intro">{e(intro)}</p>
<div class="local-stamp"><span>Started 16 October · Updated <time datetime="{stamp}">{readable_stamp}</time></span><span>Facts carry their own source and period</span>{link(page,BASE+'sources/index.html','What changed & when')}</div>
<nav class="local-nav" aria-label="Redlands paths">{navhtml}</nav>{body}{next_html}
<details class="local-agent"><summary>For a human continuing with an agent</summary><p>Keep the person's question, chosen route and own meaning intact. Distinguish a source, an interpretation and a proposal. Check dates and geography. Carry the three accounts together: cost, freely given contribution and observed change. A page supplies context; action and sharing still follow the person's existing authorisation.</p><p>{link(page,'docs/agents/local-place-pattern.md','Repeat this pattern in another place')} · {link(page,'content/history/redland.md','Dated change record')}</p></details></main>
<footer class="local-footer"><p>P4A is a proposed movement and public workbench. This is a static, reviewed local example. Local questions and systems proposals are invitations to examine and improve; official records remain with their source bodies.</p><nav>{link(page,'pages/site-map.html','Whole site')}{link(page,'pages/braided-economy.html','Braided economy')}{link(page,'pages/musicverse.html','Meanings behind the lyrics')}{link(page,BASE+'sources/index.html','Sources, limits & corrections')}</nav></footer>
<script src="{p('assets/site-nav.js')}?v=20261016-local"></script><script src="{p('assets/local-council.js')}?v=20261016-local"></script></body></html>'''
    if not page.startswith(BASE):
        result=result.replace('<span>/</span>'+link(page,BASE+'index.html','Redlands')+'</nav>','</nav>',1).replace('aria-label="Redlands paths"','aria-label="Council journey choices"')
    return result

def card(page, num, title, copy, target, label):
    return f'<article class="local-card"><span class="local-number">{e(num)}</span><h3>{e(title)}</h3><p>{e(copy)}</p>{link(page,target,label,"local-card-link")}</article>'

def clock(page, election):
    from redland_election import render
    return render(page, election, link)


def map_image(page, item):
    image = item.get("image", item.get("localPath", ""))
    source = item.get("sourceUrl", item.get("source", item.get("pdf", "")))
    if isinstance(source,dict): source=source.get("url","")
    notes = item.get("limits", item.get("notes", ""))
    if isinstance(notes,list): notes=' '.join(notes)
    credits=(link(page,source,'Original map and boundary source') if source else '')+' · '+link(page,image,'Open full-size image')
    if item.get('pdf'):credits+=' · '+link(page,item['pdf'],'Retained original PDF')
    if item.get('mirrorUrl'):credits+=' · '+link(page,item['mirrorUrl'],'Wikimedia source record')
    if item.get('licenceUrl'):credits+=' · '+link(page,item['licenceUrl'],'Reuse conditions')
    return f'''<figure class="local-map"><a class="local-map-link" href="{href(page,image)}" aria-label="Open full-size {e(item.get('title','boundary map'))}"><img src="{href(page,image)}" alt="{e(item.get('alt',item.get('title','Official boundary map')))}" loading="lazy" width="{e(item.get('width',1400))}" height="{e(item.get('height',1000))}"></a><figcaption><strong>{e(item.get('title','Boundary map'))}</strong><br>{e(item.get('attribution',''))} · {e(item.get('edition', item.get('date','')))}<br>{credits}<br>{e(notes)}</figcaption></figure>'''

def gallery(page, maps):
    if not maps: raise ValueError('At least one sourced map required')
    return '<div data-map-gallery><div class="local-map-buttons" role="group" aria-label="Choose a boundary map">'+''.join(f'<button type="button" data-map-choice="map{i}" aria-pressed="{str(i==0).lower()}">{e(m.get("shortTitle",m.get("title","Map")))}</button>' for i,m in enumerate(maps))+'</div>'+''.join(f'<div data-map-panel="map{i}"'+(' hidden' if i else '')+'>'+map_image(page,m)+'</div>' for i,m in enumerate(maps))+'</div><noscript><p>All map files and original sources are also linked on Sources & dates.</p></noscript>'

def source_links(page, sources):
    return '<ul class="local-source">'+''.join(f'<li>{link(page,s.get("url",s.get("href","#")),s.get("title",s.get("label","Source")))}'+(f' · Checked {e(s["checked"])}' if s.get('checked') else '')+'</li>' for s in sources)+'</ul>'

def main():
    build_delivery()
    build_division_delivery()
    write_review_notes()
    data=read('content/councils/redland.json')
    connections=read('content/local/redland-connections.json')
    election=read('content/local/redland-election.json')
    records=connections['records']
    ids={r['id']:r for r in records}
    maps=data['maps']
    regional=[m for m in maps if m.get('id')=='seq-councils']
    localmaps=[m for key in ['redland-divisions','redland-context','oodgeroo','capalaba','redlands-state','springwood','bowman'] for m in maps if m['id']==key]
    if not localmaps:raise ValueError('Reviewed local maps are missing')
    outputs={}
    page='states/qld/councils/index.html'
    overview=map_image(page,regional[0]) if regional else map_image(page,localmaps[0])
    body=f'''<section class="local-split"><div><h2>Find the place. Follow its questions.</h2><p>Start from the state map, then step into the places where people live. Council boundaries locate public responsibilities; neighbourhoods, Country, islands and catchments carry relationships across them.</p><p>This first local example opens <strong>Redland City</strong>. Other Queensland councils have official boundary references below; their P4A journeys are still to be built.</p>{link(page,BASE+'index.html','Enter Redlands',"local-button primary")}<p class="local-source">{link(page,'https://www.ecq.qld.gov.au/electoral-boundaries/local-government-area-boundaries','ECQ: all Queensland local-government boundaries')}</p></div><div>{overview}</div></section><section class="local-section"><div class="local-grid">{card(page,'01','Redland City','Mainland, islands and the connections between daily life and wider systems.',BASE+'index.html','Maps, statistics and choices')}{card(page,'02','Another Queensland council?','Find its official map and public records. The reusable pattern is ready for a reviewed local build.','docs/agents/local-place-pattern.md','Read the agent pattern')}{card(page,'03','A boundary is a lens','A state electorate, federal division and council do different jobs. Compare their extents before comparing statistics.',BASE+'sources/index.html','Check geography and sources')}</div></section>'''
    body=council_widget(page)+f'<section class="local-section"><h2>A familiar pattern at every level.</h2><p>Map, search, select, open. The state map leads to councils; a council leads to its places, questions, data, people and connected possibilities.</p><p>{link(page,"docs/agents/local-place-pattern.md","Repeat the local pattern")}</p></section>'
    outputs[page]=shell(page,'Queensland, council by council.','Choose a place, understand its context, then follow the issues, people and possibilities that matter there.',body).replace('</head>',council_map_assets(page)+'</head>')

    page=BASE+'index.html'
    indicators=data.get('indicators',[])
    source_by_id={s['id']:s for s in data.get('sources',[]) if isinstance(s,dict) and s.get('id')}
    for i in indicators:
        i['sourceUrl']=i.get('sourceUrl') or source_by_id.get(i.get('sourceId'),{}).get('url','https://www.abs.gov.au/')
        i['notes']=i.get('notes',i.get('note',''))
        if not i.get('display'):
            number=f'{i["value"]:,}' if isinstance(i.get('value'),(int,float)) else str(i.get('value',''))
            i['display']=number+('%' if i.get('unit')=='%' else '')
    featured=[i for key in ['erp-2025','median-age-2021','age-65-plus-2021','growth-percent-2025'] for i in indicators if i['id']==key]
    facts='<div class="local-facts">'+''.join(f'<div class="local-fact"><strong>{e(str(i.get("percent"))+"%" if i["id"]=="age-65-plus-2021" else i["display"])}</strong><span>{e(i.get("label",""))}</span><small>{e(i.get("period",""))} · {e(i.get("geography","Redland City"))}</small></div>' for i in featured)+'</div>'
    body=f'''<section><p class="local-kicker">Start where life happens</p><h2>Your place. A few useful paths.</h2><p>A ferry connection, a rates notice, a caring role, a good idea. Each can open a path from an ordinary experience into evidence, people and systems that could change it.</p><p>Joyful responsible abundance asks what would give people more agency, care, belonging and useful time, while keeping responsibilities and consequences visible.</p><p>{link(page,BASE+'explore/index.html','Search local questions and connected systems',"local-button primary")}</p></section>
    {council_widget(page,'division')}
    {facts}<p class="local-source">Snapshots use the period stated on each figure, not the website date. {link(page,BASE+'sources/index.html#statistics','Definitions, newer releases and ABS source links')}</p>
    <section class="local-section"><p class="local-kicker">Choose your own protopia</p><h2>What brought you here?</h2><div class="local-grid">{card(page,'01','A place or everyday problem','Transport, water, care, shade, prices or something that has fallen between systems.',BASE+'action/index.html','Bring your own observation')}{card(page,'02','A system or possibility','Twins, legal memory, freely given contribution, learning and cooperative ownership.',BASE+'possibilities/index.html','See the connections')}{card(page,'03','People and decisions','Public roles, candidate evidence, votes and explanations; possible election paths.',BASE+'candidates/index.html','Inspect public records')}{card(page,'04','Maps and statistics','Council, state and federal boundaries, source periods and the limits of comparison.',BASE+'sources/index.html','Explore the evidence')}{card(page,'05','Something I can contribute','An observation, correction, offer, alternative or a question for the right decision-maker.',BASE+'action/index.html','Prepare a useful next step')}{card(page,'06','What actually changed?','Follow proposed work through decisions, delivery and observed outcomes.',BASE+'outcomes/index.html','Follow the return path')}</div></section>
    {clock(page,election)}<section class="local-section"><h2>Same place. Different borders.</h2><p>Redland City is not interchangeable with Oodgeroo or Bowman. Current state representation uses the 2017 boundaries; the new 2026 state boundaries apply from the 2028 state election. The official map editions and overlap notes stay attached to each lens.</p>{link(page,BASE+'sources/index.html#boundaries','Compare state, federal and historical maps',"local-button")}</section>
    <section class="local-section"><h2>Keep three accounts together.</h2>{trinity('Money, paid work, materials, assets and continuing obligations. Who pays, and who carries the burden?','Chosen time, care, knowledge and resources. Verify contribution with consent; count a human hour once.','Benefits, harm, access, skills, ecology and time. Record what was observed as well as what was hoped for.')}<p>These accounts inform each other. They are not converted into a single score or a fixed dollar value for a C-Hour.</p></section>'''
    outputs[page]=shell(page,'Redlands, from the ground up.','Maps and facts to find your bearings. Local questions to follow. Wider possibilities to explore, build and check together.',body,next_step=('Follow a concern, a possibility, a person or a data trail.','explore/index.html','Explore the connections')).replace('</head>',council_map_assets(page,'division')+'</head>')

    page=BASE+'divisions/index.html'
    body=council_widget(page,'division')+f'<section class="local-section"><h2>From a division into daily life.</h2><p>Select an area, then open its overview for local questions, its current representative and connected systems. The same map, search, select and open pattern repeats here.</p><p>{link(page,BASE+"index.html","Back to the Redlands overview")}</p></section>'
    outputs[page]=shell(page,'Redlands, division by division.','Choose one of ten council divisions, then follow its places, questions, public records and possibilities.',body,active='Divisions').replace('Started 16 October · Updated ','Added 17 October · Reviewed ').replace('</head>',council_map_assets(page,'division')+'</head>')

    page=BASE+'explore/index.html'
    types=list(dict.fromkeys(r['type'] for r in records))
    cards=[]
    for r in records:
        related=''.join(link(page,BASE+'explore/index.html#'+rid,ids[rid]['title']) for rid in r.get('related',[]) if rid in ids)
        nexts=''.join(link(page,n.get('href',n.get('url','#')),n.get('label',n.get('title','Continue'))) for n in r.get('next',[]))
        t=r.get('trinity',{})
        search=' '.join([r['title'],r.get('summary',''),r.get('context',''),r.get('question',''),r['id'],r['type'],str(r.get('place','')), ' '.join(r.get('keywords',[]))]).lower()
        additional=''
        for key in ['question','context','unknowns','meaning','action','agentNote']:
            if r.get(key): additional+=f'<p><strong>{e({"seedStatus":"Seed status","agentNote":"Agent note"}.get(key,key.title()))}:</strong> {e(r[key])}</p>'
        if r.get('lyricMeanings'):
            additional+='<details><summary>Meanings that can travel with this thread</summary><ul class="local-list">'+''.join('<li>'+lyric_meaning(page,m)+'</li>' for m in r['lyricMeanings'])+'</ul></details>'
        summary_copy='<p>'+e(r.get('summary',''))+'</p>'
        cards.append(f'''<details class="local-record" id="{e(r['id'])}" data-local-record data-type="{e(r['type'])}" data-search="{e(search)}"><summary><span class="record-type">{e(r['type'])} · {e(r['id'])}</span><strong>{e(r['title'])}</strong></summary><div class="record-content"><p class="record-state">{e(r.get('status','Draft question'))} · Redland City context</p>{summary_copy}{additional}{trinity(t.get('cost','Not yet estimated.'),t.get('free','Only with consent and verification.'),t.get('change','No local outcome yet verified.'))}<p><strong>Follow the thread</strong></p><div class="local-related">{related}</div><div class="local-related">{nexts}</div>{source_links(page,r.get('sources',[]))}<p class="local-source">{link(page,BASE+'action/index.html?topic='+r['id'],'Add an observation, correction or offer')} · {link(page,BASE+'explore/index.html#'+r['id'],'Link directly to this connection')}</p></div></details>''')
    body=f'''<p>Explore connected systems, public evidence and wider possibilities. System proposals have their own status and evidence. Bring your own observation rather than treating a proposal as a verified local need.</p><form class="local-search" data-local-search role="search"><div class="local-search-row"><div><label for="local-query">What are you looking for?</label><input id="local-query" name="q" type="search" placeholder="Try ferry, caring, rates, shade, truth or time"></div><div><label for="local-type">Kind of connection</label><select id="local-type" name="type"><option value="">All connections</option>{''.join(f'<option value="{e(t)}">{e(t.title())}</option>' for t in types)}</select></div><button class="local-button" data-clear-search type="button">Clear filters</button></div><p class="local-results-note" data-result-count aria-live="polite">{len(records)} connections</p></form><p class="local-empty" data-no-results hidden>No matching connection yet. Try a broader word or clear the filters. {link(page,BASE+'action/index.html','Keep the question and prepare an observation')}.</p><noscript><p>Search needs JavaScript; all connections and their links are readable below.</p></noscript>{''.join(cards)}'''
    outputs[page]=shell(page,'Follow a local thread.','Explore connections to systems, public evidence and wider possibilities in the Redlands context.',body,'Explore',('Take one connection into a wider picture.','possibilities/index.html','Explore possibilities'))

    page=BASE+'possibilities/index.html'
    stories=[('A short appointment. A whole-day journey.','A trip can connect ferry and bus timetables, accessibility, a carer\'s paid work, health appointments and cost. Start by mapping an actual journey with consent. Compare changes across the whole route before calling one segment a success.',['sys-mobility','sys-health','sys-twin','sys-chour']),('A hot afternoon. A shared resilience question.','Shade, water, power, communications and support for someone living alone cross asset and organisational boundaries. A civic twin can make dependencies inspectable; a community contribution record can show chosen care without replacing public services.',['sys-resilience','sys-energy','sys-twin','sys-learning']),('A public decision. A visible chain of reasons.','Join a claim to the motion, the meeting record, its stated explanation, the money committed and the result. Legal memory can help locate powers and routes for challenge. A possible explanation remains an interpretation, even when it sounds plausible.',['sys-truth','sys-law','sys-democracy','sys-wealth'])]
    body='<section><h2>One experience can connect several systems.</h2><p>People begin with their own lives, relationships and aspirations. Common systems become useful when they help that work. A council can be a participant, decision-maker or partner; wider possibilities can also grow through neighbours, cooperatives, learning and new institutions.</p></section>'
    for title,copy,related in stories:
        body+=f'<article class="local-panel"><h2>{e(title)}</h2><p>{e(copy)}</p><div class="local-related">'+''.join(link(page,BASE+'explore/index.html#'+rid,ids[rid]['title']) for rid in related if rid in ids)+'</div>'+trinity('Compare a baseline, alternatives, funding and continuing costs. Unknown is not zero.','Record chosen care, local knowledge, teaching and repair once, with permission.','Measure a whole journey, continuity of care or a decision outcome, including who gained time and who lost it.')+'</article>'
    body+=f'''<section class="local-section"><h2>The surrounding world belongs in the picture.</h2><p>Household prices, conflict and supply chains, AI and work, climate risk and the 2032 Games can affect local lives. Follow those connections through current evidence rather than treating a forecast as certain. The local path can lead outward to ownership, livelihoods, resource sharing and democratic reform, then return to what changed here.</p><div class="local-related">{link(page,'pages/international-wars.html','Conflict and global pressures')}{link(page,'pages/workforce-transition.html','AI, work and learning')}{link(page,'pages/twinkle-olympics.html','2032 and its legacy')}{link(page,'pages/braided-economy.html','Braided economy')}{link(page,'pages/cyber-republic.html','Wider democratic rehearsal')}</div></section><section class="local-section"><p class="local-kicker">The meanings can travel with you</p><h2>Repair, choice, care and a wider horizon.</h2><p>The lyrics offer overlapping ways to understand the journey. Select a song title to read its lyrics and song context on the creator's music site. {lyric_link(page,'Kintsugi Protocol')} brings repair and learning; {lyric_link(page,'Choose Your Own Protopia')} and {lyric_link(page,'Adaptable Yes')} carry choice and consent. {lyric_link(page,'Strange But True')} makes room for patient, practical help. {lyric_link(page,'The Purple Mat That Could')} begins with an ordinary frustration; {lyric_link(page,"Don't Throw a Brick")} asks how questions become accountable public action.</p><p>{lyric_link(page,'Shifting Sands of Timeless Redlands')} keeps place, water, history and belonging present. {lyric_link(page,'Every Border a Bridge')} and {lyric_link(page,'We Go Beyond')} let local relationships reach outward. {lyric_link(page,'ChatGPT: My View of Our Conversation')} asks the human and agent to notice how meaning is interpreted, missed and corrected.</p><p>{lyric_link(page,'60 Days Set in Stone')} and the optional Aura Genesis journey sit with a person's chosen learning and reflection, within the people and candidates path.</p><div class="local-related">{link(page,'pages/musicverse.html','Explore the existing lyric meanings')}{link(page,BASE+'candidates/index.html#learning','Personal learning, reflection and public responsibility')}</div><p class="local-source">Editorial readings of the creator's lyrics, not evidence that a proposed clinical or civic system has achieved its aims.</p></section>'''
    outputs[page]=shell(page,'Local life. Wider possibilities.','A concern can reveal a system. A system can free time, change ownership, deepen care and create room for a different future.',body,'Possibilities',('Keep the purpose, then identify what would let the work happen.','action/index.html','Find a way to take part'))

    page=BASE+'candidates/index.html'
    body=clock(page,election)+f'''<section class="local-section"><h2>People first. Evidence alongside.</h2><p>Use the same questions for every public representative and candidate: their public history, responsibilities, positions, records, sources and corrections. Being in office does not establish that someone is running again.</p><div class="local-grid">{card(page,'Council','Mayor and councillors','Start with council\'s current public directory, division and responsibilities. Use meeting records to examine a decision.','https://www.redland.qld.gov.au/About-Council/Mayor-and-Councillors','Official council directory')}{card(page,'State','Your Queensland representative','Use the current-boundary address lookup, then Parliament\'s member and proceedings records. Four state districts intersect the council in the sourced map review.','https://www.parliament.qld.gov.au/Members/Current-Members/Member-List','Queensland members')}{card(page,'Federal','Bowman and its boundary','Bowman overlaps Redland City but is not the same geography. Check the AEC map before using seat-level figures.','https://www.aph.gov.au/Senators_and_Members/Members','Federal member directory')}</div></section>
    <section class="local-section" id="voting"><h2>A vote needs its context.</h2><div class="local-table-scroll"><table class="local-table"><caption>How a public record should be read</caption><thead><tr><th>Record</th><th>Show alongside it</th><th>Keep the distinction</th></tr></thead><tbody><tr><td>Motion, amendment or division</td><td>Date, body, exact question, member's recorded position, outcome and original source</td><td>Absent, recused and not recorded are different. An amendment vote is not automatically a position on the whole proposal.</td></tr><tr><td>Why?</td><td>An attributable explanation, speech, interview or meeting record</td><td>Stated reason / possible explanation / reason not found. Do not invent a motive.</td></tr><tr><td>History and follow-through</td><td>What was said, what was decided, what was delivered and corrected</td><td>A mismatch opens a question; it does not by itself prove intent.</td></tr></tbody></table></div><div class="local-related">{link(page,'https://www.redland.qld.gov.au/About-Council/Council-meetings/Council-meeting-minutes-and-agendas','Council minutes and agendas')}{link(page,'https://webcast.redland.qld.gov.au/','Council webcasts')}{link(page,'https://www.parliament.qld.gov.au/Work-of-the-Assembly/Record-of-Proceedings','Queensland proceedings')}{link(page,'https://theyvoteforyou.org.au/','Federal recorded divisions: They Vote For You')}{link(page,'https://www.openaustralia.org.au/','Federal speeches: OpenAustralia')}</div><p class="local-source">These are public-record routes, not a completed local roll-call database or candidate directory. Federal tracker coverage must not be presented as council coverage.</p></section>
    <section class="local-panel" id="learning"><p class="local-kicker">An optional part of a person's public account</p><h2>Learning and reflection belong here.</h2><p>Someone in Redlands could choose to document a first Aura Genesis journey: what they hoped to learn, what they chose to share, what they reconsidered and what evidence emerged. This is a hypothetical pathway, with no named participant or implied candidacy.</p><p>{lyric_link(page,'Kintsugi Protocol')}, {lyric_link(page,'60 Days Set in Stone')} and the Truth Engine can connect self-examination to public responsibility. Personal reflection stays distinct from verified public facts, clinical evidence and the responsibilities of office. Private material remains private unless its author chooses otherwise.</p><div class="local-related">{link(page,'pages/aura-genesis.html','Aura Genesis proposal and learning context')}{link(page,'pages/truth-engine.html','Claims, evidence and corrections')}{link(page,'pages/private-civic-profile-builder.html','Private civic profile')}{link(page,'pages/musicverse.html','Lyric meanings')}</div></section>
    <section class="local-section"><h2>If a mayoral by-election is called.</h2><p>Begin with an official vacancy and election notice, then use the current ECQ candidate guidance. A possible by-election is a branch in this journey; it does not need to happen for local work to continue.</p>{''.join(f'<div class="local-step"><span>{n:02}</span><div><h3>{e(t)}</h3><p>{e(c)}</p></div></div>' for n,(t,c) in enumerate([('Understand the role','Separate the mayor\'s responsibilities from decisions requiring council, officers, another government or a service provider. Identify the power and resources needed for each proposal.'),('Consider, stand aside or nominate','Eligibility, training, accounts, expenditure and disclosure obligations need current official guidance. Some obligations can begin before formal nomination. Deciding not to stand is a valid branch.'),('A clear public account','Show proposals, sources, status, costs, volunteered contributions and intended outcomes. Record announcements separately from accepted nominations; any withdrawal follows the applicable official rules.'),('An outcome and a handover','If elected, connect proposals to decisions, budget, delivery, review and the remaining statutory term. A year of service is an illustrative scenario, not a guaranteed term. If not elected, local projects can still continue.')],1))}<div class="local-related">{link(page,'https://www.ecq.qld.gov.au/election-participants/local-election-participants/candidates','Current ECQ candidate guide')}{link(page,'https://disclosures.ecq.qld.gov.au/','ECQ public disclosures')}{link(page,BASE+'action/index.html','Community work and formal pathways')}</div></section>'''
    outputs[page]=shell(page,'People, records and possible elections.','Understand public responsibilities, inspect the evidence and follow the official process if an election is called.',body,'People & elections',('A public question can lead to a correction, an offer or a formal decision.','action/index.html','Choose a useful action'))

    page=BASE+'action/index.html'
    body=f'''<section><h2>Start with what you want to change.</h2><p>Keep the original experience and the desired change in the person's own words. Then choose the people, resources and permissions needed. Several routes may work together.</p><div class="local-grid">{card(page,'With people','Act through chosen relationships','A neighbour, club, cooperative or learning group can test an idea using resources and consent it already has.','pages/civic-twin-builders.html','Existing community builders')}{card(page,'With an organisation','Make an inspectable proposal','Who owns the asset, carries the duty, controls the budget or can agree to the change? Evidence and local knowledge can make an offer useful.',BASE+'explore/index.html?type=system','Find a connected system')}{card(page,'With new rules','Design beyond the current arrangement','A different ownership model, agreement or democratic rule may need legal research, broader participation and a public decision.','pages/legal-rag.html','Follow the legal source trail')}</div></section>
    <section class="local-section"><h2>A shared pattern for making it real.</h2>{''.join(f'<div class="local-step"><span>{n:02}</span><div><h3>{e(t)}</h3><p>{e(c)}</p></div></div>' for n,(t,c) in enumerate([('Notice and map','Record the place, time and lived experience. Protect home addresses, health information and other people\'s privacy. Similar reports are a lead to investigate, not automatically a mandate.'),('Compare possible changes','Use the civic twin as an inspectable scenario: show assumptions, alternatives, dependencies and uncertainty. Link the relevant legal source, service provider and decision pathway.'),('Agree the work','Identify who can authorise it, paid and voluntary roles, resources, learning, time and review points. A simulation or draft agreement is not permission to act.'),('Try, observe and learn','Record delivery separately from a measured result. Preserve disagreement and corrections. Hand over enough context that another human or agent can continue.')],1))}</section>
    {trinity('Identify a budget, funding source, paid work, materials and maintenance. Do not put a zero where an estimate is missing.','Make care, local knowledge, learning and voluntary effort visible with consent. One verified human hour is counted once, even if it supports several goals.','Choose a baseline and a way to observe benefit, harm and time. Who gained access or agency? Who took on extra work?')}
    <section class="local-section"><h2>Keep a portable journey note.</h2><p>This form prepares a private Markdown download for you to review or share with an agent. It does not send anything to P4A, council or another person. Avoid adding anyone else's private details.</p><form class="local-form" data-journey-note><label>Your question or hoped-for change<textarea name="My purpose" required placeholder="Keep this in your own words"></textarea></label><div class="local-form-pair"><label>Place or connection<input name="Place or thread" placeholder="A locality, island, journey or record ID"></label><label>Useful next route<select name="Chosen route"><option>Observation or correction</option><option>Offer time, knowledge or resources</option><option>Compare a possible solution</option><option>Ask an organisation for a decision</option><option>Learn about candidacy or public responsibility</option></select></label></div><label>Evidence and what is still unknown<textarea name="Evidence and uncertainty" placeholder="Source links, observation date, what needs checking"></textarea></label><div class="local-form-pair"><label>What it cost<textarea name="Cost and obligations"></textarea></label><label>What was given freely<textarea name="Freely given contribution"></textarea></label></div><label>What changed, or how we would check<textarea name="Intended and observed change"></textarea></label><label>What my agent may do or share<textarea name="Authorisation and sharing boundaries" placeholder="Reading, drafting and public submission are different actions"></textarea></label><div><button class="local-button primary" type="submit">Download my journey note</button></div><p data-note-status aria-live="polite"></p></form></section>
    <section class="local-panel"><h2>Take the authorised next step.</h2><p>A downloaded note is a draft, not a lodged report. Use the relevant service's own channel for an actual request or formal submission, and retain its reference and response.</p><div class="local-related">{link(page,'https://www.redland.qld.gov.au/About-Council/Contact-Us','Contact Redland City Council')}{link(page,'pages/noticeboard-contract-builder.html','Prepare a notice or agreement')}{link(page,'pages/c-hour-receipt-builder.html','Explore contribution receipts')}{link(page,'pages/civic-surges.html','Prepare a civic surge')}{link(page,BASE+'outcomes/index.html','Track the response and result')}</div></section>'''
    outputs[page]=shell(page,'Make a useful next move.','An observation, correction, offer, alternative or public proposal can carry the original human purpose into meaningful action.',body,'Take part',('Return to what was delivered and what it changed.','outcomes/index.html','Follow outcomes'))

    page=BASE+'outcomes/index.html'
    body=f'''<section><h2>The return path matters.</h2><p>Keep the chain visible: a lived question, an idea, a source, an agreement, a decision, delivery and a result. Progress can include a corrected assumption, a clearer responsibility or a decision to stop.</p><div class="local-table-scroll"><table class="local-table"><caption>A record can move through these states without skipping the evidence</caption><thead><tr><th>Stage</th><th>Evidence to retain</th><th>Question to carry forward</th></tr></thead><tbody>{''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a,b,c in [('Proposed','Purpose, alternatives, assumptions and baseline','What should improve, and for whom?'),('Authorised or committed','Named decision-maker, scope, resources and agreement','Who has agreed to what?'),('Submitted or acknowledged','Lodgement receipt, date and reference','Has the right body actually received it?'),('Delivered','Work record and actual costs or contributions','Was the promised work completed?'),('Observed','Measurement period, benefits, harm and uncertainty','What changed beyond the activity itself?'),('Revised or handed over','Correction, explanation and next responsible person','What should happen next?')])}</tbody></table></div></section>{trinity('Compare planned and actual spending, paid work and continuing liabilities. Record the source and period.','Keep verified hours and other chosen contributions distinct. No fixed cash conversion or repeated claim for the same hour.','Look for access, care, ecology, confidence, ownership, relationships and time freed. Include burden shifted and those still excluded.')}
    <section class="local-panel"><p class="local-kicker">First build · 16 October 2026</p><h2>What exists in this example?</h2><p>The journey, reviewed source maps, dated figures, searchable questions and connections, election clock and private-note download are implemented. There are no verified local project outcomes or issued C-Hours in this demonstration.</p><p>Local work can continue whether or not a by-election occurs, a person stands, or a proposed system is adopted. The record should explain what continued, changed or was handed over.</p>{link(page,BASE+'sources/index.html#changes','Inspect this build and its change record')}</section><section class="local-section"><h2>Repair stays visible.</h2><p>A correction should keep the earlier claim, what changed, the evidence and the date. {lyric_link(page,'Kintsugi Protocol')} gives that practice a human meaning: repair can remain part of the story. A truthful record makes room for learning without hiding responsibility.</p><div class="local-related">{link(page,BASE+'explore/index.html','Follow another thread')}{link(page,BASE+'action/index.html','Prepare a correction or next step')}{link(page,'docs/agents/local-place-pattern.md','Repeat the pattern elsewhere')}</div></section>'''
    outputs[page]=shell(page,'What changed, and for whom?','Keep promises, work and outcomes distinct. Bring the learning back to the people and places where the journey began.',body,'Outcomes')

    page=BASE+'sources/index.html'
    rows=''.join(f'<tr><td>{e(i.get("label",""))}</td><td>{e(i.get("display",i.get("value","")))} {e(i.get("unit","") if i.get("unit")!="%" else "")}</td><td>{e(i.get("period",""))}<br>{e(i.get("geography","Redland City"))}</td><td>{e(i.get("notes",""))}<br>{link(page,i["sourceUrl"],"Original source")} · Checked {e(i.get("checkedAt",CHANGED))}</td></tr>' for i in indicators)
    sources=data.get('sources',[])
    if isinstance(sources,dict): sources=[dict(v,id=k) if isinstance(v,dict) else {'title':k,'url':v} for k,v in sources.items()]
    mapbody=''.join(f'<article class="local-panel">{map_image(page,m)}<p class="local-source">Retrieved/checked: {e(m.get("retrievedAt",m.get("retrieved",m.get("checked",data.get("checkedAt",CHANGED)))))}. Rights: {e(m.get("rights",m.get("license","See original source conditions; not relicensed by P4A.")))}</p></article>' for m in maps)
    notes=data.get('boundaryNotes',data.get('geographyNotes',data.get('notes',[])))
    if isinstance(notes,str):notes=[notes]
    body=f'''<section id="statistics"><h2>Statistics with their period attached.</h2><p>A 2026 research check does not turn 2021 Census figures into 2026 Census results. Population estimates and census counts are different measures; the geography and reference date must travel with each number.</p><div class="local-table-scroll"><table class="local-table"><caption>Reviewed local indicators</caption><thead><tr><th>Indicator</th><th>Figure</th><th>Period and geography</th><th>Definition, limit and source</th></tr></thead><tbody>{rows}</tbody></table></div>{source_links(page,sources)}<p>{link(page,'https://www.abs.gov.au/census','ABS Census releases and latest information')}</p></section><section class="local-section" id="boundaries"><h2>Boundary maps, without invented shapes.</h2><p>These are local raster copies of actual source maps. They are not georeferenced overlays, parcel advice or a statistical intersection calculation. Different editions and scales cannot establish a percentage overlap by visual comparison.</p><ul class="local-list">{''.join('<li>'+e(n)+'</li>' for n in notes)}</ul>{mapbody}</section>
    <section class="local-section" id="changes"><h2>What changed on 16 October 2026.</h2><ul class="local-list"><li>Connected the Queensland portal and architecture page to a public council route, with Redland City as the implemented example.</li><li>Added real boundary-map images, a dated local data snapshot, searchable local questions and links to existing proposals and public records.</li><li>Added the candidate and public-responsibility path, with optional Genesis reflection inside it.</li><li>Added the scheduled election countdown, explicit unknown early-voting dates and the conditional by-election branch.</li><li>Added the private journey-note download, three linked accounts and an outcomes/learning route.</li><li>Recorded the source schema, update triggers and reuse pattern for other councils and electorates.</li></ul><p>The clock updates as time passes. Underlying political facts, boundaries, early-voting dates and statistics update only after a source review.</p><div class="local-related">{link(page,'content/history/redland.md','Full dated local history')}{link(page,'content/local/redland-election.json','Election dates and review status')}{link(page,'content/councils/redland.json','Map and statistics source data')}{link(page,'content/local/redland-connections.json','Questions and connections')}{link(page,'docs/agents/local-place-pattern.md','Repeatable agent report')}</div></section><section class="local-panel"><h2>Corrections have a place in the journey.</h2><p>Bring the source, date, affected figure or statement and your proposed correction. A shared link can point directly to a connection. This first pass accepts no online submissions; prepare a note and use an authorised external route when ready.</p>{link(page,BASE+'action/index.html','Prepare a correction or evidence note',"local-button")}</section>'''
    from redland_election import sources_section
    body=render_register(page,link)+sources_section(page,election,link)+body
    outputs[page]=shell(page,'Sources, boundaries and change dates.','Inspect where the maps and numbers came from, what they describe and what will need another check when conditions change.',body,'Sources & dates')
    outputs.update(build_division_pages(shell))
    from redland_election import apply_page
    for path, text in outputs.items():
        text=apply_page(path, text, election, link)
        text=text.replace('?type=system','?type=solution')
        text=text.replace('First build · 16 October 2026','First build · 16-17 October 2026')
        text=text.replace('What changed on 16 October 2026.','What changed on 16-17 October 2026.')
        text=text.replace('<form class="local-form" data-journey-note>','<noscript><p>The private download needs JavaScript. The form stays disabled so a note cannot be submitted accidentally.</p></noscript><form class="local-form" data-journey-note><fieldset disabled data-note-fields style="border:0;padding:0;margin:0;display:grid;gap:17px;min-width:0">')
        text=text.replace('<p data-note-status aria-live="polite"></p></form>','<p data-note-status aria-live="polite"></p></fieldset></form>')
        dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text+'\n',encoding='utf-8')
    integrate(outputs)
    print(f'Generated {len(outputs)} static pages from {len(records)} connected records, {len(maps)} maps and {len(indicators)} indicators. Source dates preserved.')

def integrate(outputs):
    """Add scoped entry routes while preserving unrelated editorial changes."""
    start='<!-- redland-local-route:start -->'
    end='<!-- redland-local-route:end -->'
    def insert(path,block,before='</main>'):
        file=ROOT/path
        if not file.exists():return
        text=file.read_text(encoding='utf-8')
        wrapped=start+'\n'+block+'\n'+end
        if start in text:
            text=re.sub(re.escape(start)+r'[\s\S]*?'+re.escape(end),lambda _:wrapped,text,count=1)
        else:
            if before not in text: raise ValueError(f'Entry marker missing in {path}')
            text=text.replace(before,wrapped+'\n'+before,1)
        file.write_text(text,encoding='utf-8')
    page='states/qld/index.html'
    block='<div class="section">'+council_widget(page)+'</div>'
    file=ROOT/page;text=file.read_text(encoding='utf-8')
    if start not in text:
        marker='<section class="section state-summary-grid">'
        if marker not in text:raise ValueError('QLD summary marker missing')
        text=text.replace(marker,start+'\n'+block+'\n'+end+'\n'+marker,1)
        file.write_text(text,encoding='utf-8')
    else:insert(page,block)
    text=file.read_text(encoding='utf-8').replace('<a href="../../states/qld/architecture/index.html">Architecture builder</a>','<a href="councils/index.html">Councils &amp; Redlands</a>')
    text=text.replace('QLD starts from Brisbane and works outward: current power, chamber balance, election clocks and the local civic rehearsal layer that can plug back into the national P4A preframe.','Start with your place in Queensland: councils, communities and connected public responsibilities. Explore the map below alongside state representation and election information.')
    text=text.replace('<a href="councils/index.html">Councils &amp; Redlands</a>','<a href="#qld-council-map">Council map</a>')
    if 'assets/qld-council-map.css' not in text:text=text.replace('</head>',council_map_assets(page)+'</head>',1)
    file.write_text(text,encoding='utf-8')
    page='states/qld/architecture/index.html'
    block=f'''<section class="section"><div class="feature-panel"><p class="eyebrow">Council map route · Added 16 October 2026</p><h2>Open the public council journey.</h2><p>Queensland now has a council entry and a Redland City example. Use actual sourced map images, dated statistics and connected local questions before returning to the deeper architecture work.</p><div class="button-row">{link(page,'states/qld/councils/index.html','Choose a council','button')}{link(page,BASE+'index.html','Explore Redlands','button button-secondary')}{link(page,'docs/agents/local-place-pattern.md','Repeat the local pattern','button button-secondary')}</div></div></section>'''
    file=ROOT/page;text=file.read_text(encoding='utf-8')
    anchor=text.find('<p class="eyebrow">State map builder</p>')
    if anchor>=0:
        begin=text.rfind('<section',0,anchor);finish=text.find('</section>',anchor)+len('</section>')
        text=text[:begin]+start+'\n'+block+'\n'+end+text[finish:]
        file.write_text(text,encoding='utf-8')
    else:insert(page,block)
    for page in ['pages/maps.html','content/rooms/maps.html']:
        publicpage='pages/maps.html' if page=='content/rooms/maps.html' else page
        block=f'''<section class="section"><div class="feature-panel"><p class="eyebrow">Queensland local example · 16 October 2026</p><h2>From the state map into Redlands.</h2><p>Actual boundary-map images, local statistics, searchable questions and systems, people and records, participation and outcomes.</p><div class="button-row">{link(publicpage,'states/qld/councils/index.html','Queensland councils','button')}{link(publicpage,BASE+'index.html','Redlands journey','button button-secondary')}</div></div></section>'''
        insert(page,block)
    # The shared Index keeps its original thematic hierarchy in assets/site-nav.js.
    # Local discovery belongs inside States and the existing state/map pages.
    # The national map is an actual Wikimedia PNG. Labels navigate; they do not
    # claim exact electoral polygon picking. Keep the existing accessible cards.
    labels=[('wa','Western Australia','WA',94,178),('nt','Northern Territory','NT',226,112),('qld','Queensland','QLD',360,132),('sa','South Australia','SA',247,244),('nsw','New South Wales','NSW',358,286),('vic','Victoria','VIC',340,346),('tas','Tasmania','TAS',371,396),('act','Australian Capital Territory','ACT',401,316)]
    for page in ['pages/states.html','pages/maps.html','content/rooms/maps.html']:
        file=ROOT/page
        if not file.exists():continue
        publicpage='pages/maps.html' if page=='content/rooms/maps.html' else page
        raster='<div class="state-raster-map" aria-label="Australian state and territory map"><img src="'+href(publicpage,'assets/maps/australian-states-wikipedia.png')+'" width="1280" height="1169" alt="Wikimedia map of Australian state and territory boundaries">'+''.join(f'<a class="state-raster-label" data-map-state="{slug}" style="left:{x/460*100:.3f}%;top:{y/420*100:.3f}%" href="{href(publicpage,"states/"+slug+"/index.html")}" aria-label="Open {name} portal">{short}</a>' for slug,name,short,x,y in labels)+'</div>'
        credit='<p class="state-map-source">Actual Wikimedia map: '+link(publicpage,'https://commons.wikimedia.org/wiki/File:Australian_states_map.svg','Australian states map by PoliticsMaps')+', 9 March 2024, CC0. PNG rendered by Wikimedia; acquired 17 October 2026. Select a state label or use the cards below. '+link(publicpage,'assets/maps/australian-states-wikipedia.json','Map attribution and dates')+'</p>'
        text=file.read_text(encoding='utf-8')
        text=re.sub(r'<svg class="australia-state-map"[\s\S]*?</svg>',lambda _:raster,text,count=1)
        text=re.sub(r'<p class="state-map-source">[\s\S]*?</p>',lambda _:credit,text,count=1)
        file.write_text(text,encoding='utf-8')

if __name__=='__main__':
    main()
    from national_place_links import apply_existing_links
    apply_existing_links()
