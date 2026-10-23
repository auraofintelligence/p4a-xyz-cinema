#!/usr/bin/env python3
"""Retain primary federal sources and build the federal place adapter.

Network retrieval is explicit (--fetch); ordinary runs rebuild from retained
sources. Never replace current office with an election winner. AEC ballots and
parliamentary role rosters have independent evidence and dates.
"""
from __future__ import annotations

import argparse
import array
import csv
import hashlib
import html
import io
import json
import gzip
import re
import struct
import urllib.request
import urllib.error
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw/federal'
SOURCES = ROOT / 'content/places/sources'
MAPS = ROOT / 'assets/maps/national'
CHECKED = '2026-10-17'
URLS = {
    'federal-aec-gis-index.html': 'https://www.aec.gov.au/Electorates/gis/gis_datadownload.htm',
    'federal-aec-2025-boundaries.zip': 'https://www.aec.gov.au/Electorates/files/2025/AUS-March-2025-esri.zip',
    'federal-aec-sa-2026-boundaries.zip': 'https://www.aec.gov.au/redistributions/2025/sa/files/determination/data/GIS/SA-October-2026-esri.zip',
    'federal-aec-tas-2026-boundaries.zip': 'https://www.aec.gov.au/redistributions/2024/tas/files/determination/data/GIS/TAS-October-2026-esri.zip',
    'federal-aec-act-2026-boundaries.zip': 'https://www.aec.gov.au/redistributions/2025/act/files/determination/data/GIS/ACT-october-2026-esri.zip',
    'federal-aec-house-candidates-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/HouseCandidatesDownload-31496.csv',
    'federal-aec-house-votes-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/HouseFirstPrefsByCandidateByVoteTypeDownload-31496.csv',
    'federal-aec-house-elected-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/HouseMembersElectedDownload-31496.csv',
    'federal-aec-senate-downloads.html': 'https://results.aec.gov.au/31496/Website/SenateDownloadsMenu-31496-Csv.htm',
    'federal-aec-senate-candidates-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/SenateCandidatesDownload-31496.csv',
    'federal-aec-senate-elected-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/SenateSenatorsElectedDownload-31496.csv',
    'federal-aec-senate-votes-2025.csv': 'https://results.aec.gov.au/31496/Website/Downloads/SenateFirstPrefsByStateByVoteTypeDownload-31496.csv',
    'federal-aec-sa-2026-determination.html': 'https://www.aec.gov.au/redistributions/2025/sa/determination.html',
    'federal-aec-sa-2026-announcement.html': 'https://www.aec.gov.au/redistributions/2025/sa/announcement.html',
    'federal-aec-odonoghue-localities.html': "https://electorate.aec.gov.au/LocalitySearchResults.aspx?divid=975&filter=O%27Donoghue&filterby=Electorate",
    'federal-aec-farrer-candidates-2026.csv': 'https://results.aec.gov.au/31633/Website/Downloads/HouseCandidatesDownload-31633.csv',
    'federal-aec-farrer-votes-2026.csv': 'https://results.aec.gov.au/31633/Website/Downloads/HouseFirstPrefsByCandidateByVoteTypeDownload-31633.csv',
    'federal-aec-farrer-2026.html': 'https://results.aec.gov.au/31633/Website/HouseDivisionPage-31633-118.htm',
    'federal-aec-farrer-timetable-2026.html': 'https://www.aec.gov.au/Elections/supplementary_by_elections/2026-farrer/index.htm',
    'federal-aec-2025-timetable.html': 'https://www.aec.gov.au/Elections/federal_elections/2025/timetable.htm',
    'federal-aec-election-dates.html': 'https://www.aec.gov.au/learn/election-timetable.htm',
    'federal-aec-copyright.html': 'https://www.aec.gov.au/footer/copyright.htm',
    'federal-aph-members-photos.html': 'https://www.aph.gov.au/Senators_and_Members/Members/Members_Photos',
    'federal-aph-senators-photos.html': 'https://www.aph.gov.au/Senators_and_Members/Senators/Senators_Photos',
    'federal-aph-house-roster.html': 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?mem=1',
    'federal-aph-senate-roster.html': 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?sen=1',
    'federal-aph-roster.html': 'https://www.aph.gov.au/Senators_and_Members',
    'federal-aph-senators-list.html': 'https://www.aph.gov.au/Senators_and_Members/Senators/Senators_by_State',
    'federal-aph-contact.html': 'https://www.aph.gov.au/Senators_and_Members/Contacting_Senators_and_Members',
    'federal-aph-farley.html': 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=62329',
    'federal-aph-address-files.html': 'https://www.aph.gov.au/Senators_and_Members/Contacting_Senators_and_Members/Address_labels_and_CSV_files',
    'federal-handbook.html': 'https://handbook.aph.gov.au/',
    'federal-handbook-client.js': 'https://handbook.aph.gov.au/assets/index.js?v=2638669041',
    'federal-handbook-current.json': "https://handbookapi.aph.gov.au/api/individuals?$filter=InCurrentParliament%20eq%20'True'",
}


def fetch_one(item):
    name, url = item
    path = RAW / name
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (P4A public civic source archive)'})
        with urllib.request.urlopen(req, timeout=50) as response:
            data = response.read()
            if b'<title>404' in data[:10000]:
                raise ValueError('HTTP 200 soft-404 page; not retained as supporting evidence')
            path.write_bytes(data)
            return {'file': name, 'url': url, 'status': response.status,
                    'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'checked': CHECKED, 'responseUrl': response.url}
    except Exception as exc:
        return {'file': name, 'url': url, 'status': 'unavailable', 'error': str(exc), 'checked': CHECKED}


def fetch(only=None):
    RAW.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        selected = lambda key: not only or any(part in key for part in only.split(','))
        rows = list(pool.map(fetch_one, [(k, v) for k, v in URLS.items() if selected(k)]))
    previous = SOURCES / 'federal-transfer-log.json'
    if only and previous.exists():
        rows = [r for r in json.loads(previous.read_text()) if not selected(r['file'])] + rows
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / 'federal-transfer-log.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    for row in rows:
        if selected(row['file']):
            print(row['file'], row['status'], row.get('bytes', ''), flush=True)


def read_csv(name):
    path = RAW / name
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    return list(csv.DictReader(lines[1:]))


def dbf_records(data):
    count, header_size, row_size = struct.unpack_from('<IHH', data, 4)
    fields = []
    for pos in range(32, header_size - 1, 32):
        name = data[pos:pos + 11].split(b'\0')[0].decode('ascii')
        fields.append((name, chr(data[pos + 11]), data[pos + 16]))
    rows = []
    for index in range(count):
        pos = header_size + index * row_size + 1
        row = {}
        for name, kind, length in fields:
            value = data[pos:pos + length].decode('cp1252').strip()
            row[name] = value
            pos += length
        rows.append(row)
    return rows


def inside(point, ring):
    x, y = point
    found = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]:
            found = not found
    return found


def shape_features(path):
    """Decode ESRI polygons without altering a single coordinate or ring."""
    with zipfile.ZipFile(path) as archive:
        shp_name = next(n for n in archive.namelist() if n.lower().endswith('.shp'))
        stem = shp_name[:-4]
        rows = dbf_records(archive.read(stem + '.dbf'))
        data = archive.read(shp_name)
        projection = archive.read(stem + '.prj').decode('utf-8')
    assert 'GEOGCS' in projection and not 'PROJCS' in projection, projection
    features = []
    pos = 100
    for properties in rows:
        number, words = struct.unpack_from('>II', data, pos)
        block = data[pos + 8:pos + 8 + words * 2]
        pos += 8 + words * 2
        kind = struct.unpack_from('<I', block)[0]
        assert kind in (5, 15, 25), kind
        part_count, point_count = struct.unpack_from('<II', block, 36)
        offsets = list(struct.unpack_from('<' + 'I' * part_count, block, 44)) + [point_count]
        point_start = 44 + part_count * 4
        points = [list(struct.unpack_from('<dd', block, point_start + i * 16)) for i in range(point_count)]
        rings = [points[offsets[i]:offsets[i + 1]] for i in range(part_count)]
        exteriors, holes = [], []
        for ring in rings:
            signed = sum((b[0] - a[0]) * (b[1] + a[1]) for a, b in zip(ring, ring[1:]))
            (exteriors if signed > 0 else holes).append(ring)
        assert exteriors, properties
        polygons = [[ring] for ring in exteriors]
        for hole in holes:
            matches = [poly for poly in polygons if inside(hole[0], poly[0])]
            assert len(matches) == 1, (properties, len(matches))
            matches[0].append(hole)
        coordinates = polygons[0] if len(polygons) == 1 else polygons
        geometry = {'type': 'Polygon' if len(polygons) == 1 else 'MultiPolygon', 'coordinates': coordinates}
        features.append({'type': 'Feature', 'properties': properties, 'geometry': geometry,
                         '_pointCount': point_count, '_ringCount': part_count})
    assert pos == len(data), (pos, len(data))
    return features, projection


def write_geojson(name, features):
    MAPS.mkdir(parents=True, exist_ok=True)
    clean = [{k: v for k, v in feature.items() if not k.startswith('_')} for feature in features]
    data = json.dumps({'type': 'FeatureCollection', 'features': clean}, separators=(',', ':'), ensure_ascii=False).encode()
    path = MAPS / (name + '.geojson.gz')
    with path.open('wb') as stream:
        with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as compressed:
            compressed.write(data)
    return path.relative_to(ROOT).as_posix(), len(data), hashlib.sha256(data).hexdigest()


JURISDICTIONS = {
    'act': ('Australian Capital Territory', 'Australia/Sydney'),
    'nsw': ('New South Wales', 'Australia/Sydney'),
    'nt': ('Northern Territory', 'Australia/Darwin'),
    'qld': ('Queensland', 'Australia/Brisbane'),
    'sa': ('South Australia', 'Australia/Adelaide'),
    'tas': ('Tasmania', 'Australia/Hobart'),
    'vic': ('Victoria', 'Australia/Melbourne'),
    'wa': ('Western Australia', 'Australia/Perth'),
}


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def source_id(filename):
    return filename.rsplit('.', 1)[0]


def source(filename, title, **extra):
    path = RAW / filename
    data = path.read_bytes()
    return {'id': source_id(filename), 'title': title, 'url': URLS[filename], 'checked': CHECKED,
            'rawFile': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), **extra}


def person_name(row):
    preferred = row.get('PreferredName') or row.get('GivenName') or row.get('GivenNm')
    return preferred + ' ' + (row.get('FamilyName') or row['Surname'])


def event(jurisdiction, chamber, candidates, division_id=None, by_election=False):
    event_id = '31633' if by_election else '31496'
    url = (f'https://results.aec.gov.au/{event_id}/Website/HouseDivisionPage-{event_id}-{division_id}.htm'
           if chamber == 'House of Representatives' else
           f'https://results.aec.gov.au/{event_id}/Website/SenateStatePage-{event_id}-{jurisdiction.upper()}.htm')
    return {'id': 'aec-' + event_id + '-' + (str(division_id) if division_id else jurisdiction),
            'officialEventId': event_id,
            'label': '2026 Farrer by-election' if by_election else '2025 federal election',
            'kind': 'by-election' if by_election else 'general-election', 'status': 'final',
            'date': '2026-05-09' if by_election else '2025-05-03',
            'dateBasis': 'Official AEC polling date; final results are retained separately from current office.',
            'timezone': JURISDICTIONS[jurisdiction][1], 'sourceUrl': url,
            'dateSourceUrl': URLS['federal-aec-farrer-timetable-2026.html' if by_election else 'federal-aec-2025-timetable.html'],
            'resultsUrl': url, 'candidates': candidates,
            'boundaryEdition': '2025 federal election boundaries',
            'resultMeasure': 'House primary first preferences; election status from AEC final candidate roster' if division_id else
                             'Senate multi-member ballot; elected status from AEC final candidate roster (not House 2PP)'}


def candidate(row, url, votes=None):
    result = {'id': 'aec-candidate-' + row['CandidateID'], 'name': person_name(row), 'party': row['PartyNm'],
              'status': 'elected' if row['Elected'] == 'Y' else 'contested', 'sourceUrl': url,
              'sourceId': source_id('federal-aec-house-candidates-2025.csv' if 'DivisionID' in row else 'federal-aec-senate-candidates-2025.csv')}
    if votes is not None:
        result['votes'] = votes
        result['voteMeasure'] = 'first preferences'
    return result


def build():
    sources = [source('federal-aec-2025-boundaries.zip', 'AEC national boundaries used at the 2025 federal election',
                      licence='AEC spatial data and underlying State/Territory rights; see retained copyright and GIS terms.',
                      nativeCrs='EPSG:4283', edition='March 2025; 2025 election basis'),
               source('federal-aec-gis-index.html', 'AEC GIS editions and current/superseded boundary status'),
               source('federal-aec-copyright.html', 'AEC copyright and third-party rights'),
               source('federal-handbook-current.json', 'Parliamentary Handbook current parliamentarians API',
                      query="InCurrentParliament eq 'True'; no top/skip; 226 records; no nextLink",
                      licence='Public role/name/party facts extracted; official biographies and portraits retain Parliamentary rights.'),
               source('federal-aec-house-candidates-2025.csv', 'AEC final 2025 House candidate roster'),
               source('federal-aec-house-votes-2025.csv', 'AEC final House first preferences by candidate and vote type'),
               source('federal-aec-senate-candidates-2025.csv', 'AEC final 2025 Senate candidate roster'),
               source('federal-aec-senate-votes-2025.csv', 'AEC Senate first preferences: separate candidate below-line and group above-line rows'),
               source('federal-aec-farrer-candidates-2026.csv', 'AEC final 2026 Farrer by-election candidate roster'),
               source('federal-aec-farrer-2026.html', 'AEC Farrer by-election final results'),
               source('federal-aec-farrer-timetable-2026.html', 'AEC 2026 Farrer by-election timetable'),
               source('federal-aec-2025-timetable.html', 'AEC 2025 general election timetable'),
               source('federal-aec-election-dates.html', 'AEC explanation of federal election timing'),
               source('federal-aec-sa-2026-determination.html', 'AEC South Australia names and boundaries determination, 8 October 2026'),
               source('federal-aec-sa-2026-announcement.html', 'AEC South Australia redistribution: serving members and next election effect'),
               source('federal-aec-odonoghue-localities.html', "AEC O'Donoghue division identity 975 / locality lookup")]
    source_map = {s['id']: s for s in sources}
    house = read_csv('federal-aec-house-candidates-2025.csv')
    senate = read_csv('federal-aec-senate-candidates-2025.csv')
    votes = {r['CandidateID']: int(r['TotalVotes']) for r in read_csv('federal-aec-house-votes-2025.csv')}
    senate_votes = {r['CandidateID']: int(r['TotalVotes']) for r in read_csv('federal-aec-senate-votes-2025.csv') if r['BallotPosition'] != '0'}
    elected = read_csv('federal-aec-house-elected-2025.csv')
    by_name = {r['DivisionNm']: r for r in elected}
    by_normalized_name = {r['DivisionNm'].casefold(): r for r in elected}
    assert len(by_name) == 150
    current_data = json.loads((RAW / 'federal-handbook-current.json').read_text(encoding='utf-8-sig'))
    assert not current_data.get('@odata.nextLink'), 'Roster pagination must be resolved before build.'
    current = current_data['value']
    assert len(current) == 226
    house_people = {r['Electorate']: r for r in current if r['Electorate']}
    senate_people = [r for r in current if not r['Electorate']]
    assert len(house_people) == 150 and len(senate_people) == 76
    assert set(by_name) == set(house_people)
    features, projection = shape_features(RAW / 'federal-aec-2025-boundaries.zip')
    assert len(features) == 150
    groups = defaultdict(list)
    for feature in features:
        props = feature['properties']
        division = by_normalized_name[props['Elect_div'].casefold()]
        props['aecDivisionId'] = division['DivisionID']
        props['jurisdiction'] = division['StateAb'].lower()
        groups[props['jurisdiction']].append(feature)
    layers, geometry_audit = [], []
    for jurisdiction, collection in sorted(groups.items()):
        output, byte_count, digest = write_geojson('federal-house-' + jurisdiction + '-2025', collection)
        layers.append({'id': 'federal-house-' + jurisdiction + '-2025', 'jurisdiction': jurisdiction,
                       'kind': 'federal-division', 'name': 'House divisions — 2025 election / serving representation',
                       'geometryFile': output, 'featureIdField': 'aecDivisionId', 'featureNameField': 'Elect_div',
                       'sourceId': 'federal-aec-2025-boundaries', 'boundaryEdition': 'March 2025 — 2025 federal election',
                       'crs': 'EPSG:4326', 'nativeCrs': 'EPSG:4283',
                       'coordinateNote': 'Exact GDA94 longitude/latitude coordinates retained. Displayed on a WGS84 web base without datum shift; alignment is approximate at metre scale.',
                       'attribution': 'Australian Electoral Commission; underlying State/Territory data rights retained.',
                       'featureCount': len(collection), 'uncompressedBytes': byte_count, 'uncompressedSha256': digest,
                       'pointCount': sum(f['_pointCount'] for f in collection),
                       'ringCount': sum(f['_ringCount'] for f in collection)})
    # The proclaimed 2026 editions are available separately. They have not yet
    # been used at a federal poll and must not be joined to 2025 votes spatially.
    for jurisdiction in ('sa', 'tas', 'act'):
        filename = 'federal-aec-' + jurisdiction + '-2026-boundaries.zip'
        src = source(filename, 'AEC ' + JURISDICTIONS[jurisdiction][0] + ' 2026 proclaimed redistribution',
                     licence='AEC GIS download terms and third-party rights retained.', nativeCrs='See retained .prj',
                     edition='October 2026; not yet applied at a federal election')
        sources.append(src)
        edition_features, edition_projection = shape_features(RAW / filename)
        for feature in edition_features:
            props = feature['properties']
            if props['Elect_div'] == "O'Donoghue":
                assert jurisdiction == 'sa'
                props['aecDivisionId'] = '975'
            else:
                division = by_normalized_name[props['Elect_div'].casefold()]
                assert division['StateAb'].lower() == jurisdiction
                props['aecDivisionId'] = division['DivisionID']
            props['jurisdiction'] = jurisdiction
        output, byte_count, digest = write_geojson('federal-house-' + jurisdiction + '-2026-next', edition_features)
        layers.append({'id': 'federal-house-' + jurisdiction + '-2026-next', 'jurisdiction': jurisdiction,
                       'kind': 'federal-division', 'name': 'House divisions — 2026 proclaimed / next election',
                       'geometryFile': output, 'featureIdField': 'aecDivisionId', 'featureNameField': 'Elect_div',
                       'sourceId': src['id'], 'boundaryEdition': 'October 2026 proclaimed; next federal election date TBD',
                       'crs': 'EPSG:4326', 'nativeCrs': 'GDA94 / native geographic .prj retained' if jurisdiction != 'sa' else 'Native generic geographic .prj retained',
                       'coordinateNote': 'Every native longitude/latitude coordinate retained without rounding or transformation. WGS84 raster alignment approximate; see original .prj.',
                       'status': 'proclaimed-next-election', 'attribution': 'Australian Electoral Commission; underlying State/Territory rights retained.',
                       'featureCount': len(edition_features), 'uncompressedBytes': byte_count, 'uncompressedSha256': digest,
                       'pointCount': sum(f['_pointCount'] for f in edition_features),
                       'ringCount': sum(f['_ringCount'] for f in edition_features)})
    def representatives(rows, role):
        return [{'name': person_name(r), 'role': role, 'party': r['Party'],
                 'profileUrl': 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=' + r['PHID'],
                 'handbookUrl': 'https://handbook.aph.gov.au/parliamentarians/' + r['PHID'],
                 'sourceId': 'federal-handbook-current', 'checked': CHECKED} for r in rows]
    places = []
    for name, division in sorted(by_name.items()):
        jurisdiction = division['StateAb'].lower()
        division_id = division['DivisionID']
        results_url = f'https://results.aec.gov.au/31496/Website/HouseDivisionPage-31496-{division_id}.htm'
        roster = [candidate(r, results_url, votes.get(r['CandidateID'])) for r in house if r['DivisionID'] == division_id]
        representatives_current = representatives([house_people[name]], 'Member for ' + name)
        # Link a contestant to a current official public profile only when the
        # official electorate and full ballot surname/given-name join agree.
        member = house_people[name]
        for r, c in zip([r for r in house if r['DivisionID'] == division_id], roster):
            if r['Surname'].casefold() == member['FamilyName'].casefold() and r['GivenNm'].casefold() in (member['GivenName'].casefold(), member['PreferredName'].casefold()):
                c['profileUrl'] = representatives_current[0]['profileUrl']
        elections = [event(jurisdiction, 'House of Representatives', roster, division_id)]
        if name == 'Farrer':
            rows = read_csv('federal-aec-farrer-candidates-2026.csv')
            by_results_url = URLS['federal-aec-farrer-2026.html']
            by_candidates = [candidate(r, by_results_url) for r in rows]
            markup = (RAW / 'federal-aec-farrer-2026.html').read_text(encoding='utf-8-sig')
            fp_markup = re.search(r'<table[^>]*id="fp"[^>]*>(.*?)</table>', markup, re.S).group(1)
            vote_rows = {}
            for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', fp_markup, re.S):
                cells = [html.unescape(re.sub('<[^>]+>', '', cell)).strip() for cell in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
                if len(cells) >= 3 and re.fullmatch(r'[0-9,]+', cells[2]):
                    vote_rows[cells[0]] = int(cells[2].replace(',', ''))
            for c in by_candidates:
                c['sourceId'] = 'federal-aec-farrer-candidates-2026'
            for row, c in zip(rows, by_candidates):
                c['votes'] = vote_rows[row['Surname'] + ', ' + row['GivenNm']]
                c['voteMeasure'] = 'first preferences'
                if row['Surname'] == member['FamilyName'] and row['GivenNm'] == member['GivenName']:
                    c['profileUrl'] = representatives_current[0]['profileUrl']
            elections.append(event(jurisdiction, 'House of Representatives', by_candidates, division_id, True))
        elections.append({'id': 'federal-house-next-' + division_id, 'label': 'Next House election', 'kind': 'general-election',
                          'status': 'date-unannounced', 'date': None, 'dateBasis': 'No fixed federal polling date. No verified future date entered; check official writs/announcements.',
                          'timezone': JURISDICTIONS[jurisdiction][1], 'sourceUrl': URLS['federal-aec-election-dates.html'], 'candidates': []})
        notes = ['Current office is independently sourced from the Parliamentary Handbook roster, not inferred from the previous result.',
                 'No new Twinkles: grassroots authorship remains open.',
                 'All previous contestants are retained. Official results links are supplied; personal/campaign websites are included only where independently verified.']
        if jurisdiction in ('sa', 'tas', 'act'):
            notes.append('AEC proclaims a 2026 redistribution for the next federal election. The serving-member/2025 map and historical results retain their 2025 boundary basis; the new edition is a separate map layer.')
        if name == 'Farrer':
            notes.append('The 9 May 2026 Farrer by-election is retained as a separate event from the 3 May 2025 general election; David Farley is independently listed in the current Parliamentary roster.')
        place = {'id': 'federal-house-' + division_id, 'name': name, 'slug': slug(name), 'jurisdiction': jurisdiction,
                 'kind': 'federal-division', 'chamber': 'House of Representatives',
                 'layerId': 'federal-house-' + jurisdiction + '-2025', 'featureId': division_id,
                 'aecDivisionId': division_id,
                 'officialUrl': f"https://www.aec.gov.au/profiles/{jurisdiction}/{slug(name.replace(chr(39), ''))}.htm",
                 'sources': ['federal-aec-2025-boundaries', 'federal-aec-house-candidates-2025', 'federal-aec-house-votes-2025', 'federal-handbook-current', 'federal-aec-2025-timetable', 'federal-aec-election-dates'],
                 'boundaryEdition': 'March 2025 — 2025 federal election / serving representation',
                 'representatives': representatives_current, 'elections': elections, 'coverageNotes': notes}
        if jurisdiction in ('sa', 'tas', 'act'):
            if name != 'Grey':
                place['nextBoundaryLayerId'] = 'federal-house-' + jurisdiction + '-2026-next'
                place['mapRefs'] = [{'layerId': place['nextBoundaryLayerId'], 'featureId': division_id,
                                     'boundaryEdition': 'October 2026 proclaimed; next federal election'}]
            place['sources'].append('federal-aec-' + jurisdiction + '-2026-boundaries')
        if name == 'Grey':
            place['successorPlaceId'] = 'federal-house-975'
            place['coverageNotes'].append("The next-election successor name is O'Donoghue (AEC division 975). Historical Grey routes and 2025 results remain available; see the distinct O'Donoghue page.")
        if name == 'Farrer':
            place['sources'] += ['federal-aec-farrer-candidates-2026', 'federal-aec-farrer-2026', 'federal-aec-farrer-timetable-2026']
        places.append(place)
    places.append({'id': 'federal-house-975', 'name': "O'Donoghue", 'slug': 'odonoghue', 'jurisdiction': 'sa',
                   'kind': 'federal-division', 'chamber': 'House of Representatives',
                   'layerId': 'federal-house-sa-2026-next', 'featureId': '975', 'aecDivisionId': '975',
                   'officialUrl': URLS['federal-aec-sa-2026-determination.html'],
                   'sources': ['federal-aec-sa-2026-boundaries', 'federal-aec-sa-2026-determination', 'federal-aec-sa-2026-announcement', 'federal-aec-odonoghue-localities'],
                   'boundaryEdition': 'October 2026 proclaimed; applies to federal election writs issued after 8 October 2026',
                   'representationStatus': 'next-election-division', 'predecessorPlaceId': 'federal-house-' + by_name['Grey']['DivisionID'],
                   'representatives': [],
                   'elections': [{'id': 'federal-house-next-975', 'label': "First election under the name O'Donoghue", 'kind': 'general-election',
                                  'status': 'date-unannounced', 'date': None, 'dateBasis': 'New name determined 8 October 2026. No verified future polling date entered.',
                                  'timezone': 'Australia/Adelaide', 'sourceUrl': URLS['federal-aec-sa-2026-determination.html'], 'candidates': []}],
                   'coverageNotes': ["The 2026 redistribution replaces the electorate name Grey with O'Donoghue for the next federal election. Members continue to represent the electorate on which they were elected until that election.",
                                     'Current Member for Grey: see the serving Grey page and its independent parliamentary roster; no current Member for this future electoral edition is inferred.',
                                     'There has been no previous election under this new name/edition. Previous Grey contestants and results remain attached to Grey, with their historical boundary basis.',
                                     'The original 2026 GIS, Gazette determination page and source identity 975 are retained. No new Twinkles are created.']})
    for jurisdiction, (name, timezone) in JURISDICTIONS.items():
        url = f'https://results.aec.gov.au/31496/Website/SenateStatePage-31496-{jurisdiction.upper()}.htm'
        roster = [candidate(r, url) for r in senate if r['StateAb'].lower() == jurisdiction]
        members = [r for r in senate_people if r['StateAbbrev'].lower() == jurisdiction]
        for r, c in zip([r for r in senate if r['StateAb'].lower() == jurisdiction], roster):
            c['votes'] = senate_votes[r['CandidateID']]
            c['voteMeasure'] = 'below-the-line first preferences; group above-the-line votes are separate'
            c['voteSourceId'] = 'federal-aec-senate-votes-2025'
            matching = [p for p in members if p['FamilyName'].casefold() == r['Surname'].casefold() and r['GivenNm'].casefold() in (p['GivenName'].casefold(), p['PreferredName'].casefold())]
            if len(matching) == 1:
                c['profileUrl'] = 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=' + matching[0]['PHID']
        assert len(members) == (2 if jurisdiction in ('act', 'nt') else 12)
        places.append({'id': 'federal-senate-' + jurisdiction, 'name': name + ' Senate', 'slug': 'senate',
                       'jurisdiction': jurisdiction, 'kind': 'senate-area', 'chamber': 'Senate',
                       'officialUrl': 'https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?sen=1&sta=' + jurisdiction.upper(),
                       'sources': ['federal-aec-senate-candidates-2025', 'federal-aec-senate-votes-2025', 'federal-handbook-current', 'federal-aec-2025-timetable', 'federal-aec-election-dates'],
                       'representatives': representatives(members, 'Senator for ' + name),
                       'elections': [event(jurisdiction, 'Senate', roster),
                                     {'id': 'federal-senate-next-' + jurisdiction, 'label': 'Next Senate election', 'kind': 'general-election',
                                      'status': 'date-unannounced', 'date': None, 'dateBasis': 'No verified polling date entered. State Senate rotation and territory terms differ; current office does not establish future candidacy.',
                                      'timezone': timezone, 'sourceUrl': URLS['federal-aec-election-dates.html'], 'candidates': []}],
                       'coverageNotes': ['Senators represent the state/territory as a whole; House divisions are a different representation layer.',
                                         '2025 Senate contestants include elected and unsuccessful candidates; this was a half-Senate election for states, and an election of both territory senators.',
                                         'A state Senate casual vacancy normally uses a replacement process, not a House-style by-election. Verify the actual vacancy process before adding an event.',
                                         'Current senators are independently sourced from the Parliamentary Handbook; 2022 continuing terms and subsequent replacements are not inferred from 2025 winners.',
                                         'External territory representation needs AEC enrolment advice; state/territory context maps are navigation aids, not enrolment determinations.']})
    output = {'schemaVersion': 1, 'checked': CHECKED, 'scope': 'federal', 'sources': sources, 'layers': layers, 'places': places,
              'coverage': {'houseDivisions': 150, 'senateAreas': 8, 'currentHouseMembers': len(house_people), 'currentSenators': len(senate_people),
                           'house2025Candidates': len(house), 'senate2025Candidates': len(senate), 'farrer2026Candidates': 12,
                           'nextElectionRenamedDivisions': 1,
                           'gaps': ['No independent personal/campaign website review for every previous contestant; AEC results link is retained for everyone.',
                                    'New federal Twinkles are intentionally left to grassroots implementation.']}}
    assert len(house) == 1126 and len(senate) == 330
    (ROOT / 'content/places/federal.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    audit = {'checked': CHECKED, 'method': 'Standard-library shapefile/DBF decoding; ESRI ring orientation and containment retained; no simplification/rounding/reprojection.',
             'nativeProjection2025': projection, 'layers': layers,
             'checks': ['150 national source features match all 150 AEC result division names and independent current Parliamentary roster.',
                        '226 current Parliament API records reconciled to 150 House offices and 76 senators; no pagination nextLink.',
                        '1126 House and 330 Senate 2025 contestants reconciled to AEC final CSVs; 12 separate Farrer 2026 contestants.',
                        'All shapefile record bytes consumed; every source ring assigned exactly once; point/ring totals retained per output.'],
             'rights': 'Raw AEC files and Parliamentary public records retain original rights; no portraits copied.'}
    (SOURCES / 'federal-geometry-audit.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(output['coverage'], indent=2))


def source_ring_signatures(path):
    """Fingerprint exact IEEE-754 coordinate bytes per source ring."""
    signatures = {}
    with zipfile.ZipFile(path) as archive:
        name = next(n for n in archive.namelist() if n.lower().endswith('.shp'))
        data = archive.read(name)
        records = dbf_records(archive.read(name[:-4] + '.dbf'))
    pos = 100
    for record in records:
        words = struct.unpack_from('>I', data, pos + 4)[0]
        block = data[pos + 8:pos + 8 + words * 2]
        pos += 8 + words * 2
        count, points = struct.unpack_from('<II', block, 36)
        offsets = list(struct.unpack_from('<' + 'I' * count, block, 44)) + [points]
        start = 44 + count * 4
        signatures[record['Elect_div'].casefold()] = sorted(hashlib.sha256(block[start + offsets[i] * 16:start + offsets[i + 1] * 16]).hexdigest() for i in range(count))
    assert pos == len(data)
    return signatures


def verify():
    data = json.loads((ROOT / 'content/places/federal.json').read_text(encoding='utf-8'))
    sources = {s['id']: s for s in data['sources']}
    layers = {l['id']: l for l in data['layers']}
    place_by_ref = {}
    for place in data['places']:
        refs = ([{'layerId': place['layerId'], 'featureId': place['featureId']}] if place.get('layerId') else []) + place.get('mapRefs', [])
        for ref in refs:
            key = (ref['layerId'], str(ref['featureId']))
            assert key not in place_by_ref, key
            place_by_ref[key] = place['id']
        assert all(s in sources for s in place['sources']), place['id']
        assert all(r['sourceId'] in sources and r['profileUrl'].startswith('https://www.aph.gov.au/') for r in place['representatives'])
        assert all(e.get('date') is None for e in place['elections'] if e['status'] == 'date-unannounced')
    signatures = {}
    points = rings = features = 0
    for layer in data['layers']:
        src = sources[layer['sourceId']]
        path = ROOT / src['rawFile']
        if str(path) not in signatures:
            signatures[str(path)] = source_ring_signatures(path)
        compressed = ROOT / layer['geometryFile']
        output = gzip.decompress(compressed.read_bytes())
        assert hashlib.sha256(output).hexdigest() == layer['uncompressedSha256']
        collection = json.loads(output)
        point_total = ring_total = 0
        assert len(collection['features']) == layer['featureCount']
        for feature in collection['features']:
            assert (layer['id'], str(feature['properties']['aecDivisionId'])) in place_by_ref, (layer['id'], feature['properties'])
            geometry = feature['geometry']
            all_rings = geometry['coordinates'] if geometry['type'] == 'Polygon' else [ring for polygon in geometry['coordinates'] for ring in polygon]
            delivered_hashes = sorted(hashlib.sha256(array.array('d', (v for point in ring for v in point)).tobytes()).hexdigest() for ring in all_rings)
            assert delivered_hashes == signatures[str(path)][feature['properties']['Elect_div'].casefold()], (layer['id'], feature['properties']['Elect_div'])
            point_total += sum(len(ring) for ring in all_rings)
            ring_total += len(all_rings)
        assert point_total == layer['pointCount'] and ring_total == layer['ringCount']
        points += point_total
        rings += ring_total
        features += len(collection['features'])
    for src in sources.values():
        assert hashlib.sha256((ROOT / src['rawFile']).read_bytes()).hexdigest() == src['sha256'], src['id']
    result = {'checked': CHECKED, 'passed': True, 'sourceHashesVerified': len(sources),
              'mapLayersVerified': len(layers), 'featuresVerifiedIncludingSeparateEditions': features,
              'exactSourceCoordinatesVerified': points, 'exactSourceRingsVerified': rings,
              'mapFeatureToPageJoins': len(place_by_ref), 'currentMembers': sum(len(p['representatives']) for p in data['places']),
              'previousContestants': sum(len(e['candidates']) for p in data['places'] for e in p['elections']),
              'method': 'Compare every delivered ring against SHA-256 of the original shapefile IEEE-754 coordinate bytes; no tolerance, coordinate rounding, ring loss or invented join allowed.'}
    (SOURCES / 'federal-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


def check_links():
    """Check distinct official place/event URLs; preserve access errors honestly."""
    data = json.loads((ROOT / 'content/places/federal.json').read_text(encoding='utf-8'))
    urls = {p['officialUrl'] for p in data['places'] if p.get('officialUrl') and 'www.aph.gov.au' not in p['officialUrl']}
    urls.update(e['sourceUrl'] for p in data['places'] for e in p['elections'] if e.get('sourceUrl'))
    def check(url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (P4A civic source link check)'})
            with urllib.request.urlopen(req, timeout=25) as response:
                body = response.read()
                title = re.search(br'<title[^>]*>(.*?)</title>', body, re.S | re.I)
                label = html.unescape(title.group(1).decode('utf-8', errors='replace').strip()) if title else ''
                return {'url': url, 'status': response.status, 'responseUrl': response.url,
                        'title': label, 'soft404': '404' in label or 'Page not found' in label}
        except Exception as exc:
            return {'url': url, 'status': 'unavailable', 'error': str(exc)}
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, sorted(urls)))
    report = {'checked': CHECKED, 'links': results,
              'note': 'APH profile host returned403 during source acquisition; current identity/office verified through official Handbook API. Profile templates retain official PHID identity; no claim of HTTP200 profile checks.'}
    (SOURCES / 'federal-link-check.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    failures = [r for r in results if r['status'] != 200 or r.get('soft404')]
    print(json.dumps({'checkedUrls': len(results), 'failures': failures}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='Retrieve primary sources and retain originals.')
    parser.add_argument('--only', help='Limit retrieval to filenames containing this fragment.')
    parser.add_argument('--inspect', action='store_true', help='Inspect retained archives and tables.')
    parser.add_argument('--build', action='store_true', help='Build normalized records and lossless map delivery from retained evidence.')
    parser.add_argument('--verify', action='store_true', help='Verify all source hashes, exact source coordinate bytes, joins, office and event counts.')
    parser.add_argument('--check-links', action='store_true', help='Check each distinct AEC place/event URL and retain statuses.')
    args = parser.parse_args()
    if args.fetch:
        fetch(args.only)
    if args.build:
        build()
    if args.verify:
        verify()
    if args.check_links:
        check_links()
    if args.inspect:
        for path in RAW.glob('federal*.zip'):
            with zipfile.ZipFile(path) as archive:
                print(path.name, archive.namelist())
                for name in archive.namelist():
                    if name.endswith('.prj'):
                        print(name, archive.read(name).decode('utf-8', errors='replace'))
        for path in RAW.glob('federal*.csv'):
            print(path.name, path.read_text(encoding='utf-8-sig', errors='replace').splitlines()[:4])
