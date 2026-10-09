"""Prepare consistent local policy drafts from the existing Twinkle ideas.

No publishing, pushing, legal-status changes or fabricated pilot results.
"""
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit
import html, json, re, sys

BASE = Path(__file__).resolve().parents[1]
WORK = BASE
OUT = BASE

def section(r):
    e=html.escape
    return '<section class="section twinkle-policy-draft" id="policy-'+r['slug']+'" data-policy-draft="'+r['slug']+'"><div class="page-copy"><article class="feature-panel"><p class="eyebrow">Twinkle '+str(r['number']).zfill(2)+' / Working policy proposal</p><h2>'+e(r['policyTitle'])+'</h2><p class="policy-fix">'+e(r['proposal'])+'</p><h3>How it works</h3><ol>'+''.join('<li>'+e(x)+'</li>' for x in r['steps'])+'</ol><h3>Everyday example</h3><p>'+e(r['example'])+'</p><h3>Who acts and who pays</h3><p>'+e(r['deliveryAndFunding'])+'</p><h3>Fair-go safeguards</h3><p>'+e(r['safeguards'])+'</p><h3>How we know it works</h3><p>'+e(r['measures'])+'</p><div class="source-links"><a href="twinkle-'+r['slug']+'.html#clip">Twinkle '+str(r['number']).zfill(2)+' · video</a><a href="#policy-background">Evidence and related ideas</a></div></article></div></section>'

def write(rel,text):
    if rel.endswith('.html'):
        for name in ['twinkle-navigation.css','twinkle-navigation.js']:
            text=re.sub(r'(assets/'+re.escape(name)+r')(?:\?[^"\s]*)?',lambda m:m[1]+'?v=20261009-fairgo',text)
    path=OUT/rel
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8')

def build(proposals):
    sys.path.insert(0,str(BASE/'tools'))
    from public_copy import public_html
    from twinkle_seed_context import with_seed_context
    from web_link_policy import external_links
    groups=defaultdict(list)
    for r in proposals:groups[urlsplit(r['destination']).path].append(r)
    css=(BASE/'assets/twinkle-navigation.css').read_text(encoding='utf-8')
    css=re.sub(r'/\* twinkle-policy-upgrade:start \*/.*?/\* twinkle-policy-upgrade:end \*/','',css,flags=re.S)
    css=css.rstrip()
    css+='''\n/* twinkle-policy-upgrade:start */
.twinkle-clip-page .video-grid { display:block; margin:.8rem 0; }
.twinkle-clip-page .video-frame.video-portrait { width:min(100%,20rem); min-height:0; aspect-ratio:9/16; padding:1rem; margin:0 auto; box-sizing:border-box; }
.twinkle-clip-page .page-hero,.twinkle-policy-page .page-hero { min-height:0; padding:1.5rem clamp(1rem,4vw,3rem); }
.twinkle-policy-page .page-hero h1 { max-width:35ch; font-size:clamp(1.7rem,4vw,3rem); }
.twinkle-policy-page .twinkle-policy-context { padding-block:.5rem; }
.twinkle-policy-page .twinkle-policy-context .feature-panel { padding:.8rem 1rem; }
.twinkle-clip-page .video-brief { margin:.6rem auto 1rem; max-width:42rem; text-align:center; }
.twinkle-policy-draft { padding-block:1rem; scroll-margin-top:6rem; }
.twinkle-policy-draft .feature-panel { padding:clamp(1rem,3vw,1.6rem); }
.twinkle-policy-draft .policy-fix { font-size:1.15rem; color:var(--text,#fff); margin-bottom:1rem; }
.twinkle-policy-draft h3 { color:var(--gold); font-size:1.05rem; margin:1rem 0 .35rem; }
.twinkle-policy-draft p { margin:.35rem 0 .6rem; }
.twinkle-policy-draft ol { margin:.4rem 0; padding-left:1.3rem; }
.twinkle-policy-draft li { margin:.4rem 0; }
.twinkle-policy-draft[hidden] { display:none; }
.policy-background { padding-block:.75rem; }
.policy-background summary { cursor:pointer; color:var(--gold); font-weight:700; padding:.7rem 0; }
.policy-background .section { padding-block:1rem; }
.policy-background-note { margin:0 0 .5rem; color:var(--muted); }
/* twinkle-policy-upgrade:end */
'''
    write('assets/twinkle-navigation.css',css)
    brief='A 15–60 second vertical Twinkle, filmed or AI-generated, with the sound of urine tinkling in the background. Start with the gripe, land the joke, then point to the fair-go fix.'
    video='<div class="video-grid"><div class="video-frame video-portrait" role="img" aria-label="Vertical Twinkle video placeholder, 9:16, 15 to 60 seconds"><span>Twinkle video placeholder</span><strong>9:16 · 15–60 seconds</strong></div></div><p class="video-brief">'+html.escape(brief)+'</p>'
    for r in proposals:
        name='twinkle-'+r['slug']+'.html'
        for folder in ['content/rooms','pages']:
            text=(BASE/folder/name).read_text(encoding='utf-8')
            # Known two-frame markup, replaced as one complete block.
            text,n=re.subn(r'<div class="video-grid"[^>]*>\s*<div class="video-frame video-landscape"[^>]*>.*?</div>\s*<div class="video-frame video-portrait"[^>]*>.*?</div>\s*</div>',lambda _:video,text,count=1,flags=re.S)
            if n==0:
                text,n=re.subn(r'<div class="video-grid"[^>]*>\s*<div class="video-frame video-portrait"[^>]*>.*?</div>\s*</div>\s*<p class="video-brief">.*?</p>',lambda _:video,text,count=1,flags=re.S)
            assert n==1,name
            text=re.sub(r'<div class="feature-panel"><h2>The one-breath drop</h2><p>.*?</p></div>','',text,count=1,flags=re.S)
            write(folder+'/'+name,text)
    for name,connected in groups.items():
        source=BASE/'content/rooms'/name
        text=(source if source.exists() else BASE/'pages'/name).read_text(encoding='utf-8')
        text=re.sub(r'<!-- earlier-twinkle-seeds:start -->.*?<!-- earlier-twinkle-seeds:end -->','',text,flags=re.S)
        text=text.replace('<body data-theme="royal">','<body data-theme="royal" class="twinkle-policy-page">',1)
        # Idempotent: retain substantive background and historic source material.
        text=re.sub(r'<!-- twinkle-policy-upgrade:start -->.*?<!-- twinkle-policy-upgrade:end -->','',text,flags=re.S)
        if '<!-- twinkle-policy-background:start -->' in text:
            text=re.sub(r'<!-- twinkle-policy-background:start --><details class="policy-background" id="policy-background"[^>]*><summary>.*?</summary>','',text,count=1,flags=re.S).replace('</details><!-- twinkle-policy-background:end -->','')
        hero=re.search(r'<section\b.*?</section>',text,re.S)
        assert hero,name
        context=re.search(r'<section class="section twinkle-policy-context".*?</section>',text,re.S)
        assert context,name
        insertion=context.end()
        main_end=text.index('</main>',insertion)
        background=text[insertion:main_end]
        background=re.sub(r'<p class="policy-background-note">.*?</p>','',background,flags=re.S)
        # Background still retains dates, source links and developed architecture;
        # its generic workbench prompts are no longer the main policy answer.
        top='<!-- twinkle-policy-upgrade:start -->'+''.join(section(r) for r in connected)+'<!-- twinkle-policy-upgrade:end -->'
        role_links='<p class="policy-background-note">Delivery roles: <a href="https://peo.gov.au/understand-our-parliament/how-parliament-works/three-levels-of-government/">Australia\'s three levels of government</a> · <a href="https://www.parliament.vic.gov.au/about/how-parliament-works/what-is-parliament">Victoria\'s parliamentary responsibilities</a>. New delivery arrangements here are working proposals, not statements that a pilot is operating or a reform is already law.</p>'
        wrapper='<!-- twinkle-policy-background:start --><details class="policy-background" id="policy-background"><summary>Evidence, sources and related ideas</summary>'+role_links+background+'</details><!-- twinkle-policy-background:end -->'
        text=text[:insertion]+top+wrapper+text[main_end:]
        first=connected[0]
        # Uniform compact policy hero: specific gripe first, shared architecture below.
        title=first['policyTitle'] if len(connected)==1 else ' / '.join(r['policyTitle'].split(':')[0] for r in connected)
        text=re.sub(r'(<p class="eyebrow">).*?(</p>)',lambda m:m[1]+'Fair-go policy / Local working draft'+m[2],text,count=1,flags=re.S)
        text=re.sub(r'<h1>.*?</h1>',lambda _:'<h1>'+html.escape(title)+'</h1>',text,count=1,flags=re.S)
        text=re.sub(r'<p class="hero-copy">.*?</p>',lambda _:'<p class="hero-copy">'+html.escape(first['gripe'] if len(connected)==1 else 'Practical proposals for the connected Twinkles. Choose a topic below.')+'</p>',text,count=1,flags=re.S)
        hero_actions='<div class="hero-actions"><a class="button button-primary" href="#policy-'+first['slug']+'">The fair-go fix</a><a class="button button-secondary" data-policy-video href="twinkle-'+first['slug']+'.html#clip">Twinkle '+str(first['number']).zfill(2)+' · video</a><a class="button button-secondary" href="twinkle.html">All 49 Twinkles</a></div>'
        text=re.sub(r'<div class="hero-actions">.*?</div>',lambda _:hero_actions,text,count=1,flags=re.S)
        # Put the reader at substantive content rather than the older explainer.
        text=re.sub(r'(<a\b[^>]*class="button button-primary"[^>]*href=")[^"]*(")',lambda m:m[1]+'#policy-'+first['slug']+m[2],text,count=1)
        write('content/rooms/'+name,text)
        published=external_links(public_html(name,with_seed_context(name,text)))
        write('pages/'+name,published)
    # Home displays the first ten identities, avoiding gaps without renumbering.
    home=(BASE/'index.html').read_text(encoding='utf-8')
    hub=(BASE/'pages/twinkle.html').read_text(encoding='utf-8')
    cards={slug:markup for markup,slug in re.findall(r'(<article class="twinkle-entry"[^>]*data-twinkle="([^"]+)".*?</article>)',hub,re.S)}
    assert len(cards)==49
    homecards=''.join(cards[r['slug']].replace('href="twinkle-','href="pages/twinkle-').replace('href="'+urlsplit(r['destination']).path,'href="pages/'+urlsplit(r['destination']).path).replace('src="../assets/','src="assets/') for r in proposals[:10])
    home,n=re.subn(r'(<div class="twinkle-grid home-door-grid reveal">).*?</article>(\s*</div>)',lambda m:m[1]+'\n'+homecards+m[2],home,count=1,flags=re.S)
    assert n==1
    write('index.html',home)
    js=(BASE/'assets/twinkle-navigation.js').read_text(encoding='utf-8')
    js=re.sub(r'\n // twinkle-policy-upgrade:start.*?\n // twinkle-policy-upgrade:end','',js,flags=re.S)
    pos=' const heading = document.createElement('
    addition='''
 // twinkle-policy-upgrade:start
 const draft = document.querySelector('[data-policy-draft="'+record.slug+'"]');
 if(draft){
   document.querySelectorAll('[data-policy-draft]').forEach(section=>{section.hidden=section!==draft;});
   const title=draft.querySelector('h2'); const fix=draft.querySelector('.policy-fix');
   if(title)document.querySelector('.page-hero h1').textContent=title.textContent;
   document.querySelector('.page-hero .hero-copy').textContent=record.gripe;
   const primary=document.querySelector('.page-hero .button-primary');
   if(primary){primary.href='#'+draft.id;primary.textContent='The fair-go fix';}
   const video=document.querySelector('[data-policy-video]');
   if(video){video.href=record.clip+'#clip';video.textContent='Twinkle '+String(record.number).padStart(2,'0')+' · video';}
 }
 // twinkle-policy-upgrade:end
'''
    assert pos in js
    js=js.replace(pos,addition+pos,1)
    js=js.replace('panel.replaceChildren(label,heading,gripe,actions);','panel.replaceChildren(label,actions);')
    # Preserve existing anchor destinations and add the new substantive section.
    if "actions.append(link('The fair-go fix'" not in js:
        js=js.replace("const anchor=record.destination.split('#')[1];", "actions.append(link('The fair-go fix','#policy-'+record.slug,'button button-primary')); const anchor=record.destination.split('#')[1];")
    js=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',js)
    write('assets/twinkle-navigation.js',js)
    # Keep the historic production notes below the same evidence disclosure.
    seed_tool=(BASE/'tools/twinkle_seed_context.py').read_text(encoding='utf-8')
    seed_return=" return document.replace('</main>',section+'</main>',1)"
    seed_replacement=" if '</details><!-- twinkle-policy-background:end -->' in document:\n  return document.replace('</details><!-- twinkle-policy-background:end -->',section+'</details><!-- twinkle-policy-background:end -->',1)\n"+seed_return
    if "if '</details><!-- twinkle-policy-background:end -->' in document:" not in seed_tool:
        assert seed_return in seed_tool
        seed_tool=seed_tool.replace(seed_return,seed_replacement,1)
    write('tools/twinkle_seed_context.py',seed_tool)
    # Apply the same placement now, without importing a different cached module.
    for name in groups:
        path=OUT/'pages'/name
        text=path.read_text(encoding='utf-8')
        archive=re.search(r'<!-- earlier-twinkle-seeds:start -->.*?<!-- earlier-twinkle-seeds:end -->',text,re.S)
        if archive:
            block=archive[0]
            text=text[:archive.start()]+text[archive.end():]
            text=text.replace('</details><!-- twinkle-policy-background:end -->',block+'</details><!-- twinkle-policy-background:end -->',1)
            write('pages/'+name,text)
    write('content/twinkle-policy-drafts.json',json.dumps(proposals,ensure_ascii=False,indent=2)+'\n')
    return len(groups)

if __name__=='__main__':
    proposals=json.loads((BASE/'content/twinkle-policy-drafts.json').read_text(encoding='utf-8'))
    assert len(proposals)==49
    rooms=build(proposals)
    print(json.dumps({'twinkles':len(proposals),'policyRooms':rooms,'localOnly':True}))
