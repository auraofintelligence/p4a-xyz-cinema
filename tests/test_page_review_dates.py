"""Date provenance and generated-view parity, without advancing source dates."""
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import page_review_register as register


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


national = module('national_date_test', 'build-national-places.py')
redland = module('redland_date_test', 'build-redland.py')


class PageReviewDates(unittest.TestCase):
    def test_national_footer_uses_each_registered_date(self):
        rows = register.reviewed_page_entries(ROOT)
        for row in rows:
            rendered = national.shell(row['path'], 'Date test', '')
            self.assertIn('Page implementation updated <time datetime="' + row['lastUpdated'] + '">' + row['lastUpdated'] + '</time>', rendered, row['path'])
        self.assertEqual(national.UPDATED, '2026-10-23', 'Keep the original shared implementation date separate.')

    def test_queensland_index_uses_its_registered_date(self):
        path = 'states/qld/councils/index.html'
        expected = next(row['lastUpdated'] for row in register.reviewed_page_entries(ROOT) if row['path'] == path)
        rendered = redland.shell(path, 'Queensland', 'Date test', '')
        self.assertIn('datetime="' + expected + '"', rendered)

    def test_register_heading_uses_register_date_not_original_build_date(self):
        data = register.load_register()
        with patch.object(register, 'load_register', return_value={**data, 'updated': '2026-11-02'}):
            rendered = register.render_register('test.html', lambda page, path, label: label)
        self.assertIn('Page and rule register · updated 2 November 2026', rendered)
        self.assertIn('Nineteen new pages were verified on 17 October 2026', rendered)

    def test_markdown_renderer_preserves_all_canonical_dates(self):
        data = register.load_register()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'content/history').mkdir(parents=True)
            (root / 'docs/releases').mkdir(parents=True)
            (root / register.SOURCE).write_text(json.dumps(data))
            with patch.object(register, 'ROOT', root):
                register.write_review_notes()
            rendered = (root / 'docs/releases/2026-10-17-page-and-rule-register.md').read_text()
        for row in [entry for group in data['pageGroups'] for entry in group['pages']] + data['updatedExistingPages']:
            self.assertIn('](../../' + row['path'] + ') | ' + row['lastUpdated'] + ' |', rendered)

    def test_persisted_markdown_matches_canonical_dates(self):
        data = register.load_register()
        rendered = (ROOT / 'docs/releases/2026-10-17-page-and-rule-register.md').read_text()
        for row in [entry for group in data['pageGroups'] for entry in group['pages']] + data['updatedExistingPages']:
            self.assertIn('](../../' + row['path'] + ') | ' + row['lastUpdated'] + ' |', rendered, row['path'])

    def test_persisted_national_footers_match_canonical_dates(self):
        for row in register.reviewed_page_entries(ROOT):
            path = ROOT / row['path']
            if not path.exists():
                continue
            rendered = path.read_text()
            if 'Page implementation updated <time' not in rendered:
                continue
            found = re.search(r'Page implementation updated <time datetime="([^"]+)"', rendered)
            self.assertEqual(found.group(1), row['lastUpdated'], row['path'])


if __name__ == '__main__':
    unittest.main()
