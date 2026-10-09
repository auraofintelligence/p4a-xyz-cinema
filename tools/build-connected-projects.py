"""Refresh the reviewed project cards and contextual links without rewriting other rooms."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content/connected-projects.json').read_text(encoding='utf-8'))
cards = []
for project in data['projects']:
    if not project.get('description'):
        continue
    title = html.escape(project['title'])
    description = html.escape(project['description'])
    url = html.escape(project['links'][0], quote=True)
    cards.append(f'<article class="official-link-card"><h3>{title}</h3><p>{description}</p><div class="official-link-actions"><a href="{url}" target="_blank" rel="noopener noreferrer">Open project (new tab)</a></div></article>')
    for page in project.get('contextPages', []):
        source = ROOT / 'content/rooms' / page
        path = source if source.exists() else ROOT / 'pages' / page
        text = path.read_text(encoding='utf-8')
        key = project['links'][0].rstrip('/').rsplit('/', 1)[-1]
        start, end = f'<!-- connected:{key} -->', f'<!-- /connected:{key} -->'
        panel = f'{start}\n<div class="feature-panel"><h2>Connected project: {title}</h2><p>{description}</p><div class="source-links"><a href="{url}" target="_blank" rel="noopener noreferrer">Open {title} (new tab)</a></div></div>\n{end}'
        if start in text:
            text = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: panel, text, flags=re.S)
        elif url not in text:
            text = text.replace('<div class="next-trail">', panel + '\n<div class="next-trail">', 1)
            if start not in text:
                text = text.replace('</main>', '<section class="section"><div class="page-copy">' + panel + '</div></section>\n</main>', 1)
        path.write_text(text, encoding='utf-8')
source = ROOT / 'content/rooms/site-map.html'
path = source if source.exists() else ROOT / 'pages/site-map.html'
text = path.read_text(encoding='utf-8')
start, end = '<!-- reviewed-projects:start -->', '<!-- reviewed-projects:end -->'
block = start + '\n' + '\n'.join(cards) + '\n' + end
if start in text:
    text = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: block, text, flags=re.S)
else:
    text = re.sub(r'(<div class="official-link-grid">)\s*<article class="official-link-card"><h3>Australian Law:.*?(?=\s*<article class="official-link-card">\s*<h3>P4A</h3>)', lambda m: m[1] + '\n' + block + '\n', text, count=1, flags=re.S)
path.write_text(text, encoding='utf-8')
print(f'Refreshed {len(cards)} reviewed project cards and their contextual links.')
