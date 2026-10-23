"""Small additive entry links shared by legacy and national generators."""
from pathlib import Path
import html
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]


def apply_existing_links():
    if not (ROOT/'content/places/route-registry.json').exists():
        return []
    targets = {'pages/states.html': 'pages/places.html', 'pages/maps.html': 'pages/places.html',
               'content/rooms/maps.html':'pages/places.html',
               'states/qld/councils/index.html':'states/qld/places/councils/index.html',
               'states/qld/councils/redland/candidates/index.html':'states/qld/councils/redland/elections/index.html'}
    targets.update({f'states/{state}/index.html':f'states/{state}/places/index.html' for state in ['act','nsw','nt','qld','sa','tas','vic','wa']})
    changed = []
    for path, destination in targets.items():
        target = ROOT/path
        if not target.exists() or not (ROOT/destination).exists(): continue
        public = ROOT/'pages/maps.html' if path=='content/rooms/maps.html' else target
        href = html.escape(os.path.relpath(ROOT/destination,public.parent).replace('\\','/'),quote=True)
        section = '<!-- national-place-links:start --><section class="civic-national-entry" style="padding:1.2rem;margin:1rem;border:1px solid #a184bd;border-radius:6px"><h2>Maps, members &amp; elections</h2><p><a href="'+href+'">Open councils, electorates, election dates and previous contestants</a></p><p>Each place retains its sources, boundary edition and representation history.</p></section><!-- national-place-links:end -->'
        source = target.read_text(encoding='utf-8')
        pattern = r'<!-- national-place-links:start -->[\s\S]*?<!-- national-place-links:end -->'
        result = re.sub(pattern,lambda _:section,source) if re.search(pattern,source) else source.replace('</main>',section+'</main>',1)
        if 'assets/qld-council-map.js' in result and 'assets/qld-place-routes.js' not in result:
            route_script = '<script src="'+os.path.relpath(ROOT/'assets/qld-place-routes.js',public.parent).replace('\\','/')+'?v=20261017" defer></script>'
            result = re.sub(r'(<script\b[^>]*src="[^"]*assets/qld-council-map\.js[^"]*"[^>]*></script>)',lambda m:route_script+m[1],result,count=1)
        if result != source:
            target.write_text(result,encoding='utf-8'); changed.append(path)
    return changed


if __name__=='__main__':
    print('Restored national entry links: '+str(len(apply_existing_links()))+' files changed.')
