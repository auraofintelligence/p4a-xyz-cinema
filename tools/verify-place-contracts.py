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
from national_evidence import require_current_evidence, StableInputs, verify_contract_set

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
            # Some OrderedDict implementations call the overridden getter
            # after unlinking popitem's key. Its LRU touch then raises.
            # Delete the oldest entry without invoking our getter.
            del self[next(iter(self))]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print a compact machine-readable aggregate report.')
    parser.add_argument("--publication", action="store_true", help="Keep structural/data checks; defer browser acceptance until after deployment.")
    args = parser.parse_args(argv)
    manifests=sorted((ROOT/'content').rglob('*-pattern-contract.json'))
    if not manifests:
        print('FAIL: no civic-place contracts registered under content/')
        return 1
    spec = importlib.util.spec_from_file_location('p4a_civic_contract_validator', ROOT/'tools/verify-council-pattern.py')
    validator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator_module)
    pages = BoundedPageCache()
    inputs = StableInputs(ROOT)
    evidence_cache = {}
    national_preflights = {}

    class CachedValidator(validator_module.Validator):
        """Use the original checks; cache only identical read-only inputs."""
        def __init__(self, manifest):
            super().__init__(manifest, ROOT,inputs=inputs,publication=args.publication)
            self.pages = pages

        def read(self, relative):
            return inputs.read_json(relative)

        def prepare_inputs(self):
            pass  # The complete set is checked once by the aggregate boundary.

        def finalize_inputs(self):
            pass  # Every cached dependency is content-checked at the boundary.

        def verify_evidence(self, entry):
            # Reuse a declaration only within this content-guarded operation.
            # All direct and transitive files are rehashed before any PASS.
            key = json.dumps(entry, sort_keys=True, ensure_ascii=False)
            if key not in evidence_cache:
                start = len(self.errors)
                deferred_start = len(self.deferred)
                before = self.counts.copy()
                super().verify_evidence(entry)
                evidence_cache[key] = ([dict(e) for e in self.errors[start:]], self.counts - before, [dict(e) for e in self.deferred[deferred_start:]])
            else:
                errors, counts, deferred = evidence_cache[key]
                self.deferred.extend(dict(e) for e in deferred)
                self.errors.extend(dict(e) for e in errors)
                self.counts.update(counts)

        def verify_national_evidence(self, entry):
            evidence = entry['nationalEvidence']
            key = (evidence['validation'], evidence['browser'])
            if key not in national_preflights:
                try:
                    validation=self.read(key[0])
                    browser={} if args.publication else self.read(key[1])
                    national_preflights[key] = require_current_evidence(ROOT,validation,browser,require_browser=not args.publication)
                    inputs.bind_national(validation,browser,national_preflights[key])
                except (OSError, ValueError, TypeError, KeyError) as exc:
                    national_preflights[key] = str(exc)
            if isinstance(national_preflights[key], str):
                raise ValueError('National evidence freshness preflight failed: '+national_preflights[key])

    failures=[]
    scopes = Counter()
    counts = Counter()
    warning_count = 0
    deferred_count = 0
    run_errors=[]
    try:
        verify_contract_set(ROOT,inputs)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        run_errors.append(str(exc))
    for manifest in manifests:
        relative=manifest.relative_to(ROOT).as_posix()
        try:
            declaration = inputs.read_json(relative,cache=False)
            result = CachedValidator(declaration).run()
            scopes[declaration.get('acceptanceScope', 'legacy-declared-civic-journey')] += 1
            counts.update(result.get('counts', {}))
            warning_count += len(result.get('warnings', []))
            deferred_count += len(result.get('deferredReviewChecks', []))
        except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
            result = {'result': 'FAIL', 'errors': [{'code': 'manifest-error', 'message': str(exc)}]}
        if result['result'] != 'PASS':
            failures.append({'manifest': relative, 'errors': result.get('errors', [])})
    try:
        if manifests!=sorted((ROOT/'content').rglob('*-pattern-contract.json')):
            raise ValueError('Registered contract membership changed during validation')
        inputs.verify()
    except (OSError,ValueError,TypeError,KeyError) as exc:
        run_errors.append(str(exc))
    report = {'result': 'FAIL' if failures or run_errors else 'PASS', 'registeredContracts': len(manifests),
              'runErrors':run_errors,
              'failedContracts': len(failures), 'declaredScopes': dict(scopes), 'counts': dict(counts),
              'declaredLimitations': warning_count, 'failures': failures,
              'nationalEvidencePreflights': [{'validation':key[0], 'browser':key[1], 'result':value} for key,value in national_preflights.items()],
              'browserAcceptance': 'deferred until after live deployment' if args.publication else 'saved evidence verified only if result is PASS',
              'deferredReviewChecks':deferred_count,
              'scope': 'Publication mode defers review bindings only when requested. Original manifest validator semantics; in-process, offline, read-only. Structural route contracts do not certify complete national source/browser coverage.'}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Civic place contracts: {report['result']} · {len(manifests)} registered; {len(failures)} failed.")
        print('Declared scopes: ' + ', '.join(f'{key}: {value}' for key, value in scopes.items()))
        print('Checks: ' + ', '.join(f'{key}: {value}' for key, value in counts.items()))
        for error in run_errors:print('FAIL: '+error)
        for failure in failures[:20]:
            print('FAIL: ' + failure['manifest'])
            for error in failure['errors'][:5]:
                print(f"  [{error['code']}] {error['message']}")
        if len(failures) > 20:
            print(f'{len(failures)-20} further failed contracts; use --json for all evidence.')
        print('Browser acceptance: '+report['browserAcceptance']+'; deferred review bindings: '+str(deferred_count))
        print('Declared limits remain in each manifest; this run repeats no browser, editorial or live source review.')
    return 1 if failures or run_errors else 0

if __name__=='__main__':
    sys.exit(main())
