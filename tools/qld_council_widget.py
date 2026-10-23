"""One council-map component reused at state and council level. 17 Oct 2026."""
from pathlib import Path
import json
import html
import os
ROOT=Path(__file__).resolve().parents[1]

def national_routes():
    registry=ROOT/'content/places/route-registry.json'
    if not registry.exists():return {}
    rows=json.loads(registry.read_text(encoding='utf-8'))['places']
    return {str(p['featureId']):('states/qld/councils/redland/index.html' if str(p['featureId'])=='6250' else p['url']) for p in rows if p['jurisdiction']=='qld' and p['kind'] in ['council','special-local-body']}

def rel(page,target):
    if target.startswith('https://'):return html.escape(target,quote=True)
    return html.escape(os.path.relpath(ROOT/target,(ROOT/page).parent).replace('\\','/'),quote=True)

def base_payload():
    base=json.loads((ROOT/'content/councils/qld-basemap-sources.json').read_text(encoding='utf-8-sig'))
    return {key:base[key] for key in ['image','extent','serviceURL','attribution','roads']}

def build_delivery():
    raw=json.loads((ROOT/'assets/maps/qld-councils.geojson').read_text(encoding='utf-8'))
    payload={'type':raw['type'],'features':[{'type':'Feature','properties':{k:f['properties'][k] for k in ['lga','abbrev_name','lga_code']},'geometry':f['geometry']} for f in raw['features']]}
    payload['basemap']=base_payload()
    (ROOT/'assets/maps/qld-councils-data.js').write_text('/* Qld Government source geometry; snapshot 17 October 2026; CC BY 4.0. See content/councils/qld-map-sources.json. */\nwindow.P4A_QLD_COUNCILS='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    return raw

def build_division_delivery():
    raw=json.loads((ROOT/'assets/maps/redlands/redland-divisions-2024.geojson').read_text(encoding='utf-8-sig'))
    places=json.loads((ROOT/'content/local/redland-divisions.json').read_text(encoding='utf-8-sig'))
    records=places.get('divisions',places.get('records',[]))
    by_id={str(item.get('number',item.get('id',item.get('division')))):item for item in records}
    features=[]
    for feature in raw['features']:
        number=str(int(feature['properties']['elect_div'].split()[-1]))
        entry=by_id.get(number,{})
        aliases=' '.join(str(entry.get(key,'')) for key in ['localities','places','label','areaSummary','aliases'])
        features.append({'type':'Feature','properties':{'lga':'Division '+number,'abbrev_name':aliases,'lga_code':number},'geometry':feature['geometry']})
    payload={'type':raw['type'],'features':features,'basemap':base_payload()}
    (ROOT/'assets/maps/redland-divisions-data.js').write_text('/* Official Queensland 2024 electoral-division source geometry, retrieved 17 October 2026. No simplification. */\nwindow.P4A_REDLAND_DIVISIONS='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    return raw

def assets(page,level='council'):
    data='assets/maps/redland-divisions-data.js' if level=='division' else 'assets/maps/qld-councils-data.js'
    route_asset=f'<script src="{rel(page,"assets/qld-place-routes.js")}?v=20261017-places" defer></script>' if national_routes() else ''
    return f'<link rel="stylesheet" href="{rel(page,"assets/qld-council-map.css")}?v=20261017-places"><script src="{rel(page,data)}?v=20261017-places" defer></script>{route_asset}<script src="{rel(page,"assets/qld-council-map.js")}?v=20261017-places" defer></script>'

def widget(page,level='council'):
    division=level=='division'
    if division:
        directory=''.join(f'<li><a href="{rel(page,f"states/qld/councils/redland/divisions/{number}/index.html")}">Division {number}</a></li>' for number in range(1,11))
    else:
        raw=json.loads((ROOT/'assets/maps/qld-councils.geojson').read_text(encoding='utf-8'))
        routes=national_routes()
        directory=''.join('<li>'+('<a href="'+rel(page,routes[str(f['properties']['lga_code'])])+'">'+html.escape(f['properties']['lga'])+'</a>' if str(f['properties']['lga_code']) in routes else html.escape(f['properties']['lga']))+'</li>' for f in sorted(raw['features'],key=lambda f:f['properties']['lga']))
    atlas_id='redland-division-map' if division else 'qld-council-map'
    place='Redlands' if division else 'Queensland'
    area='division' if division else 'council'
    title="Explore Redlands' divisions." if division else "Explore Queensland's councils."
    count='10 council divisions' if division else '77 councils + Weipa Town area'
    placeholder='Division 2, Cleveland, Russell…' if division else 'Redlands, Brisbane, Cairns…'
    extra='' if division else '<button type="button" data-map-seq>South East Queensland</button><button type="button" data-map-redland>Find Redlands</button>'
    source='content/councils/redland-divisions-sources.json' if division else 'content/councils/qld-map-sources.json'
    boundary_link='https://www.ecq.qld.gov.au/electoral-boundaries/local-government-area-boundaries'
    directory_link='https://www.redland.qld.gov.au/About-Council/Mayor-and-Councillors' if division else 'https://www.dlgwv.qld.gov.au/local-government/for-the-community/local-government-directory'
    open_href='states/qld/councils/redland/divisions/1/index.html' if division else 'states/qld/councils/redland/index.html'
    fallback_note='All ten division overviews are available below.' if division else 'Redlands is the first built example.'
    source_note='The official 2024 electoral-division layer supplies all ten Redland City divisions. The 2019 review map is retained separately as a historical source.' if division else 'The boundary source contains 77 councils plus Weipa Town Authority. Only Redlands has a completed P4A local journey in this pass.'
    if not division and national_routes():
        fallback_note='Open the sourced council pages below; Redlands retains its fuller local journey.'
        source_note='The boundary source contains 77 councils plus Weipa Town Authority. National council pages connect representation, elections and original sources; each states its own evidence gaps. Local Twinkles are left to grassroots implementation.'
    site_root=rel(page,'index.html').removesuffix('index.html')
    return f'''<section class="council-atlas" id="{atlas_id}" data-qld-council-map data-map-level="{level}" data-site-root="{site_root}" aria-labelledby="{atlas_id}-heading">
<p class="atlas-kicker">The same journey, one place closer · Updated 17 October 2026</p><h2 id="{atlas_id}-heading">{title}</h2>
<p class="atlas-intro">Drag to move. Scroll, pinch or use + and − to zoom. Click a boundary or search a {area} to select it, then open its local journey. {fallback_note}</p>
<p class="atlas-load" data-map-loading>Loading the sourced council boundaries. The full text directory remains below.</p>
<div class="atlas-layout"><div class="atlas-map-panel"><div class="atlas-toolbar" role="group" aria-label="{area.title()} map controls"><button type="button" data-map-zoom-in aria-label="Zoom in">+</button><button type="button" data-map-zoom-out aria-label="Zoom out">−</button><button type="button" data-map-reset>Whole {place}</button>{extra}<button type="button" data-map-roads aria-pressed="false" disabled>Detailed roads</button></div>
<div class="atlas-canvas-wrap"><canvas class="atlas-canvas" tabindex="0" role="img" aria-label="Interactive map of {place} {area} boundaries. Drag to pan, scroll or pinch to zoom. Search provides keyboard selection.">Interactive {area} map. Use the directory and official boundary links below.</canvas><span class="atlas-map-label" data-map-label>{place} {area}s</span></div>
<p class="atlas-map-help">Click selects an area; double-click zooms to it. Keyboard: arrow keys move, +/− zoom, R resets. Soft colours distinguish areas; gold marks your selection. Colours carry no political meaning.</p><p class="atlas-map-help" data-basemap-status aria-live="polite">Quiet map · official Queensland pastel geographic base</p></div>
<div class="atlas-sidebar"><div class="atlas-search-panel"><label for="{atlas_id}-search">Find a {area}</label><input id="{atlas_id}-search" type="search" placeholder="{placeholder}" autocomplete="off" disabled data-council-search><p class="atlas-result-count" aria-live="polite" data-council-count>{count}</p><ul class="atlas-results" aria-label="{area.title()} search results" data-council-results></ul><p class="atlas-empty" data-council-no-results hidden>No matching {area}. Try its name or clear your search.</p></div>
<article class="atlas-selection" data-council-selection hidden aria-live="polite"><p class="atlas-selection-kind" data-selection-kind></p><h3 data-selection-name></h3><p data-selection-copy></p><div class="atlas-selection-links"><a class="atlas-open" href="{rel(page,open_href)}" data-open-council hidden>Open {area}</a><a href="{boundary_link}" target="_blank" rel="noopener noreferrer">Official boundaries</a><a href="{directory_link}" target="_blank" rel="noopener noreferrer">Official {'councillors' if division else 'council directory'}</a></div></article></div></div>
<div class="atlas-source">Geographic base map: © State of Queensland (Department of Natural Resources and Mines, Manufacturing and Regional and Rural Development) 2025. Boundaries: State of Queensland, {'2024 edition' if division else '2026 snapshot'}. Both <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>; checked 17 October 2026. <a href="{rel(page,'content/councils/qld-basemap-sources.json')}">Geographic map source and alignment</a> · <a href="{rel(page,source)}">Boundary sources, dates and attribution</a>.
<details><summary>What the map describes</summary><p>The official Queensland pastel raster shows actual coastlines, islands and places with subdued grey roads. Detailed roads switch to the official topographic style. Actual {area} polygons are a transparent overlay, including administrative water areas. Both share the same EPSG:3857 coordinates, aligned using the service's returned image extent. No SVG, traced outlines or synthetic geography. The retained PNG works locally; zoom-specific detail loads from the official Queensland map service when online. {source_note} Use ECQ's address finder for official electoral enquiries.</p></details></div>
<details class="atlas-fallback"><summary>Full text directory · {count}</summary><p>All named areas are listed even if the interactive display cannot load.</p><ul>{directory}</ul></details><noscript><p>JavaScript is needed for pan, zoom and search. The full text directory and links remain available.</p></noscript></section>'''
