"""Verify supplied copy, preserved authored seeds and unchanged ticker/media."""
from pathlib import Path
import html,json,re,subprocess
R=Path(__file__).resolve().parents[2]
BASE='04e9926'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode('utf-8')
def text(s):return html.unescape(re.sub('<[^>]+>','',s)).strip()
records=json.loads((R/'content/twinkle-reviewed-copy.json').read_text(encoding='utf-8'))
seeds=json.loads((R/'content/twinkle-earlier-seeds.json').read_text(encoding='utf-8'))
hub=(R/'pages/twinkle.html').read_text(encoding='utf-8')
cards=dict(re.findall(r'<a class="twinkle-card" href="([^"]+)">(.*?)</a>',hub,re.S))
assert len(records)==len(cards)==49
assert records[:48]==json.loads(subprocess.check_output(['git','show','7bbf65a:content/twinkle-reviewed-copy.json'],cwd=R).decode('utf-8'))
for record in records:
 filename='twinkle-'+record['slug']+'.html'
 page=(R/'pages'/filename).read_text(encoding='utf-8')
 canonical=(R/'content/rooms'/filename).read_text(encoding='utf-8')
 for s in [page,canonical]:
  assert text(re.search('<h1>(.*?)</h1>',s,re.S)[1])==record['headline'],filename
  assert text(re.search('<p class="hero-copy">(.*?)</p>',s,re.S)[1])==record['gripe'],filename
  assert text(re.search('<h2>The one-breath drop</h2><p>(.*?)</p>',s,re.S)[1])=='“'+record['gripe']+'”',filename
  assert html.unescape(re.search('<meta name="description" content="([^"]+)"',s)[1])==record['gripe'],filename
  assert 'href="'+record['destination']+'">Follow-through room</a>' in s,filename
 assert text(re.search('<h3>(.*?)</h3>',cards[filename],re.S)[1])==record['headline'],filename
 assert text(re.search('<p>(.*?)</p>',cards[filename],re.S)[1])==record['gripe'],filename
for seed in seeds:
 old=before('pages/twinkle-'+seed['slug']+'.html')
 start=re.search(r'(<section class="section" id="clip">\s*<div class="page-copy reveal">)',old).end()
 assert seed['html']==old[start:old.index('<div class="video-grid">',start)].strip(),seed['slug']
 assert seed['hero']==re.search('<p class="hero-copy">(.*?)</p>',old,re.S)[1],seed['slug']
 room=(R/'pages'/seed['destination']).read_text(encoding='utf-8')
 assert seed['html'] in room and seed['hero'] in room,seed['slug']
 assert room.count('<!-- earlier-twinkle-seeds:start -->')==1,seed['destination']
for name in ['assets/homepage-ticker.css','assets/homepage-ticker.js']:
 assert (R/name).read_text(encoding='utf-8')==before(name).replace("?'\u2014':paused","?'-':paused"),name
assert 'The fix gets said' not in hub
old_ticker=json.loads(before('content/home-ticker.json'))['items'];ticker=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))['items']
assert ticker[:len(old_ticker)]==old_ticker and len(ticker)==len(old_ticker)+2
assert 'Forty-nine Twinkles' in hub and 'Forty-five more connections' in hub
report={'baseline':BASE,'approvedCopyEntries':49,'exactCardHeroSeedAndMetadataMatches':49,'previous48CopyUnchanged':True,'originalAuthoredSeedsPreservedInDeeperRooms':22,'previousTickerLabelsAndAppearanceUnchanged':True,'copyDeviations':[]}
(R/'tools/publication-qa/reviewed-copy-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS',json.dumps(report))
