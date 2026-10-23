"""Create a local browser failure fixture from real retained map inputs.

This requests only a nonexistent localhost detail endpoint to exercise fallback.
It does not change canonical facts, public place pages or third-party services.
"""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
b=runpy.run_path(str(ROOT/'tools/build-national-places.py'))
places,layers,sources,inputs=b['load']()
selected=next(p for p in places if p['id']=='qld-council-1000')
peers=[p for p in places if p.get('layerId')==selected['layerId']]
for layer in layers:
    name=layer['geometryFile']
    layer['compressedFile']=name if name.endswith('.gz') else name+'.gz'
basemap=json.loads((ROOT/'content/places/sources/national-basemap.json').read_text())
basemap['onlineDetailService']='http://127.0.0.1:8768/content/places/qa/missing-detail-service'
page='content/places/qa/network-fallback.html'
body='<h1>Local fallback review</h1><p>QA fixture only. Real retained Queensland boundaries and geographic raster; the online-detail endpoint is intentionally a nonexistent localhost URL. This tests a failed detail request without changing official services or source facts.</p>'
body+=b['map_widget'](page,peers,layers,basemap,selected=selected)
body+='<section id="directory"><h2>Text navigation remains available</h2>'+b['listing'](page,peers)+'</section>'
(ROOT/page).write_text(b['shell'](page,'Local fallback review',body),encoding='utf-8')
print('Built labelled local failure fixture:',page)
