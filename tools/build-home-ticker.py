"""Regenerate only the homepage issue ticker from reviewed source records."""
import pathlib,json,re,html
R=pathlib.Path(__file__).resolve().parents[1];e=html.escape
d=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
links=[]
for item in d['items']:
 external=item['href'].startswith(('https://','http://'))
 links.append('<a href="'+e(item['href'])+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'><small>'+e(item['scope'])+'</small><span>'+e(item['headline'])+'</span></a>')
block='''<!-- homepage-ticker:start -->
    <section class="p4a-marquee issue-ticker" aria-labelledby="ticker-title" data-issue-ticker>
      <div class="ticker-top"><h2 id="ticker-title">On the radar</h2><p>Issues and useful sources · checked '''+e(d['checked'])+''' · <a href="content/home-ticker.json">Source notes</a></p><button type="button" data-ticker-toggle aria-pressed="false" hidden>Pause ticker</button></div>
      <nav class="ticker-viewport" data-ticker-viewport aria-label="Current issues"><div class="marquee-track" data-ticker-track><div class="ticker-group" data-ticker-group>'''+''.join(links)+'''</div></div></nav>
    </section>
    <!-- homepage-ticker:end -->'''
p=R/'index.html';s=p.read_text(encoding='utf-8');s,n=re.subn(r'<!-- homepage-ticker:start -->.*?<!-- homepage-ticker:end -->',lambda m:block,s,flags=re.S);assert n==1;p.write_text(s,encoding='utf-8');print('Generated',len(links),'source-linked issue headlines.')
