#!/usr/bin/env python3
"""Verify national place records and generated navigation without network access.

This is a structural/data/link check, not browser, political fact or legal
review. Missing people/contestants are counted as coverage gaps, not silently
treated as complete. --skip-pages is provisional acquisition validation only.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
import gzip
import hashlib
import html
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit
from national_evidence import collect_fingerprints
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:
    ZoneInfo = None

ROOT = Path(__file__).resolve().parents[1]
CHECKED = datetime.now(timezone(timedelta(hours=10))).date().isoformat()
SCOPES = ('councils', 'state', 'federal')
JURISDICTIONS = ('act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa')
KNOWN_ZONES = {'Australia/Brisbane', 'Australia/Sydney', 'Australia/Melbourne',
               'Australia/Adelaide', 'Australia/Perth', 'Australia/Darwin',
               'Australia/Hobart', 'Australia/Lord_Howe', 'Australia/Eucla',
               'Indian/Christmas', 'Indian/Cocos', 'Pacific/Norfolk'}

def css_urls(text):
    """Read whole quoted CSS URLs so data payloads do not invent nested assets."""
    pattern = r'''url\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|([^)'"\s][^)]*?))\s*\)'''
    for match in re.finditer(pattern, text, re.I):
        yield next(value for value in match.groups() if value is not None).strip()


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicate_ids = []
        self.links = []
        self.title_count = self.h1_count = self.map_count = self.crumb_count = self.choice_count = 0
        self.title_text = []
        self.h1_text = []
        self.configs = []
        self.inline_styles = []
        self._title = self._h1 = False
        self._config = None
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        identity = a.get('id') or (a.get('name') if tag == 'a' else None)
        if identity:
            if identity in self.ids:
                self.duplicate_ids.append(identity)
            self.ids.add(identity)
        if tag == 'title':
            self.title_count += 1
            self._title = True
        if tag == 'h1':
            self.h1_count += 1
            self._h1 = True
        if 'data-civic-map' in a:
            self.map_count += 1
        classes = (a.get('class') or '').split()
        self.crumb_count += 'civic-crumbs' in classes
        self.choice_count += tag == 'nav' and 'civic-choices' in classes
        if tag == 'script' and a.get('id') == 'civic-map-config':
            self._config = []
        for key in ('href', 'src', 'poster', 'data-src'):
            if a.get(key):
                self.links.append((tag, key, a[key]))
        if a.get('srcset') and not a['srcset'].startswith('data:'):
            self.links.extend((tag, 'srcset', item.strip().split()[0]) for item in a['srcset'].split(',') if item.strip())
        if a.get('style'):
            self.inline_styles.append(a['style'])

    def handle_endtag(self, tag):
        if tag == 'title':
            self._title = False
        elif tag == 'h1':
            self._h1 = False
        elif tag == 'script' and self._config is not None:
            self.configs.append(''.join(self._config))
            self._config = None

    def handle_data(self, value):
        if self._title:
            self.title_text.append(value)
        if self._h1:
            self.h1_text.append(value)
        if self._config is not None:
            self._config.append(value)


class Validator:
    def __init__(self, skip_pages=False, source_hashes=False, no_write=False):
        self.skip_pages = skip_pages
        self.no_write = no_write
        self.source_hashes = source_hashes
        self.errors = []
        self.warnings = []
        self.counts = Counter()
        self.gaps = defaultdict(Counter)
        self.inputs = {}
        self.sources = {}
        retention = json.loads((ROOT / 'content/places/source-retention.json').read_text(encoding='utf-8'))
        self.local_source_prefixes = tuple(retention.get('localOnlyPathPrefixes', []))
        self.layers = {}
        self.places = {}
        self.registry_places = {}
        self.registry_layers = {}
        self.geometry_ids = {}
        self.geometry_types = {}
        self.documents = {}
        self.anchor_cache = {}
        self.files = set()
        self.casefold_files = {}
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.venv', '__pycache__')]
            for name in files:
                path = (Path(base) / name).relative_to(ROOT).as_posix()
                self.files.add(path)
                self.casefold_files[path.casefold()] = path

    def check(self, condition, message):
        self.counts['assertions'] += 1
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def read_json(self, path, required=True):
        try:
            return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
        except (OSError, ValueError) as exc:
            if required:
                self.errors.append(f'{path}: unavailable/invalid JSON: {exc}')
            return None

    def iso_date(self, value, context, allow_future=True):
        if not isinstance(value, str):
            self.check(False, f'{context}: missing ISO date')
            return False
        try:
            parsed = date.fromisoformat(value)
            self.check(parsed.isoformat() == value, f'{context}: date must be YYYY-MM-DD')
            if not allow_future:
                self.check(value <= CHECKED, f'{context}: checked date is later than review date {CHECKED}')
            return True
        except ValueError:
            return self.check(False, f'{context}: invalid date {value!r}')

    def web_url(self, value, context):
        parsed = urlsplit(value) if isinstance(value, str) else None
        return self.check(bool(parsed and parsed.scheme in ('https', 'http') and parsed.netloc), f'{context}: missing/invalid public source URL')

    def load_records(self):
        all_ids = []
        for scope in SCOPES:
            file = f'content/places/{scope}.json'
            data = self.read_json(file)
            if data is None:
                continue
            self.inputs[scope] = data
            self.check(data.get('schemaVersion') == 1, f'{file}: unsupported schemaVersion')
            self.check(data.get('scope') == scope, f'{file}: scope mismatch')
            self.iso_date(data.get('checked'), file + ' checked', False)
            for source in data.get('sources', []):
                key = source.get('id')
                if key in self.sources:
                    self.check(self.sources[key] == source, f'Different sources share ID {key}')
                self.sources[key] = source
            for layer in data.get('layers', []):
                key = layer.get('id')
                self.check(key and key not in self.layers, f'Duplicate/missing layer ID {key}')
                self.layers[key] = layer
            for place in data.get('places', []):
                key = place.get('id')
                all_ids.append(key)
                self.places[key] = {**place, 'scope': scope}
                self.counts[f'{scope}_places'] += 1
        self.check(len(all_ids) == len(set(all_ids)), 'Duplicate stable place identities across canonical inputs')
        self.counts['canonical_places'] = len(all_ids)
        for key, source in self.sources.items():
            self.check(bool(key), 'Source has no stable ID')
            self.web_url(source.get('url'), f'Source {key}')
            if source.get('checked'):
                self.iso_date(source['checked'], f'Source {key} checked', False)
            else:
                self.warnings.append(f'Source {key} does not carry a checked date')
            raw = source.get('rawFile')
            if raw:
                if raw.startswith(self.local_source_prefixes) and not (ROOT / raw).is_file():
                    self.counts['local_only_source_snapshots_absent'] += 1
                    self.warnings.append(f'Source {key}: original research snapshot is local-only and absent; public manifest retains URL/hash, not a fresh source check')
                    continue
                self.exact_file(raw, f'Source {key} retained original')
                if self.source_hashes and source.get('sha256') and (ROOT / raw).is_file():
                    actual = hashlib.sha256((ROOT / raw).read_bytes()).hexdigest()
                    self.check(actual == source['sha256'], f'Source {key} retained bytes differ from SHA-256')
                    self.counts['source_hashes_checked'] += 1
        self.counts['sources'] = len(self.sources)

    def records(self):
        for key, layer in self.layers.items():
            if layer.get('sourceId'):
                self.check(layer['sourceId'] in self.sources, f'Layer {key}: unresolved sourceId {layer["sourceId"]}')
            else:
                self.check(False, f'Layer {key}: missing sourceId')
            self.check(layer.get('crs') in ('EPSG:4326', 'EPSG:4283'), f'Layer {key}: delivered CRS must be geographic EPSG4326/4283')
            self.check(bool(layer.get('boundaryEdition')), f'Layer {key}: missing boundary edition')
            self.check(bool(layer.get('featureIdField')), f'Layer {key}: missing feature ID field')
        for key, place in self.places.items():
            scope = place['scope']
            self.check(bool(place.get('name')) and bool(place.get('kind')), f'Place {key}: missing name/kind')
            if place.get('officialUrl'):
                self.web_url(place['officialUrl'], f'Place {key} official URL')
            for ref in place.get('sources', []):
                if isinstance(ref, str):
                    self.check(ref in self.sources, f'Place {key}: unresolved source reference {ref}')
                elif isinstance(ref, dict):
                    self.web_url(ref.get('url'), f'Place {key} embedded source')
                else:
                    self.check(False, f'Place {key}: invalid source reference')
            for relationship in ('parentId', 'predecessorPlaceId', 'successorPlaceId'):
                if place.get(relationship):
                    self.check(place[relationship] in self.places, f'Place {key}: unresolved {relationship} {place[relationship]}')
            reps = place.get('representatives', [])
            if place.get('status') == 'historical':
                self.check(not reps, f'Place {key}: historical-only boundary record must not acquire current representatives')
                self.counts['historical_only_place_records'] += 1
            if not reps and place.get('status') != 'historical' and place.get('kind') not in ('unincorporated-area', 'special-local-body') and place.get('representationStatus') != 'next-election-division':
                self.gaps[scope]['places_without_individual_current_office_records'] += 1
            for person in reps:
                self.counts['current_representative_records'] += 1
                self.check(bool(person.get('name')), f'Place {key}: current person has no name')
                vacancy = any(w in str(person.get('status', '')).lower() for w in ('vacant', 'vacancy'))
                if not vacancy:
                    self.web_url(person.get('profileUrl') or person.get('officialUrl'), f'Place {key} current person {person.get("name")} profile')
                if person.get('website'):
                    self.web_url(person['website'], f'Place {key} current person website')
                source_id = person.get('sourceId')
                self.check(bool(source_id and source_id in self.sources), f'Place {key} current person {person.get("name")}: unresolved/missing sourceId')
                checked = person.get('checked') or self.sources.get(source_id, {}).get('checked')
                self.iso_date(checked, f'Place {key} person {person.get("name")} checked', False)
            events = place.get('elections', [])
            electoral_place = place.get('kind') not in ('unincorporated-area', 'special-local-body')
            if not events and electoral_place:
                self.gaps[scope]['places_without_event_records'] += 1
            event_ids = []
            historic_rosters = 0
            for event in events:
                event_id = event.get('id')
                event_ids.append(event_id)
                self.check(bool(event_id), f'Place {key}: event missing stable ID')
                self.check(bool(event.get('kind')) and bool(event.get('status')), f'Place {key} event {event_id}: missing kind/status')
                self.check(bool(event.get('dateBasis')), f'Place {key} event {event_id}: missing date basis')
                zone = event.get('timezone')
                zone_ok = isinstance(zone, str) and zone in KNOWN_ZONES
                if ZoneInfo is not None and isinstance(zone, str):
                    try:
                        ZoneInfo(zone)
                        zone_ok = True
                    except (ZoneInfoNotFoundError, ValueError):
                        pass
                self.check(zone_ok, f'Place {key} event {event_id}: invalid/unverified IANA timezone {zone!r}')
                url = event.get('sourceUrl') or event.get('resultsUrl')
                self.web_url(url, f'Place {key} event {event_id}')
                poll_date = event.get('date')
                if poll_date is not None:
                    self.iso_date(poll_date, f'Place {key} event {event_id} polling date')
                if event.get('dateTime') is not None:
                    try:
                        deadline = datetime.fromisoformat(event['dateTime'].replace('Z', '+00:00'))
                        self.check(deadline.tzinfo is not None, f'Place {key} event {event_id}: exact deadline requires UTC offset')
                        self.check(event['dateTime'][:10] == poll_date, f'Place {key} event {event_id}: deadline and local date differ')
                        if deadline.tzinfo is not None and ZoneInfo is not None and zone_ok:
                            try:
                                local = deadline.astimezone(ZoneInfo(zone))
                                self.check(local.utcoffset() == deadline.utcoffset() and local.date().isoformat() == poll_date, f'Place {key} event {event_id}: deadline offset/date disagrees with event timezone')
                            except ZoneInfoNotFoundError:
                                pass
                    except (TypeError, ValueError):
                        self.check(False, f'Place {key} event {event_id}: invalid exact deadline')
                unsupported = re.search(r'\b(estimated?|unverified|unknown|unannounced)\b|not (?:yet )?announced|to be determined', str(event.get('dateBasis', '')).lower())
                if unsupported or event.get('status') in ('date-unannounced', 'unknown', 'unannounced', 'cancelled', 'postponed'):
                    self.check(poll_date is None, f'Place {key} event {event_id}: unsupported exact polling-date timer')
                candidates = event.get('candidates', [])
                self.check(isinstance(candidates, list), f'Place {key} event {event_id}: contestants must be a list')
                if not isinstance(candidates, list):
                    continue
                if poll_date and poll_date <= CHECKED:
                    historic_rosters += bool(candidates)
                    if not candidates:
                        self.gaps[scope]['historical_events_without_individual_contestants'] += 1
                self.counts['election_events'] += 1
                self.counts['contestant_records'] += len(candidates)
                candidate_ids = [c['id'] for c in candidates if c.get('id')]
                self.check(len(candidate_ids) == len(set(candidate_ids)), f'Place {key} event {event_id}: duplicate candidate IDs')
                for candidate in candidates:
                    self.check(bool(candidate.get('name')) and bool(candidate.get('status') or candidate.get('result')), f'Place {key} event {event_id}: contestant missing name/event stage')
                    self.web_url(candidate.get('sourceUrl') or url, f'Place {key} contestant {candidate.get("name")} original record')
                    if candidate.get('profileUrl'):
                        self.web_url(candidate['profileUrl'], f'Place {key} contestant public profile')
                    if candidate.get('sourceId'):
                        self.check(candidate['sourceId'] in self.sources, f'Place {key} contestant {candidate.get("name")}: unresolved sourceId')
                    if candidate.get('votes') is not None:
                        value = candidate['votes']
                        self.check(isinstance(value, (int, float)) and math.isfinite(value) and value >= 0, f'Place {key} contestant {candidate.get("name")}: invalid recorded vote count')
                        self.check(bool(candidate.get('voteMeasure')), f'Place {key} contestant {candidate.get("name")}: missing vote measure')
            self.check(len(event_ids) == len(set(event_ids)), f'Place {key}: duplicate event identities')
            if not historic_rosters and electoral_place and place.get('representationStatus') != 'next-election-division':
                self.gaps[scope]['places_without_individual_historical_contestants'] += 1

    def exact_file(self, path, context):
        path = posixpath.normpath(str(path).replace('\\', '/'))
        if path in self.files:
            return True
        actual = self.casefold_files.get(path.casefold())
        return self.check(False, f'{context}: ' + (f'filename case mismatch {path!r}; actual {actual!r}' if actual else f'missing local file {path!r}'))

    def load_registry(self):
        registry = self.read_json('content/places/route-registry.json', required=not self.skip_pages)
        if registry:
            rows = registry.get('places', [])
            ids = [p.get('id') for p in rows]
            routes = [p.get('url') for p in rows]
            self.check(len(ids) == len(set(ids)), 'Route registry has duplicate place IDs')
            self.check(len(routes) == len(set(routes)), 'Route registry has duplicate public routes')
            self.registry_places = {p['id']: p for p in rows}
            self.registry_layers = {l['id']: l for l in registry.get('layers', [])}
            self.check(len(self.registry_layers) == len(registry.get('layers', [])), 'Route registry has duplicate layer IDs')
            expected = {key for key, p in self.places.items() if p.get('jurisdiction') in JURISDICTIONS}
            self.check(expected == set(self.registry_places), 'Route registry does not match canonical supported-jurisdiction places')
            for key, row in self.registry_places.items():
                canonical = self.places.get(key)
                if not canonical:
                    continue
                for field in ('id', 'name', 'jurisdiction', 'kind', 'scope', 'parentId', 'boundaryEdition'):
                    self.check(row.get(field) == canonical.get(field), f'Registry place {key}: stale canonical {field}')
                if canonical.get('layerId'):
                    for field in ('layerId', 'featureId'):
                        self.check(row.get(field) == canonical.get(field), f'Registry place {key}: stale canonical {field}')
                elif canonical.get('kind') in ('senate-area', 'statewide-upper-house'):
                    code = {'nsw':'1','vic':'2','qld':'3','sa':'4','wa':'5','tas':'6','nt':'7','act':'8'}[canonical['jurisdiction']]
                    self.check(row.get('layerId') == 'context-'+canonical['kind']+'-'+canonical['jurisdiction'] and str(row.get('featureId')) == code,
                               f'Registry place {key}: whole-jurisdiction context identity differs')
            for key, canonical in self.layers.items():
                generated = self.registry_layers.get(key)
                if not self.check(generated is not None, f'Canonical layer {key}: absent from generated registry'):
                    continue
                for field, value in canonical.items():
                    if field not in ('geometryFile', 'compressedFile'):
                        self.check(generated.get(field) == value, f'Registry layer {key}: stale canonical {field}')
                original = canonical.get('geometryFile')
                self.check(generated.get('geometryFile') in (original, original[:-3] if original and original.endswith('.gz') else original),
                           f'Registry layer {key}: unexpected replacement geometry path')
            self.counts['registered_routes'] = len(routes)

    def geometry(self):
        delivery = self.read_json('content/places/geometry-delivery.json', required=not self.skip_pages)
        deliveries = {r['id']: r for r in delivery.get('layers', [])} if delivery else {}
        # Generated delivery fields may supplement canonical metadata, never
        # override the source edition/CRS/identity under validation.
        effective = dict(self.registry_layers)
        for key, canonical in self.layers.items():
            effective[key] = {**canonical, 'compressedFile': self.registry_layers.get(key, {}).get('compressedFile') or canonical.get('compressedFile')}
        refs = defaultdict(set)
        for place in list(self.places.values()) + list(self.registry_places.values()):
            if place.get('layerId'):
                refs[place['layerId']].add(str(place.get('featureId')))
            for ref in place.get('mapRefs', []):
                refs[ref['layerId']].add(str(ref.get('featureId')))
        for key, layer in effective.items():
            filename = layer.get('geometryFile')
            if not filename or not self.exact_file(filename, f'Layer {key} geometry'):
                continue
            raw = (ROOT / filename).read_bytes()
            if filename.endswith('.gz'):
                raw = gzip.decompress(raw)
            generated_file = self.registry_layers.get(key, {}).get('geometryFile')
            if key in self.layers and generated_file and generated_file != filename and self.exact_file(generated_file, f'Layer {key} generated fallback'):
                fallback = (ROOT / generated_file).read_bytes()
                if generated_file.endswith('.gz'):
                    fallback = gzip.decompress(fallback)
                self.check(fallback == raw, f'Layer {key}: generated fallback differs from canonical original bytes')
                self.counts['canonical_delivery_byte_comparisons'] += 1
            compressed = layer.get('compressedFile') or deliveries.get(key, {}).get('compressed')
            if compressed and self.exact_file(compressed, f'Layer {key} gzip'):
                self.check(gzip.decompress((ROOT / compressed).read_bytes()) == raw, f'Layer {key}: gzip changes exact source JSON bytes')
                self.counts['gzip_byte_round_trips'] += 1
            try:
                data = json.loads(raw)
            except ValueError as exc:
                self.check(False, f'Layer {key}: invalid GeoJSON {exc}')
                continue
            self.check(data.get('type') == 'FeatureCollection', f'Layer {key}: not a FeatureCollection')
            features = data.get('features', [])
            field = layer.get('featureIdField')
            identities = [str(f.get('properties', {}).get(field, f.get('id'))) for f in features]
            self.check(len(identities) == len(set(identities)), f'Layer {key}: duplicate feature identities')
            self.check('None' not in identities, f'Layer {key}: missing feature identity')
            self.geometry_ids[key] = set(identities)
            self.check(refs[key] <= set(identities), f'Layer {key}: place feature join(s) absent from geometry: {sorted(refs[key] - set(identities))[:10]}')
            unsupported = [f.get('geometry', {}).get('type') if f.get('geometry') else None for f in features if not f.get('geometry') or f['geometry'].get('type') not in ('Polygon', 'MultiPolygon')]
            self.check(not unsupported, f'Layer {key}: unsupported/missing polygon geometry {unsupported[:3]}')
            row = deliveries.get(key)
            if row:
                self.check(hashlib.sha256(raw).hexdigest() == row.get('sha256'), f'Layer {key}: delivery SHA-256 differs')
                self.check(len(features) == row.get('features'), f'Layer {key}: delivery feature count differs')
            elif not self.skip_pages:
                self.check(False, f'Layer {key}: missing generated geometry-delivery entry')
            if layer.get('uncompressedSha256'):
                self.check(hashlib.sha256(raw).hexdigest() == layer['uncompressedSha256'], f'Layer {key}: adapter uncompressed hash differs')
            self.counts['geometry_layers'] += 1
            self.counts['geometry_features_including_editions'] += len(features)
        for key in refs:
            self.check(key in effective, f'Place map reference uses unknown layer {key}')

    def get_document(self, path):
        if path not in self.documents:
            self.documents[path] = Document((ROOT / path).read_text(encoding='utf-8-sig'))
        return self.documents[path]

    def local_target(self, page, url):
        parsed = urlsplit(url)
        if parsed.scheme and parsed.scheme not in ('https', 'http'):
            return None
        if parsed.netloc and parsed.netloc.lower() not in ('p4a.xyz', 'www.p4a.xyz'):
            return None
        path = unquote(parsed.path).replace('\\', '/')
        if not path:
            target = page
        elif path.startswith('/'):
            target = path.lstrip('/')
        else:
            target = posixpath.join(posixpath.dirname(page), path)
        target = posixpath.normpath(target)
        if target == '.' or path.endswith('/'):
            target = posixpath.join(target if target != '.' else '', 'index.html')
        return target, unquote(parsed.fragment)

    def local_link(self, page, url, context):
        resolved = self.local_target(page, url)
        if resolved is None:
            self.counts['external_link_references_not_fetched'] += 1
            return
        target, fragment = resolved
        self.counts['local_link_references'] += 1
        if not self.check(not target.startswith('../') and not posixpath.isabs(target), f'{page}: local link escapes site root: {url}'):
            return
        if not self.exact_file(target, f'{page} {context} {url}'):
            return
        if fragment and target.lower().endswith(('.html', '.htm')):
            if target not in self.anchor_cache:
                self.anchor_cache[target] = self.get_document(target).ids
            self.check(fragment in self.anchor_cache[target], f'{page}: missing fragment #{fragment} in {target}')
            self.counts['fragment_references_checked'] += 1

    def validate_config(self, page, raw):
        try:
            config = json.loads(raw)
        except ValueError as exc:
            self.check(False, f'{page}: invalid map JSON {exc}')
            return
        layers = {l['id']: l for l in config.get('layers', [])}
        self.check(len(layers) == len(config.get('layers', [])), f'{page}: duplicate map-config layers')
        seen = set()
        joins = defaultdict(set)
        for place in config.get('places', []):
            for identity in place.get('featureIds', [place.get('featureId')]):
                key = (place.get('layerId'), str(identity))
                self.check(key not in seen, f'{page}: repeated map feature/page join {key}')
                seen.add(key)
                joins[key[0]].add(key[1])
                self.check(key[0] in layers, f'{page}: map record uses absent layer {key[0]}')
                self.check(key[1] in self.geometry_ids.get(key[0], set()), f'{page}: selectable record absent from geometry {key}')
            registered = self.registry_places.get(place.get('id'))
            self.check(registered is not None and place.get('url') == registered.get('url'), f'{page}: map Open route does not match route registry for {place.get("id")}')
        if not config.get('filterGeometry'):
            for layer_id in layers:
                missing = self.geometry_ids.get(layer_id, set()) - joins[layer_id]
                self.check(not missing, f'{page}: visible polygon(s) cannot be inspected/opened in layer {layer_id}: {sorted(missing)[:8]}')
        basemap = config.get('basemap', {})
        if basemap.get('image'):
            self.exact_file(basemap['image'], page + ' geographic raster')
        self.check(bool(basemap.get('extent')), page + ': missing returned geographic raster extent')
        self.counts['map_configs_checked'] += 1

    def pages(self):
        if self.skip_pages:
            self.warnings.append('Page/navigation validation skipped: this is provisional acquisition validation, not final structural acceptance.')
            return
        targets = {p['url'] for p in self.registry_places.values()}
        targets.add('pages/places.html')
        for state in JURISDICTIONS:
            targets.add(f'states/{state}/places/index.html')
            for scope in SCOPES:
                targets.add(f'states/{state}/places/{scope}/index.html')
        by_route = {p['url']: self.places.get(p['id'], p) for p in self.registry_places.values()}
        css_files = set()
        for page in sorted(targets):
            if not self.exact_file(page, 'Generated page'):
                continue
            doc = self.get_document(page)
            self.check(doc.title_count == 1 and bool(''.join(doc.title_text).strip()), f'{page}: requires one meaningful title')
            self.check(doc.h1_count == 1 and bool(''.join(doc.h1_text).strip()), f'{page}: requires one meaningful h1')
            self.check(doc.choice_count >= 1, f'{page}: missing navigation choices')
            if page != 'pages/places.html':
                self.check(doc.crumb_count >= 1, f'{page}: missing place breadcrumbs')
            self.check(not doc.duplicate_ids, f'{page}: duplicate fragment IDs {doc.duplicate_ids[:8]}')
            self.check(len(doc.configs) == doc.map_count and doc.map_count <= 1, f'{page}: map config and exactly-one-primary-map contract differs')
            place = by_route.get(page)
            if place:
                if place.get('layerId') and place['layerId'] in self.geometry_ids:
                    self.check(doc.map_count == 1, f'{page}: sourced mapped place lacks primary interactive map')
                elif doc.map_count == 0:
                    self.gaps[place.get('scope', 'unknown')]['place_pages_without_map_context'] += 1
                self.check(place.get('name', '').casefold() in ''.join(doc.h1_text).casefold(), f'{page}: h1 does not identify its place')
                self.rendered_records(page, place, doc)
            for raw in doc.configs:
                self.validate_config(page, raw)
            doc.configs.clear()
            for tag, attribute, url in doc.links:
                self.local_link(page, url, f'{tag}.{attribute}')
                resolved = self.local_target(page, url)
                if resolved and resolved[0].endswith('.css') and resolved[0] in self.files:
                    css_files.add(resolved[0])
            for style in doc.inline_styles:
                for url in css_urls(style):
                    self.local_link(page, url.strip(), 'inline style asset')
            self.counts['generated_pages_checked'] += 1
        for css in css_files:
            text = (ROOT / css).read_text(encoding='utf-8-sig')
            for url in css_urls(text):
                self.local_link(css, url.strip(), 'stylesheet asset')
        self.counts['stylesheets_checked'] = len(css_files)

    def rendered_records(self, page, place, doc):
        """Check canonical people/event rows in the controlled generated markup.

        This is output parity, not a fresh verification of the political facts.
        Scope each comparison to its own people section or event article so a
        neighbour's directory entry cannot stand in for a missing person/ballot.
        """
        markup = (ROOT / page).read_text(encoding='utf-8-sig')
        plain = lambda value: ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', value)).split())
        people = re.search(r'<section\b[^>]*\bid="people"[^>]*>(.*?)</section>', markup, re.S)
        self.check(people is not None, f'{page}: missing dedicated representation section')
        if people:
            body = people[1]
            reps = [p for p in place.get('representatives', []) if p.get('name')]
            self.check(body.count('civic-person') == len(reps), f'{page}: rendered current-role card count differs from canonical records')
            text = plain(body)
            for person in reps:
                self.check(' '.join(person['name'].split()) in text, f'{page}: current-role name omitted from representation section: {person["name"]}')
            self.counts['rendered_representative_records_checked'] += len(reps)
        for event in place.get('elections', []):
            identity = 'event-' + re.sub('[^a-z0-9]+', '-', str(event['id']).lower()).strip('-')
            self.check(identity in doc.ids, f'{page}: canonical event has no rendered fragment: {event["id"]}')
            article = re.search(r'<article\b[^>]*\bid="' + re.escape(identity) + r'"[^>]*>(.*?)</article>', markup, re.S)
            if not self.check(article is not None, f'{page}: canonical event has no dedicated article: {event["id"]}'):
                continue
            tbody = re.search(r'<tbody\b[^>]*>(.*?)</tbody>', article[1], re.S)
            rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', tbody[1], re.S) if tbody else []
            candidates = event.get('candidates', [])
            self.check(len(rows) == len(candidates), f'{page} event {event["id"]}: rendered contestant count differs from canonical roster')
            for candidate, row in zip(candidates, rows):
                text = plain(row)
                values = [('ballot name', candidate.get('name')), ('ballot affiliation', candidate.get('party'))]
                if candidate.get('votes') is not None:
                    values += [('recorded votes', str(candidate['votes'])), ('vote measure', candidate.get('voteMeasure'))]
                for label, value in values:
                    if value:
                        self.check(' '.join(str(value).split()) in text, f'{page} event {event["id"]}: {candidate.get("name")} rendered {label} differs')
            self.counts['rendered_event_records_checked'] += 1
            self.counts['rendered_contestant_records_checked'] += len(candidates)

    def retained_reports(self):
        reports = []
        folder = ROOT / 'content/places/sources'
        candidates = set(folder.glob('*verification*.json')) | set(folder.glob('*geometry-audit*.json')) | set(folder.glob('*validation*.json'))
        for path in sorted(candidates):
            try:
                data = json.loads(path.read_text(encoding='utf-8-sig'))
            except ValueError:
                continue
            status = data.get('status', 'pass' if data.get('passed') is True else 'fail' if data.get('passed') is False else 'retained evidence; review original report')
            reports.append({'file': path.relative_to(ROOT).as_posix(), 'checked': data.get('checked') or data.get('updated'), 'status': status,
                            'note': 'Retained adapter report read; this national structural validator does not independently establish official/legal source completeness.'})
            if data.get('passed') is False or str(data.get('status', '')).casefold() == 'fail':
                self.errors.append(f'Retained adapter verification reports failure: {path.relative_to(ROOT).as_posix()}')
        return reports

    def run(self):
        before = []
        if not self.skip_pages:
            try:
                before = collect_fingerprints(ROOT)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.check(False, 'Evidence snapshot before validation: '+str(exc))
        self.load_records()
        self.records()
        self.load_registry()
        self.geometry()
        self.pages()
        retained = self.retained_reports()
        fingerprints = []
        if not self.skip_pages:
            try:
                fingerprints = collect_fingerprints(ROOT)
                self.check(before == fingerprints, 'Inputs or generated artifacts changed during validation; rerun after the build is stable')
                self.counts['evidence_artifacts_bound'] = len(fingerprints)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.check(False, 'Evidence snapshot after validation: '+str(exc))
        declared = {scope: data.get('coverage') for scope, data in self.inputs.items() if data.get('coverage') is not None}
        report = {'schemaVersion': 1, 'checked': CHECKED, 'status': 'fail' if self.errors else 'pass',
                  'mode': 'provisional-acquisition' if self.skip_pages else 'generated-pages-and-data',
                  'checks': dict(self.counts), 'errors': self.errors, 'warnings': self.warnings,
                  'artifactFingerprints': fingerprints, 'sourceHashesRequested': self.source_hashes,
                  'coverageGaps': {scope: dict(gaps) for scope, gaps in self.gaps.items()},
                  'declaredSourceCoverage': declared, 'retainedAdapterReports': retained,
                  'limits': ['Structural checks do not establish current political truth, source legal rights, complete biographies or complete historical contestants.',
                             'Missing people/contestants are explicit coverage gaps; a structural pass does not claim those are complete.',
                             'No browser, visual, keyboard, performance or external HTTP check is claimed by this script.',
                             'Local links/assets/fragments are checked on generated place/detail/directory pages; linked existing pages supply fragment targets without expanding this run into an unrelated legacy-site audit.']}
        output = ROOT / 'content/places/qa/national-validation.json'
        if not self.no_write:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(json.dumps({key: report[key] for key in ('status', 'mode', 'checks', 'coverageGaps')}, indent=2))
        for error in self.errors[:30]:
            print('FAIL:', error)
        if len(self.errors) > 30:
            print(f'... {len(self.errors) - 30} additional failures in {output.relative_to(ROOT).as_posix()}')
        return 1 if self.errors else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-pages', action='store_true', help='Provisional acquisition checks only; not final acceptance.')
    parser.add_argument('--source-hashes', action='store_true', help='Also hash every available retained original source file.')
    parser.add_argument('--no-write', action='store_true', help='Repeat checks without replacing reviewed evidence, for example in CI or a public checkout.')
    args = parser.parse_args()
    raise SystemExit(Validator(args.skip_pages, args.source_hashes, args.no_write).run())
