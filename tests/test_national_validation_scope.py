"""Synthetic evidence only: scoped contracts, fresh bindings and bounded readers."""
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import national_evidence as evidence
import national_geometry as geometry


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


builder = module('scope_builder', 'build-national-contracts.py')
contract = module('scope_contract', 'verify-council-pattern.py')
national = module('scope_national', 'verify-national-places.py')
runner = module('scope_runner', 'verify-place-contracts.py')


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Actual discovery runs on this complete miniature national site.
        for name in evidence.BASE_FILES:
            self.write(name, '{}')
        self.write('content/places/source-retention.json', {'localOnlyPathPrefixes': ['content/places/raw/']})
        self.write('content/places/sources/national-basemap.json', {})
        self.features = {'type': 'FeatureCollection', 'features': [self.feature('one')]}
        self.write('map.geojson', self.features)
        self.write('fixture.html', '<p>Synthetic browser fixture, not production evidence.</p>')
        self.places = [{'id': key, 'kind': 'council', 'name': key.title(), 'jurisdiction': 'qld',
                        'boundaryEdition': 'test-edition', 'checked': '2026-10-01'} for key in ('one', 'two')]
        self.routes = [{'id': p['id'], 'url': p['id'] + '.html'} for p in self.places]
        self.write_canonical()
        self.write('content/places/route-registry.json', {'places': self.routes, 'layers': []})
        self.write('content/places/geometry-delivery.json', {'layers': []})
        for state in evidence.JURISDICTIONS:
            for suffix in ('', 'councils/', 'state/', 'federal/'):
                self.write(f'states/{state}/places/{suffix}index.html', '<title>Directory</title>')
        self.write('pages/places.html', '<title>Places</title>')
        for row in self.routes:
            self.write(row['url'], '<title>Place</title><h1>Place</h1>'
                       '<nav class="civic-crumbs" aria-label="Parents"><a href="pages/places.html">Places</a></nav>'
                       '<nav class="civic-choices"><a href="states/qld/places/councils/index.html">Councils</a>'
                       '<a href="pages/places.html">Places</a></nav><time datetime="2026-10-23">Updated</time>')
        self.browser = {'status': 'PASS', 'testedPagePaths': ['one.html'], 'fixturePaths': ['fixture.html']}
        self.browser['artifactFingerprints'] = self.fingerprints([*evidence.BROWSER_CODE_FILES, 'one.html', 'fixture.html'])
        self.write(builder.DEFAULT_BROWSER, self.browser)
        self.refresh_validation()
        self.build()

    @staticmethod
    def feature(key):
        return {'type': 'Feature', 'properties': {'id': key},
                'geometry': {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 0]]]}}

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data if isinstance(data, str) else json.dumps(data), encoding='utf-8')

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding='utf-8'))

    def fingerprints(self, names):
        return [{'path': name, 'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest()} for name in names]

    def write_canonical(self):
        for scope in evidence.SCOPES:
            self.write(f'content/places/{scope}.json', {'places': self.places if scope == 'councils' else [],
                       'layers': [{'geometryFile': 'map.geojson'}] if scope == 'councils' else []})

    def refresh_validation(self, checked='2026-10-23'):
        self.validation = {'status': 'PASS', 'mode': 'generated-pages-and-data', 'checked': checked,
                           'artifactFingerprints': evidence.collect_fingerprints(self.root)}
        self.write(builder.DEFAULT_VALIDATION, self.validation)

    def build(self):
        dates = [{'path': r['url'], 'lastUpdated': '2026-10-23'} for r in self.routes]
        with patch.object(builder, 'ROOT', self.root), patch.object(builder, 'reviewed_page_entries', return_value=dates), contextlib.redirect_stdout(io.StringIO()):
            builder.generate(builder.DEFAULT_VALIDATION, builder.DEFAULT_BROWSER)

    def manifest(self, key='one'):
        return self.read(f'content/places/contracts/{key}-pattern-contract.json')

    def validate(self, declaration=None):
        return contract.Validator(declaration or self.manifest(), self.root).run()


class SharedEvidence(Fixture):
    def test_one_record_changes_only_its_contract_and_shared_binding(self):
        neighbour = self.root / 'content/places/contracts/two-pattern-contract.json'
        old_bytes, old_stat = neighbour.read_bytes(), neighbour.stat().st_mtime_ns
        old_target = self.manifest()
        old_binding = (self.root / builder.DEFAULT_SHARED).read_bytes()
        self.places[0]['coverageNotes'] = ['One scoped change; source check date preserved.']
        self.write_canonical()
        self.refresh_validation('2026-11-05')
        self.assertEqual(self.validate()['result'], 'FAIL', 'A new global report must not bless an old canonical pin.')
        self.build()
        self.assertNotEqual(old_target, self.manifest())
        self.assertEqual(neighbour.read_bytes(), old_bytes)
        self.assertEqual(neighbour.stat().st_mtime_ns, old_stat, 'Unchanged neighbour must not even be rewritten.')
        self.assertNotEqual((self.root / builder.DEFAULT_SHARED).read_bytes(), old_binding)
        self.assertEqual(self.validate()['result'], 'PASS')
        self.assertEqual(self.places[0]['checked'], '2026-10-01')
        self.assertEqual(self.manifest()['routeDefaults']['visibleDateValues'], ['2026-10-23'])

    def test_shared_report_date_does_not_rewrite_any_place(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in (self.root / 'content/places/contracts').glob('*.json')}
        index=self.root/evidence.CONTRACT_SET
        index_before=(index.read_bytes(),index.stat().st_mtime_ns)
        self.refresh_validation('2026-11-05')
        self.build()
        for path, saved in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), saved)
        self.assertEqual((index.read_bytes(),index.stat().st_mtime_ns),index_before)

    def test_legacy_inline_manifest_and_freshness_are_preserved(self):
        declaration = self.manifest()
        declaration['reviewEvidence'] = evidence.resolve_review_evidence(self.root, declaration['reviewEvidence'])
        self.assertEqual(self.validate(declaration)['result'], 'PASS')
        self.write('map.geojson', {**self.features, 'note': 'changed'})
        self.assertEqual(self.validate(declaration)['result'], 'FAIL')

    def test_corrupt_missing_escaping_or_overridden_shared_binding_fails(self):
        original = self.read(builder.DEFAULT_SHARED)
        for corrupt in ({}, [], 'invalid', {**original, 'schemaVersion': 99}, {**original, 'artifactFingerprints': []},
                        {**original, 'sharedEvidence': builder.DEFAULT_SHARED}):
            with self.subTest(corrupt=corrupt):
                self.write(builder.DEFAULT_SHARED, corrupt)
                self.assertEqual(self.validate()['result'], 'FAIL')
        self.write(builder.DEFAULT_SHARED, original)
        declaration = self.manifest()
        declaration['reviewEvidence']['reviewedOn'] = '2026-11-05'
        self.assertEqual(self.validate(declaration)['result'], 'FAIL')
        declaration['reviewEvidence'] = {'sharedEvidence': '../outside.json'}
        self.assertEqual(self.validate(declaration)['result'], 'FAIL')
        (self.root / builder.DEFAULT_SHARED).unlink()
        self.assertEqual(self.validate()['result'], 'FAIL')

    def test_shared_date_cannot_silently_advance_the_validation_review(self):
        shared = self.read(builder.DEFAULT_SHARED)
        shared['reviewedOn'] = '2026-11-05'
        self.write(builder.DEFAULT_SHARED, shared)
        self.assertEqual(self.validate()['result'], 'FAIL')

    def test_tampered_report_binding_fails_standalone(self):
        shared = self.read(builder.DEFAULT_SHARED)
        shared['artifactFingerprints'][-1]['sha256'] = '0' * 64
        self.write(builder.DEFAULT_SHARED, shared)
        self.assertEqual(self.validate()['result'], 'FAIL')

    def test_changed_shared_code_geometry_and_new_artifact_fail(self):
        for name in ('assets/civic-places.js', 'tools/national_geometry.py', 'map.geojson'):
            with self.subTest(name=name):
                path = self.root / name
                before = path.read_bytes()
                path.write_bytes(before + b' ')
                self.assertEqual(self.validate()['result'], 'FAIL')
                path.write_bytes(before)
        self.write('new.css', 'body{}')
        self.write('two.html', (self.root / 'two.html').read_text() + '<link rel="stylesheet" href="new.css">')
        self.validation['artifactFingerprints'] = self.fingerprints([r['path'] for r in self.validation['artifactFingerprints']])
        with self.assertRaisesRegex(ValueError, 'artifact set changed'):
            evidence.require_current_evidence(self.root, self.validation, self.browser)

    def test_builder_refuses_stale_browser_without_writing_or_refreshing_it(self):
        saved = {p: p.read_bytes() for p in (self.root / 'content/places').rglob('*.json')}
        browser_bytes = (self.root / builder.DEFAULT_BROWSER).read_bytes()
        self.write('fixture.html', '<p>Changed fixture</p>')
        self.refresh_validation()
        with self.assertRaisesRegex(ValueError, 'Browser evidence'):
            self.build()
        self.assertEqual((self.root / builder.DEFAULT_BROWSER).read_bytes(), browser_bytes)
        for path, content in saved.items():
            if path.name != 'national-validation.json':
                self.assertEqual(path.read_bytes(), content)

    def test_discovery_does_not_rehash_verified_artifacts(self):
        with patch.object(evidence, '_digest', wraps=evidence._digest) as digest:
            evidence.discover_artifacts(self.root)
            self.assertEqual(digest.call_count, 0)
            evidence.require_current_evidence(self.root, self.validation, self.browser)
            self.assertEqual(digest.call_count, len(self.validation['artifactFingerprints']) + len(self.browser['artifactFingerprints']))

    def test_optional_retained_original_still_matches_canonical_source_hash(self):
        name = 'content/places/raw/source.txt'
        self.write(name, 'actual retained bytes')
        canonical = self.read('content/places/councils.json')
        canonical['sources'] = [{'rawFile': name, 'sha256': '0' * 64}]
        self.write('content/places/councils.json', canonical)
        required, optional = evidence.discover_artifacts(self.root)
        self.validation['artifactFingerprints'] = self.fingerprints(sorted(required | set(optional)))
        with self.assertRaisesRegex(ValueError, 'Retained original differs from canonical source hash'):
            evidence.require_current_evidence(self.root, self.validation, self.browser)

    def test_legacy_non_national_journey_keeps_its_declared_checks(self):
        declaration = self.manifest()
        declaration.pop('acceptanceScope')
        inline = evidence.resolve_review_evidence(self.root, declaration['reviewEvidence'])
        inline.pop('nationalEvidence')
        declaration['reviewEvidence'] = inline
        self.assertEqual(self.validate(declaration)['result'], 'PASS')
        self.write('one.html', '<title>Broken route</title>')
        self.assertEqual(self.validate(declaration)['result'], 'FAIL')

    def test_malformed_outer_review_evidence_returns_structured_failure(self):
        for entry in (None,[],42,'invalid'):
            declaration=self.manifest();declaration['reviewEvidence']=entry
            with self.subTest(entry=entry):
                result=self.validate(declaration)
                self.assertEqual(result['result'],'FAIL')
                self.assertTrue(any(e['code']=='invalid-evidence' for e in result['errors']))

    def test_aggregate_reuses_national_checks_and_rejects_stale_shared_bytes(self):
        # The dynamic validator import uses the repository's real tool, but the
        # content and evidence remain inside the miniature temporary site.
        target = self.root / 'tools/verify-council-pattern.py'
        target.write_bytes((ROOT / 'tools/verify-council-pattern.py').read_bytes())
        self.refresh_validation()
        self.build()
        with patch.object(runner, 'ROOT', self.root), patch.object(runner, 'require_current_evidence', wraps=evidence.require_current_evidence) as preflight, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(['--json']), 0)
            self.assertEqual(preflight.call_count, 1)
        self.write('map.geojson', {})
        self.assertEqual(self.validate()['result'], 'FAIL')
        with patch.object(runner, 'ROOT', self.root), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(['--json']), 1)


class MutationAndMigration(Fixture):
    def mutate_same_metadata(self,name):
        path=self.root/name;stat=path.stat();data=path.read_bytes()
        for before,after in ((b'2026-10-01',b'2026-10-02'),(b'2026-10-23',b'2026-10-24'),(b'"one"',b'"xxx"')):
            if before in data:
                changed=data.replace(before,after,1);break
        else:
            changed=(b'[' if data[:1]!=b'[' else b'{')+data[1:]
        path.write_bytes(changed)
        os.utime(path,ns=(stat.st_atime_ns,stat.st_mtime_ns))
        self.assertEqual(path.stat().st_size,stat.st_size)
        self.assertEqual(path.stat().st_mtime_ns,stat.st_mtime_ns)

    def prepare_runner(self):
        (self.root/'tools/verify-council-pattern.py').write_bytes((ROOT/'tools/verify-council-pattern.py').read_bytes())
        self.refresh_validation();self.build()

    def test_aggregate_rejects_transitive_mutations_after_cached_preflight(self):
        self.prepare_runner()
        for name in ('map.geojson','tools/national_geometry.py','content/places/councils.json',
                     builder.DEFAULT_SHARED,'one.html','content/places/contracts/one-pattern-contract.json'):
            path=self.root/name;original=path.read_bytes();calls=[]
            def injected(root,validation,browser,**kwargs):
                result=evidence.require_current_evidence(root,validation,browser,**kwargs)
                calls.append(True);self.mutate_same_metadata(name)
                return result
            output=io.StringIO()
            with self.subTest(name=name),patch.object(runner,'ROOT',self.root),patch.object(runner,'require_current_evidence',side_effect=injected),contextlib.redirect_stdout(output):
                self.assertEqual(runner.main(['--json']),1)
                report=json.loads(output.getvalue())
                self.assertEqual(report['result'],'FAIL')
                self.assertTrue(report['runErrors'])
                self.assertEqual(len(calls),1,'Shared checks stay cached; the final content guard rejects the mutation.')
            path.write_bytes(original)

    def test_standalone_rejects_metadata_preserved_cache_mutation(self):
        original=evidence.require_current_evidence
        def injected(root,validation,browser,**kwargs):
            result=original(root,validation,browser,**kwargs)
            self.mutate_same_metadata('content/places/councils.json')
            return result
        with patch.object(contract,'require_current_evidence',side_effect=injected):
            result=self.validate()
        self.assertEqual(result['result'],'FAIL')
        self.assertTrue(any('changed during operation' in e['message'] for e in result['errors']))

    def test_available_and_absent_local_original_mutations_fail(self):
        name='content/places/raw/original.txt';source_bytes=b'reviewed original'
        canonical=self.read('content/places/councils.json')
        canonical['sources']=[{'rawFile':name,'sha256':hashlib.sha256(source_bytes).hexdigest()}]
        self.write('content/places/councils.json',canonical)
        for initially_present in (True,False):
            path=self.root/name
            if initially_present:self.write(name,source_bytes.decode())
            elif path.exists():path.unlink()
            self.refresh_validation();self.build()
            def injected(root,validation,browser,**kwargs):
                result=evidence.require_current_evidence(root,validation,browser,**kwargs)
                if initially_present:self.mutate_same_metadata(name)
                else:self.write(name,source_bytes.decode())
                return result
            with self.subTest(initially_present=initially_present),patch.object(contract,'require_current_evidence',side_effect=injected):
                self.assertEqual(self.validate()['result'],'FAIL')

    def test_builder_rejects_assembly_mutation_before_any_output_write(self):
        outputs=list((self.root/'content/places/contracts').glob('*.json'))+[self.root/builder.DEFAULT_SHARED,self.root/evidence.CONTRACT_SET]
        before={p:p.read_bytes() for p in outputs}
        original=evidence.StableInputs.verify
        def injected(inputs):
            self.mutate_same_metadata('content/places/councils.json')
            return original(inputs)
        with patch.object(evidence.StableInputs,'verify',injected),self.assertRaisesRegex(ValueError,'changed during operation'):
            self.build()
        for path,content in before.items():self.assertEqual(path.read_bytes(),content)

    def test_builder_mid_write_mutation_leaves_incomplete_set_and_no_pass(self):
        self.places[0]['coverageNotes']=['Force one scoped output change']
        self.write_canonical();self.refresh_validation()
        original=builder.atomic_write;output=io.StringIO()
        def injected(path,data):
            original(path,data)
            if path.name=='one-pattern-contract.json':self.mutate_same_metadata('content/places/councils.json')
        with patch.object(builder,'atomic_write',side_effect=injected),contextlib.redirect_stdout(output),self.assertRaisesRegex(ValueError,'changed during operation'):
            self.build()
        self.assertEqual(self.read(evidence.CONTRACT_SET)['status'],'in-progress')
        self.assertNotIn('"result": "PASS"',output.getvalue())
        self.assertEqual(self.validate()['result'],'FAIL')

    def test_interrupted_migration_is_rejected_then_resumable(self):
        self.prepare_runner()
        self.places[0]['coverageNotes']=['One changed declaration']
        self.write_canonical();self.refresh_validation()
        original=builder.atomic_write
        def interrupted(path,data):
            original(path,data)
            if path.name=='one-pattern-contract.json':raise OSError('Injected interruption')
        with patch.object(builder,'atomic_write',side_effect=interrupted),self.assertRaisesRegex(OSError,'Injected interruption'):
            self.build()
        self.assertEqual(self.read(evidence.CONTRACT_SET)['status'],'in-progress')
        self.assertEqual(self.validate()['result'],'FAIL')
        with patch.object(runner,'ROOT',self.root),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(['--json']),1)
        self.build()
        self.assertEqual(self.read(evidence.CONTRACT_SET)['status'],'complete')
        self.assertEqual(self.validate()['result'],'PASS')

    def test_partial_missing_and_extra_contract_sets_fail(self):
        target=self.root/'content/places/contracts/two-pattern-contract.json';saved=target.read_bytes()
        target.unlink()
        self.assertEqual(self.validate()['result'],'FAIL')
        target.write_bytes(saved)
        extra=self.root/'content/places/contracts/extra-pattern-contract.json';extra.write_bytes(saved)
        self.assertEqual(self.validate()['result'],'FAIL')
        with self.assertRaisesRegex(ValueError,'Unexpected existing national contracts'):self.build()

    def test_mutation_on_completion_replacement_cannot_report_pass(self):
        self.places[0]['coverageNotes']=['Changed declaration'];self.write_canonical();self.refresh_validation()
        original=builder.atomic_write
        def injected(path,data):
            original(path,data)
            if path==self.root/evidence.CONTRACT_SET and json.loads(data)['status']=='complete':
                self.mutate_same_metadata('content/places/councils.json')
        with patch.object(builder,'atomic_write',side_effect=injected),self.assertRaisesRegex(ValueError,'changed during operation'):
            self.build()
        self.assertEqual(self.read(evidence.CONTRACT_SET)['status'],'in-progress')
        self.assertEqual(self.validate()['result'],'FAIL')


class BoundedValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_streamed_features_equal_json_decode_across_chunk_boundaries(self):
        features = [Fixture.feature('café'), Fixture.feature('two')]
        data = {'metadata': {'number': 1.2e-7, 'escaped': 'a"b'}, 'features': features, 'type': 'FeatureCollection'}
        raw = json.dumps(data, ensure_ascii=False).encode('utf-8-sig')
        for filename in ('geometry.json', 'geometry.json.gz'):
            path = self.root / filename
            path.write_bytes(gzip.compress(raw) if filename.endswith('.gz') else raw)
            for size in (1, 7, 64, 1024):
                with self.subTest(filename=filename, chunk=size):
                    self.assertEqual(list(geometry.iter_features(path, size)), features)

    def test_malformed_truncated_and_wrong_collections_fail(self):
        for text in ('{}', '{"type":"FeatureCollection","features":[',
                     '{"type":"FeatureCollection","features":[{}]} trailing',
                     '{"type":"FeatureCollection","features":[{},]}',
                     '{"type":"FeatureCollection","features":{},"features":[]}',
                     '{"type":"Other","features":[]}', '{"features":[],"type":"FeatureCollection",}'):
            path = self.root / 'bad.json'
            path.write_text(text)
            with self.subTest(text=text), self.assertRaises(ValueError):
                list(geometry.iter_features(path, 7))

    def test_delivery_comparison_checks_every_decoded_byte_and_suffix(self):
        raw = b'0123456789' * 1000
        original, compressed = self.root / 'original.json', self.root / 'copy.gz'
        original.write_bytes(raw)
        with patch.object(geometry, 'CHUNK_SIZE', 97):
            for changed, equal in ((raw, True), (raw[:-1] + b'x', False), (raw + b'x', False), (raw[:-1], False)):
                compressed.write_bytes(gzip.compress(changed))
                digest, size, matches = geometry.delivery_digest(original, [compressed])
                self.assertEqual((digest, size, matches), (hashlib.sha256(raw).hexdigest(), len(raw), [equal]))

    def test_page_and_anchor_caches_evict_without_losing_fragment_checks(self):
        (self.root / 'content/places').mkdir(parents=True)
        (self.root / 'content/places/source-retention.json').write_text('{}')
        for index in range(120):
            (self.root / f'{index}.html').write_text('<title>Test</title><h1 id="good">Test</h1>')
        with patch.object(national, 'ROOT', self.root):
            validator = national.Validator(no_write=True)
            for index in range(120):
                validator.get_document(f'{index}.html')
                validator.local_link('0.html', f'{index}.html#good', 'test')
            self.assertLessEqual(len(validator.documents), 96)
            self.assertLessEqual(len(validator.anchor_cache), 96)
            self.assertNotIn('0.html', validator.documents)
            validator.local_link('0.html', '0.html#missing', 'test')
            self.assertTrue(any('missing fragment' in e for e in validator.errors))

    def test_national_geometry_keeps_identity_type_count_and_hash_guards(self):
        (self.root / 'content/places').mkdir(parents=True)
        (self.root / 'content/places/source-retention.json').write_text('{}')
        path = self.root / 'map.json'
        raw = json.dumps({'type': 'FeatureCollection', 'features': [Fixture.feature('one')]}).encode()
        path.write_bytes(raw)
        (self.root / 'map.gz').write_bytes(gzip.compress(raw))
        delivery = {'layers': [{'id': 'layer', 'sha256': hashlib.sha256(raw).hexdigest(), 'features': 1, 'compressed': 'map.gz'}]}
        (self.root / 'content/places/geometry-delivery.json').write_text(json.dumps(delivery))
        def validate():
            validator = national.Validator(no_write=True)
            validator.layers = {'layer': {'geometryFile': 'map.json', 'featureIdField': 'id', 'uncompressedSha256': hashlib.sha256(raw).hexdigest()}}
            validator.places = {'one': {'layerId': 'layer', 'featureId': 'one'}}
            validator.geometry()
            return validator
        with patch.object(national, 'ROOT', self.root):
            self.assertEqual(validate().errors, [])
            bad = Fixture.feature('wrong')
            bad['geometry']['type'] = 'Point'
            path.write_text(json.dumps({'type': 'FeatureCollection', 'features': [bad, bad]}))
            errors = '\n'.join(validate().errors)
            for message in ('gzip changes', 'duplicate feature', 'join(s) absent', 'unsupported/missing', 'SHA-256 differs', 'feature count differs', 'uncompressed hash differs'):
                self.assertIn(message, errors)


class RetainedProvenance(unittest.TestCase):
    def test_redland_archive_checkout_retains_reviewed_original_bytes(self):
        canonical = json.loads((ROOT / 'content/places/councils.json').read_text(encoding='utf-8'))
        source = next(s for s in canonical['sources'] if s['id'] == 'council-redland-profiles')
        self.assertEqual(hashlib.sha256((ROOT / source['rawFile']).read_bytes()).hexdigest(), source['sha256'])



class PublicationStages(Fixture):
    def publish_bindings(self):
        with patch.object(builder,'ROOT',self.root), patch.object(builder,'reviewed_page_entries',return_value=[{'path':r['url'],'lastUpdated':'2026-10-23'} for r in self.routes]),contextlib.redirect_stdout(io.StringIO()):
            builder.generate(builder.DEFAULT_VALIDATION,builder.DEFAULT_BROWSER,publication=True)

    def test_failed_browser_is_deferred_without_changing_report(self):
        self.browser['status']='NOT TESTED';self.write(builder.DEFAULT_BROWSER,self.browser)
        original=(self.root/builder.DEFAULT_BROWSER).read_bytes()
        with self.assertRaises(ValueError):evidence.require_current_evidence(self.root,self.validation,self.browser)
        result=evidence.require_current_evidence(self.root,self.validation,self.browser,require_browser=False)
        self.assertIsNone(result['browser']);self.publish_bindings()
        self.assertEqual((self.root/builder.DEFAULT_BROWSER).read_bytes(),original)
        self.assertEqual(contract.Validator(self.manifest(),self.root,publication=True).run()['result'],'PASS')
        self.assertEqual(self.validate()['result'],'FAIL')

    def test_missing_or_malformed_browser_does_not_gate_publication(self):
        for content in (None,'{malformed'):
            path=self.root/builder.DEFAULT_BROWSER
            if content is None:path.unlink()
            else:path.write_text(content)
            self.publish_bindings()
            self.assertEqual(contract.Validator(self.manifest(),self.root,publication=True).run()['result'],'PASS')
            self.assertEqual(self.validate()['result'],'FAIL')

    def test_publication_still_rejects_changed_data_geometry_and_pages(self):
        for name in ('content/places/councils.json','map.geojson','one.html'):
            path=self.root/name;original=path.read_bytes();self.write(name,{})
            with self.subTest(name=name),self.assertRaises(ValueError):
                evidence.require_current_evidence(self.root,self.validation,self.browser,require_browser=False)
            path.write_bytes(original)

    def test_publication_keeps_shared_structural_fingerprints(self):
        for name in (builder.DEFAULT_VALIDATION,'assets/civic-places.js',evidence.CONTRACT_SET):
            path=self.root/name;original=path.read_bytes();path.write_bytes(original+b' ')
            with self.subTest(name=name):self.assertEqual(contract.Validator(self.manifest(),self.root,publication=True).run()['result'],'FAIL')
            path.write_bytes(original)

    def test_errors_are_not_globally_suppressed(self):
        v=contract.Validator(self.manifest(),self.root,publication=True)
        for code in ('review-evidence-stale','source-hash','review-date-drift','recorded-horizontal-overflow'):v.error(code,'explicit failure')
        self.assertEqual(len(v.errors),4)
        self.assertEqual(v.deferred,[])

if __name__ == '__main__':
    unittest.main()
