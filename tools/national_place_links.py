"""Deterministic visitor navigation for legacy state pages; no factual refresh."""
from pathlib import Path
import html
import os
import re

ROOT = Path(__file__).resolve().parents[1]
STATES = {'act':'Australian Capital Territory','nsw':'New South Wales','nt':'Northern Territory','qld':'Queensland','sa':'South Australia','tas':'Tasmania','vic':'Victoria','wa':'Western Australia'}

def href(page, destination):
    path, _, anchor = destination.partition('#')
    return html.escape(os.path.relpath(ROOT/path, (ROOT/page).parent).replace('\\','/') + ('#'+anchor if anchor else ''), quote=True)

def a(page, destination, label):
    return '<a href="'+href(page,destination)+'">'+html.escape(label)+'</a>'

def wayfinding(page, state=None):
    links = [a(page,'pages/states.html','Australia map')]
    if state:
        links += [a(page,f'states/{state}/index.html',STATES[state]),
                  a(page,f'states/{state}/places/state/index.html','Electorate map'),
                  a(page,f'states/{state}/places/councils/index.html','Local areas map' if state=='act' else 'Council map')]
    return '<nav class="site-layer-strip civic-wayfinding" aria-label="Map navigation">'+''.join(links)+'</nav>'

def entry(page, state=None, destination=None):
    if state:
        links = [(f'states/{state}/places/state/index.html','State / territory electorate map'),
                 (f'states/{state}/places/councils/index.html','ACT local areas map' if state=='act' else 'Council and local areas map'),
                 (f'states/{state}/places/federal/index.html','Federal electorate map')]
        note = 'The ACT has no separate elected councils; local areas retain their actual arrangements.' if state=='act' else 'Switch between the electorate and council maps at any time.'
    elif page=='pages/states.html':
        links = [('pages/states.html#state-map','Choose a state on the map'),('pages/places.html','Browse all councils and electorates')]
        note = 'Choose a state or territory to open its electorate map, then switch to councils or federal representation.'
    else:
        links = [(destination or 'pages/states.html','Open maps, members and elections'),('pages/states.html','Australia map')]
        note = 'Find your area, select it on the map, then open its members, election dates and previous contestants.'
    return '<!-- national-place-links:start --><section class="civic-national-entry" aria-label="Maps, members and elections"><h2>Maps, members &amp; elections</h2><p>'+note+'</p><nav class="civic-entry-choices" aria-label="Choose a map">'+''.join(a(page,p,l) for p,l in links)+'</nav><small class="civic-navigation-date">Map navigation updated <time datetime="2026-10-23">23 October 2026</time>. Facts retain their own source dates.</small></section><!-- national-place-links:end -->'

def apply_existing_links():
    if not (ROOT/'content/places/route-registry.json').exists(): return []
    targets = {'pages/states.html':'pages/places.html','pages/maps.html':'pages/places.html','content/rooms/maps.html':'pages/places.html',
               'states/qld/councils/index.html':'states/qld/places/councils/index.html',
               'states/qld/councils/redland/candidates/index.html':'states/qld/councils/redland/elections/index.html'}
    targets.update({f'states/{state}/index.html':None for state in STATES})
    files=set(targets)|{'pages/state-history.html'}
    files.update(f'states/{state}/{section}/index.html' for state in STATES for section in ('history','architecture','constitution'))
    changed=[]
    for page in sorted(files):
        target=ROOT/page
        if not target.exists(): continue
        public='pages/maps.html' if page=='content/rooms/maps.html' else page
        source=target.read_text(encoding='utf-8'); result=source
        state=page.split('/')[1] if page.startswith('states/') else None
        result=re.sub(r'<div class="site-layer-strip\b[^>]*>[\s\S]*?</div>|<nav class="site-layer-strip civic-wayfinding"[\s\S]*?</nav>',lambda _:wayfinding(public,state),result,count=1)
        result=result.replace('Data-first pages generated from markdown files agents can use, with edits handled through permissioned review.','Maps, public representation, election dates and sources for every state and territory.')
        result=re.sub(r'<a href="[^"]*content/(?:states|history)/README\.md">(?:State|History) data notes</a>\s*','',result)
        result=re.sub(r'<p>Editable source: <code>[^<]*</code></p>\s*','',result)
        result=re.sub(r'<a\b[^>]*href="[^"]*docs/agents/local-place-pattern\.md"[^>]*>Build another local pattern</a>\s*','',result)
        if page=='pages/states.html':
            result=result.replace('State layer unlocked','Maps, members &amp; elections').replace('Eight local doors into the purple republic rehearsal.','Find your state. Explore your area.')
            result=result.replace('p4A starts national, but the work becomes real state by state: who holds power, how the chambers split, when voters next move, and where a cyber-republic referendum simulator needs local proof before 2032.','Start with the electorate map, switch to councils or federal areas, and open a place for its members, election dates and public records.')
            result=result.replace('Each jurisdiction opens a local clone with current power, chamber and election data.','Choose a state or territory to open its electorate map. Council and federal maps are one clear choice away.')
            result=result.replace('<section class="section state-map-section">','<section class="section state-map-section" id="state-map">')
        if page in ('pages/states.html','pages/maps.html','content/rooms/maps.html'):
            for slug,name in STATES.items():
                result=re.sub(r'(<a\b[^>]*class="state-raster-label"[^>]*data-map-state="'+slug+r'"[^>]*>)',lambda m:m[0].replace('states/'+slug+'/index.html','states/'+slug+'/places/state/index.html').replace('Open '+name+' portal','Open '+name+' electorate map'),result)
                result=re.sub(r'<a class="state-portal-card" href="[^"]*" data-state="'+slug+r'">',lambda _: '<a class="state-portal-card" href="'+href(public,f'states/{slug}/places/state/index.html')+'" data-state="'+slug+'">',result)
        result=re.sub(r'<section class="section state-data-note reveal">[\s\S]*?</section>\s*','',result)
        result=result.replace('Each card links to the history page inside that state or territory clone, keeping the national layer and state layer distinct before future council layers arrive.','Explore the history of each state or territory, then return to its maps and public records.')
        if state and page==f'states/{state}/index.html':
            result=re.sub(r'<article class="summary-panel reveal">\s*<p class="eyebrow">Tailoring notes</p>[\s\S]*?</article>\s*','',result)
            result=result.replace('These totals are the data layer future agents should refresh when resignations, recounts or by-elections change the map.','These dated chamber totals show party representation. Follow the linked sources for changes since the recorded check.')
            result=result.replace('including days-until, days-since and the markdown archive rule.','including days until and days since each event.')
        if page in targets:
            result=re.sub(r'<!-- national-place-links:start -->[\s\S]*?<!-- national-place-links:end -->','',result)
            panel=entry(public,state if page==f'states/{state}/index.html' else None,targets[page])
            hero=re.search(r'<section class="state-hero\b[\s\S]*?</section>',result)
            if hero: result=result[:hero.end()]+'\n'+panel+'\n'+result[hero.end():].lstrip()
            else: result=re.sub(r'(<main\b[^>]*>)',lambda m:m[0]+panel,result,count=1)
        elif 'civic-navigation-date' not in result:
            result=result.replace('</footer>','<small class="civic-navigation-date">Map navigation updated <time datetime="2026-10-23">23 October 2026</time>. Facts retain their own source dates.</small></footer>',1)
        if 'assets/qld-council-map.js' in result and 'assets/qld-place-routes.js' not in result:
            script='<script src="'+href(public,'assets/qld-place-routes.js')+'?v=20261017" defer></script>'
            result=re.sub(r'(<script\b[^>]*src="[^"]*assets/qld-council-map\.js[^"]*"[^>]*></script>)',lambda m:script+m[1],result,count=1)
        if result!=source: target.write_bytes(result.encode('utf-8'));changed.append(page)
    return changed

if __name__=='__main__':
    print('Updated civic entry navigation: '+str(len(apply_existing_links()))+' files changed.')
