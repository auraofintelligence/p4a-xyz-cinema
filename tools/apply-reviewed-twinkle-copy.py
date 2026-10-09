"""One-time application of the author's reviewed 47-entry copy, 3 October 2026.

Do not rerun after subsequent editorial changes. Published HTML is maintained in
content/rooms; the JSON records the approved copy and preserved earlier seeds.
"""
import json,re,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
COPY="""tolls|At this rate, I own a lane.|I've paid so much in tolls the tag should open the bloody boardroom.
food|Two bags. One payslip.|The self-checkout asked if I'd brought my own bags; at these prices I thought I'd bought the shop.
insurance|Covered. Except for that.|My insurance covers everything except the thing that happened, which must be why they call it comprehensive.
workforce|Train your own replacement.|They want me to teach the AI my job before they make me redundant; do I have to organise my own farewell too?
housing|Rent went up. He painted one wall.|My landlord's calling it a renovation; I watched him do it with a sample pot.
power|Opened the power bill standing up. Mistake.|I'm saving power by sitting in the dark, which makes it harder to read the bill telling me I'm saving fuck-all.
health|Doctor says less stress. How much is that?|The GP said I need less stress, so I asked if they bulk-bill.
family-violence|Stop asking why she didn't leave.|A woman gets told to leave a violent man, then asked where she plans to live.
childcare|Daycare's a second mortgage.|After childcare fees, I'm mainly going to work for the air-conditioning.
beer-tax|Beer tax froze. Did your schooner?|They froze the tax on draught beer and wanted a round of applause; I was hoping for a round I could afford.
datacentres|Big shed. Very clever light switch.|They've built a giant data centre up the road so AI can tell me to switch the lights off to save power.
breaches|My licence has frequent flyer points.|My licence has been leaked so often I'm waiting for the scammers to remind me when it expires.
resources|Dig it up. Buy the megaphone.|We dig up the country, a few blokes get rich, then they buy a newspaper to explain why we should be grateful.
triple-zero|Four bars of 5G. Zero for Triple Zero.|My phone can stream a bloke falling off a roof in 4K, but I'd like it to call an ambulance if it's me.
aukus|Subs by the 2040s. GP by Thursday week.|We've ordered submarines decades ahead, but booking a GP for next Thursday is getting ambitious.
revolving-door|Friday: parliament. Monday: gas company.|The revolving door between politics and big business is moving so fast we could put a turbine on it.
donations|Who paid for that ad?|They tell me who authorised the election ad at auctioneer speed; whoever paid for it must be shy.
olympics|Gold in changing the plans.|Brisbane's warming up for the Olympics by doing laps of the stadium decision.
treaty|Funny where the paperwork starts.|We managed to claim a whole continent, but a national treaty with First Peoples is where the paperwork gets tricky.
uap|Aliens? We'll take that on notice.|If a UFO landed in Canberra, they'd be halfway through denying it before anyone asked.
deep-time|Third hundred-year flood this decade.|I've had three hundred-year floods and one pay rise; something's wrong with the calendar.
ptsd|The tour didn't break him. The form did.|He came home with PTSD and got sent back through the worst of it, one claim form at a time.
ai-copyright|Mine was free. Yours is licensed.|My work is 'training data' when AI companies take it and 'intellectual property' when they sell it back.
child-safety|A chatbot shouldn't need a babysitter.|The chatbot calls my kid its best mate; I'm the one getting asked to upgrade the friendship.
online-safety|Copyright gets a bodyguard.|The platform can recognise three seconds of a song, but the bloke threatening a kid is somehow a complex case.
gender-pay-gap|Full-price equality.|Women earn less than men on average, but somehow the landlord’s never heard of a gender rent gap.
closing-the-gap|Another report. How is the gap?|We've got enough reports on Indigenous disadvantage to build a bridge across the bloody gap.
youth-crime|Tough on crime. Handy for ads.|Some kid's nicked my car; now a politician's trying to nick the story for his campaign.
family-choices|We'd love a baby.|They keep asking why we're not having kids, like we're hoarding all these spare bedrooms and stable futures.
marriage-divorce|Till fees do us part.|We've agreed the marriage is over; the lawyers reckon it's still got a few good years in it.
super-housing|Same broke. Different decade.|The plan is to let me raid my super for a house, so now I can be broke at two different ages.
wealth-inequality|The house got the pay rise.|My landlord's house made more than I did, and it spent the year sitting on its arse.
multinational-tax|Big revenue. Pay tax.|A multinational can lose its profits somewhere offshore, but I'd better have a receipt for those work socks.
ndis-scams|The wrong people got supported.|The NDIS scammers don't need support; they seem to be doing very well on mine.
ai-scams|Sounds just like Mum.|They said AI would give us more time with our families; now it rings pretending to be one of them.
aged-care-scams|Lovely visit. Never happened.|Mum's aged-care bill has a better social life than she does.
gambling-harm|Any chance of some footy?|I'm trying to watch the footy, but first six blokes need to tell me how to lose the grocery money responsibly.
fuel|Tax on the tax. Nice touch.|I'm paying tax on the fuel tax while dodging potholes; at least one part of the road system is beautifully maintained.
tobacco|For my own good. At my own expense.|The government is so worried about my smoking it's made itself the most expensive part of the packet.
migration-equations|Three plans. Never met.|We've got a migration target, a housing target and a transport plan; be nice if someone introduced them.
international-wars|Funny who never goes.|The people most certain we need another war never seem to need a seat on the plane.
security-fallacies|Billions later, 'trust us'.|I get a clearer explanation of what could go wrong when I hire a trailer than when we buy another national-security plan.
ancient-aliens|Depends which bloke in the sky.|Tell people a bloke came down from the sky and it's religion; ask what he arrived in and suddenly you're the idiot.
mental-health|Very aware. Still waiting.|By the time I get a mental-health appointment, I'll have been through three awareness weeks.
psychedelic-mental-health|God had better chip in.|At the price of legal psychedelic therapy, I'd want to meet God and get him to chip in.
restricted-plants|Medicine, until I grow it.|Some plants are medicine when a company grows them and evidence when I do.
super-investments|My super. What the hell's it buying?|I'm saving for a quiet retirement; I'd like to know if my super's spending the meantime in the arms trade."""

def main():
 records=[];seeds=[]
 archive=R/'content/twinkle-earlier-seeds.json'
 assert not archive.exists(),'One-time migration already applied'
 hubpath=R/'content/rooms/twinkle.html';hub=hubpath.read_text(encoding='utf-8')
 for number,line in enumerate(COPY.splitlines(),1):
  slug,headline,gripe=line.split('|');filename='twinkle-'+slug+'.html'
  source=R/'content/rooms'/filename
  s=(source if source.exists() else R/'pages'/filename).read_text(encoding='utf-8')
  destination=re.search(r'href="([^"]+)">Follow-through room</a>',s).group(1)
  if number<=22:
   start=re.search(r'(<section class="section" id="clip">\s*<div class="page-copy reveal">)',s).end()
   end=s.index('<div class="video-grid">',start)
   seeds.append({'number':number,'slug':slug,'destination':destination,'hero':re.search(r'<p class="hero-copy">(.*?)</p>',s,re.S).group(1),'html':s[start:end].strip()})
   s=s[:start]+'\n<div class="feature-panel"><h2>The one-breath drop</h2><p>&ldquo;'+html.escape(gripe)+'&rdquo;</p></div>\n'+s[end:]
  else:
   s,n=re.subn(r'(<h2>The one-breath drop</h2><p>).*?(</p>)',lambda m:m[1]+'&ldquo;'+html.escape(gripe)+'&rdquo;'+m[2],s,count=1,flags=re.S);assert n==1,slug
  for pattern,replacement in [(r'<h1>.*?</h1>','<h1>'+html.escape(headline)+'</h1>'),(r'<p class="hero-copy">.*?</p>','<p class="hero-copy">'+html.escape(gripe)+'</p>'),(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+html.escape(gripe)+'">'),(r'<title>.*?</title>','<title>'+html.escape(headline)+' | P4A</title>')]:
   s,n=re.subn(pattern,lambda m:replacement,s,count=1,flags=re.S);assert n==1,slug
  source.write_text(s,encoding='utf-8')
  def card(m):
   b=re.sub(r'<h3>.*?</h3>','<h3>'+html.escape(headline)+'</h3>',m[2],count=1,flags=re.S)
   b=re.sub(r'<p>.*?</p>','<p>'+html.escape(gripe)+'</p>',b,count=1,flags=re.S)
   return m[1]+b+m[3]
  hub,n=re.subn(r'(<a class="twinkle-card" href="'+re.escape(filename)+r'">)(.*?)(</a>)',card,hub,flags=re.S);assert n==1,slug
  records.append({'number':number,'slug':slug,'headline':headline,'gripe':gripe,'destination':destination})
 hub=hub.replace('Forty-six Twinkles','Forty-seven Twinkles').replace('forty-two open seeds','forty-three open seeds').replace('Forty-two more connections','Forty-three more connections')
 hub=hub.replace('The fix gets said in one breath before the flush. If it needs a second breath, that breath lives in the follow-through room, not the clip.','The gripe gets said in one breath before the flush. Follow the link for the policy options, evidence and ways to take part.')
 hubpath.write_text(hub,encoding='utf-8')
 archive.write_text(json.dumps(seeds,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (R/'content/twinkle-reviewed-copy.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Applied',len(records),'approved entries; preserved',len(seeds),'earlier seeds')

if __name__=='__main__':main()
