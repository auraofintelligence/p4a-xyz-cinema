#!/usr/bin/env python3
"""Bind real national QA to narrowly declared per-place route contracts.

Requires completed national structural validation and a real browser review
record before writing any manifest. The generated scope is route identity,
visible dates, breadcrumbs, choices and source identity pins. It does not turn
a shared browser smoke test into a full per-place source or browser approval.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from national_evidence import require_current_evidence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = 'content/places/qa/national-validation.json'
DEFAULT_BROWSER = 'content/places/qa/browser-review.json'
FINGERPRINT_PATHS = ('assets/civic-places.js', 'assets/civic-places.css',
                     'tools/build-national-places.py', 'tools/verify-national-places.py')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def passed(report):
    return str(report.get('status', report.get('result', ''))).upper() == 'PASS'


def generate(validation_path, browser_path, dry_run=False):
    # All guards precede every write. A real file alone is not a passing review.
    validation = read(validation_path)
    browser = read(browser_path)
    if not passed(validation) or validation.get('mode') != 'generated-pages-and-data':
        raise ValueError('A passing default national structural report is required; provisional --skip-pages evidence cannot bind contracts.')
    if not passed(browser):
        raise ValueError('The real browser-review record must report PASS before contracts can bind its actual limited scope.')
    require_current_evidence(ROOT, validation, browser)
    reviewed = validation.get('checked') or validation.get('reviewedOn')
    date.fromisoformat(reviewed)
    registry = read('content/places/route-registry.json')
    implementation_date = registry['implementationUpdated']
    date.fromisoformat(implementation_date)
    canonical = {}
    for scope in ('councils', 'state', 'federal'):
        path = f'content/places/{scope}.json'
        payload = read(path)
        for index, place in enumerate(payload['places']):
            if place['id'] in canonical:
                raise ValueError('Duplicate canonical identity ' + place['id'])
            canonical[place['id']] = (scope, path, index, place)
    fingerprints = []
    for path in (*FINGERPRINT_PATHS, validation_path, browser_path):
        fingerprints.append({'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()})
    limitations = [
        'Declared scope is this place route, visible implementation date, breadcrumbs, choices and canonical place identity/boundary pins only.',
        'This manifest does not claim a complete civic journey, current source/legal correctness, full biographies or full historical contestant coverage.',
        'Geometry, people, candidate measures and timing received only the actual checks recorded in the linked national report; their missing coverage remains explicit there.',
        'Browser evidence is a shared-renderer smoke review of its recorded fixtures and viewport/device conditions. It does not establish full per-place source, geometry, mobile, accessibility or browser review.',
        'No new Twinkles were authored; grassroots implementation remains open. A structural PASS is not a national completeness claim.',
    ]
    required_human = [
        'Review this place against its actual official boundary/role/event sources and source rights when facts or boundaries change; do not infer office from a historical winner.',
        'Repeat affected map/search/select/Open, direct-link, Back, keyboard and narrow-screen checks and record the real tested fixtures.',
        'Treat missing current-member or contestant coverage in the national report and canonical coverage notes as unresolved research, not as passing source review.',
    ]
    manifests = []
    names = set()
    for row in registry['places']:
        key = row['id']
        if key not in canonical:
            raise ValueError('Registry identity has no canonical source: ' + key)
        scope, source_path, index, place = canonical[key]
        page = row['url']
        if not (ROOT / page).is_file():
            raise ValueError('Cannot bind an unbuilt page: ' + page)
        pins = [{'path': source_path, 'pointer': f'/places/{index}/{field}', 'expected': place[field]}
                for field in ('id', 'name', 'boundaryEdition') if field in place]
        pins.append({'path': source_path, 'pointer': f'/places/{index}', 'expected': place})
        notes = list(place.get('coverageNotes', [])) + limitations
        if 'boundaryEdition' not in place:
            notes.append('No boundaryEdition value is populated in this canonical place record; no boundary-edition value is invented or pinned.')
        filename = re.sub(r'[^A-Za-z0-9._-]+', '-', key).strip('-') + '-pattern-contract.json'
        if filename in names:
            raise ValueError('Two stable identities collide in contract filename ' + filename)
        names.add(filename)
        manifest = {
            'schemaVersion': 1,
            'title': place['name'] + ' — declared route and canonical identity contract',
            'purpose': 'Reviewable structural scope only. Shared national QA is linked with its actual limits; official source and per-place browser review remain distinct.',
            'acceptanceScope': 'structural-route-and-canonical-identity',
            'place': {field: place[field] for field in ('id', 'kind', 'name', 'jurisdiction', 'chamber') if field in place},
            'canonicalInput': {'path': source_path, 'recordPointer': f'/places/{index}', 'scope': scope},
            'coverageNotes': notes,
            'routeDefaults': {'noSvgMaps': True, 'breadcrumbClass': 'civic-crumbs', 'choicesClass': 'civic-choices',
                              'minimumChoices': 2, 'visibleDateValues': [implementation_date]},
            'routes': [{'path': page, 'role': 'place-overview',
                        'requiredNextPaths': [f'states/{place["jurisdiction"]}/places/{scope}/index.html']}],
            'datePins': pins,
            'reviewEvidence': {'reviewedOn': reviewed, 'paths': [validation_path, browser_path],
                               'nationalEvidence': {'validation': validation_path, 'browser': browser_path},
                               'artifactFingerprints': fingerprints, 'requiredHumanChecks': required_human,
                               'limitations': limitations},
        }
        manifests.append((filename, manifest))
    if not dry_run:
        destination = ROOT / 'content/places/contracts'
        destination.mkdir(parents=True, exist_ok=True)
        for filename, manifest in manifests:
            text = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
            path = destination / filename
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                path.write_text(text, encoding='utf-8')
    print(json.dumps({'result': 'PASS', 'scope': 'structural route and canonical identity only',
                      'manifests': len(manifests), 'written': not dry_run,
                      'evidence': [validation_path, browser_path],
                      'limits': 'Shared renderer smoke evidence does not establish full per-place source/browser review.'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validation', default=DEFAULT_VALIDATION)
    parser.add_argument('--browser-review', default=DEFAULT_BROWSER)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        generate(args.validation, args.browser_review, args.dry_run)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print('FAIL:', exc)
        raise SystemExit(1)
