#!/usr/bin/env python3
"""Merge retained NT/WA/SA ward geometry, with no network or page generation.

The council acquisition adapter calls merge(data). This standalone entry point
checks a copy by default; --write explicitly updates councils.json. Retained
source hashes, every original feature/ring/coordinate, parent identities and
idempotence are checked before writing. Empty source people/events never erase
independently sourced canonical records. Original map assets are read-only.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'content/places/councils.json'
REPORT = ROOT / 'content/places/sources/council-ward-integration-verification.json'
CHECKED = '2026-10-17'
SA_REVIEW = ROOT / 'content/places/sources/council-sa-ward-edition-review.json'
SA_EDITION = 'Location SA source snapshot checked 17 October 2026; preceding ward structures where 2024/2025 reviews apply; not verified as the next periodic election edition'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(value):
    return re.sub('[^a-z0-9]', '', str(value).lower())


def slug(value):
    return re.sub('[^a-z0-9]+', '-', str(value).lower()).strip('-')


def unique(values):
    return list(dict.fromkeys(values))


def add_note(place, note):
    place['coverageNotes'] = unique(place.get('coverageNotes', []) + [note])


def upsert(rows, record):
    existing = next((r for r in rows if r['id'] == record['id']), None)
    if existing is None:
        rows.append(deepcopy(record))
    else:
        existing.update(deepcopy(record))


def source_hash(source, audit):
    path = ROOT / source['rawFile']
    assert path.is_file(), 'Missing retained original: ' + source['rawFile']
    actual = sha(path)
    assert actual == source['sha256'], 'Source hash mismatch: ' + source['rawFile']
    audit[path.relative_to(ROOT).as_posix()] = actual


def pair_count(node):
    if isinstance(node, list) and len(node) >= 2 and all(isinstance(v, (int, float)) for v in node[:2]):
        return 1
    if isinstance(node, list):
        return sum(pair_count(child) for child in node)
    return 0


def geometry_counts(features):
    polygons = rings = pairs = 0
    for feature in features:
        geometry = feature['geometry']
        assert geometry['type'] in ('Polygon', 'MultiPolygon')
        parts = [geometry['coordinates']] if geometry['type'] == 'Polygon' else geometry['coordinates']
        polygons += len(parts)
        rings += sum(len(part) for part in parts)
        pairs += pair_count(geometry['coordinates'])
    return {'polygonParts': polygons, 'rings': rings, 'coordinatePairs': pairs}


def add_refs(place, refs):
    prior = {(r['layerId'], str(r['featureId'])) for r in place.get('mapRefs', [])}
    primary = (place.get('layerId'), str(place.get('featureId')))
    for ref in refs:
        identity = (ref['layerId'], str(ref['featureId']))
        if identity != primary and identity not in prior:
            place.setdefault('mapRefs', []).append(deepcopy(ref))
            prior.add(identity)


def merge_place(data, record):
    existing = next((p for p in data['places'] if p['id'] == record['id']), None)
    if existing is None:
        data['places'].append(deepcopy(record))
        return
    assert (existing['jurisdiction'], existing['kind'], existing.get('parentId')) == (record['jurisdiction'], record['kind'], record.get('parentId')), record['id']
    # Supplemental geometry does not own people, event history, future maps or
    # existing routes. Preserve those facts while refreshing only owned fields.
    refs = [{'layerId': record['layerId'], 'featureId': record['featureId'], 'boundaryEdition': record['boundaryEdition']}] + record.get('mapRefs', [])
    if (existing.get('layerId'), str(existing.get('featureId'))) != (record['layerId'], str(record['featureId'])):
        add_refs(existing, refs)
    else:
        existing['boundaryEdition'] = record['boundaryEdition']
        add_refs(existing, record.get('mapRefs', []))
    for field in ('sourceWardId', 'sourceLgaId', 'sourceLgaName', 'sourceWardName'):
        if field in record:
            existing[field] = record[field]
    existing['sources'] = unique(existing.get('sources', []) + record.get('sources', []))
    if record.get('layerId') == 'council-sa-official-wards':
        existing['coverageNotes'] = [n for n in existing.get('coverageNotes', []) if n != 'This source snapshot has not been verified as the 2026 council-election boundary edition. No current ward member or previous contestant is inferred from geometry; individual reconciliation remains required.']
    for note in record.get('coverageNotes', []):
        add_note(existing, note)


def references(place, layer_id):
    refs = [{'layerId': place.get('layerId'), 'featureId': place.get('featureId')}] + place.get('mapRefs', [])
    return [str(r['featureId']) for r in refs if r['layerId'] == layer_id]


def merge(data):
    """Mutate the caller's canonical council records; return a source audit."""
    assert data['scope'] == 'councils'
    hashes = {}
    report = {'schemaVersion': 1, 'checked': CHECKED, 'status': 'pass', 'scope': 'Retained ward source integrity, exact geometry delivery, real parent joins and preservation of canonical people/events', 'checks': [], 'limitations': []}
    places = {p['id']: p for p in data['places']}
    assert len(places) == len(data['places']), 'Duplicate input place IDs'
    preserved = {p['id']: (deepcopy(p.get('representatives', [])), deepcopy(p.get('elections', []))) for p in data['places']}
    original_assets = {}

    supplement = read(ROOT / 'content/places/council-ward-supplement.json')
    for source in supplement['sources']:
        source_hash(source, hashes)
        upsert(data['sources'], source)
    raw_lgas = read(ROOT / 'content/places/raw/council-ward-supp-geoscape-lga-attributes.json')
    assert not raw_lgas.get('exceededTransferLimit')
    lgas = {f['attributes']['lga_pid']: f['attributes'] for f in raw_lgas['features']}
    assert len(lgas) == len(raw_lgas['features'])
    for original_layer in supplement['layers']:
        layer = deepcopy(original_layer)
        layer.setdefault('nativeCrs', layer['nativeCRS'])
        upsert(data['layers'], layer)
        path = ROOT / layer['geometryFallbackFile']
        original_assets[path] = sha(path)
        raw = path.read_bytes()
        gzpath = ROOT / layer['geometryFile']
        original_assets[gzpath] = sha(gzpath)
        assert gzip.decompress(gzpath.read_bytes()) == raw, layer['id']
        geo = json.loads(raw)
        source = next(s for s in supplement['sources'] if s['id'] == layer['sourceId'])
        assert sha(ROOT / source['rawFile']) == sha(path), 'Delivered source bytes changed'
        j = layer['jurisdiction']
        ids_path = ROOT / ('content/places/raw/council-ward-supp-geoscape-' + j + '-ids.json')
        ids = read(ids_path)['objectIds']
        assert len(ids) == len(set(ids))
        assert set(ids) == {f['properties']['objectid'] for f in geo['features']}
        assert not geo.get('exceededTransferLimit')
        by_part = {str(f['properties']['wd_ply_pid']): f for f in geo['features']}
        assert len(by_part) == len(geo['features'])
        wards = [p for p in supplement['places'] if p['jurisdiction'] == j]
        parents = set()
        for ward in wards:
            parent = places.get(ward['parentId'])
            assert parent and parent['kind'] == 'council' and parent['jurisdiction'] == j, ward['id']
            identity = lgas[ward['sourceLgaId']]
            assert key(identity['abb_name']) == key(parent['name']), (ward['id'], identity, parent['name'])
            assert identity['state'].lower() == j
            refs = references(ward, layer['id'])
            assert refs and len(refs) == len(set(refs)), ward['id']
            for feature_id in refs:
                prop = by_part[feature_id]['properties']
                assert (prop['ward_pid'], prop['lga_pid'], prop['ward_name'], prop['state'].lower()) == (ward['sourceWardId'], ward['sourceLgaId'], ward['name'], j)
                assert not re.search(r'undivided|unsubdivided|no wards|not applicable', prop['ward_name'], re.I), prop
            merge_place(data, ward)
            parent['sources'] = unique(parent.get('sources', []) + [layer['sourceId'], 'council-ward-supp-geoscape-lga-attributes'])
            add_note(parent, 'The Digital Atlas/Geoscape ward layer retains every original polygon part. Its live item says August 2026 while the service description says November 2025; later amendments and individual ward representation require separate reconciliation.')
            parents.add(parent['id'])
        joined = [ref for p in data['places'] for ref in references(p, layer['id'])]
        assert Counter(joined) == Counter(by_part.keys()), (layer['id'], 'Unreferenced or duplicate original polygon parts')
        report['checks'].append({'jurisdiction': j, 'realWards': len(wards), 'parentCouncils': len(parents), 'sourceFeatures': len(geo['features']), **geometry_counts(geo['features']), 'allObjectIdsAndPartsJoinedOnce': True, 'deliveryBytesEqualSource': True, 'gzipRoundTripExactBytes': True, 'sourceAndDeliverySha256': sha(path), 'nativeCRS': 'EPSG:4283'})

    sa = read(ROOT / 'content/places/sources/council-sa-ward-supplement.json')
    review = read(SA_REVIEW)
    source_hash(sa['source'], hashes)
    upsert(data['sources'], sa['source'])
    for request in sa['requests']:
        source_hash(request, hashes)
    # Register original catalogue, object inventory and paginated feature hashes,
    # so the normal national --source-hashes check covers the actual geometry.
    for index, request in enumerate(sa['requests']):
        sid = 'council-sa-ward-original-' + str(index)
        upsert(data['sources'], {'id': sid, 'title': 'Location SA ward retained original: ' + Path(request['rawFile']).name, 'checked': sa['checked'], 'url': request['url'], 'rawFile': request['rawFile'], 'sha256': request['sha256'], 'licence': sa['source']['licence'], 'licenceUrl': sa['source']['licenceUrl']})
    review_sid = 'council-sa-ward-edition-review'
    upsert(data['sources'], {'id': review_sid, 'title': 'Primary web review: Grant identity and SA council ward edition changes', 'url': review['reviewSummary']['sourceUrl'], 'checked': review['checked'], 'rawFile': SA_REVIEW.relative_to(ROOT).as_posix(), 'sha256': sha(SA_REVIEW), 'verificationMethod': review['method']})
    hashes[SA_REVIEW.relative_to(ROOT).as_posix()] = sha(SA_REVIEW)
    layer = deepcopy(sa['layer'])
    layer.update(featureNameField='ward', boundaryEdition=SA_EDITION, name='South Australia preceding ward structure and APY context (Location SA snapshot)', coordinateNote='Exact GeoJSON coordinates returned by the official service in EPSG:4326. Native service CRS is EPSG:3857; the service transformation is declared, not a claim of native longitude/latitude. No rounding, union, clipping or simplification. Upcoming representation-review boundaries are separate and not supplied by this snapshot.')
    upsert(data['layers'], layer)
    path = ROOT / layer['geometryFile']
    original_assets[path] = sha(path)
    geo = read(path)
    originals = []
    for request in sa['requests']:
        if Path(request['rawFile']).name.startswith('features-'):
            page = read(ROOT / request['rawFile'])
            assert not page.get('exceededTransferLimit')
            originals.extend(page['features'])
    assert geo['features'] == originals, 'SA source properties, polygon parts, rings or coordinates changed'
    ids = read(ROOT / 'content/places/raw/sa-ward-geometry/ids.json')['objectIds']
    assert len(ids) == len(set(ids)) == sa['sourceFeatureCount']
    assert len(geo['features']) == len(ids) == 140
    assert set(ids) == {f['properties'][layer['featureIdField']] for f in geo['features']}
    assert len({f['properties'][layer['featureIdField']] for f in geo['features']}) == len(ids)

    # Source-only identifiers are not an ABS code. Explicit reviewed identity
    # exceptions prevent fuzzy joins and preserve the original Grant route.
    identity_exceptions = {'SOUTHERN LIMESTONE COAST': 'sa-council-42250', 'APY': 'sa-council-40250'}
    parents_by_name = {}
    for p in data['places']:
        if p['jurisdiction'] == 'sa' and p['kind'] == 'council':
            name = re.sub(r'\s*\(SA\)$', '', p['name'], flags=re.I)
            assert key(name) not in parents_by_name
            parents_by_name[key(name)] = p
    renamed = places[review['identity']['placeId']]
    assert renamed['name'] in ('Grant', 'Southern Limestone Coast', 'Southern Limestone Coast Council'), renamed['name']
    renamed['aliases'] = unique(renamed.get('aliases', []) + ['Grant', 'District Council of Grant', 'Southern Limestone Coast Council'])
    renamed['name'] = review['identity']['currentName']
    renamed['sources'] = unique(renamed.get('sources', []) + [review_sid])
    renamed['nameChange'] = {'previousName': review['identity']['previousName'], 'effectiveDate': review['identity']['entityNameFrom'], 'sourceUrl': review['identity']['sourceUrl'], 'sourceId': review_sid, 'stableIdAndPreviousRouteRetained': True}
    add_note(renamed, 'The same council is now Southern Limestone Coast (ABN Lookup name from 1 July 2026; ECSA corroboration). Its stable ID and Grant URL retain existing inbound routes and histories.')

    by_parent = defaultdict(list)
    for feature in geo['features']:
        prop = feature['properties']
        source_name = prop['abbname']
        parent = places.get(identity_exceptions.get(source_name)) if source_name in identity_exceptions else parents_by_name.get(key(source_name))
        assert parent and parent['jurisdiction'] == 'sa', ('Unresolved SA parent identity', prop)
        assert parent['kind'] == ('special-local-body' if source_name == 'APY' else 'council'), prop
        by_parent[parent['id']].append(feature)
        ref = {'layerId': layer['id'], 'featureId': str(prop[layer['featureIdField']]), 'boundaryEdition': SA_EDITION}
        parent['sources'] = unique(parent.get('sources', []) + [sa['source']['id'], review_sid])
        if source_name == 'APY':
            ref['contextOnly'] = True
            add_refs(parent, [ref])
            add_note(parent, review['apy'])
            continue
        assert re.search(r'\bWARD\b', prop['ward'], re.I), ('Non-ward placeholder must be parent context', prop)
        pid = 'sa-ward-' + parent['id'].removeprefix('sa-council-') + '-' + slug(prop['ward'])
        name = ' '.join(prop['ward'].split()).title()
        notes = ['Official Location SA ward source feature; original geometry, multipart components, holes and coordinates retained. Source ward and parent labels are retained separately from the normalized display name.', 'This source snapshot has not been verified as the next periodic council-election boundary edition. No current ward member or previous contestant is inferred from geometry; individual reconciliation remains required.']
        if source_name in review['reviewSummary']['wardChanges']:
            note = 'The 2024/2025 representation review changes this council for the next periodic election: ' + review['reviewSummary']['wardChanges'][source_name] + '. This page preserves the preceding source ward, and must not be used as the upcoming-election ward map. See the linked ECSA review/gazette source; new geometry and successor joins remain unresolved.'
            notes.append(note)
            add_note(parent, note)
            gazette = next((g for g in review['gazettes'] if g['council'] == source_name), None)
            if gazette:
                exact_note = gazette['effect'] + ' Gazette ' + gazette['date'] + ', p. ' + gazette['page'] + '; ' + gazette['sourceUrl']
                notes.append(exact_note)
                add_note(parent, exact_note)
        record = {'id': pid, 'name': name, 'slug': slug(parent['name']) + '-' + slug(prop['ward']), 'jurisdiction': 'sa', 'kind': 'ward', 'parentId': parent['id'], 'layerId': layer['id'], 'featureId': ref['featureId'], 'officialUrl': parent['officialUrl'], 'sources': [sa['source']['id'], review_sid] + ['council-sa-ward-original-' + str(i) for i in (2, 3, 4)], 'boundaryEdition': SA_EDITION, 'sourceWardId': str(prop[layer['featureIdField']]), 'sourceWardName': prop['ward'], 'sourceLgaName': source_name, 'representatives': [], 'elections': [], 'coverageNotes': notes}
        merge_place(data, record)
    all_refs = [ref for p in data['places'] for ref in references(p, layer['id'])]
    expected = Counter(str(i) for i in ids)
    assert Counter(all_refs) == expected, 'SA original parts must be joined exactly once'
    sa_wards = [p for p in data['places'] if p['kind'] == 'ward' and p.get('layerId') == layer['id']]
    assert len(sa_wards) == 133
    assert len(references(places['sa-council-40250'], layer['id'])) == 7
    assert all(p.get('parentId') != 'sa-council-40250' for p in data['places']), 'APY is not an ordinary council ward hierarchy'
    report['checks'].append({'jurisdiction': 'sa', 'realWards': len(sa_wards), 'parentCouncils': len(by_parent) - 1, 'specialBodyParentContexts': 1, 'specialBodySourceFeatures': 7, 'sourceFeatures': len(geo['features']), **geometry_counts(geo['features']), 'allObjectIdsAndPartsJoinedOnce': True, 'allSourceFeaturesPropertiesAndCoordinatesEqual': True, 'deliverySha256': sha(path), 'sourceCRS': 'EPSG:3857', 'officialServiceResponseCRS': 'EPSG:4326', 'identityExceptions': identity_exceptions})
    assert len(data['places']) == len({p['id'] for p in data['places']})
    final = {p['id']: p for p in data['places']}
    for pid, (people, events) in preserved.items():
        assert final[pid].get('representatives', []) == people and final[pid].get('elections', []) == events, ('Canonical people/events altered', pid)
    for asset, digest in original_assets.items():
        assert sha(asset) == digest, ('Original asset changed', str(asset))
    report['originalSourceHashes'] = dict(sorted(hashes.items()))
    report['allOriginalMapAssetsUnchanged'] = True
    report['existingCanonicalPeopleAndEventsUnchanged'] = True
    report['limitations'] = ['Geometry integration alone does not establish complete current ward members or previous ballots.', 'NT/WA item/service currency disagreement remains explicit. No restrictive Landgate source is imported.', 'SA preceding ward editions remain separate from next-election representation reviews; upcoming geometry/successor joins are not fabricated.', 'Seven APY statutory electoral features are parent-only geographic context, without ordinary council wards or election assumptions.', 'NSW ward coverage remains incomplete. Retained Western Parkland source requires edition reconciliation, Ballina KML remains unparsed/unreviewed, North Sydney prohibits reproduction without permission and NSW ward proxy services required unavailable tokens. None are delivered by this adapter.', 'This local source/join verification does not certify generated pages, map picking, browser behaviour, accessibility, discovery, contracts or publication.']
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write councils.json after all checks; default checks a copy only')
    args = parser.parse_args()
    data = read(OUT)
    report = merge(data)
    once = deepcopy(data)
    assert merge(data) == report and data == once, 'Ward merge is not deterministic/idempotent'
    report['deterministicSecondMergeIdentical'] = True
    if args.write:
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report['canonicalWritten'] = args.write
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'canonicalWritten': args.write, 'placesAfterMerge': len(data['places']), 'checks': report['checks'], 'report': REPORT.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == '__main__':
    main()
