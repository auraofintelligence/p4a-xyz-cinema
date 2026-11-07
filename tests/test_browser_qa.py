"""No browser, server, dependency installation or external requests in unit tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('browser_qa', ROOT / 'tools/browser-qa/run.py')
qa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qa)


class BrowserQATest(unittest.TestCase):
    def test_baseline_configuration(self):
        scope = qa.load_scope(ROOT, ROOT / 'tools/browser-qa/smoke-scope.json')
        self.assertEqual([v['width'] for v in scope['viewports']], [390, 680, 1440])
        self.assertEqual(len(scope['map_journeys']), 2)

    def test_path_validation(self):
        for p in ('../README.md', '/README.md', 'https://example.com/a.html',
                  'README.md?x=1', 'README.md#x', 'a\\b', '%2e%2e/a', './README.md', 'a//b'):
            with self.subTest(p=p), self.assertRaises(ValueError):
                qa.site_file(ROOT, p)
        self.assertEqual(qa.site_file(ROOT, 'README.md'), ROOT / 'README.md')

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'; root.mkdir()
            outside = Path(d) / 'private'; outside.write_text('x')
            (root / 'link').symlink_to(outside)
            with self.assertRaises(ValueError):
                qa.site_file(root, 'link')

    def test_scope_malformed_or_missing_files(self):
        source = json.loads((ROOT / 'tools/browser-qa/smoke-scope.json').read_text())
        for mutation in [lambda s: s.update(schema_version=9),
                         lambda s: s.update(viewports=[{'width': True, 'height': 844}]),
                         lambda s: s['pages'][0].update(path='missing.html'),
                         lambda s: s['pages'][0].update(expected_text=['']),
                         lambda s: s.update(pages=[]),
                         lambda s: s['map_journeys'][0].update(destination='README.md')]:
            s = json.loads(json.dumps(source)); mutation(s)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=ROOT) as f:
                f.write(json.dumps(s)); f.flush()
                with self.assertRaises((ValueError, KeyError)):
                    qa.load_scope(ROOT, Path(f.name))

    def test_output_does_not_overwrite_content_or_prior_evidence(self):
        with self.assertRaises(ValueError):
            qa.output_directory(ROOT, ROOT / 'content/places/qa')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'results'
            qa.output_directory(ROOT, p)
            (p / 'report.json').write_text('existing evidence')
            with self.assertRaises(ValueError):
                qa.output_directory(ROOT, p)

    def test_exact_commit_and_hash_provenance(self):
        scope_path = ROOT / 'tools/browser-qa/smoke-scope.json'
        scope = qa.load_scope(ROOT, scope_path)
        with patch.object(qa.subprocess, 'check_output', side_effect=['a' * 40 + '\n', ' M README.md\n']) as git, patch.dict(qa.os.environ, {'GITHUB_SHA': 'b' * 40}):
            result = qa.provenance(ROOT, scope_path, scope)
        self.assertEqual(result['tested_commit'], 'a' * 40)
        self.assertEqual(result['github']['GITHUB_SHA'], 'b' * 40)
        self.assertEqual(git.call_args_list[0].args[0][-2:], ['rev-parse', 'HEAD'])
        self.assertEqual(result['scope_sha256'], qa.digest(scope_path))
        self.assertEqual(result['files_sha256']['pages/states.html'], qa.digest(ROOT / 'pages/states.html'))

    def test_result_failure_propagation_and_visual_pending(self):
        for checks, expected in [([], 1), ([{'status': 'FAIL'}], 1), ([{'status': 'PASS'}], 0)]:
            with tempfile.TemporaryDirectory() as d:
                report = {'checks': checks, 'screenshots': []}
                self.assertEqual(qa.finish(report, Path(d)), expected)
                self.assertEqual(report['visual_review']['status'], 'PENDING')
                self.assertTrue((Path(d) / 'index.html').is_file())

    def test_artifact_hashes_bind_visual_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / '390-page-0.png').write_bytes(b'image evidence')
            (output / '390-trace.zip').write_bytes(b'trace evidence')
            report = {'checks': [{'status': 'PASS'}], 'screenshots': ['390-page-0.png']}
            qa.finish(report, output)
            self.assertEqual(report['artifact_sha256']['390-page-0.png'], qa.digest(output / '390-page-0.png'))
            self.assertEqual(report['artifact_sha256']['390-trace.zip'], qa.digest(output / '390-trace.zip'))

    def test_runner_exception_writes_failure_report(self):
        with tempfile.TemporaryDirectory() as d, patch.object(qa, 'run', side_effect=RuntimeError('browser unavailable')), patch.object(qa, 'provenance', return_value={'tested_commit': 'a' * 40, 'working_tree_status': ''}):
            output = Path(d) / 'result'
            code = qa.main(['--output', str(output)])
            result = json.loads((output / 'report.json').read_text())
            self.assertEqual(code, 1)
            self.assertEqual(result['automated_status'], 'FAIL')
            self.assertIn('browser unavailable', result['checks'][0]['error'])

    def test_scope_must_be_in_repository(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'; root.mkdir()
            outside = Path(d) / 'scope.json'
            outside.write_text('{}')
            (root / 'scope.json').symlink_to(outside)
            for scope in (outside, root / 'scope.json'):
                with self.assertRaisesRegex(ValueError, 'inside the repository'):
                    qa.load_scope(root, scope)

    def test_dirty_checkout_cannot_pass(self):
        with tempfile.TemporaryDirectory() as d, patch.object(qa, 'run') as run, patch.object(qa, 'provenance', return_value={'tested_commit': 'a' * 40, 'working_tree_status': ' M pages/states.html'}):
            output = Path(d) / 'result'
            self.assertEqual(qa.main(['--output', str(output)]), 1)
            run.assert_not_called()
            result = json.loads((output / 'report.json').read_text())
            self.assertIn('dirty working tree', result['checks'][0]['error'])

    def test_validate_does_not_launch_or_create_output(self):
        with tempfile.TemporaryDirectory() as d, patch.object(qa, 'run') as run:
            output = Path(d) / 'unused'
            self.assertEqual(qa.main(['--validate-only', '--output', str(output)]), 0)
            run.assert_not_called()
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
