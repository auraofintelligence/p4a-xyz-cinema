"""One-time repair of source URLs identified by the October publication audit."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
replacements={
'https://www.ato.gov.au/law/view/document?LocID=%22SAV%2FTOBACCO%2FFTFNREF74%22':'https://www.ato.gov.au/illicittobacco#Domesticallygrowntobacco',
'https://www.aihw.gov.au/reports/australias-welfare/housing-affordability':'https://www.aihw.gov.au/reports/housing-assistance/housing-assistance-in-australia-2026/contents/housing-assistance',
'https://www.tga.gov.au/resources/resource/guidance/software-based-medical-devices':'https://www.tga.gov.au/products/medical-devices/software-and-artificial-intelligence-ai',
'33.9% of children commencing school developmentally on track in 2024 and 81.4% living in appropriately sized housing in 2021':'33.9% of Aboriginal and Torres Strait Islander children commencing school developmentally on track in 2024, and 81.4% of Aboriginal and Torres Strait Islander people living in appropriately sized housing in 2021',
}
for f in (R/'content/rooms').glob('*.html'):
 s=f.read_text(encoding='utf-8')
 for old,new in replacements.items():s=s.replace(old,new)
 f.write_text(s,encoding='utf-8')
f=R/'assets/site-nav.js';s=f.read_text(encoding='utf-8').replace('Twinkle 38: Fuel\'','Twinkle 38: Fuel tax\'').replace('Twinkle 39: Tobacco\'','Twinkle 39: Tobacco tax\'');f.write_text(s,encoding='utf-8')
f=R/'README.md';s=f.read_text(encoding='utf-8').replace('## Homepage issue ticker\n\n## October','## October').replace('### Ticker source','## Homepage issue ticker');f.write_text(s,encoding='utf-8')
t=json.loads((R/'content/home-ticker.json').read_text(encoding='utf-8'))
if not any(x['headline']=='UAP' for x in t['items']):t['items'].insert(23,{'headline':'UAP','scope':'Explore P4A','href':'pages/twinkle-uap.html','note':'No giggle tax: observations, archives and competing explanations.'})
(R/'content/home-ticker.json').write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
