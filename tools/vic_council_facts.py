"""Dated local-government profiles from reviewed source snapshots; no network."""
from html import escape as e
def num(v):return 'Unavailable' if v is None else f'{v:,.2f}'.rstrip('0').rstrip('.') if isinstance(v,float) else f'{v:,}'
def link(url,label):return f'<a href="{e(url)}">{e(label)}</a>'
def roster(rows):
 if not rows:return '<p>No current councillor roster is assigned to this record. This is not a claim that a seat is vacant.</p>'
 s='<ul class="vic-local-roster">'
 for x in rows:
  if x['status']=='vacant':s+=f'<li><strong>Vacant — {e(x["role"])}</strong><small>VEC note: {e(x["sourceNote"])} '+ ' · '.join(link(a['url'],a['label']) for a in x.get('links',[]))+'</small></li>'
  else:s+=f'<li><strong>{e(x["name"])}</strong><small>{e(x["role"])}</small></li>'
 return s+'</ul>'
def facts(r,data):
 parents={p['id']:p for p in data['lga']};ward=r['body']=='ward';parent=parents[r['parentId']] if ward else r
 out=['<div data-local-facts>']
 out.append(f'<span class="vic-kicker">Local government · {"electoral structure" if ward else "unincorporated area" if r["kind"]=="unincorporated" else "municipality"}</span><h2>{e(r["name"])}</h2>')
 if ward:
  p=r['sourceProperties'];out.append(f'<p>{link("?chamber=lga&electorate="+parent["id"],parent["name"])} · <strong>{e(r["kind"])}</strong> · Official ward code {e(str(r["code"]))}</p>')
  out.append(f'<p class="vic-data-note">Vicmap ward edition 2024. Effective from {e((p["effective_from"] or "Not supplied")[:10])}; gazetted {e((p["gazettal_date"] or "Not supplied")[:10])}. Source capacity: {e(p["members"] or "Not supplied")} member(s). Unsubdivided electoral areas are not multiple wards. A source geometry record does not establish that every seat is currently occupied.</p>')
 else:out.append(f'<p class="vic-quiet">Vicmap code {e(r["code"])} · ABS code {e(r["absCode"])} · Boundary snapshot 2 October 2026</p>')
 if parent.get('kind')=='unincorporated':
  out.append('<p class="vic-data-note">This is an unincorporated area, not one of Victoria’s 79 municipal councils. It is retained in the boundary layer so the map does not silently fill it with a neighbouring council. No municipal councillors or council finances are assigned.</p>')
  out.append(f'<p>{e(parent["populationNote"])}</p>')
 else:
  out.append('<section><h3>Current governance and representation</h3>')
  if parent['governance']=='administration':
   out.append(f'<p><strong>Administered council — no sitting councillors.</strong> {e(parent["administrationNote"])}</p><ul>')
   out.extend(f'<li>{e(x["name"])} — {e(x["role"])}</li>' for x in parent['administrators']);out.append('</ul>'+link(parent['administrationSource'],'Official administrator panel'))
  else:out.append(roster(r['roster']))
  out.append(f'<p>{e(parent["structure"])}</p><p class="vic-quiet">{link(parent["source"]["url"],"VEC current council profile")} · retrieved 2 October 2026. Vacancies are explicit. Councillor party affiliations are not inferred; current rosters are distinct from past election winners. Municipal monitors, where appointed, do not replace elected councillors.</p></section>')
 if not ward and r['kind']=='municipality':
  out.append(f'<section><h3>Wards and electoral structure</h3><p><button type="button" data-local-wards="{e(r["id"])}">Explore {len(r["wardIds"])} electoral area(s) on the map</button></p><ul class="vic-ward-links">')
  for w in data['ward']:
   if w['parentId']==r['id']:out.append(f'<li>{link("?chamber=ward&electorate="+w["id"]+"&council="+r["id"],w["name"])} <small>{e(w["kind"])}</small></li>')
  out.append('</ul><p class="vic-quiet">Ward geometry is loaded only when requested. The 2024 source may contain unsubdivided or unspecified electoral areas; these are labelled as supplied, not invented wards.</p></section>')
 if ward:
  out.append(f'<p class="vic-data-note">Population history and financial-source coverage are available in the {link("?chamber=lga&electorate="+parent["id"],"parent council profile")}. Council-wide values are not allocated to wards.</p>')
 elif r['statistics']:
  st=r['statistics'];out.append('<section><h3>Population — estimates with their dates</h3><dl class="vic-census-metrics">')
  for label,k,unit in [('Residents at 30 June 2025','erp_2025','people'),('Change, 2024–25','erp_change_number_2024_25','people'),('Growth, 2024–25','erp_change_per_cent_2024_25','%'),('ABS LGA 2025 area','area_km2','km²'),('Density at 30 June 2025','pop_density_2025_people_per_km2','people/km²')]:out.append(f'<div><dt>{e(label)}</dt><dd>{num(st[k])}<small>{e(unit)}</small></dd></div>')
  out.append(f'</dl><p class="vic-data-note">{e(data["populationNote"])} {e(data["populationGeography"])}. Statistical area and population are not recalculated from the legal map polygons.</p>')
  if r.get('codeCrosswalkNote'):out.append(f'<p class="vic-quiet">{e(r["codeCrosswalkNote"])}</p>')
  vals=[st[f'erp_{year}'] for year in range(2001,2026)];maximum=max(v for v in vals if v is not None)
  out.append('<div class="vic-pop-chart" role="img" aria-label="Estimated resident population history from 2001 to 2025. Exact annual values follow in the table.">')
  for year,v in zip(range(2001,2026),vals):out.append(f'<span style="--bar:{0 if v is None else v/maximum*100:.4f}%" title="{year}: {num(v)} people"></span>')
  out.append('</div><div class="vic-history-axis"><span>2001</span><span>30 June each year</span><span>2025</span></div><details><summary>All 25 annual population estimates (2001–2025)</summary><div class="vic-table-scroll"><table><caption>ABS estimated resident population; LGA 2025 geography</caption><thead><tr><th scope="col">At 30 June</th><th scope="col">Residents (people)</th></tr></thead><tbody>')
  for year,v in zip(range(2001,2026),vals):out.append(f'<tr><th scope="row">{year}</th><td>{num(v)}</td></tr>')
  out.append('</tbody></table></div></details><details><summary>Components of population change, 2024–25</summary><dl class="vic-component-list">')
  for label,k in [('Births','births'),('Deaths','deaths'),('Natural increase','natural_increase'),('Net internal migration','net_internal_migration'),('Net overseas migration','net_overseas_migration')]:out.append(f'<div><dt>{label}</dt><dd>{num(st.get(k+"_2024_25"))} people</dd></div>')
  out.append('</dl></details><p>'+link(data['populationPublication'],'ABS Regional population, 2024–25')+' · '+link(data['populationSource'],'Exact source fields and metadata')+' · retrieved 2 October 2026. Source: Australian Bureau of Statistics.</p></section>')
 if not ward:
  out.append('<section><h3>Where levels of government overlap</h3><p>These are positive-area polygon intersections with the 2022 state electoral boundaries. A municipality can cross several electorates. Tiny boundary slivers can appear because municipal boundaries are property-aligned and have a different vintage. Links are not population shares or allocations of money.</p>')
  for chamber,label in [('assembly','Assembly districts'),('council','Legislative Council regions')]:out.append(f'<p><strong>{label}:</strong> '+ ' · '.join(link('?chamber='+chamber+'&electorate='+x['id'],x['name'].title()) for x in r['overlaps'][chamber])+'</p>')
  out.append('<p class="vic-quiet">Source topology defects are repaired only in a separate analysis copy for intersections and labels; map/download coordinates are unchanged. '+link('../../../content/councils/vic.json','Method, source hashes and defect log')+'</p><p>'+link('https://www.aec.gov.au/Electorates/gis/gis_datadownload.htm','Federal electorates: official AEC boundaries')+' — federal geometry and crosswalks are not loaded or inferred here.</p></section>')
  out.append('<section><h3>Budgets, debt, rates and services</h3><p><strong>Numerical series unavailable in this release.</strong> No values are assumed to be zero or allocated from state figures. The LGPRF bulk download returned HTTP 403. LGV terms allow conditional non-commercial reuse; each acquired dataset still needs its own terms and coverage checked. No access restriction was bypassed. Council budgets, actual expenditure, borrowings and total liabilities are different measures and must remain separate.</p><p>'+link(data['finance']['performanceSource'],'Official local-government performance dataset')+' · '+link(data['finance']['financeSource'],'Victoria Grants Commission financial data and source reports')+'</p></section>')
  if r['historyLinks']:
   out.append('<details><summary>Election history and boundary reviews — official sources</summary><p>Historical links are retained as evidence; they do not establish the current roster or current ward boundaries.</p><ul>');out.extend('<li>'+link(x['url'],x['label'])+'</li>' for x in r['historyLinks']);out.append('</ul></details>')
 out.append('<p>'+link('https://discover.data.vic.gov.au/dataset/vicmap-admin-ward-polygon-2024' if ward else 'https://discover.data.vic.gov.au/dataset/vicmap-admin-local-government-area-lga-polygon-aligned-to-property','Official Vicmap boundary dataset')+' · © State of Victoria, CC BY 4.0 · retrieved 2 October 2026.</p></div>')
 return ''.join(out)
