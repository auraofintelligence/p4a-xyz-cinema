"""Retain licensed official SA ward geometry, with verified HTTPS and exact coordinates.

Produces a separate supplement for the council adapter to join to real parents.
No names, boundaries, electoral structures or representative assignments are guessed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw/sa-ward-geometry'
SERVICE = 'https://lsa4.geohub.sa.gov.au/server/rest/services/LSA/LocationSAViewerV34/MapServer/12'
CATALOGUE = 'https://location.sa.gov.au/lms/Reports/ReportMetadata.aspx?p_no=836&pa=dpti'
CHECKED = '2026-10-17'


def get(name, url, offline):
    path = RAW / name
    if path.is_file():
        return path.read_bytes()
    if offline:
        raise ValueError('Missing retained source: ' + str(path))
    request = urllib.request.Request(url, headers={'User-Agent': 'P4A public civic atlas research/1.0'})
    # Default platform TLS validation stays enabled; no fallback bypass.
    with urllib.request.urlopen(request, timeout=100) as response:
        raw = response.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    requests = []

    def fetch(name, url):
        raw = get(name, url, args.offline)
        requests.append({'url': url, 'rawFile': (RAW / name).relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        if name.endswith('.html'):
            return None
        result = json.loads(raw)
        if result.get('error'):
            raise ValueError('Official service error: ' + str(result['error']))
        return result

    fetch('catalogue.html', CATALOGUE)
    metadata = fetch('metadata.json', SERVICE + '?f=pjson')
    ids = fetch('ids.json', SERVICE + '/query?' + urllib.parse.urlencode({'where': '1=1', 'returnIdsOnly': 'true', 'f': 'json'}))['objectIds']
    features = []
    for start in range(0, len(ids), 100):
        url = SERVICE + '/query?' + urllib.parse.urlencode({'objectIds': ','.join(str(x) for x in ids[start:start+100]), 'outFields': '*', 'returnGeometry': 'true', 'outSR': '4326', 'f': 'geojson'})
        response = fetch('features-' + str(start) + '.json', url)
        if response.get('exceededTransferLimit'):
            raise ValueError('Incomplete official response')
        features.extend(response['features'])
    if len(features) != len(ids):
        raise ValueError('Official feature count mismatch')
    output = ROOT / 'assets/maps/national/council-sa-wards.geojson'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'type': 'FeatureCollection', 'features': features}, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    source = {'id': 'council-sa-official-wards', 'title': 'Location SA: Local Government Area Wards (dataset 836)', 'url': CATALOGUE, 'checked': CHECKED, 'rawFile': 'content/places/raw/sa-ward-geometry/metadata.json', 'sha256': requests[1]['sha256'], 'licence': 'Dataset metadata: AusGOAL CC BY (Attribution); metadata report CC BY 3.0 Australia. Copyright Crown in right of South Australia and licensors; original terms retained.', 'licenceUrl': CATALOGUE, 'attribution': 'Local Government Area Wards, Location SA / Government of South Australia. CC BY (Attribution); source rights and accuracy limitations apply.'}
    supplement = {'schemaVersion': 1, 'checked': CHECKED, 'source': source, 'layer': {'id': 'council-sa-official-wards', 'jurisdiction': 'sa', 'kind': 'ward', 'name': 'South Australia local government wards', 'geometryFile': output.relative_to(ROOT).as_posix(), 'featureIdField': metadata.get('objectIdField', 'objectid'), 'sourceId': source['id'], 'crs': 'EPSG:4326', 'nativeCrs': metadata.get('extent', {}).get('spatialReference'), 'boundaryEdition': 'Current Location SA source snapshot 17 October 2026; verify applicable election edition separately', 'attribution': source['attribution']}, 'sourceFeatureCount': len(ids), 'metadata': metadata, 'requests': requests, 'processing': 'Official source GeoJSON response requested in EPSG4326; all properties, polygon parts, rings and coordinates retained without rounding, union, clipping or simplification. Parent joins must use source local-government fields; no spatially inferred parent.'}
    (ROOT / 'content/places/sources/council-sa-ward-supplement.json').write_text(json.dumps(supplement, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'features': len(features), 'fields': [field['name'] for field in metadata['fields']], 'sampleProperties': features[0]['properties'] if features else {}, 'output': str(output)}))


if __name__ == '__main__':
    main()
