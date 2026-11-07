"""Normalize public display punctuation without rewriting facts or source archives.
Run after content generators and before publication-qa/punctuation-qa.py.
Quoted/source/code blocks and HTML URL attributes remain byte-for-byte intact.
"""
from pathlib import Path
from public_punctuation import public_punctuation, plain_dashes
ROOT = Path(__file__).resolve().parents[1]

def main():
    paths = [ROOT / 'index.html', *sorted((ROOT / 'pages').rglob('*.html')),
             *sorted((ROOT / 'states').rglob('*.html')),
             *sorted((ROOT / 'content/rooms').glob('*.html'))]
    changed = []
    for path in paths:
        before = path.read_bytes().decode('utf-8')
        after = public_punctuation(before)
        if before != after:
            path.write_bytes(after.encode('utf-8'))
            changed.append(path.relative_to(ROOT).as_posix())
    # Audited display-only strings in these runtime files; no URL/code operators
    # contain these punctuation characters. Keep canonical factual data unchanged.
    for rel in ('assets/state-data.js', 'assets/vic-early-voting.js'):
        path = ROOT / rel
        before = path.read_bytes().decode('utf-8')
        after = plain_dashes(before)
        if before != after:
            path.write_bytes(after.encode('utf-8'))
            changed.append(rel)
    print(f'Normalized public punctuation in {len(changed)} files')

if __name__ == '__main__':
    main()
