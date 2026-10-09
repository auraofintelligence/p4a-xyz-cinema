"""Keep the shared index and static sitemap in reviewed Twinkle order."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];D=R/'content/rooms'
inv=json.loads((R/'content/public-topic-inventory.json').read_text(encoding='utf-8'))
new=inv['newTwinkleOrder']
original=['tolls','food','insurance','workforce','housing','power','health','family-violence','childcare','beer-tax','datacentres','breaches','resources','triple-zero','aukus','revolving-door','donations','olympics','treaty','uap','deep-time','ptsd']
order=original+new
nav=(R/'assets/site-nav.js').read_text(encoding='utf-8')
for section in ['spark','system']:
 start=nav.index("id: '"+section+"'");left=nav.index('links: [',start)+len('links: [');right=nav.index('\n      ]',left)
 entries=re.findall(r'\{ href: .*?\}',nav[left:right])
 positions={e:i for i,e in enumerate(entries)}
 def key(e):
  href=re.search(r"href: '([^']+)'",e)[1]
  if section=='spark':
   if href=='pages/twinkle.html':return -1
   slug=href.removeprefix('pages/twinkle-').removesuffix('.html')
   return order.index(slug) if slug in order else 1000
  slug=href.removeprefix('pages/').removesuffix('.html')
  return 100+new.index(slug) if slug in new else positions[e]
 entries.sort(key=key)
 nav=nav[:left]+'\n        '+',\n        '.join(entries)+nav[right:]
nav=nav.replace('Twinkle 28: Tobacco','Twinkle 39: Tobacco tax').replace('Twinkle 29: Fuel','Twinkle 38: Fuel tax')
(R/'assets/site-nav.js').write_text(nav,encoding='utf-8')
# Put new rooms in one ordered sitemap group instead of two chronological batches.
f=D/'site-map.html';s=f.read_text(encoding='utf-8')
for heading in ['New Twinkle doors and policy rooms','More public questions','More Twinkle doors and public rooms']:
 s=re.sub(r'<section class="section"><div class="page-copy"><div class="feature-panel"><h2>'+heading+r'</h2>.*?</section>','',s,flags=re.S)
labels={x['href'].removeprefix('pages/twinkle-').removesuffix('.html'):x['headline'] for x in json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))['items']}
body='<section class="section"><div class="page-copy"><div class="feature-panel"><h2>More Twinkle doors and public rooms</h2><div class="source-links">'
destinations={x['twinkle'].removeprefix('pages/twinkle-').removesuffix('.html'):x['room'].removeprefix('pages/') for x in inv.get('followupTopics',[])}
for n,slug in enumerate(new,23):body+=f'<a href="twinkle-{slug}.html">Twinkle {n:02d}: {labels[slug]}</a><a href="{destinations.get(slug,slug+".html")}">{labels[slug]}: explore the room</a>'
body+='<a href="family-violence.html">Violence against women: explore the room</a><a href="price-tax.html">Alcohol: price and tax</a></div></div></div></section>'
s=s.replace('</main>',body+'</main>');f.write_text(s,encoding='utf-8')
print('Shared index and sitemap follow the reviewed topic order.')
