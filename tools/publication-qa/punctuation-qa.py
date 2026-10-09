"""Reject typographic dashes in authored display copy without rewriting quotations."""
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import sys, json, re
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'tools'))
from public_punctuation import public_punctuation
sample='<p title="1&#8211;2">A &mdash; B; 1&#x2013;2.</p><q>Original \u2014 quote</q><script>let x="\u2013";</script><a href="https://example.com/\u2014">link</a>'
expected='<p title="1-2">A - B; 1-2.</p><q>Original \u2014 quote</q><script>let x="\u2013";</script><a href="https://example.com/\u2014">link</a>'
assert public_punctuation(sample)==expected
paths=[R/'index.html',*R.glob('pages/**/*.html'),*R.glob('states/**/*.html'),*R.glob('content/rooms/*.html')]
errors=[]
for p in paths:
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for x in s.select('script,style,code,pre,blockquote,q'):x.decompose()
 for node in s.find_all(string=True):
  if not isinstance(node,Comment) and any(c in node for c in '\u2013\u2014'):errors.append([str(p.relative_to(R)),str(node)[:120]])
 for x in s.find_all(True):
  for attr in ['title','alt','aria-label','placeholder']:
   if any(c in x.get(attr,'') for c in '\u2013\u2014'):errors.append([str(p.relative_to(R)),attr])
for p in (R/'assets').glob('*.js'):
 if re.search(r'\u2013|\u2014|&(?:ndash|mdash);|\\u201[34]',p.read_text(encoding='utf-8')):errors.append([str(p.relative_to(R)),'runtime display string'])
assert not errors,errors
print('PASS',len(paths),'public/canonical pages; both dash characters and entities; quotation, script and URL preservation')
