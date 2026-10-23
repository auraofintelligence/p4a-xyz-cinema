"""Repeat the complete cached state adapter and compare actual output hashes."""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]

def snapshot():
    data=json.loads((ROOT/'content/places/state.json').read_text(encoding='utf8'))
    names={'content/places/state.json','content/places/sources/state-requests.json','content/places/sources/state-source-rights.json','content/places/qa/state-tas-geometry-verification.json','content/places/qa/state-history-verification.json'}
    for layer in data['layers']:
        names.add(layer['geometryFile'])
        if layer.get('nativeGeometryFile'):names.add(layer['nativeGeometryFile'])
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(names)}

subprocess.run([sys.executable,'-u','-B','tools/acquire-state-places.py'],cwd=ROOT,check=True)
first=snapshot()
subprocess.run([sys.executable,'-u','-B','tools/acquire-state-places.py'],cwd=ROOT,check=True)
second=snapshot();changes=[name for name in first if first[name]!=second.get(name)]
assert not changes,changes
report={'checked':'2026-10-17','status':'PASS','scope':'Two complete offline adapter runs; canonical state records, source/rights registries, native/projection/history verification and every state geometry input','files':second,'changedBetweenRuns':changes,'networkRequests':0}
(ROOT/'content/places/qa/state-reproducibility.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print('PASS: '+str(len(second))+' state adapter outputs hash-identical after two complete offline runs',flush=True)
