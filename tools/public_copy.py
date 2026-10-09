"""Public-facing copy rules. Originals, legal notices and research archives are not rewritten."""
from pathlib import Path
import re,html
from html.parser import HTMLParser
from public_punctuation import public_punctuation
ROOT=Path(__file__).resolve().parents[1]

def panel(title,body,links=()):
 return '<div class="feature-panel"><h2>'+title+'</h2><p>'+body+'</p>'+ ('<div class="source-links">'+''.join('<a href="'+u+'"'+(' target="_blank" rel="noopener noreferrer"' if u.startswith('https:') else '')+'>'+label+'</a>' for u,label in links)+'</div>' if links else '')+'</div>'
base='https://auraofintelligence.github.io/'
# These are direct mechanisms retained by the association-fit review, not a generic project box.
DIRECT={
 'ai-scams':panel('Recognising an impersonation','The AI Trust Index Australia guide describes AI-voice and fake-video scams. Use it as a literacy resource alongside the official reporting and recovery routes above; it is not an authentication service or scam detector.',[(base+'strange-but-true-ai-trust-index/australia.html','AI scam literacy guide')]),
 'closing-the-gap':panel('Put decision rights in the agreement','Nation-authored agreement records can identify who decides, what is funded and how obligations can be reviewed. Country-controlled return proposals and cultural-data permissions address specific control over resources and information. These proposals do not establish consent, endorsement or measured outcomes.',[(base+'p4a-native-nations-cinema/','Nation-authored agreement workbench'),(base+'moreton-bay-community-wealth-and-mutuals/country-deals.html','Resource control and returns'),(base+'ready-set-co-op-cultural-intelligence-node/culture.html','Cultural-data permissions')]),
 'gender-pay-gap':panel('Who gets to lead and invest?','500 Queens and Designing Equality explore women’s executive and investment decision-making pathways. That is a specific leadership and ownership lever. Judge its outcomes separately from equal pay, progression and caring penalties; a proposal is not evidence that the pay gap has closed.',[(base+'500-Queens-VC-2026/designing-equality.html','Leadership and investment design')]),
 'family-choices':panel('Share care without surrendering a voice','Global Group Marriages explores an optional household structure for sharing care, resources and responsibility while preserving individual autonomy. Compare actual time, costs, entry and exit arrangements with other household choices. A different family structure does not remove every financial pressure or conflict.',[(base+'global-group-marriages/framework.html','Household framework'),(base+'global-group-marriages/sovereignty-care.html','Sovereignty and care')]),
 'migration-equations':panel('Inspect a local capacity model','Minjerribah Living Twin models residents, housing, jobs, prices and service dependencies. Its work-in-progress simulation offers assumptions to inspect when designing a capacity comparison. It is not a validated migration forecast, and its public-record model does not speak for Traditional Owners.',[(base+'minjerribah-living-twin/','Local capacity simulation'),('https://github.com/auraofintelligence/minjerribah-living-twin','Model documentation and limits')]),
 'psychedelic-mental-health':panel('From a research concept to a care pathway','Consciousness Parlor proposes professionally guided psychedelic research and therapy. Examine preparation, supervision, follow-up, consent and access costs against condition-specific evidence. The concept is not an operating clinic, an approved protocol or proof of effective treatment.',[(base+'aura-ecosystem/consciousness-parlor.html','Consciousness Parlor research concept')]),
 'restricted-plants':panel('Name the rule you want changed','A useful reform case identifies the substance, conduct and jurisdiction, then compares the exact provision, evidence of harm and proposed change. The Relevance Ladder and Australian Legal Engine support legal inquiry and source retrieval; they are not an adopted plant policy or a substitute for legal advice.',[(base+'australian-law-2012-lukes-relevance/','Relevance Ladder: examining a law'),('https://github.com/auraofintelligence/australian-legal-engine','Source-linked legal retrieval')]),
 'wealth-inequality':panel('Test a change in productive ownership','Mutual Futures explores business succession into shared ownership, technology upgrades and learning. Its capital and succession workbenches make financing and control assumptions inspectable. A case should show debt, wages, reserves, decision rights and who carries losses; shared ownership does not guarantee returns.',[(base+'mutual-futures/capital.html','Capital comparison'),(base+'mutual-futures/succession.html','Succession workbench'),(base+'moreton-bay-community-wealth-and-mutuals/wealth-funds.html','Community ownership and returns')]),
 'international-wars':panel('Compare peaceful capability','The UNGA81 capability argument and AUKUS submission examine civilian capability and strategic alternatives. Science, health, learning and disaster resilience can be compared with defence choices on their actual purposes, costs and dependencies. A civilian facility and a submarine do different jobs.',[(base+'UNGA81-Luke-Hayes/capability.html','Capability without domination'),(base+'aukus-space-gambit/','Space Gambit thought experiment')]),
 'security-fallacies':panel('Test the dependency, not the promise','The missing-middle compute proposal treats skills, local recovery and the ability to change providers as security assets. Compare concentrated and distributed capability against specific failures, costs and recovery tasks. Distribution alone does not guarantee security, and infrastructure is only one part of this wider debate.',[(base+'UNGA81-Luke-Hayes/capability.html','Capability and dependency'),(base+'ready-set-co-op-cultural-intelligence-node/','Community compute proposal')]),
}
REMOVE={'aged-care-scams','gambling-harm','ndis-scams','online-safety','youth-crime'}
OVERRIDES={
 ('child-safety','A local alternative needs safeguards too'):'',
 ('mental-health','Luke’s care pathways, tested in public'):panel('Help people find the next step','The Mental Health Support venture brief proposes non-clinical navigation with maintained resources and a named owner. Test whether people find appropriate support and complete handovers. Navigation cannot replace qualified care or solve a shortage of appointments.',[(base+'500-Queens-VC-2026/startup-mental-health-support.html','Non-clinical navigation proposal')]),
 ('super-investments','Luke’s public receipts, applied to retirement money'):'',
 ('tobacco','Luke’s public receipt: test the bargain'):panel('Test the bargain','Ask representatives to publish excise assumptions, programme spending, enforcement costs and measured outcomes. Submit a redacted household-cost example, a proposed tax redesign or a specific evidence question. No personal smoking history is needed.',[('twinkle-tobacco.html','Tobacco tax Twinkle')]),
 ('super-housing','Show the whole household path'):panel('Show the whole household path','Compare super balance and returns, rent avoided, deposit, interest, repayments, maintenance, transaction costs, price changes and retirement housing security. Include people without a deposit or substantial super, and run downside cases. This is a policy comparison, not personal financial advice.'),
 ('fuel','Make a local trip ledger'):panel('Compare the actual journey','A route comparison should show cost, time, accessibility, fuel or charging access and disruption for workers, passengers and freight. Moreton Bay Autonomous Mobility proposes an alternative service model to examine; it is not an operating service or a tax reform.',[(base+'moreton-bay-autonomous-mobility/','Passenger and freight proposal')]),
 ('ancient-aliens','Luke’s tools for a good rabbit hole'):panel('Follow the object, story and evidence','Cosmic Nexus offers research lanes for ancient-astronaut questions and competing explanations. Keep dates, provenance, translations and uncertainty attached to a claim. The Alien Necklace film is a creative doorway, not archaeological evidence.',[(base+'strange-but-true-cosmic-nexus/','Cosmic Nexus research lanes'),('alien-necklace-film.html','Alien Necklace film'),('twinkle-uap.html','UAP observations')]),
}

class Panels(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=False);self.text=text;self.lines=[0];self.stack=[];self.spans=[]
  for m in re.finditer('\n',text):self.lines.append(m.end())
  self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='div':
   pos=self.lines[self.getpos()[0]-1]+self.getpos()[1];self.stack.append((pos,'feature-panel' in dict(attrs).get('class','').split()))
 def handle_endtag(self,tag):
  if tag=='div' and self.stack:
   start,feature=self.stack.pop()
   if feature:self.spans.append((start,self.lines[self.getpos()[0]-1]+self.getpos()[1]+6))

def neutral_copy(text):
 # Protect addresses, project identifiers and real external authorship. These substitutions target display copy.
 urls=[]
 def stash(m):urls.append(m[0]);return 'PUBLIC_URL_'+str(len(urls)-1)+'_END'
 text=re.sub(r'https?://[^\s<>"\']+',stash,text)
 replacements={
 'Built on Minjerribah by Luke × Claude.':'A civic workbench, started on Minjerribah.',
 'The original cinematic site was created by Luke Nathan Hayes with Claude. The October 2026 Victoria workbench and maintenance were developed with Codex. Original design and project credits remain with their authors.':'Explore evidence, compare proposals and learn from tools that make public decisions easier to question. The workbench is open to contributions and corrections; it is not a personal election campaign.',
 'Australian Law: Luke’s Relevance':'Australian Law: Relevance Ladder',"Australian Law: Luke's Relevance":'Australian Law: Relevance Ladder',
 'UNGA81: Luke Hayes':'UNGA81: capability and a fair go',
 "Luke Nathan Hayes's personal UNGA81 contribution, connected with the Fair Go discussion. This is not an official UN endorsement.":'A contribution on capability, public participation and a fair go. It is not an official UN endorsement.',
 'Luke Nathan Hayes&#x27;s personal UNGA81 contribution, connected with the Fair Go discussion. This is not an official UN endorsement.':'A contribution on capability, public participation and a fair go. It is not an official UN endorsement.',
 'Submission 2 by Luke Nathan Hayes':'Local government funding inquiry: submission 2',
 'Submission 2: Luke Nathan Hayes':'Local government funding inquiry: submission 2',
 'Starting map drafted Luke x Claude from a Claude deep-research run':'Starting map developed from an AI-assisted research draft',
 'Drafted Luke x Claude.':'An exploratory research draft.',
 "Luke proposes an additional family form":'The framework proposes an additional family form',
 'Luke: capability without domination':'Capability without domination',
 'Anyone can run it without asking Luke; anyone can check the work afterwards.':'Anyone can run the documented process and check the work afterwards.',
 'anyone should be able to add a supplier without asking Luke.':'anyone should be able to add a supplier through the documented process.',
 "Strange But True is Luke's sole trader pattern library, not a mandate.":'The linked field examples are optional patterns, not a mandate.',
 "Strange But True is Luke's personal sole trader business and can be used as one pattern library for practical field setup.":'The linked field examples offer one optional pattern library for practical setup.',
 'his Web3 global sensorium plan':'the Web3 global sensorium proposal',
 'sits missing middle:':'sits the missing middle:',
 'public-resource receipt should record':'A public-resource record should record',
 'It is marriage-based simulacrum':'It is a marriage-based simulacrum',
 'His Protopian Gambit':'The Protopian Gambit',
 'His Oceania and Native Nations connections':'The separate Oceania and Native Nations projects',
 }
 for a,b in replacements.items():text=text.replace(a,b)
 text=re.sub(r"\bLuke(?:’s|'s|&#x27;s|&#39;s|&rsquo;s)\s+",'',text)
 text=text.replace('The The missing-middle proposal','The missing-middle proposal')
 text=re.sub(r'(?<!The )missing-middle proposal adds public access','The missing-middle proposal adds public access',text)
 for i,u in enumerate(urls):text=text.replace('PUBLIC_URL_'+str(i)+'_END',u)
 return text

def public_html(name,text):
 stem=Path(name).stem
 # Apply the relevance audit before removing personal framing, including reruns of older room generators.
 for a,b in sorted(Panels(text).spans,reverse=True):
  raw=text[a:b];m=re.search(r'<h2[^>]*>(.*?)</h2>',raw,re.S)
  if not m:continue
  title=html.unescape(re.sub('<[^>]+>','',m[1]));replacement=None
  if title.casefold() in ['luke’s related solutions','related solutions']:
   if stem in REMOVE:replacement=''
   elif stem in DIRECT:replacement=DIRECT[stem]
  if (stem,title) in OVERRIDES:replacement=OVERRIDES[(stem,title)]
  if replacement is not None:text=text[:a]+replacement+text[b:]
 if stem=='gambling-harm' and 'https://www.gamblinghelponline.org.au/' not in text:
  text=text.replace('For help, use Gambling Help Online and official self-exclusion information.','For help, use <a href="https://www.gamblinghelponline.org.au/" target="_blank" rel="noopener noreferrer">Gambling Help Online</a> and <a href="https://www.betstop.gov.au/" target="_blank" rel="noopener noreferrer">BetStop</a>.')
 if stem=='joke':
  for a,b in sorted(Panels(text).spans,reverse=True):
   raw=text[a:b]
   if 'origin-deck' in raw:text=text[:a]+panel('Two blokes from Straddie. An open invitation.','A friendly disagreement over a beer became a question: how could people make public decisions more transparent, useful and open to correction? Bring a problem, test an idea, share what you learn. The workbench belongs to the conversation, not a candidate.')+text[b:]
   elif 'trying to get off Centrelink' in raw:text=text[:a]+panel('Small wins before big claims.','Start with a useful local task: explain a form, trace a public decision, test a tool or help neighbours compare options. Publish what worked and what did not. Communities can adapt the method without adopting a brand.',[('starter-field-kit.html','Practical starter field kit')])+text[b:]
 if stem=='marriage-divorce':text=text.replace('<h2>related solutions</h2>','<h2>Household agreements and a wider thought experiment</h2>')
 text=public_punctuation(neutral_copy(text))
 # Keep geographic maps separate from the rabbit-hole policy directory.
 text=re.sub(r'(<a href=")([^"]*)rabbit-hole.html(">)Map</a>',r'\1\2maps.html\3Maps</a>',text)
 return text

if __name__=='__main__':
 paths=[ROOT/'index.html',*sorted((ROOT/'pages').rglob('*.html')),*sorted((ROOT/'content/rooms').glob('*.html'))]
 changed=[]
 for p in paths:
  old=p.read_text(encoding='utf-8');new=public_html(p.name,old)
  if new!=old:p.write_text(new,encoding='utf-8');changed.append(str(p.relative_to(ROOT)))
 print('Updated',len(changed),'public/canonical HTML files')
