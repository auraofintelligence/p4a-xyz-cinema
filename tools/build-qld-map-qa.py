"""Local browser QA fixtures for actual picking and responsive layout, no network."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
from qld_council_widget import widget,assets
page='qa/redland-20261017/council-map.html'
fixtures=[('Cleveland',153.267,-27.526,'6250'),('Dunwich',153.402,-27.497,'6250'),('Point Lookout',153.533,-27.433,'6250'),('Russell Island',153.379,-27.667,'6250'),('Macleay Island',153.36,-27.60,'6250'),('Coochiemudlo',153.332,-27.57,'6250'),('Brisbane CBD',153.025,-27.47,'1000'),('Moreton Island',153.4,-27.2,'1000'),('Logan Central',153.109,-27.643,'4590')]
import json
tests='''<script>document.addEventListener('DOMContentLoaded',()=>{
 const tests=FIXTURES;
 const results=tests.map(([name,lon,lat,expected])=>({name,expected,actual:window.P4A_QLD_MAP.pickLonLat(lon,lat)}));
 const out=document.querySelector('[data-testid=qld-map-tests]');
 out.textContent=JSON.stringify({result:results.every(r=>r.actual===r.expected)?'PASS':'FAIL',devicePixelRatio:window.devicePixelRatio,picking:results},null,2);
 document.querySelector('[data-read-state]').addEventListener('click',()=>{document.querySelector('[data-map-state]').textContent=JSON.stringify(window.P4A_QLD_MAP.getState());});
});</script>'''.replace('FIXTURES',json.dumps(fixtures))
html='''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Queensland map QA</title><link rel="stylesheet" href="../../styles.css"><style>body{padding:22px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1{font-size:1.7rem}</style><script>if(new URLSearchParams(location.search).get('dpr')==='2')Object.defineProperty(window,'devicePixelRatio',{value:2});</script>'''+assets(page)+'''</head><body><h1>Queensland council geometry QA</h1><p>Local test fixture. The points below were checked independently against the retained source. The optional DPR2 query is synthetic display testing.</p><pre data-testid="qld-map-tests">Checking geometry…</pre><button data-read-state>Read map view</button><p data-map-state></p>'''+widget(page)+tests+'</body></html>'
(ROOT/page).write_text(html,encoding='utf-8')
division_fixtures=[('Wellington Point',153.241,-27.487,'1'),('Cleveland',153.267,-27.526,'2'),('Dunwich',153.402,-27.497,'2'),('Point Lookout',153.533,-27.433,'2'),('Thornlands',153.269,-27.56,'3'),('Coochiemudlo',153.332,-27.57,'4'),('Victoria Point',153.293,-27.584,'4'),('Russell Island',153.379,-27.667,'5'),('Macleay Island',153.36,-27.60,'5'),('Redland Bay',153.303,-27.613,'5'),('Mount Cotton',153.221,-27.633,'6'),('Capalaba',153.193,-27.523,'8')]
division_page='qa/redland-20261017/division-map.html'
division_tests=tests.replace(json.dumps(fixtures),json.dumps(division_fixtures)).replace('P4A_QLD_MAP','P4A_REDLAND_MAP')
division_html=html[:html.index('<body>')].replace(assets(page),assets(division_page,'division'))+'<body><h1>Redlands division geometry QA</h1><pre data-testid="qld-map-tests">Checking geometry…</pre><button data-read-state>Read map view</button><p data-map-state></p>'+widget(division_page,'division')+division_tests+'</body></html>'
(ROOT/division_page).write_text(division_html,encoding='utf-8')
parent='''<!doctype html><html lang="en-AU"><meta charset="utf-8"><title>Queensland tablet and phone checks</title><style>body{font:16px system-ui;margin:18px;background:#ddd}iframe{display:block;height:750px;border:2px solid #555;margin-bottom:25px}pre{white-space:pre-wrap}</style><h1>Map and tablet checks, 17 October 2026</h1><p>Local QA fixture only.</p><h2>680px Redlands navigation</h2><iframe style="width:680px" title="680px Redland navigation" src="../../states/qld/councils/redland/index.html"></iframe><h2>390px map at synthetic DPR2</h2><iframe style="width:390px" title="390px QLD map DPR2" src="council-map.html?dpr=2"></iframe><pre data-testid="layout-metrics"></pre><script>const reports=[];document.querySelectorAll('iframe').forEach(f=>f.addEventListener('load',()=>{const d=f.contentDocument;const links=[...d.querySelectorAll('.local-nav a,.atlas-toolbar button')];const boxes=links.map(el=>el.getBoundingClientRect());let overlaps=0;for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(a.left<b.right-1&&a.right>b.left+1&&a.top<b.bottom-1&&a.bottom>b.top+1)overlaps++;}reports.push({page:f.title,viewport:d.documentElement.clientWidth,scrollWidth:d.documentElement.scrollWidth,buttonOverlaps:overlaps,canvas:[...d.querySelectorAll('canvas.atlas-canvas')].map(c=>({cssWidth:c.getBoundingClientRect().width,bitmapWidth:c.width})),picking:d.querySelector('[data-testid=qld-map-tests]')?.textContent});document.querySelector('[data-testid=layout-metrics]').textContent=JSON.stringify(reports,null,2);}));</script></html>'''
parent=parent.replace('<pre data-testid="layout-metrics">','<h2>390px division map at synthetic DPR2</h2><iframe style="width:390px" title="390px division map DPR2" src="division-map.html?dpr=2"></iframe><pre data-testid="layout-metrics">')
(ROOT/'qa/redland-20261017/tablet-map.html').write_text(parent,encoding='utf-8')
print('Generated local council-map and responsive QA fixtures.')
