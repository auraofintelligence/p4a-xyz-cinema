"""Source-backed HTML fragments shared by interactive and no-JS profiles."""
import html,json,pathlib,datetime
e=lambda v:html.escape(str(v),quote=True)
def num(v):return f'{v:,.2f}'.rstrip('0').rstrip('.') if isinstance(v,float) else f'{v:,}'
def facts(record,data,elections,census):
 result=elections[record['id']];date=datetime.date.fromisoformat(result['date']).strftime('%d %B %Y').lstrip('0')
 totals=result['totals'];winner='; '.join(f"{x['name']} ({x['party'] or 'no party listed'})" for x in result['elected'])
 out=[f'<div class="vic-profile-facts" data-facts><section><h3>Historical election · {e(date)}</h3><p>{e(result["event"])} · <strong>Elected: {e(winner)}</strong></p><p class="vic-quiet">Election-time affiliations and outcomes; separate from today’s membership and future candidates.</p><dl class="vic-fact-metrics">']
 for label in ['Total enrolment as at close of rolls:','Formal votes:','Informal votes:','Total votes:']:
  metric=totals[label];suffix=''
  if metric['percentage'] is not None:suffix=f'<small>{metric["percentage"]:.2f}% {"of enrolment" if label=="Total votes:" else "of total votes"}</small>'
  out.append(f'<div><dt>{e(label.rstrip(":"))}</dt><dd>{num(metric["count"])}{suffix}</dd></div>')
 out.append('</dl>')
 if result.get('note'):out.append(f'<p class="vic-data-note">{e(result["note"])}</p>')
 for table in result['tables']:
  is_distribution=table['kind']=='distribution'
  title=table['label'];caption=title+' · '+date
  out.append(f'<details class="vic-result-table" {"open" if is_distribution else ""}><summary>{e(title)} · {len(table["rows"])} candidates</summary>')
  if table['kind']=='primary':out.append('<p class="vic-quiet">Primary votes: first preferences before preferences are distributed.</p>')
  if table['kind']=='twoPartyPreferred':out.append('<p class="vic-quiet">Two-party preferred (2PP) is a separate comparison of the major party blocs; it is not interchangeable with a two-candidate result.</p>')
  if table.get('note'):out.append(f'<p class="vic-data-note">{e(table["note"])}</p>')
  out.append(f'<div class="vic-table-scroll" tabindex="0" role="region" aria-label="{e(caption)}"><table><caption>{e(caption)}</caption><thead><tr><th scope="col">Candidate</th><th scope="col">Party at election</th><th scope="col">Votes</th><th scope="col">Source %</th></tr></thead><tbody>')
  for row in table['rows']:out.append(f'<tr><th scope="row">{e(row["candidate"])}</th><td>{e(row["party"] or "Not listed")}</td><td>{num(row["votes"])}</td><td>{row["percentage"]:.2f}%</td></tr>')
  out.append('</tbody></table></div></details>')
 out.append(f'<p class="vic-quiet"><a href="{e(result["source"])}">Official VEC result and definitions</a> · retrieved {e(result["retrieved"])}. Percentages are those reported by VEC, not recomputed.</p></section><section><h3>2021 Census · 2022 electoral boundaries</h3>')
 if record['id'] in census['districts']:
  values=census['districts'][record['id']]['values'];out.append('<dl class="vic-census-metrics">')
  for field in census['fields']:
   observation=values[field['id']];formatted=('$'+num(observation['value'])) if field['unit']=='AUD/week' else (num(observation['value']*100)+'%') if field['unit']=='share' else num(observation['value'])
   out.append(f'<div><dt>{e(field["label"])}</dt><dd>{formatted}<small>{e(("source percentage" if field["unit"]=="share" else field["unit"]))}</small></dd></div>')
  out.append('</dl><details><summary>Exact source fields and cells</summary><ul class="vic-quiet">')
  for field in census['fields']:out.append(f'<li>{e(field["label"])}: {e(field["sheet"])}!{e(values[field["id"]]["cell"])}; source header “{e(field["sourceHeader"])}”, group “{e(field["sourceGroup"])}”. {e(field.get("note", ""))}</li>')
  out.append('</ul></details>')
 else:
  out.append('<p class="vic-data-note">This workbook does not publish Council-region Census statistics. The table below shows its 11 districts separately. District medians have not been averaged or presented as a regional estimate.</p><div class="vic-table-scroll" tabindex="0" role="region" aria-label="Constituent district Census values"><table><caption>District observations · 2021 Census on 2022 boundaries</caption><thead><tr><th scope="col">District</th><th scope="col">Total persons</th><th scope="col">Median age (years)</th><th scope="col">Median rent ($/week)</th></tr></thead><tbody>')
  for district in record['districts']:
   values=census['districts'][district['id']]['values'];out.append(f'<tr><th scope="row"><a data-census-district="{e(district["id"])}" href="?chamber=assembly&amp;electorate={e(district["id"])}">{e(district["name"])}</a></th><td>{num(values["population"]["value"])}</td><td>{num(values["medianAge"]["value"])}</td><td>${num(values["medianWeeklyRent"]["value"])}</td></tr>')
  out.append('</tbody></table></div>')
 out.append(f'<p class="vic-quiet">{e(census["note"])}</p><p class="vic-quiet"><a href="{e(census["source"])}">Official Parliament workbook</a> · <a href="{e(census["explainer"])}">Definitions and confidentiality notes</a> · retrieved {e(census["retrieved"])}.</p></section></div>')
 return ''.join(out)
