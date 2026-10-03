"""Verify complete numerical snapshots; optionally compare all Census cells
against the downloaded official workbook: --sources <local source directory>."""
import pathlib,json,math,argparse
R=pathlib.Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--sources',type=pathlib.Path);args=parser.parse_args()
 elections=json.loads((R/'content/electorates/vic-election-results.json').read_text(encoding='utf-8'))
 census=json.loads((R/'content/electorates/vic-census-2021.json').read_text(encoding='utf-8'))
 assert len(elections)==96 and len(census['districts'])==88 and len(census['fields'])==7
 kinds={};differences=[]
 for ident,event in elections.items():
  assert len(event['elected'])==(1 if 'assembly' in ident else 5)
  totals=event['totals'];formal=totals['Formal votes:']['count'];assert formal+totals['Informal votes:']['count']==totals['Total votes:']['count']
  primary=[t for t in event['tables'] if t['kind']=='primary'];assert len(primary)==1
  assert sum(row['votes'] for row in primary[0]['rows'])==formal,ident
  assert all(any(row['candidate']==winner['name'] for row in primary[0]['rows']) for winner in event['elected']),ident
  for row in primary[0]['rows']:assert abs(row['votes']/formal*100-row['percentage'])<=.011,(ident,row)
  for table in event['tables']:
   kinds[table['kind']]=kinds.get(table['kind'],0)+1
   if table['kind']=='twoCandidatePreferred' and sum(row['votes'] for row in table['rows'])!=formal:differences.append(ident)
  assert event['source'].startswith('https://www.vec.vic.gov.au/') and len(event['sourceSha256'])==64
 assert elections['vic-assembly-57']['date']=='2023-01-28'
 assert elections['vic-assembly-55']['date']=='2023-11-18'
 assert elections['vic-assembly-60']['date']=='2026-05-02'
 assert elections['vic-assembly-69']['date']==elections['vic-assembly-86']['date']=='2025-02-08'
 assert elections['vic-assembly-84']['date']=='2023-08-26'
 assert len(next(t for t in elections['vic-assembly-57']['tables'] if t['kind']=='distribution')['rows'])==4
 assert census['observationYear']==2021 and census['boundaryEdition']==2022
 for ident,record in census['districts'].items():
  assert set(record['values'])=={f['id'] for f in census['fields']}
  for item in record['values'].values():assert isinstance(item['value'],(int,float)) and math.isfinite(item['value']) and item['value']>=0 and item['cell']
 if args.sources:
  import hashlib
  from openpyxl import load_workbook
  path=args.sources/'electorate-data.xlsx';assert hashlib.sha256(path.read_bytes()).hexdigest()==census['sourceSha256']
  workbook=load_workbook(path,read_only=True,data_only=True)
  for record in census['districts'].values():
   for field in census['fields']:
    item=record['values'][field['id']];assert workbook[field['sheet']][item['cell']].value==item['value']
  print('All 616 numerical Census values match their official workbook cells exactly.')
  for ident,event in elections.items():
   path=args.sources/('mulgrave-2023.html' if ident=='vic-assembly-55' else ident+'.html');assert hashlib.sha256(path.read_bytes()).hexdigest()==event['sourceSha256']
  print('All 96 VEC source-page checksums match the downloaded snapshots.')
 print('PASS: 96 results, 616 Census values; all primary votes reconcile with formal votes; all formal + informal totals reconcile.')
 print('Distinct table kinds:',kinds)
 print('Indicative 2CP totals differing from rechecked formal totals (retained separately):',differences)
if __name__=='__main__':main()
