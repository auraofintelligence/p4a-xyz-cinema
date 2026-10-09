from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];D=R/'content/rooms'
copy={
'ai-copyright':('The studio invoice meets the training bill.','An artist can sell a finished work without agreeing to every future use. The question is who can trace a training use, negotiate terms and afford a remedy.','If my work has value to the model, let’s talk terms before it disappears into the machine.'),
'child-safety':('Homework help, or a relationship designed to keep them chatting?','A parent can set a screen-time limit and still have no idea what a companion asks a child to reveal. The policy turn is safer defaults, independent testing and human help when a tool crosses a line.','Build the safety into the service. Don’t leave the child holding the instruction manual.'),
'mental-health':('The appointment ends. The problem doesn’t.','Someone finally gets through the door, then starts again with another service, another bill and another explanation. Continuity, housing, peers and affordable care belong in the same conversation.','Help should come with a next step, not another dead end.'),
'super-housing':('Which future pays for the deposit?','A renter weighs a home now against savings later. Put rent avoided, mortgage costs, compounding and price effects on the same page, alongside supply and secure-rental options.','Show me the home, the mortgage and the retirement balance. Same spreadsheet.'),
'multinational-tax':('A tiny tax number beside a giant revenue number.','That contrast deserves questions, but revenue is not taxable profit. Follow the entity, losses, related-party charges and rules before deciding whether the system or the conduct needs changing.','A big number deserves a proper receipt, not a guess dressed as a verdict.'),
'tobacco':('A legal habit becomes a household budget crisis.','Smokers can question punitive costs and government trust while taking health harms seriously. The room compares tax design, quitting support, enforcement and adult-autonomy reform.','If the policy is about health, show the help as clearly as the tax.'),
'fuel':('The commute gets first bite of the pay packet.','The same pump-price change lands differently on a city commuter with a train and a regional carer with no alternative. Test tax relief, pass-through, targeted help and better transport against real trips.','Before you tell me to drive less, show me another way to get there.'),
'ancient-aliens':('That object has a story. Which one survives the evidence?','Start with the actual object and its history, then compare human techniques, cultural interpretation and extraordinary hypotheses. The interesting part is what each explanation predicts and what could change our minds.','Open the archive. Bring the measurements. Keep the wonder.'),
}
for slug,(title,body,drop) in copy.items():
 f=D/f'twinkle-{slug}.html';s=f.read_text(encoding='utf-8')
 s=re.sub(r'<div class="feature-panel"><h2>Take it to the serious room</h2><p>.*?</p>',f'<div class="feature-panel"><h2>{title}</h2><p>{body}</p>',s)
 s=re.sub(r'<div class="feature-panel"><h2>Make it yours</h2>.*?</div>',f'<div class="feature-panel"><h2>The one-breath drop</h2><p>“{drop}”</p></div>',s)
 f.write_text(s,encoding='utf-8')
t=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
changes={'Job apocalypse':('Job apocalypse','workforce'),'Illicit tobacco':('Tobacco tax','tobacco'),'Tobacco':('Tobacco tax','tobacco'),'Fuel excise':('Fuel tax','fuel'),'Fuel':('Fuel tax','fuel'),'Copyright':('AI copyright','ai-copyright'),'Multinational tax avoidance':('Multinational tax avoidance','multinational-tax'),'Multinational tax':('Multinational tax avoidance','multinational-tax')}
for x in t['items'][23:]:
 if x['headline'] in changes:
  x['headline'],slug=changes[x['headline']];x['href']='pages/twinkle-'+slug+'.html'
seen=set();items=[]
for x in t['items']:
 if x['headline'] not in seen:items.append(x);seen.add(x['headline'])
t['items']=items
if 'PTSD' not in seen:t['items'].append({'headline':'PTSD','scope':'Explore P4A','href':'pages/twinkle-ptsd.html'})
(R/'content/home-ticker.json').write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
f=D/'twinkle-ptsd.html';s=f.read_text(encoding='utf-8');n='<a class="button button-secondary" href="twinkle-ai-copyright.html">Next Twinkle 23</a>';s=s.replace(n,'').replace('<a class="button button-primary" href="aura-clinical-path.html">Follow-through room</a>',n+'<a class="button button-primary" href="aura-clinical-path.html">Follow-through room</a>');f.write_text(s,encoding='utf-8')
