"""Keep original Twinkle wording in its nominated context home."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
START='<!-- earlier-twinkle-seeds:start -->'
END='<!-- earlier-twinkle-seeds:end -->'

def with_seed_context(page_name,document):
 source=ROOT/'content/twinkle-earlier-seeds.json'
 if not source.exists():return document
 seeds=[x for x in json.loads(source.read_text(encoding='utf-8')) if x.get('contextPage',x['destination'])==page_name]
 document=re.sub(re.escape(START)+'.*?'+re.escape(END),'',document,flags=re.S)
 if not seeds:return document
 if page_name.startswith('twinkle-'):
  blocks=[]
  for seed in seeds:
   blocks.append('<details class="feature-panel"><summary>Original Twinkle '+str(seed['number']).zfill(2)+' brief</summary><p>'+seed['hero']+'</p>'+seed['html']+'<p><a href="'+seed['destination']+'#policy-'+seed['slug']+'">Current policy proposal</a></p></details>')
  section=START+'<section class="section" id="earlier-twinkle-seeds"><div class="page-copy">'+''.join(blocks)+'</div></section>'+END
  return document.replace('</main>',section+'</main>',1)
 blocks=[]
 for seed in seeds:
  blocks.append('<details class="feature-panel"><summary>Twinkle '+str(seed['number']).zfill(2)+' - earlier seed and related proposals</summary><p>'+seed['hero']+'</p>'+seed['html']+'<p><a href="twinkle-'+seed['slug']+'.html">Back to Twinkle '+str(seed['number']).zfill(2)+'</a></p></details>')
 section=START+'<section class="section" id="earlier-twinkle-seeds"><div class="page-copy reveal"><h2>From the original Twinkle seeds</h2><p>Earlier clip briefs and proposals are kept here alongside the current evidence and options above. These are exploratory ideas, not adopted policy.</p>'+''.join(blocks)+'</div></section>'+END
 if '</details><!-- twinkle-policy-background:end -->' in document:
  return document.replace('</details><!-- twinkle-policy-background:end -->',section+'</details><!-- twinkle-policy-background:end -->',1)
 return document.replace('</main>',section+'</main>',1)

if __name__=='__main__':
 from web_link_policy import external_links
 for p in (ROOT/'pages').glob('*.html'):
  old=p.read_text(encoding='utf-8');new=with_seed_context(p.name,old)
  if new!=old:p.write_text(external_links(new),encoding='utf-8')
