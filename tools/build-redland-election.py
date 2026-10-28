"""Refresh three existing Redlands election/news/source sections, offline and scoped."""
from pathlib import Path
import importlib.util
import re
from redland_election import apply_page, validate
from page_review_register import render_register

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('redland_builder', ROOT / 'tools/build-redland.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
data = builder.read('content/local/redland-election.json')
validate(data)
paths = [builder.BASE + suffix for suffix in ['index.html', 'candidates/index.html', 'sources/index.html']]
for page in paths:
    path = ROOT / page
    text = path.read_text(encoding='utf-8')
    text = apply_page(page, text, data, builder.link)
    if page.endswith('/sources/index.html'):
        text = re.sub(r'<section class="local-section" id="review-register">[\s\S]*?</section>', lambda _: render_register(page, builder.link), text, count=1)
    path.write_bytes(text.encode('utf-8'))
print('Updated only: ' + ', '.join(paths))
