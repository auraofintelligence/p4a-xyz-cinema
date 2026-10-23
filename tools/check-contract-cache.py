"""Regress bounded-cache overflow without changing contract validation semantics."""
import importlib.util
from pathlib import Path,PureWindowsPath

spec=importlib.util.spec_from_file_location('contract_runner',Path(__file__).with_name('verify-place-contracts.py'))
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
cache=runner.BoundedPageCache()
keys=[PureWindowsPath(f'C:/fixture/{i}.html') for i in range(240)]
for i in range(96):cache[keys[i]]=i
assert cache[keys[0]]==0
cache[keys[96]]=96
assert len(cache)==96 and keys[0] in cache and keys[1] not in cache
for i in range(97,240):cache[keys[i]]=i
assert len(cache)==96
assert set(cache)==set(keys[144:])
for i in range(144,240):assert cache[keys[i]]==i
cache[keys[144]]='updated'
assert len(cache)==96 and cache[keys[144]]=='updated'
assert next(reversed(cache))==keys[144]
print('PASS: cache overflow, LRU eviction, retained reads and replacement preserve 96 complete entries')
