"""Regenerate only the homepage issue ticker from reviewed source records."""
import pathlib,json,re,html
R=pathlib.Path(__file__).resolve().parents[1];e=html.escape
d=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
# The original topic inventory is preserved in the archived source and live data.
original=json.loads((R/'content/archive/home-ticker-before-2026-10-02.json').read_text(encoding='utf-8'))['topics']
assert d['preservation']['originalTopics']==original, 'Original ticker inventory changed'
assert [x['headline'] for x in d['items'][:len(original)]]==original, 'Keep every original ticker topic before additions'
assert all(1<=len(x['headline'].split())<=3 for x in d['items']), 'Ticker labels must be one to three words'
links=[]
for item in d['items']:
 external=item['href'].startswith(('https://','http://'))
 links.append('<a href="'+e(item['href'])+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'><span>'+e(item['headline'])+'</span></a>')
block='''<!-- homepage-ticker:start -->
    <div class="p4a-marquee issue-ticker" role="region" aria-label="Political topics" data-issue-ticker>
      <button class="ticker-toggle" type="button" data-ticker-toggle aria-label="Pause ticker" aria-pressed="false" hidden>Ⅱ</button>
      <nav class="ticker-viewport" data-ticker-viewport aria-label="Political topics"><div class="marquee-track" data-ticker-track><div class="ticker-group" data-ticker-group>'''+''.join(links)+'''</div></div></nav>
    </div>
    <!-- homepage-ticker:end -->'''
p=R/'index.html';s=p.read_text(encoding='utf-8');s,n=re.subn(r'<!-- homepage-ticker:start -->.*?<!-- homepage-ticker:end -->',lambda m:block,s,flags=re.S);assert n==1;p.write_text(s,encoding='utf-8');print('Generated',len(links),'source-linked issue headlines.')
