"""Run every registered civic-place contract without changing any files.

New council/state/federal builds register their manifest under content/ with a
unique name ending in -pattern-contract.json. No edit to this runner is needed.
Legacy Victoria checks remain separate until its wider journey is adapted.
"""
import argparse
from collections import Counter, OrderedDict
import importlib.util
import json
from pathlib import Path
import sys
from national_evidence import require_current_evidence

ROOT=Path(__file__).resolve().parents[1]

class BoundedPageCache(OrderedDict):
    """Share repeated fragment targets without retaining thousands of full DOMs."""
    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        while len(self) > 96:
            self.popitem(last=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print a compact machine-readable aggregate report.')
    args = parser.parse_args(argv)
    manifests=sorted((ROOT/'content').rglob('*-pattern-contract.json'))
    if not manifests:
        print('FAIL: no civic-place contracts registered under content/')
        return 1
    spec = importlib.util.spec_from_file_location('p4a_civic_contract_validator', ROOT/'tools/verify-council-pattern.py')
    validator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator_module)
    pages = BoundedPageCache()
    documents = {}
    evidence_cache = {}

    class CachedValidator(validator_module.Validator):
        """Use the original checks; cache only identical read-only inputs."""
        def __init__(self, manifest):
            super().__init__(manifest, ROOT)
            self.pages = pages

        def read(self, relative):
            path = self.path(relative)
            stat = path.stat()
            signature = (stat.st_mtime_ns, stat.st_size)
            cached = documents.get(path)
            if cached is None or cached[0] != signature:
                cached = (signature, json.loads(path.read_text(encoding='utf-8-sig')))
                documents[path] = cached
            return cached[1]

        def verify_evidence(self, entry):
            # Thousands of structural manifests bind the same actual shared
            # renderer/evidence. Reuse the original validator's result only
            # when both the entire declaration and all relevant files match.
            paths = set(entry.get('paths', [])) | {a['path'] for a in entry.get('artifactFingerprints', [])}
            if entry.get('layoutEvidence'):
                paths.add(entry['layoutEvidence'])
            signature = []
            for relative in sorted(paths):
                path = self.path(relative)
                stat = path.stat() if path.exists() else None
                signature.append((relative, stat.st_mtime_ns if stat else None, stat.st_size if stat else None))
            key = (json.dumps(entry, sort_keys=True, ensure_ascii=False), tuple(signature))
            if key not in evidence_cache:
                start = len(self.errors)
                before = self.counts.copy()
                super().verify_evidence(entry)
                evidence_cache[key] = ([dict(e) for e in self.errors[start:]], self.counts - before)
            else:
                errors, counts = evidence_cache[key]
                self.errors.extend(dict(e) for e in errors)
                self.counts.update(counts)

    failures=[]
    scopes = Counter()
    counts = Counter()
    warning_count = 0
    national_preflights = {}
    for manifest in manifests:
        relative=manifest.relative_to(ROOT).as_posix()
        try:
            declaration = json.loads(manifest.read_text(encoding='utf-8-sig'))
            if declaration.get('acceptanceScope') == 'structural-route-and-canonical-identity':
                evidence = declaration.get('reviewEvidence', {}).get('nationalEvidence', {})
                validation_path = evidence.get('validation', 'content/places/qa/national-validation.json')
                browser_path = evidence.get('browser', 'content/places/qa/browser-review.json')
                key = (validation_path, browser_path)
                if key not in national_preflights:
                    try:
                        validation = json.loads((ROOT/validation_path).read_text(encoding='utf-8-sig'))
                        browser = json.loads((ROOT/browser_path).read_text(encoding='utf-8-sig'))
                        national_preflights[key] = require_current_evidence(ROOT, validation, browser)
                    except (OSError, ValueError, TypeError, KeyError) as exc:
                        national_preflights[key] = str(exc)
                if isinstance(national_preflights[key], str):
                    raise ValueError('National evidence freshness preflight failed: '+national_preflights[key])
            result = CachedValidator(declaration).run()
            scopes[declaration.get('acceptanceScope', 'legacy-declared-civic-journey')] += 1
            counts.update(result.get('counts', {}))
            warning_count += len(result.get('warnings', []))
        except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
            result = {'result': 'FAIL', 'errors': [{'code': 'manifest-error', 'message': str(exc)}]}
        if result['result'] != 'PASS':
            failures.append({'manifest': relative, 'errors': result.get('errors', [])})
    report = {'result': 'FAIL' if failures else 'PASS', 'registeredContracts': len(manifests),
              'failedContracts': len(failures), 'declaredScopes': dict(scopes), 'counts': dict(counts),
              'declaredLimitations': warning_count, 'failures': failures,
              'nationalEvidencePreflights': [{'validation':key[0], 'browser':key[1], 'result':value} for key,value in national_preflights.items()],
              'scope': 'Original manifest validator semantics; in-process, offline, read-only. Structural route contracts do not certify complete national source/browser coverage.'}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Civic place contracts: {report['result']} · {len(manifests)} registered; {len(failures)} failed.")
        print('Declared scopes: ' + ', '.join(f'{key}: {value}' for key, value in scopes.items()))
        print('Checks: ' + ', '.join(f'{key}: {value}' for key, value in counts.items()))
        for failure in failures[:20]:
            print('FAIL: ' + failure['manifest'])
            for error in failure['errors'][:5]:
                print(f"  [{error['code']}] {error['message']}")
        if len(failures) > 20:
            print(f'{len(failures)-20} further failed contracts; use --json for all evidence.')
        print('Declared limits remain in each manifest; this run repeats no browser, editorial or live source review.')
    return 1 if failures else 0

if __name__=='__main__':
    sys.exit(main())
