"""Per-route contracts use authored dates, never a global build timestamp."""
import importlib.util,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('contracts',ROOT/'tools/build-national-contracts.py')
contracts=importlib.util.module_from_spec(spec);spec.loader.exec_module(contracts)
class ContractDates(unittest.TestCase):
 def test_every_real_route_has_unique_authored_date(self):
  rows=json.loads((ROOT/'content/places/route-registry.json').read_text())['places']
  dates=contracts.registered_route_dates(ROOT,rows)
  self.assertEqual(len(dates),2080)
  for path,date in dates.items():
   text=(ROOT/path).read_text()
   self.assertIn('Page implementation updated <time datetime="'+date+'">'+date+'</time>',text,path)
 def test_missing_route_fails_without_fallback(self):
  with patch.object(contracts,'reviewed_page_entries',return_value=[]):
   with self.assertRaisesRegex(ValueError,'lacks a registered implementation date'):
    contracts.registered_route_dates(ROOT,[{'url':'missing.html'}])
 def test_distinct_dates_preserved(self):
  with patch.object(contracts,'reviewed_page_entries',return_value=[{'path':'a','lastUpdated':'2026-10-23'},{'path':'b','lastUpdated':'2026-11-02'}]):
   self.assertEqual(contracts.registered_route_dates(ROOT,[{'url':'a'},{'url':'b'}]),{'a':'2026-10-23','b':'2026-11-02'})
if __name__=='__main__':unittest.main()
