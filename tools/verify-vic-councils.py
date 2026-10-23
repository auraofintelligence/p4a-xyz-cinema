import pathlib,json,hashlib,collections
R=pathlib.Path(__file__).resolve().parents[1];d=json.loads((R/'content/councils/vic.json').read_text(encoding='utf-8'))
assert collections.Counter(r['kind'] for r in d['lga'])=={'municipality':79,'unincorporated':8}
assert len(d['ward'])==467 and sum(len(r['members']) for r in d['lga'])==646
assert sum(x['status']=='vacant' for r in d['lga'] for x in r['roster'])==1
verified_replacements={'vic-ward-3030220200423':'Nicola Rooks','vic-ward-3250720240215':'David Thorpe','vic-ward-3520320240215':'Christine Leahy','vic-ward-3370620240215':'Rob Moffatt','vic-ward-3350820200709':'Nikki Kaur','vic-ward-3750620240215':'Kim McAliney'}
for area,name in verified_replacements.items():
 row=next(r for r in d['ward'] if r['id']==area)
 assert row['roster'][0]['name']==name and row['roster'][0]['status']=='current' and row['roster'][0]['checked']=='2026-10-23'
 assert row['roster'][0]['sourceUrl'].startswith('https://')
for layer,source in [('lga','lga_polygon'),('ward','ward_2024')]:
 raw=(R/f'assets/maps/vic-{layer}.geojson').read_bytes();assert hashlib.sha256(raw).hexdigest()==d['sourceSnapshots'][source]['sha256']
for r in d['lga']:
 if r['kind']=='unincorporated':assert r['statistics'] is None and all(v is None for v in r['sortMetrics'].values());continue
 st=r['statistics'];assert all(isinstance(st[f'erp_{year}'],int) for year in range(2001,2026))
 assert st['erp_2025']-st['erp_2024']==st['erp_change_number_2024_25']
 assert st['natural_increase_2024_25']+st['net_internal_migration_2024_25']+st['net_overseas_migration_2024_25']==st['erp_change_number_2024_25']
 assert all(x['id'].startswith('vic-assembly-') for x in r['overlaps']['assembly'])
assert all(v is None for v in d['finance']['values'].values())
page=(R/'states/vic/map/index.html').read_text(encoding='utf-8');assert page.count('class="vic-local-record"')==554
print('PASS: 79 municipalities, 8 unincorporated areas, 467 ward records, 646 councillors/1 vacancy; six sourced replacements; 1975 annual population values, source hashes, financial nulls and no-JS profiles.')
