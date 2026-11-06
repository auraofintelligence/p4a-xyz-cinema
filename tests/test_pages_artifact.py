import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("pages_artifact", Path(__file__).resolve().parents[1] / "scripts/prepare-pages-artifact.py")
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


class PagesArtifactTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "source"
        self.root.mkdir()
        self.paths = []

    def add(self, name, content=b"unchanged"):
        if name.endswith(".json") and content == b"unchanged":
            content = b"{}"
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        self.paths.append(name)

    def test_only_unreferenced_qa_rasters_are_omitted(self):
        self.add("tools/publication-qa/unreferenced.png")
        self.add("tools/publication-qa/referenced.png")
        self.add("tools/publication-qa/report.json", b'{"screenshot":"referenced.png"}')
        for name in ["assets/maps/exact.geojson", "assets/maps/exact.geojson.gz", "assets/maps/exact-data.js", "assets/maps/base.png", "content/licences/maps.md", "content/places/contracts/example.json", "qa/retained.png"]:
            self.add(name)
        included, omitted, refs = pack.plan(self.root, self.paths)
        self.assertEqual(omitted, ["tools/publication-qa/unreferenced.png"])
        self.assertEqual(len(included), len(self.paths) - 1)
        self.assertEqual(refs["tools/publication-qa/referenced.png"], ["tools/publication-qa/report.json"])

    def test_ambiguous_and_encoded_links_are_preserved(self):
        self.add("tools/publication-qa/a/saved map.png")
        self.add("tools/publication-qa/b/saved map.png")
        self.add("index.html", b'<img src="tools/publication-qa/a/saved%20map.png">')
        self.assertEqual(pack.plan(self.root, self.paths)[1], [])

    def test_copy_is_byte_identical_and_source_is_untouched(self):
        self.add("index.html", b"<h1>Exact</h1>\r\n")
        self.add("assets/maps/exact.geojson.gz", bytes(range(256)))
        self.add("tools/publication-qa/not-used.png", b"retained in source")
        output = self.root.parent / "artifact"
        result = pack.build(self.root, self.paths, output)
        self.assertTrue(result["copiedAndHashVerified"])
        self.assertEqual(result["mapFileCount"], 1)
        self.assertEqual(result["savedBytes"], len(b"retained in source"))
        for entry in result["files"]:
            self.assertEqual((output / entry["path"]).read_bytes(), (self.root / entry["path"]).read_bytes())
        self.assertTrue((self.root / "tools/publication-qa/not-used.png").exists())
        self.assertFalse((output / "tools/publication-qa/not-used.png").exists())

    def test_dynamic_runtime_qa_references_keep_all_candidates(self):
        self.add("tools/publication-qa/not-named.png")
        self.add("assets/viewer.js", b"const root = 'tools/publication-qa/'; const image = root + selected + '.png';")
        self.assertEqual(pack.plan(self.root, self.paths)[1], [])

    def test_svg_html_entities_and_tool_runtime_references_are_kept(self):
        self.add("tools/publication-qa/proof.png")
        for name, text in [("assets/drawing.svg", b'<image href="../tools/publication-qa/proof.png"/>'), ("proof.html", b'<img src="tools/publication-qa/proof&#46;png">'), ("tools/gallery.html", b'<script>const base = "publication-qa/"; const name = location.hash;</script>')]:
            with self.subTest(name=name):
                self.add(name, text)
                self.assertEqual(pack.plan(self.root, [self.paths[0], name])[1], [])

    def test_escaped_json_and_javascript_names_are_kept(self):
        self.add("tools/publication-qa/proof.png")
        self.add("content/data.json", b'{"screenshot":"pr\\u006fof.png"}')
        self.assertEqual(pack.plan(self.root, self.paths)[1], [])

    def test_source_or_existing_destination_is_never_overwritten(self):
        self.add("index.html")
        for destination in [self.root, self.root / "nested", self.root.parent]:
            with self.assertRaises(ValueError):
                pack.build(self.root, self.paths, destination)

    def test_only_unused_non_map_non_media_webp_originals_are_candidates(self):
        for name in ["assets/unused.png", "assets/unused.webp", "assets/active.jpg", "assets/active.webp", "assets/maps/exact.png", "assets/maps/exact.webp", "assets/media/cover.jpg", "assets/media/cover.webp", "assets/only-original.png"]:
            self.add(name)
        self.add("index.html", b'<img src="assets/active.jpg"><img src="assets/unused.webp">')
        self.assertEqual(pack.plan(self.root, self.paths)[1], ["assets/unused.png"])


if __name__ == "__main__":
    unittest.main()
