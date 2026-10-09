"""One-time editorial pass for the agreed labels, topic order and inline icons."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1];D=R/'content/rooms'
order=['ai-copyright','child-safety','online-safety','gender-pay-gap','closing-the-gap','youth-crime','family-choices','marriage-divorce','super-housing','wealth-inequality','multinational-tax','ndis-scams','ai-scams','aged-care-scams','gambling-harm','fuel','tobacco','migration-equations','international-wars','security-fallacies','ancient-aliens','mental-health','psychedelic-mental-health','restricted-plants']
numbers={slug:n for n,slug in enumerate(order,23)}
labels={'restricted-plants':'Prohibited plants','psychedelic-mental-health':'Psychedelic care','tobacco':'Tobacco tax','fuel':'Fuel tax','ancient-aliens':'Ancient aliens','marriage-divorce':'Marriage & divorce'}
for slug in order:
 f=D/f'twinkle-{slug}.html';s=f.read_text(encoding='utf-8');n=numbers[slug]
 s=re.sub(r'Twinkle \d+ /',f'Twinkle {n:02d} /',s)
 prev='ptsd' if n==23 else order[n-24];nxt='tolls' if n==46 else order[n-22]
 s=re.sub(r'<a class="button button-secondary" href="twinkle-[^"]+">Previous Twinkle[^<]*</a>',f'<a class="button button-secondary" href="twinkle-{prev}.html">Previous Twinkle {n-1:02d}</a>',s)
 s=re.sub(r'<a class="button button-secondary" href="twinkle-[^"]+">Next Twinkle[^<]*</a>',f'<a class="button button-secondary" href="twinkle-{nxt}.html">Next Twinkle {n+1 if n<46 else 1:02d}</a>',s)
 s=s.replace('Plant prohibition','Prohibited plants')
 f.write_text(s,encoding='utf-8')
 f=D/f'{slug}.html';s=f.read_text(encoding='utf-8');s=re.sub(r'Twinkle \d+:',f'Twinkle {n:02d}:',s).replace('Plant prohibition','Prohibited plants');f.write_text(s,encoding='utf-8')
f=D/'twinkle-ptsd.html';s=f.read_text(encoding='utf-8');s=re.sub(r'href="twinkle-[^"]+">Next Twinkle[^<]*</a>','href="twinkle-ai-copyright.html">Next Twinkle 23</a>',s);f.write_text(s,encoding='utf-8')
f=D/'twinkle-tolls.html';s=f.read_text(encoding='utf-8').replace('href="twinkle-security-fallacies.html">Previous Twinkle 46','href="twinkle-restricted-plants.html">Previous Twinkle 46');f.write_text(s,encoding='utf-8')
hub=(D/'twinkle.html').read_text(encoding='utf-8')
cards={m[1]:m[0] for m in re.finditer(r'<a class="twinkle-card" href="twinkle-([^"]+)\.html">.*?</a>',hub,re.S)}
assert len(cards)==46,len(cards)
for slug in order:
 card=cards[slug];card=re.sub(r'<span>\d+</span>',f'<span>{numbers[slug]:02d}</span>',card);cards[slug]=card
first=hub.index(cards['ai-copyright'].split('<span>')[0])
# All post-original cards occupy the end of the seeds grid.
last=hub.index('</a>',hub.index('href="twinkle-security-fallacies.html"'))+4
hub=hub[:first]+''.join(cards[x] for x in order)+hub[last:]
def inline(m):
 slug,icon,num=m.groups()
 visual='<b class="olympic-rings" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></b>' if slug=='olympics' else icon
 return f'<a class="twinkle-card" href="twinkle-{slug}.html"><div class="seed-marker"><span>{num}</span>{visual}</div>'
hub=re.sub(r'<a class="twinkle-card" href="twinkle-([^"]+)\.html">(<img class="seed-icon"[^>]+>)<span>(\d+)</span>',inline,hub)
hub=hub.replace('Plant prohibition','Prohibited plants')
(D/'twinkle.html').write_text(hub,encoding='utf-8')

# Preserve original ticker order, then group additions by the reviewed topic sequence.
t=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
for item in t['items'][23:]:
 if item['headline']=='Plant prohibition':item['headline']='Prohibited plants'
extra=t['items'][23:];by_slug={}
for slug in order:
 matches=[x for x in extra if x['href']==f'pages/twinkle-{slug}.html']
 assert matches,slug
 by_slug[slug]=matches[0]
others=[x for x in extra if x not in by_slug.values()]
t['items']=t['items'][:23]+others+[by_slug[x] for x in order]
(R/'content/home-ticker.json').write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
nav=(R/'assets/site-nav.js').read_text(encoding='utf-8')
for slug,n in numbers.items():
 nav=re.sub(r"(href: 'pages/twinkle-"+re.escape(slug)+r"\.html', title: ['\"]Twinkle )\d+",lambda m:m[1]+str(n),nav)
nav=nav.replace('Plant prohibition','Prohibited plants').replace("title: 'Tobacco'","title: 'Tobacco tax'").replace("title: 'Fuel'","title: 'Fuel tax'")
(R/'assets/site-nav.js').write_text(nav,encoding='utf-8')
f=D/'site-map.html';s=f.read_text(encoding='utf-8')
for slug,n in numbers.items():s=re.sub(r'(href="twinkle-'+re.escape(slug)+r'\.html">Twinkle )\d+',lambda m:m[1]+f'{n:02d}',s)
s=s.replace('Plant prohibition','Prohibited plants');f.write_text(s,encoding='utf-8')
inv=json.loads((R/'content/public-topic-inventory.json').read_text(encoding='utf-8'))
for x in inv['requestedTopics']:
 if x['topic']=='Restricted plants and fungi':x['topic']='Prohibited plants'
inv['requestedTopics'].sort(key=lambda x: numbers.get(x['twinkle'].removeprefix('pages/twinkle-').removesuffix('.html'),0))
inv['newTwinkleOrder']=order
(R/'content/public-topic-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Tobacco is an open workbench on tax, affordability, trust and adult choice.
f=D/'tobacco.html';s=f.read_text(encoding='utf-8')
s=s.replace('A serious tobacco policy has to help people quit, reduce harm and confront illicit supply without treating smokers as the enemy.','What is tobacco excise trying to achieve, who carries the cost, and what would make the rules more trustworthy? Explore affordability, health, autonomy and reform on the same page.')
start=s.index('<div class="feature-panel"><h2>Keep three questions separate')
end=s.index('<div class="feature-panel"><h2>A public workbench',start)
body='''<div class="feature-panel"><h2>The price is a real public question</h2><p>For someone who smokes, a rising legal price is an immediate household cost. A government may describe the same tax as a health measure or a source of revenue. What evidence would show that the balance is working, and for whom? Distrust deserves an answer in visible numbers and clear objectives, rather than an assumption that the person asking wants harm.</p><p>Compare the tax component, retail price, household spending, consumption, quitting, substitution and revenue over the same period. Separate cigarettes, loose tobacco and vaping products. ABS’s June 2026 experimental illicit-source estimate covers total nicotine products including vapes; it is not a measure of the share of cigarette smokers using illicit tobacco.</p><div class="source-links"><a href="https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products">ABS: experimental tobacco and nicotine estimates</a><a href="https://www.ato.gov.au/illicittobacco">ATO: enforcement data and definitions</a></div></div>
<div class="feature-panel"><h2>What would you change?</h2><div class="clue-grid"><div class="clue"><strong>Pause, reduce or redesign excise</strong><span>Could ease legal-product costs and change the gap with untaxed supply. What would happen to retail pass-through, consumption, household budgets and public revenue? Which outcomes would justify keeping or reversing the change?</span></div><div class="clue"><strong>Retain price incentives, change the support</strong><span>Could preserve a price signal while making voluntary health and quitting support more accessible. How would the policy account for people who continue smoking and carry repeated cost increases?</span></div><div class="clue"><strong>Review autonomy and regulation together</strong><span>What restrictions are justified by harm to others, what belongs to informed adult choice, and how could quality, youth access and commercial incentives be handled? Personal cultivation has a separate reform room.</span></div></div></div>
<div class="feature-panel"><h2>Health evidence, without ending the argument</h2><p>Tobacco’s health harms matter to the comparison. They do not by themselves tell us the best tax rate, how to distribute costs, or which enforcement model works. A useful review could compare health outcomes, affordability and autonomy under several policies, including unintended effects. People interested in quitting can use the linked support; it is not a condition of joining this discussion.</p><div class="source-links"><a href="https://www.health.gov.au/topics/smoking-vaping-and-tobacco">Health evidence and public programmes</a><a href="https://www.quit.org.au/">Optional quitting support</a></div></div>
<div class="feature-panel"><h2>public receipt: test the bargain</h2><p>The Civic Ledger proposal offers a place to put tax receipts, programme spending, enforcement costs and measured outcomes beside one another. Ask representatives to publish the assumptions behind the excise path and compare credible alternatives. A person could submit a redacted household-cost example, a proposed tax redesign or a question about the evidence. No personal smoking history is needed.</p><div class="source-links"><a href="civic-ledger.html">Civic Ledger</a><a href="restricted-plants.html">Prohibited plants: reclassification and personal cultivation</a><a href="price-tax.html">Alcohol and tax choices</a><a href="twinkle-tobacco.html">Tobacco tax Twinkle</a></div></div>'''
s=s[:start]+body+s[end:]
# Remove the earlier appended tobacco panel, now covered by the full rewrite.
s=re.sub(r'<section class="section"><div class="page-copy"><div class="feature-panel"><h2>Tobacco tax: affordability, autonomy and trust</h2>.*?</section>','',s,flags=re.S)
f.write_text(s,encoding='utf-8')
for file in [D/'twinkle-tobacco.html',D/'twinkle.html']:
 s=file.read_text(encoding='utf-8').replace('A serious tobacco policy has to help people quit, reduce harm and confront illicit supply without treating smokers as the enemy.','What is tobacco excise trying to achieve, who carries the cost, and what would make the rules more trustworthy? Explore affordability, health, autonomy and reform on the same page.').replace('If the policy is about health, show the help as clearly as the tax.','Show us the tax, the evidence and the alternatives. Let’s examine the bargain.');file.write_text(s,encoding='utf-8')
print('Ordered 46 Twinkles; inline number/icon rows; Olympic rings; Prohibited plants; tobacco rewrite.')
