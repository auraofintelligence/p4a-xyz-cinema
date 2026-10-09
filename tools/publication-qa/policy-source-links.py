"""Read-only public-link availability check; WAF blocks are reported separately."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urldefrag
import urllib.request,urllib.error,concurrent.futures,json,re
R=Path(__file__).resolve().parents[2]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and a.get('href','').startswith('https://'):self.urls.add(a['href'])
urls=set()
for p in (R/'content/rooms').glob('*.html'):
 d=Links();d.feed(p.read_text(encoding='utf-8'));urls.update(d.urls)
def check(url):
 try:
  req=urllib.request.Request(urldefrag(url)[0],headers={'User-Agent':'Mozilla/5.0 P4A public source link check'})
  with urllib.request.urlopen(req,timeout=12) as r:
   result={'url':url,'status':r.status,'resolved':r.url}
   if urlsplit(url).fragment and 'github.io' in url:
    s=r.read().decode('utf-8',errors='replace');result['anchorFound']=bool(re.search(r'id=[\"\']'+re.escape(urlsplit(url).fragment)+r'[\"\']',s))
   return result
 except urllib.error.HTTPError as e:return {'url':url,'status':e.code,'result':'blocked' if e.code in (403,429) else 'needs review'}
 except Exception as e:return {'url':url,'status':None,'result':type(e).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:results=list(pool.map(check,sorted(urls)))
(R/'tools/publication-qa/policy-source-links.json').write_text(json.dumps({'checked':'2026-10-03','results':results},indent=2)+'\n',encoding='utf-8')
print('Checked',len(results),'public URLs')
for x in results:
 if x['status']!=200 or x.get('anchorFound') is False:print(json.dumps(x))
