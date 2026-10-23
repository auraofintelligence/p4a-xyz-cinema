"""Prepare an explicit public-source snapshot; never stage, commit, push or deploy.

Run from any directory with Python 3.10+: python scripts/prepare-github-upload.py
Outputs are outside this checkout by default. The archive contains the current
public tree, including prior working changes, rather than a selective Git patch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {
    '.gitattributes', '.gitignore', '.nojekyll', 'AGENTS.md', 'CNAME',
    'index.html', 'styles.css', 'script.js', 'site.webmanifest', 'README.md',
    'LICENCE.md', 'LOCALISE_WITH_AN_AGENT.md', 'REFRESH_WITH_AN_AGENT.md',
    'SUPPLIER-INTAKE.md', 'robots.txt', 'sitemap.xml', 'llms.txt',
}
PUBLIC_DIRS = ('.github', 'assets', 'backend', 'content', 'documents', 'docs', 'pages',
               'scripts', 'states', 'tools', 'qa/redland-20261017')
BLOCKED_DIRS = {'.git', '__pycache__', 'node_modules', 'public-polish-browser',
                'browser-profile', 'user-data-dir', 'tmp', 'upload-ready'}
TEXT_SUFFIXES = {'.md', '.html', '.js', '.mjs', '.json', '.py', '.ps1', '.css', '.txt', '.xml', '.gs'}
LOCAL_ONLY_FILES = set(json.loads((ROOT/'content/places/source-retention.json').read_text(encoding='utf-8')).get('localOnlyFiles', []))
SECRET_PATTERNS = [
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),
    re.compile(rb'github_pat_[A-Za-z0-9_]{50,}'),
    re.compile(rb'AKIA[0-9A-Z]{16}'),
]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip()


def excluded(path):
    return (path.parts[:3] == ('content', 'places', 'raw')
            or path.as_posix() in LOCAL_ONLY_FILES
            or any(part in BLOCKED_DIRS for part in path.parts)
            or path.name == '.env' or path.name.startswith('.env.')
            or path.suffix.lower() in {'.pyc', '.pyo', '.log', '.pem', '.key'}
            or path.name.lower() in {'id_rsa', 'id_ed25519', 'cookies', 'login data'})


def public_files():
    files = {ROOT / name for name in ROOT_FILES if (ROOT / name).is_file()}
    for folder in PUBLIC_DIRS:
        base = ROOT / folder
        if not base.is_dir():
            continue
        for directory, names, filenames in os.walk(base, followlinks=False):
            parent = Path(directory)
            names[:] = sorted(name for name in names if not excluded((parent/name).relative_to(ROOT))
                               and not (parent/name).is_symlink()
                               and not getattr(parent/name, 'is_junction', lambda: False)())
            for name in filenames:
                path = parent / name
                if not excluded(path.relative_to(ROOT)):
                    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
                        raise ValueError(f'Public-source path escapes checkout: {path.relative_to(ROOT)}')
                    files.add(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT.parent/'_upload-ready')
    parser.add_argument('--date', default=datetime.now(timezone(timedelta(hours=10))).date().isoformat(), help='Release label, not a source research date')
    args = parser.parse_args()
    if not re.fullmatch(r'\d{4}-\d\d-\d\d', args.date):
        parser.error('--date must use YYYY-MM-DD')
    output = args.output_dir.resolve()
    if output.is_relative_to(ROOT):
        parser.error('Keep upload output outside the checkout to avoid recursive packaging')
    files = public_files()
    tracked = set(git('ls-files').splitlines())
    included = {path.relative_to(ROOT).as_posix() for path in files}
    omitted_tracked = sorted(name for name in tracked if name not in included and not excluded(Path(name)))
    if omitted_tracked:
        raise ValueError('Review tracked files outside the public-source allowlist: '+', '.join(omitted_tracked[:12]))
    entries = []
    warnings = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        if len(raw) >= 100*1024*1024:
            raise ValueError(f'File exceeds the package Git-upload size gate: {relative}')
        if path.suffix.lower() in TEXT_SUFFIXES and any(pattern.search(raw) for pattern in SECRET_PATTERNS):
            raise ValueError(f'Possible credential material requires review in {relative}; value withheld')
        if len(raw) > 25*1024*1024:
            warnings.append({'path': relative, 'bytes': len(raw), 'note': 'Use Git rather than browser file upload; preserve exact source bytes.'})
        entries.append({'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    output.mkdir(parents=True, exist_ok=True)
    stem = f'p4a-xyz-cinema-public-source-{args.date}'
    archive = output/(stem+'.zip')
    record_path = output/(stem+'.manifest.json')
    created = datetime.now(timezone(timedelta(hours=10))).isoformat(timespec='seconds')
    record = {
        'schemaVersion': 1, 'releaseLabel': args.date, 'preparedAt': created,
        'source': str(ROOT), 'remote': git('remote', 'get-url', 'origin'),
        'branch': git('branch', '--show-current'), 'baseCommit': git('rev-parse', 'HEAD'),
        'scope': 'Complete current public-source allowlist, including existing uncommitted public work. Not a Git patch.',
        'gitIndexChanged': False, 'committed': False, 'pushed': False,
        'domain': (ROOT/'CNAME').read_text(encoding='utf-8').strip(),
        'fileCount': len(entries), 'uncompressedBytes': sum(entry['bytes'] for entry in entries),
        'includedDirectories': list(PUBLIC_DIRS),
        'retentionRegister': 'content/places/source-retention.json',
        'localOnlyFiles': sorted(LOCAL_ONLY_FILES),
        'excluded': ['.git', 'all QA except qa/redland-20261017', 'browser sessions and caches',
                     'dependencies', 'bytecode', 'temporary files', 'environment/key files', 'upload output',
                     'content/places/raw local-only original research snapshots; access does not grant republication rights'],
        'scopeNote': 'Preserves other current public changes; this preparation does not claim a fresh editorial audit of every page.',
        'checks': ['path allowlist', 'tracked-file completeness', 'source hashes', 'common credential signatures',
                   'per-file size gate', 'archive path/hash readback'],
        'largeFiles': warnings, 'files': entries,
    }
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as bundle:
        for entry in entries:
            bundle.write(ROOT/entry['path'], entry['path'])
        bundle.writestr('UPLOAD_MANIFEST.json', json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    with zipfile.ZipFile(archive) as bundle:
        if len(bundle.namelist()) != len(entries)+1 or bundle.testzip():
            raise ValueError('Archive readback failed')
        for entry in entries:
            if hashlib.sha256(bundle.read(entry['path'])).hexdigest() != entry['sha256']:
                raise ValueError('Archive content changed: '+entry['path'])
    record['archive'] = str(archive)
    record['archiveBytes'] = archive.stat().st_size
    record['archiveSha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: record[key] for key in ['fileCount','uncompressedBytes','archive','archiveBytes','archiveSha256','pushed']}, indent=2))
    print('Manifest: '+str(record_path))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as error:
        print('UPLOAD PREPARATION FAILED: '+str(error), file=sys.stderr)
        sys.exit(1)
