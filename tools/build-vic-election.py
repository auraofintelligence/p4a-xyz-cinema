from web_link_policy import external_links
"""Generate the source-dated Victoria election page and direct-file browser data."""
import pathlib,json,re,html
R=pathlib.Path(__file__).resolve().parents[1];e=html.escape
def build():
 d=json.loads((R/'content/elections/vic-2026.json').read_text(encoding='utf-8'))
 source=(R/'states/vic/index.html').read_text(encoding='utf-8');header=re.search(r'<header class="site-header">.*?</header>',source,re.S)[0].replace('../../','../../../')
 cards=[]
 for c in sorted(d['candidates'],key=lambda c:(c['name'].casefold(),c['party'].casefold(),c['electorate'].casefold())):
  assert c['status'] in ['announced','preselected','nominated'] and c['chamber'] in ['assembly','council'] and c['source'].startswith('https://')
  label={'announced':'Announced','preselected':'Preselected','nominated':'Nominated — VEC verified'}[c['status']]
  actions=('<a href="'+e(c['profile'])+'">Profile</a>' if c.get('profile') else '')+'<a href="'+e(c['source'])+'">Source</a>'
  if c.get('areaId'):actions+='<a href="../map/index.html?chamber='+e(c['chamber'])+'&amp;electorate='+e(c['areaId'])+'&amp;section=election">Electorate</a>'
  extra='<p>Checked '+e(c['checked'])+'.'+(' Announcement dated '+e(c['announcedDate'])+'.' if c.get('announcedDate') else '')+'</p>'
  if c.get('notes'):extra+='<p>'+e(c['notes'])+'</p>'
  if c.get('conflict'):extra+='<p>'+e(c.get('conflict_details') or '')+'</p><p>'+e(c.get('conflict_resolution') or '')+'</p><a href="'+e(c.get('conflict_source_url') or c['source'])+'">Conflicting source</a>'
  summary='Source discrepancy and record details' if c.get('conflict') else 'Source dates and record details'
  caveat='<p class="ve-record-note">Affiliation; registered ballot label unverified.</p>' if c['party']=='Socialist Alliance' else ''
  cards.append('<article class="ve-candidate" id="'+e(c['id'])+'" data-candidate-id="'+e(c['id'])+'"><h3>'+e(c['name'])+'</h3><p class="ve-candidate-party">'+e(c['party'])+'</p><p class="ve-candidate-place">'+e(c['electorate'])+' · '+('Assembly' if c['chamber']=='assembly' else 'Council')+'</p><span class="ve-status" data-status="'+c['status']+'">'+label+'</span><div class="ve-candidate-actions">'+actions+'</div>'+caveat+'<details class="'+('ve-conflict ' if c.get('conflict') else '')+'ve-record-details"><summary>'+summary+'</summary>'+extra+'</details></article>')
 assert len({c['id'] for c in d['candidates']})==len(d['candidates'])
 timeline=''.join(f'<li><time datetime="{e(x["date"])}">{e(x["label"])}</time><div><h3>{e(x["title"])}</h3><p>{e(x["description"])}</p><a href="{e(x["source"])}">Official source ↗</a></div></li>' for x in d['timeline'])
 replacements={'STATUS_OPTIONS':''.join('<option value="'+e(status)+'">'+e({'announced':'Announced','preselected':'Preselected','nominated':'Nominated — VEC verified'}[status])+'</option>' for status in ['announced','preselected','nominated'] if any(c['status']==status for c in d['candidates'])),'HEADER':header,'REQUIREMENTS':d['requirementsHtml'],'TIMELINE':timeline,'COVERAGE':d['coverageHtml'],'COUNT':str(len(d['candidates'])),'CANDIDATES':'\n'.join(cards) or '<p>Source-verified candidate records are being prepared for this local draft.</p>','SOURCES':''.join('<li><a href="'+e(s['url'])+'">'+e(s['label'])+'</a> — '+e(s.get('note',''))+'</li>' for s in d['sources'])}
 page=(R/'tools/templates/vic-election.html').read_text(encoding='utf-8')
 for k,v in replacements.items():page=page.replace('@@'+k+'@@',v)
 page=external_links(page)
 assert '@@' not in page
 target=R/'states/vic/election';target.mkdir(exist_ok=True);(target/'index.html').write_text(page,encoding='utf-8');(R/'assets/vic-election-data.js').write_text('window.P4A_VIC_ELECTION = '+json.dumps(d,ensure_ascii=False)+';\n',encoding='utf-8');print('Built Victoria election page:',len(cards),'dated candidate records')
if __name__=='__main__':build()
