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
import os
from pathlib import Path
import re
import tempfile
from national_evidence import require_current_evidence, StableInputs, CONTRACT_SET
from page_review_register import reviewed_page_entries

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = 'content/places/qa/national-validation.json'
DEFAULT_BROWSER = 'content/places/qa/browser-review.json'
DEFAULT_SHARED = 'content/places/qa/shared-contract-evidence.json'
FINGERPRINT_PATHS = ('assets/civic-places.js', 'assets/civic-places.css',
                     'tools/build-national-places.py', 'tools/verify-national-places.py')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def passed(report):
    return str(report.get('status', report.get('result', ''))).upper() == 'PASS'


def encoded(document):
    return (json.dumps(document,indent=2,ensure_ascii=False)+'\n').encode('utf-8')


def atomic_write(path,data):
    """Replace one output exactly; the set remains incomplete until the end."""
    if path.exists() and path.read_bytes()==data:return
    path.parent.mkdir(parents=True,exist_ok=True)
    handle,name=tempfile.mkstemp(prefix='.contract-stage-',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(handle,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if temporary.exists():temporary.unlink()


def registered_route_dates(root, routes):
    """Require an explicit unique editorial date for every contracted route."""
    dates = {row['path']: row['lastUpdated'] for row in reviewed_page_entries(root)}
    result = {}
    for row in routes:
        page = row['url']
        if page not in dates:
            raise ValueError('Contract route lacks a registered implementation date: ' + page)
        date.fromisoformat(dates[page])
        result[page] = dates[page]
    return result


def generate(validation_path, browser_path, dry_run=False):
    # All guards precede every write. A real file alone is not a passing review.
    inputs=StableInputs(ROOT)
    validation = inputs.read_json(validation_path)
    browser = inputs.read_json(browser_path)
    if not passed(validation) or validation.get('mode') != 'generated-pages-and-data':
        raise ValueError('A passing default national structural report is required; provisional --skip-pages evidence cannot bind contracts.')
    if not passed(browser):
        raise ValueError('The real browser-review record must report PASS before contracts can bind its actual limited scope.')
    result=require_current_evidence(ROOT, validation, browser)
    inputs.bind_national(validation,browser,result)
    reviewed = validation.get('checked') or validation.get('reviewedOn')
    date.fromisoformat(reviewed)
    registry = inputs.read_json('content/places/route-registry.json')
    register_path='content/history/civic-page-review-register-2026-10-17.json'
    if (ROOT/register_path).is_file():
        register=inputs.read_json(register_path)
        for name in register.get('additionalPageRegisters',[]):inputs.read_json(name)
    implementation_dates = registered_route_dates(ROOT, registry['places'])
    canonical = {}
    for scope in ('councils', 'state', 'federal'):
        path = f'content/places/{scope}.json'
        payload = inputs.read_json(path)
        for index, place in enumerate(payload['places']):
            if place['id'] in canonical:
                raise ValueError('Duplicate canonical identity ' + place['id'])
            canonical[place['id']] = (scope, path, index, place)
    fingerprints = []
    for path in (*FINGERPRINT_PATHS, validation_path, browser_path):
        fingerprints.append({'path': path, 'sha256': inputs.fingerprint(path)})
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
    shared_evidence = {
        'schemaVersion': 1, 'kind': 'national-place-shared-evidence',
        'reviewedOn': reviewed, 'paths': [validation_path, browser_path,CONTRACT_SET],
        'nationalEvidence': {'validation': validation_path, 'browser': browser_path},
        'contractSet':CONTRACT_SET,
        'artifactFingerprints': fingerprints,
    }
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
                              'minimumChoices': 2, 'visibleDateValues': [implementation_dates[page]]},
            'routes': [{'path': page, 'role': 'place-overview',
                        'requiredNextPaths': [f'states/{place["jurisdiction"]}/places/{scope}/index.html']}],
            'datePins': pins,
            'reviewEvidence': {'sharedEvidence': DEFAULT_SHARED, 'requiredHumanChecks': required_human,
                               'limitations': limitations},
        }
        manifests.append((filename, manifest))
    destination = ROOT / 'content/places/contracts'
    outputs=[(destination/filename,encoded(manifest)) for filename,manifest in manifests]
    desired={path.relative_to(ROOT).as_posix() for path,_ in outputs}
    actual={path.relative_to(ROOT).as_posix() for path in destination.glob('*-pattern-contract.json')}
    if actual-desired:raise ValueError('Unexpected existing national contracts; review retirement explicitly: '+str(sorted(actual-desired)[:8]))
    contract_set={'schemaVersion':1,'kind':'national-place-contract-set','status':'complete',
                  'manifests':[{'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest()} for path,data in outputs]}
    index_bytes=encoded(contract_set)
    fingerprints.append({'path':CONTRACT_SET,'sha256':hashlib.sha256(index_bytes).hexdigest()})
    outputs.insert(0,(ROOT/DEFAULT_SHARED,encoded(shared_evidence)))
    inputs.verify()  # No output is touched if assembly observed stale inputs.
    changed=[(path,data) for path,data in outputs if not path.exists() or path.read_bytes()!=data]
    index_current=(ROOT/CONTRACT_SET).read_bytes() if (ROOT/CONTRACT_SET).exists() else None
    changing_set=False
    if not dry_run and (changed or index_current!=index_bytes):
        # Global acceptance rejects this marker, including remaining inline
        # legacy manifests. Interruption leaves an explicit incomplete set.
        changing_set=index_current!=index_bytes or any(path!=ROOT/DEFAULT_SHARED for path,_ in changed)
        if changing_set:
            atomic_write(ROOT/CONTRACT_SET,encoded({'schemaVersion':1,'kind':'national-place-contract-set','status':'in-progress'}))
        for path,data in changed:atomic_write(path,data)
        for path,data in outputs:
            if not path.is_file() or path.read_bytes()!=data:raise ValueError('Migration output changed before completion: '+path.relative_to(ROOT).as_posix())
        inputs.verify()
        actual={path.relative_to(ROOT).as_posix() for path in destination.glob('*-pattern-contract.json')}
        if actual!=desired:raise ValueError('National contract membership changed during migration')
        if changing_set:atomic_write(ROOT/CONTRACT_SET,index_bytes)  # Completion is the last write.
        if (ROOT/CONTRACT_SET).read_bytes()!=index_bytes:raise ValueError('National contract completion record changed during generation')
    else:
        inputs.verify()
    try:
        inputs.verify()  # Also covers mutation injected by the final replacement.
    except (OSError,ValueError,TypeError,KeyError):
        if not dry_run and changing_set:
            atomic_write(ROOT/CONTRACT_SET,encoded({'schemaVersion':1,'kind':'national-place-contract-set','status':'in-progress'}))
        raise
    print(json.dumps({'result': 'PASS', 'scope': 'structural route and canonical identity only',
                      'stage':'generation only; complete post-migration acceptance required',
                      'requiresPostMigrationValidation':True,'changedOutputs':len(changed),
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
