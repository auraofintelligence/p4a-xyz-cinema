"""Static HTML counterpart of the shared external web-link policy."""
import re,html
from urllib.parse import urlsplit
def external_links(markup):
    def anchor(match):
        tag=match[0]
        if re.search(r'\sdownload(?:\s|=|>)',tag,re.I):return tag
        href=re.search(r'\bhref\s*=\s*([\"\'])(.*?)\1',tag,re.I)
        if not href:return tag
        url=urlsplit(html.unescape(href[2]))
        if url.scheme not in ('http','https') and not (not url.scheme and url.netloc):return tag
        # Canonical same-site absolute links remain same-tab at the deployed site.
        if url.hostname in ('p4a.xyz','www.p4a.xyz') or (url.hostname=='auraofintelligence.github.io' and url.path.startswith('/p4a-xyz-cinema/')):return tag
        rel=re.search(r'\brel\s*=\s*([\"\'])(.*?)\1',tag,re.I)
        tokens=list(dict.fromkeys((rel[2].split() if rel else [])+['noopener','noreferrer']))
        tag=re.sub(r'\s+(?:target|rel)\s*=\s*([\"\']).*?\1','',tag,flags=re.I)
        return tag[:-1]+' target="_blank" rel="'+' '.join(tokens)+'">'
    return re.sub(r'<a\b[^>]*>',anchor,markup,flags=re.I)
