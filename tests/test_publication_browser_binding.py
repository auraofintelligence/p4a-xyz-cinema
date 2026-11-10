"""Explicit historical browser bindings do not replace current data checks."""
import importlib.util,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('validator',ROOT/'tools/verify-council-pattern.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class BrowserBindings(unittest.TestCase):
 def run_binding(self, publication, browser_only, path='data.json'):
  with tempfile.TemporaryDirectory() as directory:
   Path(directory,path).write_text('{}')
   v=m.Validator({},root=directory,publication=publication)
   v.verify_evidence({'reviewedOn':'2026-10-17','paths':[], 'artifactFingerprints':[{'path':path,'sha256':'stale','browserOnly':browser_only}], 'requiredHumanChecks':['browser'], 'limitations':['historical']})
   return v
 def test_explicit_browser_binding_deferred_for_publication(self):
  v=self.run_binding(True,True);self.assertFalse(v.errors);self.assertEqual(v.deferred[0]['code'],'browser-binding-deferred')
 def test_strict_acceptance_still_rejects_stale_browser_binding(self):
  self.assertEqual(self.run_binding(False,True).errors[0]['code'],'review-evidence-stale')
 def test_nonbrowser_fingerprint_still_required(self):
  self.assertEqual(self.run_binding(True,False).errors[0]['code'],'review-evidence-stale')
 def test_renderer_binding_deferred_only_with_explicit_browser_marker(self):
  self.assertFalse(self.run_binding(True,True,'renderer.py').errors)
  self.assertEqual(self.run_binding(True,False,'renderer.py').errors[0]['code'],'review-evidence-stale')
  self.assertEqual(self.run_binding(False,True,'renderer.py').errors[0]['code'],'review-evidence-stale')
if __name__=='__main__':unittest.main()
