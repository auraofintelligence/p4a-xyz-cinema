"""Retain Geoscience Australia's registered raster background, never boundary geometry."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SERVICE = 'https://services.ga.gov.au/gis/rest/services/NationalBaseMap/MapServer'
OUT = ROOT / 'assets/maps/national'
SOURCE = ROOT / 'content/places/sources'


def fetch(url):
    return urlopen(Request(url, headers={'User-Agent': 'P4A-source-review/1.0'}), timeout=90).read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    metadata = fetch(SERVICE + '?f=pjson')
    (SOURCE / 'national-basemap-service.json').write_bytes(metadata)
    info = json.loads(metadata)
    # Geographic viewing extent only. This box is not an administrative boundary.
    params = {'bbox': '10500000,-6000000,19000000,-900000', 'bboxSR': 3857,
              'imageSR': 3857, 'size': '2400,1440', 'format': 'png32',
              'transparent': 'false', 'f': 'pjson'}
    request = SERVICE + '/export?' + urlencode(params)
    response = fetch(request)
    (SOURCE / 'national-basemap-export.json').write_bytes(response)
    export = json.loads(response)
    if 'error' in export:
        raise RuntimeError(export['error'])
    image = fetch(export['href'])
    assert image.startswith(b'\x89PNG\r\n\x1a\n')
    (OUT / 'national-geographic-grey.png').write_bytes(image)
    manifest = {'schemaVersion': 1, 'checked': '2026-10-17',
                'publisher': 'Geoscience Australia', 'serviceURL': SERVICE,
                'request': request, 'image': 'assets/maps/national/national-geographic-grey.png',
                'extent': export['extent'], 'width': export['width'], 'height': export['height'],
                'crs': 'EPSG:3857', 'bytes': len(image), 'sha256': hashlib.sha256(image).hexdigest(),
                'licence': 'Creative Commons Attribution 4.0 International; retain component rights',
                'licenceUrl': 'https://creativecommons.org/licenses/by/4.0/',
                'attribution': info['copyrightText'],
                'roads': 'Original colour raster rendered in subdued greyscale by default; detailed colour/roads online view is optional.',
                'processing': 'Original export PNG bytes retained. Canvas uses the returned extent in EPSG:3857. Overlay boundaries are independently sourced, transparent and unchanged.',
                'onlineDetailService': SERVICE,
                'refreshWhen': 'Service, source rights, image extent, geographic coverage or display projection changes.'}
    (SOURCE / 'national-basemap.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Retained official geographic raster: {len(image):,} bytes; returned extent {export["extent"]}.')


if __name__ == '__main__':
    main()
