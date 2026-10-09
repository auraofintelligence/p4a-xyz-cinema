"""Merge attributed cross-repository evidence into the unpublished local map."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]

def merge_research(data,lines,link):
 source=R/'docs/planning/cross-repo-evidence-2026-10-03.json'
 if not source.exists():return data,lines
 research=json.loads(source.read_text(encoding='utf-8'))
 data['crossRepositoryResearch']=research
 data['housingRepository']=research['housingLocalExample']['status']
 for row in data['topics']:
  row['crossRepositoryAdditions']=research['topics'].get(str(row['number']),{'status':'Topic section missing from transferred research; verified local findings preserved without invented additions.'})
 summary=['## What to develop next','',
 'Start with **housing as the depth benchmark**, then repair the broad destinations that currently do not answer their gripe. Build on the authored work below rather than inventing a uniform policy template. This remains a planning map; no visitor room is being rewritten.', '',
 '- **Housing and supported living:** retain the many-pathway P4A room; use Capsule Surge Lab and Living Twin as relevant connections. Multi-site Minjerribah is a concrete local collaboration, not the missing housing-policy source.',
 '- **Work, ownership and care:** connect Mutual Futures succession and its capital calculator, current nonmonetary C-Hour, and 500 Queens.',
 '- **Compute, sovereignty and security:** use Ready S.E.T., Aura Direct Hardware, and the original Senate/AUKUS submissions; distinguish public tools from the proposed infrastructure.',
 '- **Food, power and continuity:** deepen Shared Table, Clean Energy Superpower, Community Wealth and Mutuals, and Disaster Kiosks into worked local cases.',
 '- **Families and public truth:** retain Global Group Marriages/U.N. of Love and Aura Politics; connect actual legal retrieval code, Legal Memory Workbench and the UNGA81 source transcript.', '',
 '**Version point:** '+research['currentCHour']+' The original local audit records what P4A currently says; where it mentions a future blockchain/receipt mechanism or contribution-based housing access, that is a version-reconciliation task, not the current C-Hour product.', '',
 '**Housing clarification from Luke:** Multi-site Minjerribah is an actual local plan he was invited to collaborate on with Indigenous people on Straddie. It is **not** the separate housing-policy work he meant. Keep the '+link('housing page',research['housingLocalExample']['url'])+' and '+link('document library',research['housingLocalExample']['documents'])+' as a concrete local example, without inferring a public mandate, completed implementation or wider endorsement. The separate housing-policy source remains unidentified; wait for a targeted lead.', '',
 '**Evidence stages:** locally exercised Markdown tools; externally reported browser tools/retrieval code; developed proposals and thought experiments; and supporting files whose title/path alone were verified are identified separately. The public researcher reports 168 repositories and 166 retrieved READMEs. This editor has not rerun that entire review.', '']
 missing=research.get('missingTransferredTopicSections',[])
 if missing:summary+=['**Transfer gap:** sections '+', '.join(str(x) for x in missing)+' were absent from the supplied research message, and #15 was partial. All 48 local rows remain complete; missing cross-repository additions are awaiting the exact text.','']
 at=lines.index('## What housing already does well');lines[at:at]=summary
 for i,line in enumerate(lines):
  if line.startswith('**The separate housing repository is unresolved.'):
   lines[i]='**Local link finding retained:** the existing Housing Simulations page directly links '+link('Shared Table Initiative source','https://github.com/auraofintelligence/shared-table-initiative')+' as a food/community pattern and links local ledger/builders. No separate housing-policy repository was found in this project. The external Multi-site page is useful in its local collaboration context, but Luke has explicitly ruled it out as the policy source he meant.'
  elif line.startswith('1. Resolve the separate housing repository'):
   lines[i]='1. Develop one housing case from the existing many-pathway room while awaiting a targeted lead to the separate housing-policy source. Use Multi-site only as its actual local collaboration, not a national framework.'
  elif line.startswith('Links below were found in the inspected P4A'):
   lines[i]='These original local references are preserved. The additional cross-repository register below records the supplied research and its source-status limits separately.'
  elif line.startswith('Outstanding: identify the separate housing repository;'):
   lines[i]='Outstanding: the separate housing-policy source remains unidentified; no broader search is planned without a targeted lead. '+('The missing transferred topic sections still need their exact research text. ' if missing else 'The supplied cross-repository topic research is merged. ')+'The next decision is which substantive room/case to develop. No visitor-page rewriting is included in this step.'
  elif line.startswith('The Senate Markdown was read directly.'):
   lines[i]=line+' The cross-repository report now supplies a public Markdown copy of the local-government submission and Shared Table findings; the original local fetch limitations remain historical facts, not a claim that those sources do not exist.'
 def additions(number):
  x=research['topics'].get(str(number))
  if not x:return ['**Cross-repository addition:** exact transferred section pending; the verified local findings above are retained.','']
  return ['**Additional authored work found across repositories:** '+x['additionalSubstance'],'','**Stage / remaining gap:** '+x['stageAndGap'],'','**Refined next step:** '+x['proposedNextWork'],'','**Specific project and supporting-document links:** '+'; '.join(link(research['sources'][key]['title'],research['sources'][key]['url'])+' ([repo]('+research['sources'][key]['repository']+'))' for key in x['sourceKeys'])+'.','']
 merged=[];current=None
 for line in lines:
  m=re.match(r'### (\d+)\.',line)
  if m or line=='## Project and supporting-document register':
   if current is not None:merged.extend(additions(current))
   current=int(m[1]) if m else None
  merged.append(line)
 if current is not None:merged.extend(additions(current))
 appendix=['## Additional cross-repository evidence register','', 'Source keys below are stable references in the structured map. Status descriptions are attributed to the supplied research unless they explicitly refer to a local check. PDF/DOCX file/title verification is not full-content verification. Current legal, financial, engineering and medical claims need case-specific evidence before implementation. AlphaInfinityFoundation retains its full name if included in later work.','']
 for key,x in research['sources'].items():
  appendix+=['- **'+key+' - '+link(x['title'],x['url'])+'** · '+link('Repository',x['repository'])+'. '+x['status']+'.']
 appendix+=['']
 at=merged.index('## Evidence and follow-up limits');merged[at:at]=appendix
 return data,merged
