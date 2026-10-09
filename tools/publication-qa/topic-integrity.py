"""Meaningful integration checks for topic coverage, media and ticker regression."""
from pathlib import Path
import subprocess,json,re,hashlib
R=Path(__file__).resolve().parents[2]
def old(path):return subprocess.check_output(['git','show','a33bb49:'+path],cwd=R).decode('utf-8')
inventory=json.loads((R/'content/public-topic-inventory.json').read_text(encoding='utf-8')); total=inventory['totalTwinkles']
t=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
baseline=json.loads(old('content/home-ticker.json'))
assert [(x['headline'],x['href']) for x in t['items'][:23]]==[(x['headline'],x['href']) for x in baseline['items'][:23]]
assert all(1<=len(x['headline'].split())<=3 for x in t['items'])
for f in ['assets/homepage-ticker.css','assets/homepage-ticker.js']:
 assert (R/f).read_text(encoding='utf-8')==old(f).replace("?'\u2014':paused","?'-':paused"),f
hub=(R/'pages/twinkle.html').read_text(encoding='utf-8');nav=(R/'assets/site-nav.js').read_text(encoding='utf-8');sm=(R/'pages/site-map.html').read_text(encoding='utf-8')
cards=re.findall(r'<a class="twinkle-card" href="(twinkle-[^"]+\.html)">(.*?)</a>',hub,re.S)
assert len(cards)==total and len(set(x[0] for x in cards))==total
for filename,body in cards:
 assert '<div class="seed-marker"><span>' in body and ('class="seed-icon"' in body or 'class="olympic-rings"' in body),filename
 assert any(x['href']=='pages/'+filename for x in t['items']),filename
 assert filename in nav and filename in sm,filename
 for asset in re.findall(r'src="\.\./([^"]+)"',body):assert (R/asset).exists(),asset
games=dict(cards)['twinkle-olympics.html'];assert games.count('<i></i>')==5
inventory=json.loads((R/'content/public-topic-inventory.json').read_text(encoding='utf-8'));assert len(inventory['requestedTopics'])==24
for topic in inventory['requestedTopics']+inventory.get('followupTopics',[]):
 assert (R/topic['twinkle']).exists() and (R/topic['room']).exists()
for n,(filename,body) in enumerate(cards,1):
 assert f'<span>{n:02d}</span>' in body,[filename,n]
 s=(R/'pages'/filename).read_text(encoding='utf-8')
 prev=cards[(n-2)%total][0];nxt=cards[n%total][0]
 assert prev in s and nxt in s,[filename,prev,nxt]
 if n<=22:
  before=old('pages/'+filename)
  media=lambda x:re.findall(r'<(?:video|source|iframe)\b[^>]*>',x)+re.findall(r'class="video-frame[^\"]*"',x)
  assert media(before)==media(s),filename
for listing in [[f for f,b in cards],[x['href'] for x in t['items']]]:
 i=next(i for i,x in enumerate(listing) if 'psychedelic-mental-health' in x)
 assert 'mental-health' in listing[i-1] and 'restricted-plants' in listing[i+1]
 assert not any('child' in x or 'youth' in x for x in listing[max(0,i-2):i+3])
def snapshot():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'index.html',*R.glob('pages/*.html')]}
before=snapshot()
subprocess.run(['python','tools/build-policy-rooms.py'],cwd=R,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['python','tools/build-home-ticker.py'],cwd=R,check=True,stdout=subprocess.DEVNULL)
assert snapshot()==before,'Generators must be idempotent'
report={'checked':'2026-10-04','requestedTopics':24,'twinkles':total,'inlineVisualCoverage':total,'tickerLabels':len(t['items']),'originalTickerTopicsPreserved':23,'tickerStyleAndBehaviourPreserved':True,'reducedMotionSymbol':'ASCII hyphen by user request','originalTwinkleMediaPreserved':22,'sequenceAndDestinations':True,'adultResearchGrouping':True,'generatorsIdempotent':True}
(R/'tools/publication-qa/topic-integrity-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS',json.dumps(report))
