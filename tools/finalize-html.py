"""Preserve shared publication styles and external-link policy after generation."""
import re
import sys
from pathlib import Path
from web_link_policy import external_links
from public_copy import public_html

for name in sys.argv[1:]:
    path = Path(name)
    text = external_links(public_html(path.name,path.read_text(encoding='utf-8')))
    text = re.sub(r'(styles\.css|assets/site-nav\.js)\?v=[^"\s]+', r'\1?v=20261002-publication', text)
    if 'assets/site-nav.js' not in text:
        match = re.search(r'href="([^"]*)styles\.css', text)
        if match:
            text = text.replace('</body>', f'<script src="{match[1]}assets/site-nav.js?v=20261002-publication"></script>\n</body>')
    path.write_text(text, encoding='utf-8')
