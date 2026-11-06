import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("site_size", Path(__file__).resolve().parents[1] / "scripts/check-site-size.py")
size = importlib.util.module_from_spec(spec)
spec.loader.exec_module(size)


class SiteSizeTests(unittest.TestCase):
    def test_exact_byte_boundary_and_maps(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "assets/maps").mkdir(parents=True)
            (root / "assets/maps/exact.gz").write_bytes(bytes(range(16)))
            (root / "index.html").write_bytes(b"five!")
            names = ["assets/maps/exact.gz", "index.html"]
            report = size.measure(root, names, 22)
            self.assertTrue(report["underBudget"])
            self.assertEqual(report["trackedBytes"], 21)
            self.assertEqual(report["headroomBytes"], 1)
            self.assertEqual((report["mapFiles"], report["mapBytes"]), (1, 16))
            self.assertFalse(size.measure(root, names, 21)["underBudget"])
            self.assertFalse(size.measure(root, names, 20)["underBudget"])

    def test_missing_symlink_and_invalid_budget_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaises(ValueError):
                size.measure(root, ["missing.html"], 100)
            with self.assertRaises(ValueError):
                size.measure(root, [], 0)
            (root / "file").write_bytes(b"x")
            (root / "link").symlink_to(root / "file")
            with self.assertRaises(ValueError):
                size.measure(root, ["link"], 100)


if __name__ == "__main__":
    unittest.main()
