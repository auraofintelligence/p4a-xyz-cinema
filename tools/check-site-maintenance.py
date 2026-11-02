#!/usr/bin/env python3
"""Check maintenance references/count arithmetic, not factual truth or publication."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def local_file(path):
    if not isinstance(path, str) or not path:
        raise AssertionError(f'Expected a nonempty repository path: {path!r}')
    target = (ROOT / path.split('#', 1)[0]).resolve()
    assert target.is_relative_to(ROOT), f'Reference escapes repository: {path}'
    assert target.is_file(), f'Missing maintenance evidence: {path}'


def main():
    index = load('content/history/site-maintenance-index.json')
    assert index['schemaVersion'] == 1
    inventory = load('content/site-page-inventory.json')
    routes = [p['path'] for p in inventory['pages']]
    assert len(routes) == len(set(routes)) == inventory['pageCount']
    seen = set()
    for kind in ('wholeSiteAudits', 'scopedUpdates'):
        for item in index[kind]:
            key = (kind, item['date'], item['report'])
            assert key not in seen, f'Duplicate maintenance entry: {key}'
            seen.add(key)
            local_file(item['report'])
            if item.get('sources'):
                local_file(item['sources'])
            if kind != 'wholeSiteAudits':
                continue
            report = load(item['report'])
            assert report['schemaVersion'] == 1
            assert sum(p['count'] for p in report['routePartition']) == report['publicRouteCount']
            assert all(isinstance(p['count'], int) and p['count'] >= 0 for p in report['routePartition'])
            assert len({p['id'] for p in report['routePartition']}) == len(report['routePartition'])
            # Historical audit totals remain historical; compare only latest audit to current inventory.
            if item is index['wholeSiteAudits'][-1]:
                assert report['publicRouteCount'] == inventory['pageCount']
            def references(value):
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k in ('evidence', 'report', 'sourcePath', 'inventoryPath'):
                            for path in v if isinstance(v, list) else [v]:
                                if isinstance(path, str) and path.startswith(('content/', 'docs/', 'tools/', 'tests/')):
                                    local_file(path)
                        references(v)
                elif isinstance(value, list):
                    for v in value:
                        references(v)
            references(report)
    local_file(index['publicationEvidence'])
    publication = load(index['publicationEvidence'])
    assert publication['schemaVersion'] == 1
    for record in publication['records']:
        assert re.fullmatch(r'[0-9a-f]{40}', record['commit']), 'Invalid publication commit format'
        assert record.get('liveVerification'), 'Publication records need stated verification scope'
        assert record['pagesRun'].startswith('https://github.com/auraofintelligence/p4a-xyz-cinema/actions/runs/')
    doc = ROOT / 'docs/site-maintenance.md'
    for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
        if not re.match(r'^[a-z]+:|^#', target):
            local_file(str((doc.parent / target.split('#', 1)[0]).relative_to(ROOT)))
    print(f'Maintenance references and route-count arithmetic passed ({inventory["pageCount"]} routes). Not a factual or deployment verification.')


if __name__ == '__main__':
    main()
