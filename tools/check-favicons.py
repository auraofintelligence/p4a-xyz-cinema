"""Check public routes and source mirrors for a valid local favicon declaration."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Icons(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'icon' in attrs.get('rel', '').lower().split():
            self.hrefs.append(attrs.get('href', ''))

def verify(root=ROOT):
    public = {'index.html'} | {p.relative_to(root).as_posix() for folder in ('pages', 'states') for p in (root/folder).rglob('*.html')}
    sources = {p.relative_to(root).as_posix() for p in (root/'content/rooms').glob('*.html')}
    errors = []
    assets = set()
    for route in sorted(public | sources):
        parser = Icons()
        parser.feed((root/route).read_text(encoding='utf-8-sig'))
        if not parser.hrefs:
            errors.append(route + ': missing rel=icon')
        for href in parser.hrefs:
            url = urlsplit(href)
            if not href or url.scheme or url.netloc:
                errors.append(route + ': expected a nonempty local icon path')
                continue
            target = ((root/unquote(url.path).lstrip('/')) if url.path.startswith('/') else root/Path(route).parent/unquote(url.path)).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append(route + ': missing or out-of-root icon ' + href)
                continue
            assets.add(target)
    for asset in sorted(assets):
        if asset.suffix.lower() == '.svg':
            try:
                svg = ET.fromstring(asset.read_bytes())
                if svg.tag != '{http://www.w3.org/2000/svg}svg':
                    errors.append(str(asset) + ': invalid SVG root')
            except ET.ParseError as error:
                errors.append(str(asset) + ': ' + str(error))
    if errors:
        raise AssertionError('\n'.join(errors))
    return {'publicPages': len(public), 'sourceMirrors': len(sources), 'localIconAssets': len(assets), 'result': 'PASS'}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
