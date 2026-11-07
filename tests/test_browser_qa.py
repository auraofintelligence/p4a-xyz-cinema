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

    def test_request_url_maps_root_nested_directory_and_queries(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'index.html').write_text('root')
            (root / 'nested').mkdir()
            (root / 'nested/index.html').write_text('nested')
            (root / 'nested/map data.js').write_text('asset')
            cases = {'/': 'index.html', '/?v=1': 'index.html',
                     '/nested': 'nested/index.html', '/nested/': 'nested/index.html',
                     '/nested/index.html?area=x': 'nested/index.html',
                     '/nested/map%20data.js?v=2': 'nested/map data.js'}
            for url, relative in cases.items():
                with self.subTest(url=url):
                    self.assertEqual(qa.served_repository_file(root, qa.BASE + url), root / relative)

    def test_request_url_mapping_rejects_traversal_and_other_origins(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'; root.mkdir()
            outside = Path(d) / 'private'; outside.write_text('private')
            (root / 'link').symlink_to(outside)
            urls = ['/../private', '/%2e%2e/private', '/nested/%2e%2e/private',
                    '/%2F../private', '/.git/config', '/link', '/missing',
                    '/nested%5c..%5cprivate', '//private']
            for suffix in urls:
                with self.subTest(url=suffix), self.assertRaises(ValueError):
                    qa.served_repository_file(root, qa.BASE + suffix)
            for url in ('https://example.com/index.html', qa.BASE + '/#fragment'):
                with self.subTest(url=url), self.assertRaises(ValueError):
                    qa.served_repository_file(root, url)

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

    def test_clock_observation_precedes_oracle_and_cannot_be_repaired(self):
        class Page:
            def __init__(self):
                self.calls = []
                self.live_text = 'Uninitialized delivered clock'

            def evaluate(self, script, arg=None):
                self.calls.append(script)
                if arg is None:
                    # This is the pre-import DOM observation, just as Playwright serializes it.
                    self_outer.assertNotIn('import(', script)
                    return {'now': 1000, 'module_declared': True, 'panels': [{'item': {'status': 'awaiting-confirmation'},
                        'actual': self.live_text, 'hidden': True, 'values': []}]}
                self_outer.assertIn('import(', script)
                self_outer.assertNotIn('querySelector', script)
                self.live_text = 'Awaiting confirmation to begin'  # Simulated module side effect.
                return [{'text': self.live_text, 'active': False}]

        self_outer = self
        page = Page()
        observed = qa.observe_clock_panels(page)
        with self.assertRaisesRegex(ValueError, 'Clock status mismatch'):
            qa.compare_clock_observation(page, observed)
        self.assertEqual(len(page.calls), 2)
        self.assertEqual(observed['panels'][0]['actual'], 'Uninitialized delivered clock')

    def test_clock_missing_script_fails_even_when_fallback_text_matches(self):
        from unittest.mock import Mock
        page = Mock()
        observed = {'now': 1000, 'module_declared': False, 'panels': [
            {'item': {'status': 'awaiting-confirmation'},
             'actual': 'Awaiting confirmation to begin', 'hidden': True, 'values': []}]}
        with self.assertRaisesRegex(ValueError, 'missing the Redland clock module'):
            qa.compare_clock_observation(page, observed)
        page.evaluate.assert_not_called()

    def test_clock_valid_observation_passes_without_dom_reread(self):
        from unittest.mock import Mock
        page = Mock()
        page.evaluate.return_value = [{'text': 'Awaiting confirmation to begin', 'active': False}]
        observed = {'now': 1000, 'module_declared': True, 'panels': [{'item': {'status': 'awaiting-confirmation'},
            'actual': 'Awaiting confirmation to begin', 'hidden': True, 'values': []}]}
        self.assertEqual(len(qa.compare_clock_observation(page, observed)), 1)
        self.assertIs(page.evaluate.call_args.args[1], observed)

    def test_settle_awaits_fonts_and_transition_without_suppressing_errors(self):
        from unittest.mock import Mock
        page = Mock()
        qa.settle_page(page)
        script = page.evaluate.call_args.args[0]
        self.assertIn('await document.fonts.ready', script)
        self.assertIn('await document.activeViewTransition.finished', script)
        self.assertNotIn('catch', script)
        page.wait_for_timeout.assert_called_once_with(750)
        page.evaluate.side_effect = RuntimeError('Transition failed')
        with self.assertRaisesRegex(RuntimeError, 'Transition failed'):
            qa.settle_page(page)

    def test_history_and_screenshot_wait_for_transition(self):
        import inspect
        source = inspect.getsource(qa.run)
        self.assertNotIn("animations='disabled'", source)
        for operation in ("page.go_back(wait_until='load')", "page.go_forward(wait_until='load')"):
            after = source.split(operation, 1)[1].lstrip()
            self.assertTrue(after.startswith('settle()'))
        self.assertTrue(source.split('def screenshot(label):', 1)[1].lstrip().startswith('settle()'))

    def test_scroll_sweep_visits_below_fold_then_restores_and_settles(self):
        class Page:
            y = 0
            def __init__(self):
                self.events = []
            def evaluate(self, script, arg=None):
                self.events.append(('evaluate', script, arg))
                if arg is not None:
                    self.y = min(arg, 1400)
                    return None
                return {'y': self.y, 'viewport': 600, 'height': 2000}
            def wait_for_timeout(self, ms):
                self.events.append(('wait', ms))
        page = Page()
        with patch.object(qa, 'settle_page', side_effect=lambda p: p.events.append(('settle',))):
            qa.reveal_by_scrolling(page)
        positions = [e[2] for e in page.events if e[0] == 'evaluate' and e[2] is not None]
        self.assertEqual(positions, [0, 480, 960, 1440, 0])
        self.assertEqual(page.events[-1], ('settle',))
        self.assertEqual(page.y, 0)
        scripts = '\n'.join(e[1] for e in page.events if e[0] == 'evaluate')
        for mutation in ('classList', '.style', 'setAttribute', 'reducedMotion', 'hidden ='):
            self.assertNotIn(mutation, scripts)
        import inspect
        capture = inspect.getsource(qa.run).split('def screenshot(label):', 1)[1].split('def layout', 1)[0]
        self.assertLess(capture.index('reveal_by_scrolling(page)'), capture.index('page.screenshot('))

    def test_scroll_sweep_bounds_endless_page_and_restores_on_failure(self):
        from unittest.mock import Mock
        page = Mock()
        page.evaluate.return_value = {'y': 0, 'viewport': 600, 'height': 1000000}
        with patch.object(qa, 'settle_page') as settle:
            with self.assertRaisesRegex(ValueError, 'exceeded 3 steps'):
                qa.reveal_by_scrolling(page, max_steps=3)
        self.assertEqual(page.evaluate.call_count, 8)  # start + 3 reads/scrolls + restoration
        self.assertEqual(page.evaluate.call_args.args[1], 0)
        settle.assert_called_once_with(page)

    def test_validate_does_not_launch_or_create_output(self):
        with tempfile.TemporaryDirectory() as d, patch.object(qa, 'run') as run:
            output = Path(d) / 'unused'
            self.assertEqual(qa.main(['--validate-only', '--output', str(output)]), 0)
            run.assert_not_called()
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
