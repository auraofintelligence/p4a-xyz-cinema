"""Build sourced civic directories and place pages; never acquire or redating facts.

Inputs: content/places/{councils,state,federal}.json. Existing Victoria/Redland
workbenches remain. Rebuild all, or use --jurisdiction/--scope/--place to limit
detail output. Shared route/data indexes still represent the complete source.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import html
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
UPDATED = '2026-10-23'
NAMES = {'act':'Australian Capital Territory','nsw':'New South Wales','nt':'Northern Territory','qld':'Queensland','sa':'South Australia','tas':'Tasmania','vic':'Victoria','wa':'Western Australia'}
SCOPES = {'councils': 'Councils and local areas', 'state': 'State and territory electorates', 'federal': 'Federal representation'}
KINDS = {'council':'Local council','ward':'Council electoral area','unincorporated-area':'Unincorporated area','special-local-body':'Special local body','state-district':'State/territory district','state-region':'State upper-house region','statewide-upper-house':'Statewide upper house','federal-division':'House of Representatives division','senate-area':'Senate state/territory area'}
WRITTEN = []


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    data = value.encode('utf-8') if isinstance(value, str) else value
    if not target.exists() or target.read_bytes() != data:
        target.write_bytes(data)
        WRITTEN.append(path)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def esc(value):
    return html.escape(str(value if value is not None else ''), quote=True)


def rel(page, path):
    if str(path).startswith(('https://', 'http://', 'mailto:')):
        return str(path)
    path, sep, anchor = str(path).partition('#')
    return os.path.relpath(ROOT / path, (ROOT / page).parent).replace('\\', '/') + (sep + anchor if sep else '')


def link(page, path, label, cls=''):
    external = str(path).startswith(('https://', 'http://'))
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a href="{esc(rel(page, path))}"{attrs}' + (f' class="{cls}"' if cls else '') + f'>{esc(label)}</a>'


def slug(value):
    return re.sub('[^a-z0-9]+', '-', str(value).lower()).strip('-')


def route(place):
    state, kind = place['jurisdiction'], place['kind']
    key = place.get('slug') or slug(place['name'])
    if kind in ('council', 'special-local-body', 'unincorporated-area'):
        if state == 'qld' and (str(place.get('featureId')) == '6250' or key in ('redland', 'redland-city')):
            return 'states/qld/councils/redland/elections/index.html'
        return f'states/{state}/councils/{key}/index.html'
    if kind == 'ward':
        return f'states/{state}/local-electoral-areas/{slug(place["id"])}/index.html'
    if kind == 'senate-area':
        return f'states/{state}/federal/senate/index.html'
    if kind == 'federal-division':
        return f'states/{state}/federal/{key}/index.html'
    branch = 'districts' if kind == 'state-district' else 'regions'
    return f'states/{state}/electorates/{branch}/{key}/index.html'


def directory_route(state, scope=None):
    return f'states/{state}/places/' + (scope + '/' if scope else '') + 'index.html'


def load():
    places, layers, sources, inputs = [], [], {}, {}
    for scope in SCOPES:
        file = ROOT / f'content/places/{scope}.json'
        if not file.exists():
            raise SystemExit(f'Missing reviewed input {file.relative_to(ROOT)}; acquire source records before building.')
        data = json.loads(file.read_text(encoding='utf-8-sig'))
        inputs[scope] = data
        for source in data.get('sources', []):
            sources[source['id']] = source
        for layer in data.get('layers', []):
            layers.append({**layer, 'scope': scope})
        for place in data['places']:
            if place['jurisdiction'] not in NAMES:
                # External territories retain their actual context through official
                # source links; they must not become invented ninth-state portals.
                continue
            places.append({**place, 'scope': scope, 'url': route(place)})
    # Whole-jurisdiction chambers use sourced geographic context rather than
    # invented district subdivisions. Distinct layer IDs keep institutions apart.
    state_context = next((l for l in layers if l['id']=='national-state-context'),None)
    state_codes = {'nsw':'1','vic':'2','qld':'3','sa':'4','wa':'5','tas':'6','nt':'7','act':'8'}
    if state_context:
        for p in places:
            if not p.get('layerId') and p['kind'] in ('senate-area','statewide-upper-house'):
                layer_id = 'context-'+p['kind']+'-'+p['jurisdiction']
                note = 'Geographic state/territory context from ABS; this is not a legal voting-entitlement boundary or a map of subdivisions within this chamber.'
                layers.append({**state_context,'id':layer_id,'jurisdiction':p['jurisdiction'],'kind':p['kind'],'scope':p['scope'],'name':p.get('chamber',KINDS[p['kind']])+' · geographic context','coordinateNote':note})
                p.update(layerId=layer_id,featureId=state_codes[p['jurisdiction']],contextMapNote=note)
                p['sources']=list(dict.fromkeys(p.get('sources',[])+[state_context['sourceId']]))
    ids = [p['id'] for p in places]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate stable place identity')
    paths = [p['url'] for p in places]
    if len(paths) != len(set(paths)):
        raise ValueError('Two places share an output route; use distinct area/chamber identities')
    return places, layers, sources, inputs


def prepare_layers(layers):
    """Gzip exact JSON bytes. No quantisation, ring omission or geometry edits."""
    records = []
    for layer in layers:
        raw_file = ROOT / layer['geometryFile']
        if not raw_file.exists():
            layer['unavailable'] = True
            continue
        raw = raw_file.read_bytes()
        if raw_file.suffix == '.gz':
            layer['compressedFile'] = layer['geometryFile']
            original = gzip.decompress(raw)
            plain = layer['geometryFile'][:-3]
            # A compressed original is a complete lossless public delivery.
            # Never expand large source layers into an unpublishable duplicate.
            # Keep optional expanded copies below 25 MiB. Larger exact gzip
            # originals avoid duplicating hundreds of MiB in GitHub Pages.
            if len(original) < 25 * 1024 * 1024 and (ROOT / plain).exists() and (ROOT / plain).stat().st_size < 25 * 1024 * 1024:
                if (ROOT / plain).read_bytes() != original:
                    write(plain, original)
                layer['geometryFile'] = plain
            raw = original
        else:
            compressed_path = layer['geometryFile'] + '.gz'
            prior = (ROOT/compressed_path).read_bytes() if (ROOT/compressed_path).exists() else None
            compressed = prior if prior is not None and gzip.decompress(prior) == raw else gzip.compress(raw, compresslevel=9, mtime=0)
            write(compressed_path, compressed)
            assert gzip.decompress(compressed) == raw
            layer['compressedFile'] = compressed_path
        data = json.loads(raw.decode('utf-8-sig'))
        if data.get('type') != 'FeatureCollection':
            raise ValueError(f'Not GeoJSON: {layer["id"]}')
        records.append({'id': layer['id'], 'source': layer['geometryFile'], 'compressed': layer['compressedFile'],
                        'sha256': hashlib.sha256(raw).hexdigest(), 'features': len(data['features']),
                        'bytes': len(raw), 'compressedBytes': (ROOT / layer['compressedFile']).stat().st_size,
                        'coordinateChange': 'none; gzip byte equality verified', 'boundaryEdition': layer.get('boundaryEdition'), 'crs': layer.get('crs'), 'nativeCrs':layer.get('nativeCrs'), 'coordinateNote':layer.get('coordinateNote')})
    write('content/places/geometry-delivery.json', json.dumps({'updated': UPDATED, 'method': 'Original source JSON, exact gzip byte round trip; no simplification', 'layers': records}, ensure_ascii=False, indent=2) + '\n')


def header(page):
    doors = [('pages/rabbit-hole.html','Map'),('pages/architecture.html','System'),('pages/twinkle.html','Twinkle'),('pages/states.html','States'),('pages/starter-field-kit.html','Start local'),('pages/deployment-gear.html','Gear')]
    return f'''<header class="site-header"><a class="brand" href="{rel(page,'index.html')}" aria-label="P4A home"><span class="brand-mark">P4A</span><span class="brand-text"><strong>Purple Party</strong><span>for Australia</span></span></a><nav class="site-nav" data-nav aria-label="Primary">{''.join(link(page,path,label) for path,label in doors)}</nav><button class="index-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-index"><span class="index-toggle-label">Index</span></button></header>'''


def shell(page, title, body, description=None):
    return f'''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#30104c"><title>{esc(title)} | P4A</title><meta name="description" content="{esc(description or title + ': boundaries, public representatives, election history and sources.')}"><link rel="icon" href="{rel(page,'assets/favicon.svg')}"><link rel="stylesheet" href="{rel(page,'styles.css')}?v=20261017"><link rel="stylesheet" href="{rel(page,'assets/civic-places.css')}?v=20261017"><script src="{rel(page,'assets/civic-places.js')}?v=20261017" defer></script><script src="{rel(page,'assets/site-nav.js')}?v=20261017" defer></script><script src="{rel(page,'assets/external-links.js')}?v=20261017" defer></script></head><body data-theme="royal"><a class="skip-link" href="#main">Skip to content</a>{header(page)}<main id="main" class="civic-main">{body}<footer class="civic-footer"><p>Page implementation updated <time datetime="{UPDATED}">{UPDATED}</time>. Facts, roles and boundaries keep their own source dates. This is a static public workbench; use the responsible electoral authority for official address and voting enquiries.</p><p>{link(page,'pages/site-map.html','Site map')} · {link(page,'LICENCE.md','Project licence and third-party rights')} · <a href="#main">Back to top ↑</a></p></footer></main></body></html>'''


def crumbs(page, state=None, scope=None):
    items = [link(page, 'pages/states.html', 'Australia map')]
    if state:
        items.append(link(page, f'states/{state}/index.html', NAMES[state]))
        items.append(link(page, directory_route(state), 'Places & representation'))
    if scope:
        items.append(link(page, directory_route(state, scope), SCOPES[scope]))
    return '<nav class="civic-crumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(items) + '</nav>'


def choices(page, state, selected_scope=None):
    labels = {'state':'State / territory electorates', 'councils':'ACT local areas' if state=='act' else 'Councils and local areas', 'federal':'Federal electorates'}
    links = []
    for scope, label in labels.items():
        item = link(page, directory_route(state, scope), label)
        if scope == selected_scope:
            item = item.replace('<a ', '<a aria-current="page" ', 1)
        links.append(item)
    return '<nav class="civic-choices civic-map-choices" aria-label="Choose a map">' + ''.join(links) + '</nav>'


def listing(page, places, identifier='place-directory'):
    ordered = sorted(places, key=lambda p: (p['name'].casefold(), p['kind']))
    rows = []
    for p in ordered:
        people = ' · '.join(r['name'] for r in p.get('representatives', []) if r.get('name'))
        rows.append(f'<li data-search="{esc(p.get("aliases", ""))}">{link(page,p["url"],p["name"])}<small>{esc(KINDS.get(p["kind"],p["kind"]))}{" · " + esc(people) if people else ""}</small></li>')
    return f'<div><label for="{identifier}-search">Search the full text directory</label> <input class="civic-directory-filter" id="{identifier}-search" type="search" data-directory-filter aria-controls="{identifier}" placeholder="Place or representative"><p class="civic-note" data-directory-count aria-live="polite">{len(ordered)} places · every entry is a direct page link</p></div><ul id="{identifier}" class="civic-directory">' + ''.join(rows) + '</ul>'


def map_widget(page, places, layers, basemap, selected=None, filter_geometry=True, initial_layer=None):
    layer_ids = {p.get('layerId') for p in places if p.get('layerId')}
    layer_ids.update(ref['layerId'] for p in places for ref in p.get('mapRefs', []))
    available = [l for l in layers if l['id'] in layer_ids and not l.get('unavailable')]
    if not available:
        return '<p class="civic-note">No compatible interactive boundary layer is available for this view. The linked directory and original sources remain below.</p>'
    records = []
    for p in places:
        refs = [{'layerId':p.get('layerId'),'featureId':p.get('featureId')}] + p.get('mapRefs', [])
        grouped = {}
        for ref in refs:
            if ref.get('layerId') not in {l['id'] for l in available}: continue
            grouped.setdefault(ref['layerId'], [])
            if str(ref.get('featureId')) not in [str(x) for x in grouped[ref['layerId']]]:
                grouped[ref['layerId']].append(ref.get('featureId'))
        for layer_id, feature_ids in grouped.items():
            records.append({key:p.get(key) for key in ('id','name','kind','url','aliases')} | {'layerId':layer_id,'featureId':feature_ids[0],'featureIds':feature_ids, 'kindLabel': KINDS.get(p['kind'],p['kind']), 'members':[r['name'] for r in p.get('representatives',[]) if r.get('name')]})
    selected_id = selected['id'] if selected else None
    selected_layer = selected.get('layerId') if selected else initial_layer
    config = {'siteRoot': rel(page, 'index.html').removesuffix('index.html'), 'layers': available, 'places': records, 'basemap': basemap, 'selectedId': selected_id, 'initialLayer': selected_layer, 'filterGeometry': filter_geometry}
    options = ''.join(f'<option value="{esc(l["id"])}">{esc(l["name"])}</option>' for l in available)
    attribution = ' '.join(dict.fromkeys(l.get('attribution','') for l in available))
    datum_notes = ' '.join(dict.fromkeys(l.get('coordinateNote','') for l in available))
    credit = 'Geographic background: Geoscience Australia; boundary publishers retain their rights. ' + link(page,'content/places/sources/national-basemap.json','Raster source and registration') + ' · ' + link(page,'content/places/geometry-delivery.json','Boundary editions and lossless delivery') + '<details><summary>Full attribution, datum and display notes</summary><p>' + esc(basemap.get('attribution','')) + '</p><p>' + esc(attribution) + '</p><p>' + esc(datum_notes) + '</p><p>EPSG:3857 display projection; original source datums and coordinates are retained. Zoom detail requests the official geographic service; the retained raster and text directory remain available if it cannot load.</p></details>'
    return f'''<section class="civic-map" id="civic-map" data-civic-map aria-label="Interactive place map" aria-busy="true"><div class="civic-map-tools"><label for="civic-layer">Boundary layer</label><select id="civic-layer" data-civic-layer>{options}</select><button type="button" data-civic-zoom-in aria-label="Zoom in">+</button><button type="button" data-civic-zoom-out aria-label="Zoom out">−</button><button type="button" data-civic-reset>Whole layer</button><button type="button" data-civic-selected>Selected area</button><button type="button" data-civic-detail aria-pressed="false">Detailed map / roads</button></div><div class="civic-map-layout"><div class="civic-map-stage"><canvas tabindex="0" role="img" aria-label="Interactive official boundary map. Drag to pan; pinch, scroll or use buttons to zoom. Arrow keys pan, plus/minus zoom, Home resets. Use the adjacent search for keyboard selection.">Use the complete linked text directory below.</canvas><p class="civic-map-message" data-civic-message aria-live="polite">Loading official boundaries. Text navigation remains available.</p></div><aside class="civic-map-side"><div class="civic-search"><label for="civic-search">Find an area or representative</label><input id="civic-search" type="search" data-civic-search autocomplete="off" placeholder="Official name or member"><p class="civic-note" data-civic-count aria-live="polite"></p><ul class="civic-map-results" data-civic-results></ul></div><article class="civic-selection" data-civic-selection hidden><p class="civic-kicker" data-civic-selection-kind></p><h3 data-civic-selection-name></h3><p class="civic-note" data-civic-selection-people></p><a class="civic-card-link" data-civic-open href="#directory">Open selected area</a></article></aside></div><div class="civic-map-credit">Select an actual polygon or search result, inspect it, then Open. Subdued categorical colours have no political meaning; gold marks selection. Transparent administrative water preserves the geographic coast beneath. {credit}<noscript><p>JavaScript enables map interaction; the full linked directory is available below.</p></noscript></div></section><script type="application/json" id="civic-map-config">{json_text(config)}</script>'''


def people_section(page, place):
    people = place.get('representatives', [])
    cards = []
    for person in people:
        if not person.get('name'):
            continue
        profile = person.get('profileUrl') or person.get('officialUrl')
        name = link(page, profile, person['name']) if profile else esc(person['name'])
        public_site = link(page, person['website'], 'Public website') if person.get('website') else ''
        profile_note = '<span class="civic-note">Name links to the official roster.</span>' if 'roster' in str(person.get('profileType','')).lower() else ''
        cards.append(f'<article class="civic-panel civic-person"><h3>{name}</h3><p>{esc(person.get("role","Published representative"))}{" · " + esc(person["party"]) if person.get("party") else ""}</p><small>{esc(person.get("status","Dated current-office snapshot"))} · source checked {esc(person.get("checked",place.get("checked","see source record")))}</small><p>{public_site} {profile_note}</p></article>')
    if not cards:
        if place.get('status') == 'historical':
            cards = ['<p>This record preserves a historical boundary edition. No current member is assigned to it. Consult the current electoral-area directory for serving representation; historical boundaries and contests remain separate.</p>']
        elif place.get('representationStatus') == 'next-election-division':
            cards = ['<p>This is a division for the next election on the newly determined boundaries. It does not yet have an elected member under that edition. Serving representation and previous results remain attached to their applicable historical/current areas.</p>']
        else:
            cards = ['<p>Individual current-office records have not yet been verified in this collection. Use the official directory below for the current roster; an earlier election winner is not automatically a current officeholder.</p>']
    official = link(page, place['officialUrl'], 'Official place / representative directory') if place.get('officialUrl') else ''
    return '<section class="civic-section" id="people"><h2>Current representation</h2><div class="civic-grid">' + ''.join(cards) + '</div><p>' + official + '</p><p class="civic-note">Current office, previous contestants and future candidacy are separate records. Published affiliation and links retain their source dates; no recontest is inferred.</p></section>'


def elections_section(page, place):
    events = place.get('elections', [])
    sections = []
    for index, event in enumerate(events):
        date = event.get('date')
        status = event.get('status', 'Check official status')
        label = event.get('label', event.get('name', 'Election event'))
        basis = event.get('dateBasis','See official event notice')
        zone = event.get('timezone') or {'qld':'Australia/Brisbane','nsw':'Australia/Sydney','vic':'Australia/Melbourne','tas':'Australia/Hobart','sa':'Australia/Adelaide','wa':'Australia/Perth','nt':'Australia/Darwin','act':'Australia/Sydney'}[place['jurisdiction']]
        supported = date and not any(word in str(basis).lower() for word in ('estimate','unverified','unknown'))
        clock = f'<strong class="civic-clock" data-civic-clock="{esc(json_text({"date":date,"dateTime":event.get("dateTime"),"timezone":zone,"milestoneLabel":event.get("milestoneLabel")}))}">Calendar timer</strong>' if supported else '<strong class="civic-clock">Voting date not announced / verified</strong>'
        source_url = event.get('sourceUrl') or event.get('resultsUrl') or place.get('officialUrl')
        source_link = link(page, source_url, 'Official event / results') if source_url else ''
        candidates = event.get('candidates', [])
        rows = []
        for candidate in candidates:
            name = candidate.get('name', '')
            profile = candidate.get('profileUrl') or candidate.get('website')
            name_html = link(page, profile, name) if profile else esc(name)
            candidate_source = candidate.get('sourceUrl') or source_url
            details = link(page, candidate_source, 'Official record') if candidate_source else 'Source unavailable'
            votes = candidate.get('votes')
            result = candidate.get('result') or candidate.get('status','Contestant in this event')
            if candidate.get('contest'):
                result = str(candidate['contest']) + ' · ' + result
            if votes is not None:
                result += ' · ' + str(votes) + ' ' + str(candidate.get('voteMeasure') or 'recorded votes (see source measure)')
            rows.append(f'<tr><td>{name_html}</td><td>{esc(candidate.get("party") or "Affiliation not recorded")}</td><td>{esc(result)}</td><td>{details}</td></tr>')
        table = '<p class="civic-note">The individual contestant roster is not populated for this event. Follow the official record; this collection does not claim a complete historical candidate list here.</p>'
        if not rows and (not date or date[:10] > UPDATED):
            table = '<p class="civic-note">No verified contestant roster has been entered for this future event. Previous candidacy does not establish future candidacy; follow the official nominations record.</p>'
        if rows:
            table = f'<details><summary>{len(rows)} recorded contestants · names, affiliations and public records</summary><div class="civic-table-wrap"><table class="civic-table"><caption>{esc(label)} · event-specific contestant records</caption><thead><tr><th>Name / public profile</th><th>Affiliation at this event</th><th>Recorded status / result</th><th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>'
        time_note = 'Published closing time: '+esc(event['dateTime'])+'. The clock respects this deadline.' if event.get('dateTime') else 'Calendar days to the local event date; exact polling or closing hours remain with the official notice.'
        sections.append(f'<article class="civic-panel civic-event" id="event-{slug(event.get("id",str(index)))}"><h3>{esc(label)}</h3><p>{esc(status)} · {esc(event.get("kind","election"))}</p>{clock}<p>{"<time datetime=" + chr(34) + esc(date) + chr(34) + ">" + esc(date) + "</time> · " if date else ""}{esc(basis)}</p><p class="civic-note">{esc(zone)} · {time_note} The clock does not refresh results or declare a winner. {esc(event.get("boundaryEdition", ""))}</p><p>{source_link}</p>{table}</article>')
    if not sections:
        sections.append('<p>No verified election/timetable record is populated here yet. Use the official electoral authority and place directory; no exact future countdown has been invented.</p>')
    return '<section class="civic-section" id="elections"><h2>Election dates & previous contestants</h2><p class="civic-note">Each event keeps its own roster, result stage and boundary edition. A subsequent by-election does not replace the previous general-election record.</p>' + ''.join(sections) + '</section>'


def sources_section(page, place, sources):
    rows = []
    for ref in place.get('sources', []):
        source = sources.get(ref, {}) if isinstance(ref, str) else ref
        if source.get('url'):
            rows.append('<li>' + link(page, source['url'], source.get('title', source['url'])) + ' · checked ' + esc(source.get('checked','see source record')) + ('. ' + esc(source.get('licence','')) if source.get('licence') else '') + '</li>')
    notes = ''.join('<li>' + esc(note) + '</li>' for note in place.get('coverageNotes', []))
    return f'<section class="civic-section" id="sources"><h2>Sources, boundaries & coverage</h2><p>Boundary basis: {esc(place.get("boundaryEdition", "See layer/source edition"))}. Geographic boundaries describe the sourced edition; they do not determine a person\'s current address entitlement.</p><p class="civic-note">{esc(place.get("contextMapNote", ""))}</p><ul class="civic-source-list">{"".join(rows)}</ul>{"<ul class=" + chr(34) + "civic-source-list" + chr(34) + ">" + notes + "</ul>" if notes else ""}<p>{link(page,"content/places/"+place["scope"]+".json","Canonical records, dates and source references")} · {link(page,"content/places/geometry-delivery.json","Map source editions and delivery checks")}</p></section>'


def place_page(place, places, layers, sources, basemap):
    page, state, scope = place['url'], place['jurisdiction'], place['scope']
    parent = next((p for p in places if p['id'] == place.get('parentId')), None)
    children = [p for p in places if p.get('parentId') == place['id']]
    selected_layers = {place.get('layerId')} | {r['layerId'] for r in place.get('mapRefs',[])}
    selected_layers.discard(None)
    peers = [p for p in places if p['jurisdiction'] == state and selected_layers.intersection({p.get('layerId')} | {r['layerId'] for r in p.get('mapRefs',[])})] if selected_layers else []
    if parent:
        peers = [p for p in peers if p.get('parentId') == parent['id']]
    map_places = children if any(p.get('layerId') for p in children) else peers
    selected = place if not children else None
    body = crumbs(page, state, scope) + f'<div class="civic-heading"><div><p class="civic-kicker">{esc(NAMES[state])} / {esc(KINDS.get(place["kind"],place["kind"]))}</p><h1>{esc(place["name"])}</h1><p>Find the boundaries, current representation, previous election contestants and original public records for this place.</p></div><aside><span class="civic-chip">{esc(place.get("chamber") or KINDS.get(place["kind"],place["kind"]))}</span></aside></div>'
    body += choices(page, state, scope) + '<nav class="civic-choices" aria-label="On this page"><a href="#people">Current members</a><a href="#elections">Dates & contestants</a><a href="#sources">Evidence & boundaries</a><a href="#take-part">Take part</a></nav>'
    if place.get('status') == 'historical':
        body += '<p class="civic-note">Historical boundary record. This area is retained for the earlier source edition; it is not a current electoral district.</p>'
    if parent:
        body += '<p>Local-government parent: ' + link(page,parent['url'],parent['name']) + '.</p>'
    for key,label in (('predecessorPlaceId','Previous-boundary place'),('successorPlaceId','Next-boundary place')):
        related = next((p for p in places if p['id'] == place.get(key)),None)
        if related:
            body += '<p>'+esc(label)+': '+link(page,related['url'],related['name'])+'. Each edition keeps its own representation and result history.</p>'
    if place['kind'] == 'federal-division':
        senate = next((p for p in places if p['jurisdiction']==state and p['kind']=='senate-area'),None)
        if senate: body += '<p>Separate upper-house representation: '+link(page,senate['url'],'Senators for '+NAMES[state])+'.</p>'
    if place['url'].endswith('/redland/elections/index.html'):
        body += '<p>' + link(page,'states/qld/councils/redland/index.html','Open the existing Redlands local journey') + '</p>'
    if state == 'vic':
        body += '<p>' + link(page,'states/vic/map/index.html','Explore the existing Victoria atlas, comparisons and profile details') + '</p>'
    body += map_widget(page, map_places, layers, basemap, selected=selected, filter_geometry=True)
    if children:
        body += '<section class="civic-section" id="directory"><h2>Local electoral areas</h2>' + listing(page,children) + '</section>'
    else:
        body += '<details id="directory"><summary>Other areas in this map · full text navigation</summary>' + listing(page,peers) + '</details>' if peers else ''
    body += people_section(page, place) + elections_section(page, place)
    body += '<section class="civic-section" id="take-part"><h2>Evidence into useful participation</h2><div class="civic-grid"><article class="civic-panel"><h3>Check a public record</h3><p>Follow the original member, electoral authority and institutional records linked here. For a decision, retain its exact motion, date and stage; a missing individual vote or stated reason stays unknown.</p></article><article class="civic-panel"><h3>Prepare a question or proposal</h3><p>Choose your purpose and responsible institution. ' + link(page,'pages/private-civic-profile-builder.html','Prepare a private civic draft') + ' or inspect ' + link(page,'pages/legal-rag.html','the legal-memory proposal') + '. These workbench links do not submit a request to an authority.</p></article><article class="civic-panel"><h3>Track what changed</h3><p>Keep three accounts together: what it cost, what was given freely, and what changed. Record evidence and time periods; proposed benefits remain distinct from observed outcomes. ' + link(page,'pages/braided-economy.html','Explore the braided economy') + '.</p></article></div><p class="civic-note">Local Twinkles and resident-authored concerns are left to grassroots implementation. Existing wider-system rooms are proposals to explore, with their own stages and sources.</p></section>'
    body += sources_section(page, place, sources)
    write(page, shell(page,place['name'],body))


def directory_page(state, scope, places, layers, basemap):
    page = directory_route(state, scope)
    subset = [p for p in places if p['jurisdiction'] == state and (not scope or p['scope'] == scope)]
    title = NAMES[state] + ' · ' + ({'state':'electorate map','councils':'local areas map' if state=='act' else 'council map','federal':'federal electorate map'}[scope] if scope else 'maps, members & elections')
    body = crumbs(page,state) + f'<div class="civic-heading civic-directory-heading"><div><p class="civic-kicker">Maps, members &amp; elections</p><h1>{esc(title)}</h1><p>Choose a map below. Search or select an area, then open its members and election records.</p></div><aside><span class="civic-chip">{len(subset)} sourced area records</span></aside></div>' + choices(page,state,scope)
    if state == 'act' and scope == 'councils':
        body += '<p class="civic-note">The ACT context is shown using its actual territory/local-government arrangements. A mapped statistical local area is not an invented elected council or council election.</p>'
    preferred = next((p.get('layerId') for p in subset if p['kind']=='state-district' and p.get('status')!='historical' and p.get('layerId')),None) if scope in (None,'state') else None
    body += map_widget(page,subset,layers,basemap,initial_layer=preferred)
    body += '<section class="civic-section" id="directory"><h2>Every area · direct page links</h2>' + listing(page,subset) + '</section>'
    body += '<p class="civic-note">Each place page states its own source coverage. A public directory link does not mean every individual profile or historical contestant has been verified. Compare boundary editions before comparing results or statistics.</p>'
    write(page,shell(page,title,body))


def national_page(places,layers,basemap):
    page='pages/places.html'
    body=crumbs(page)+'<div class="civic-heading"><div><p class="civic-kicker">Australia / places & representation</p><h1>Find your place.<br>Follow the public record.</h1><p>Councils, state and territory electorates, House divisions and Senate representation. Exact sourced maps connect to dedicated pages, people, election dates and previous contestants.</p></div></div><div class="civic-grid">'
    for state,name in NAMES.items():
        subset=[p for p in places if p['jurisdiction']==state]
        body+='<article class="civic-panel"><h2>'+link(page,directory_route(state,'state'),name)+'</h2><p>'+str(len(subset))+' sourced area records</p>'+choices(page,state)+'</article>'
    body+='</div><p class="civic-note">Maps load one layer at a time. Source dates and current/upcoming boundary editions are retained. Local Twinkles are left for grassroots implementation.</p><section class="civic-section"><h2>Existing deeper workbenches</h2><div class="civic-choices">'+link(page,'states/vic/map/index.html','Victoria atlas & profiles')+link(page,'states/qld/councils/redland/index.html','Redlands local journey')+link(page,'pages/site-map.html','Every public page')+'</div></section>'
    write(page,shell(page,'Councils, electorates & public representation',body))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jurisdiction',choices=list(NAMES))
    parser.add_argument('--scope',choices=list(SCOPES))
    parser.add_argument('--place',help='Exact stable place ID; shared source indexes stay complete')
    args=parser.parse_args()
    places,layers,sources,inputs=load()
    affected_ids = None
    if args.place:
        target = next((p for p in places if p['id'] == args.place),None)
        if target is None: raise SystemExit('Unknown stable place ID: '+args.place)
        target_layers = {target.get('layerId')} | {r['layerId'] for r in target.get('mapRefs',[])}
        target_layers.discard(None)
        # Detail pages embed same-layer search/directory/member summaries. They
        # are real dependants of a member/name change, not unrelated rebuilds.
        affected_ids = {p['id'] for p in places if p['jurisdiction']==target['jurisdiction'] and (p['id']==target['id'] or p.get('parentId')==target['id'] or p['id']==target.get('parentId') or target_layers.intersection({p.get('layerId')} | {r['layerId'] for r in p.get('mapRefs',[])}))}
    prepare_layers(layers)
    basemap=json.loads((ROOT/'content/places/sources/national-basemap.json').read_text(encoding='utf-8'))
    for place in places:
        if args.jurisdiction and place['jurisdiction']!=args.jurisdiction:continue
        if args.scope and place['scope']!=args.scope:continue
        if affected_ids is not None and place['id'] not in affected_ids:continue
        place_page(place,places,layers,sources,basemap)
    for state in NAMES:
        if args.jurisdiction and state!=args.jurisdiction:continue
        for scope in (None,*SCOPES):
            directory_page(state,scope,places,layers,basemap)
    national_page(places,layers,basemap)
    index={'schemaVersion':1,'implementationUpdated':UPDATED,'sourceInputs':[f'content/places/{s}.json' for s in SCOPES],'layers':layers,'places':[{key:p.get(key) for key in ('id','name','jurisdiction','kind','scope','url','parentId','layerId','featureId','boundaryEdition')} for p in places]}
    write('content/places/route-registry.json',json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    qld_routes = {str(p['featureId']):('states/qld/councils/redland/index.html' if str(p['featureId'])=='6250' else p['url']) for p in places if p['jurisdiction']=='qld' and p['kind'] in ('council','special-local-body')}
    write('assets/qld-place-routes.js','/* Sourced national place routes; geometry remains unchanged. */\nwindow.P4A_NATIONAL_QLD_ROUTES='+json_text(qld_routes)+';\n')
    from national_place_links import apply_existing_links
    apply_existing_links()
    counts=Counter(p['scope'] for p in places)
    print('Built national place pages: '+str(dict(counts))+f'; {len(WRITTEN)} files changed. Source research dates preserved.')


if __name__=='__main__':main()
