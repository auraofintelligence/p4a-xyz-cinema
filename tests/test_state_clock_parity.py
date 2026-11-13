"""Delivered state cards must use the exact canonical event timing, never invented hours."""
import json,re,unittest,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class StateClockParity(unittest.TestCase):
 def test_canonical_rendered_parity(self):
  states=[]
  for p in (R/'content/states').glob('*.md'):
   m=re.search(r'```json state-data\s*(.*?)```',p.read_text(),re.S)
   if m:states.append(json.loads(m[1]))
  states.sort(key=lambda s:s['order'])
  asset=json.loads((R/'assets/state-data.js').read_text().split('=',1)[1].strip().rstrip(';'))
  for row in asset:
   self.assertEqual(row.pop("sourceMarkdown"),f'content/states/{row["slug"]}.md')
  self.assertEqual(asset,states)
  zones=dict(qld='Brisbane',nsw='Sydney',vic='Melbourne',tas='Hobart',sa='Adelaide',wa='Perth',nt='Darwin',act='Sydney')
  checked=0
  for state in states:
   for path in ['pages/states.html',f'states/{state["slug"]}/index.html']:
    cards=re.findall(r'<article class="election-timer [^"]*"[^>]*data-election-card[^>]*>.*?</article>',(R/path).read_text(),re.S)
    for event in state['elections']:
     matches=[c for c in cards if 'data-state="'+state['slug']+'"' in c and html.unescape(dict(re.findall(r'([\w-]+)="([^"]*)"',c.split('>',1)[0]))['data-election-label'])==event['label']]
     self.assertEqual(len(matches),1,(path,event['label']))
     c=matches[0];attrs=dict(re.findall(r'([\w-]+)="([^"]*)"',c.split('>',1)[0]))
     date='' if event.get('timingStatus')=='awaiting-confirmation' else event.get('date') or ''
     self.assertEqual(attrs['data-election-date'],date)
     self.assertEqual(attrs['data-election-timezone'],event.get('timezone','Australia/'+zones[state['slug']]))
     self.assertEqual(attrs['data-timing-status'],event.get('timingStatus',''))
     if not date:self.assertIn('Awaiting confirmation to begin',c);self.assertNotIn('data-countdown=',c)
     if event.get('datePrecision')=='day':self.assertEqual(attrs['data-election-precision'],'day');self.assertNotIn('T08:00',date)
     if event.get('indicativeDate'):self.assertIn('Indicative statutory date: '+event['indicativeDate'],c)
     checked+=1
  self.assertEqual(checked,52)
 def test_calendar_embedded_data(self):
  text=(R/'assets/state-election-calendar.js').read_text()
  data=json.loads(re.search(r'const DATA=(.*?);\n',text)[1])
  self.assertEqual(data,json.loads((R/'content/elections/state-election-calendar.json').read_text()))
if __name__=='__main__':unittest.main()
