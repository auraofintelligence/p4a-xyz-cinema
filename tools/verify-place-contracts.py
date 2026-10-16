"""Run every registered civic-place contract without changing any files.

New council/state/federal builds register their manifest under content/ with a
unique name ending in -pattern-contract.json. No edit to this runner is needed.
Legacy Victoria checks remain separate until its wider journey is adapted.
"""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    manifests=sorted((ROOT/'content').rglob('*-pattern-contract.json'))
    if not manifests:
        print('FAIL: no civic-place contracts registered under content/')
        return 1
    failures=[]
    for manifest in manifests:
        relative=manifest.relative_to(ROOT).as_posix()
        print('Checking '+relative,flush=True)
        result=subprocess.run([sys.executable,str(ROOT/'tools/verify-council-pattern.py'),'--manifest',relative],cwd=ROOT)
        if result.returncode:
            failures.append(relative)
    print(f'{len(manifests)} registered contract(s); {len(failures)} failed.')
    return 1 if failures else 0

if __name__=='__main__':
    sys.exit(main())
