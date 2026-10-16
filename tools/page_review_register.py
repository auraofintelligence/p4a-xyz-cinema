"""Render the explicit reviewed page/rule register without advancing its dates."""
from pathlib import Path
import html
import json

ROOT=Path(__file__).resolve().parents[1]
SOURCE='content/history/civic-page-review-register-2026-10-17.json'

def load_register():
    return json.loads((ROOT/SOURCE).read_text(encoding='utf-8'))

def render_register(page,link):
    data=load_register()
    escape=lambda value:html.escape(str(value),quote=True)
    result='<section class="local-section" id="review-register"><p class="local-kicker">Page and rule updates · 17 October 2026</p><h2>What was built, and when?</h2><p>Nineteen new pages were verified on 17 October 2026. The original journey began on 16 October; the division pages were added on 17 October. Page updates and source research dates are recorded separately.</p>'
    for group in data['pageGroups']:
        rows=''.join('<tr><td>'+link(page,entry['path'],entry['label'])+'</td><td><time datetime="'+entry['lastUpdated']+'">'+entry['lastUpdated']+'</time></td><td>'+escape(entry['reviewWhen'])+'</td></tr>' for entry in group['pages'])
        result+='<details class="local-panel"><summary>'+escape(group['label'])+' · '+str(len(group['pages']))+' pages</summary><p>Work started '+group['workStarted']+' · first verified build '+group['firstVerifiedBuild']+'.</p><div class="local-table-scroll"><table class="local-table"><caption>'+escape(group['label'])+' review dates</caption><thead><tr><th>Page</th><th>Last updated</th><th>Review when</th></tr></thead><tbody>'+rows+'</tbody></table></div></details>'
    rows=''.join('<tr><td>'+link(page,entry['path'],entry['label'])+'</td><td>'+escape(entry['version'])+'</td><td>'+escape(entry['updated'])+'</td></tr>' for entry in data['rules'])
    result+='<details class="local-panel"><summary>Rules and their versions</summary><div class="local-table-scroll"><table class="local-table"><caption>Agent rule versions</caption><thead><tr><th>Rules</th><th>Version</th><th>Updated</th></tr></thead><tbody>'+rows+'</tbody></table></div></details>'
    result+='<p>'+link(page,SOURCE,'Full page register, changes and review triggers')+' · '+link(page,'content/history/redland.md','Chronological change history')+'</p><p>A page update is not a new Census observation, map edition or election notice. The source records keep those dates. Review before publishing and when the listed conditions change.</p></section>'
    return result

def write_review_notes():
    data=load_register()
    lines=['# Pages and rules review register','', 'Updated '+data['updated']+', Australia/Brisbane. This records the pages built in this local pass and the existing entry pages updated to reach them. Source research dates remain separate.','']
    for group in data['pageGroups']:
        lines+=['## '+group['label'],'','Work started '+group['workStarted']+'; first verified build '+group['firstVerifiedBuild']+'.','','| Page | Last updated | Change | Review when |','| --- | --- | --- | --- |']
        for entry in group['pages']:
            lines.append('| ['+entry['label']+'](../../'+entry['path']+') | '+entry['lastUpdated']+' | '+entry.get('change','Added a division overview with public representative links and connected local paths.')+' | '+entry['reviewWhen']+' |')
        lines+=['']
    lines+=['## Existing pages updated','','These were updated, rather than newly created.','','| Page | Updated | Change |','| --- | --- | --- |']
    for entry in data['updatedExistingPages']:
        lines.append('| ['+entry['label']+'](../../'+entry['path']+') | '+entry['lastUpdated']+' | '+entry['change']+' |')
    lines+=['','## Rules and versions','','| Rules | Version | Updated | Review when |','| --- | --- | --- | --- |']
    for entry in data['rules']:
        lines.append('| ['+entry['label']+'](../../'+entry['path']+') | '+entry['version']+' | '+entry['updated']+' | '+entry['reviewWhen']+' |')
    lines+=['','## Keeping this reviewable','']+[ '- '+rule for rule in data['maintenanceRules']]+['','[Machine-readable register](../../'+SOURCE+') · [Place history](../../'+data['history']+')','']
    (ROOT/'docs/releases/2026-10-17-page-and-rule-register.md').write_text('\n'.join(lines),encoding='utf-8')
