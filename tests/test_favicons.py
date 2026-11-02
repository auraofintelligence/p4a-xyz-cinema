import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('favicons', Path(__file__).resolve().parents[1]/'tools/check-favicons.py')
favicons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(favicons)

class FaviconChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for directory in ('assets', 'pages', 'states/qld/councils/redland', 'content/rooms'):
            (self.root/directory).mkdir(parents=True, exist_ok=True)
        (self.root/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        (self.root/'index.html').write_text('<link rel="icon" href="assets/favicon.svg">')

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_depths(self):
        (self.root/'pages/example.html').write_text('<link rel="icon" href="../assets/favicon.svg">')
        (self.root/'content/rooms/example.html').write_text('<link rel="icon" href="../../assets/favicon.svg">')
        (self.root/'states/qld/councils/redland/index.html').write_text('<link rel="icon" href="/assets/favicon.svg">')
        self.assertEqual(favicons.verify(self.root)['publicPages'], 3)

    def test_missing_declaration(self):
        (self.root/'pages/example.html').write_text('<title>Missing</title>')
        with self.assertRaisesRegex(AssertionError, 'missing rel=icon'):
            favicons.verify(self.root)

    def test_wrong_source_depth(self):
        (self.root/'content/rooms/example.html').write_text('<link rel="icon" href="../assets/favicon.svg">')
        with self.assertRaisesRegex(AssertionError, 'missing or out-of-root icon'):
            favicons.verify(self.root)

    def test_invalid_svg(self):
        (self.root/'assets/favicon.svg').write_text('<html/>')
        with self.assertRaisesRegex(AssertionError, 'invalid SVG root'):
            favicons.verify(self.root)

if __name__ == '__main__':
    unittest.main()
