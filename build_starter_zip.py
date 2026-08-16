#!/usr/bin/env python3
"""
build_starter_zip.py - Generate downloads/is2053-starter.zip from source.

The starter zip was hand-assembled for its first two terms, which is how
test.py went missing from lab-5-1/ (ledger F-043) and how the Lab 5.1 data
files stayed on their Module 4 versions for a term after the solution moved on.
Both were found by reading the zip, not by building it. This builds it.

The zip is a WORKSPACE, not a code drop. Two kinds of file live in it:

  REAL       data files and provided code, copied byte-for-byte out of
             pages/labs/data/. check_provided_files.py enforces that these
             stay identical to what the assignment sheets serve.

  SCAFFOLD   zero-byte files, correctly named, one for every file the student
             is expected to write. This is deliberate and it is the single
             most useful thing the zip does: a student who opens the folder
             and types into the file that is already there cannot submit
             lab5-1.py or Lab_5_1.py and have CodeGrade reject it on the
             filename.

Nothing here is a hand-maintained list. The inventory is derived:

  BookEx      pages/bookex/json/bookex-ch*.json - every .py named in the
              sheet, cross-checked against meta.programCount.
  Labs        pages/labs/json/lab-*.json - meta.filename plus every
              overview.dataFiles entry. Entries WITH a path are real files
              pulled from pages/labs/data/; entries WITHOUT one are files the
              student supplies, so they ship as scaffolds.
  Data        everything under pages/labs/data/<lab>/ is included whether or
              not the sheet declares it, because check_provided_files.py
              requires the two to agree.

Builds are deterministic: fixed timestamps, sorted entries, fixed compression.
Re-running with no source change produces a byte-identical zip, so a diff on
downloads/is2053-starter.zip always means something actually changed.

    python3 build_starter_zip.py
    python3 build_starter_zip.py --check     # fail if the zip is out of date
"""
import argparse
import glob
import hashlib
import json
import io
import os
import re
import sys
import zipfile

REPO = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(REPO, 'downloads', 'is2053-starter.zip')
DATA = os.path.join(REPO, 'pages', 'labs', 'data')
ROOT = 'is2053'

# Fixed so the build is reproducible. Bump only when you want every entry's
# date to move; it has no meaning to students.
STAMP = (2026, 8, 16, 0, 0, 0)

VSCODE = """{
  "editor.rulers": [4, 8, 79],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "files.eol": "\\n",
  "python.REPL.enableREPLSmartSend": false
}
"""

# Files served from pages/labs/data/ that must ship EMPTY in the zip instead.
# Mirrors ALLOWED in check_provided_files.py; keep the two in step.
FORCE_EMPTY = {
    '5-2/city.py':
        'Lab 5.2 students bring their own City class forward from Lab 5.1. '
        'The page serves a working reference implementation as a fallback; '
        'the zip must not hand them a finished answer.',
}

# Scaffolds a sheet needs but does not declare in dataFiles.
EXTRA_SCAFFOLDS = {
    '5-2': {'function_library.py':
            'lab-5-2.py imports it, but 5.2 submits player.py alone so the '
            'sheet never lists it. Without the scaffold the provided main '
            'will not run in a fresh folder.'},
}


def lab_dir(lab):
    return f'{ROOT}/code/modules/mod{lab.split("-")[0]}/lab-{lab}'


def bookex_programs(path):
    """The .py files a BookEx sheet assigns, verified against programCount."""
    doc = json.load(open(path, encoding='utf-8'))
    blob = json.dumps(doc)
    names = sorted({n for n in re.findall(r'[A-Za-z0-9_\-]+\.py', blob)
                    if not n.startswith('bookex-')})
    declared = doc['meta'].get('programCount')
    if declared is not None and declared != len(names):
        raise SystemExit(
            f'build_starter_zip: {os.path.basename(path)} says programCount='
            f'{declared} but {len(names)} .py files are named in the sheet: '
            f'{names}. One of the two is wrong; fix the sheet before building.')
    return doc['meta']['chapterId'].replace('bookex-', ''), names


def collect():
    """Return {archive path: bytes|None}. None means a zero-byte scaffold."""
    files = {}

    def put(path, blob):
        if path in files and files[path] != blob:
            raise SystemExit(f'build_starter_zip: conflicting content for {path}')
        files[path] = blob

    def workspace(folder):
        put(f'{folder}/.vscode/settings.json', VSCODE.encode())

    # Start Here: the very first file, before any module.
    put(f'{ROOT}/start_here/hello.py', None)
    workspace(f'{ROOT}/start_here')

    # BookEx: every assigned program, as a scaffold.
    for src in sorted(glob.glob(os.path.join(REPO, 'pages/bookex/json/bookex-ch*.json'))):
        chapter, programs = bookex_programs(src)
        folder = f'{ROOT}/code/bookex/{chapter}'
        for name in programs:
            put(f'{folder}/{name}', None)
        workspace(folder)

    # Labs.
    for src in sorted(glob.glob(os.path.join(REPO, 'pages/labs/json/lab-*.json'))):
        lab = os.path.basename(src)[4:-5]
        doc = json.load(open(src, encoding='utf-8'))
        folder = lab_dir(lab)

        # Real files: everything the assignment page serves for this lab.
        for path in sorted(glob.glob(os.path.join(DATA, lab, '*'))):
            name = os.path.basename(path)
            rel = f'{lab}/{name}'
            put(f'{folder}/{name}',
                None if rel in FORCE_EMPTY else open(path, 'rb').read())

        # The submitted file, and anything the student supplies themselves.
        put(f'{folder}/{doc["meta"]["filename"]}', None)
        for entry in doc.get('overview', {}).get('dataFiles', []) or []:
            name = re.sub(r'<[^>]+>', '', str(entry.get('file', ''))).strip()
            if name and not entry.get('path'):
                put(f'{folder}/{name}', None)
        for name in EXTRA_SCAFFOLDS.get(lab, {}):
            put(f'{folder}/{name}', None)

        workspace(folder)

    # Somewhere to try things out that is not a graded folder.
    put(f'{ROOT}/scratch/.keep', b'')
    workspace(f'{ROOT}/scratch')

    return files


def build(files):
    buf = io.BytesIO()
    dirs = set()
    for path in files:
        parts = path.split('/')[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add('/'.join(parts[:i]) + '/')

    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for d in sorted(dirs):
            info = zipfile.ZipInfo(d, STAMP)
            info.external_attr = (0o40755 << 16) | 0x10
            z.writestr(info, b'')
        for path in sorted(files):
            info = zipfile.ZipInfo(path, STAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, files[path] or b'')
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='exit non-zero if the committed zip is out of date')
    args = ap.parse_args()

    files = collect()
    blob = build(files)

    scaffolds = sum(1 for v in files.values() if not v)
    real = len(files) - scaffolds
    print(f'build_starter_zip: {len(files)} files '
          f'({real} real, {scaffolds} scaffold) in {len(blob):,} bytes')

    if args.check:
        if not os.path.isfile(ZIP):
            print('build_starter_zip: FAIL - the zip has never been built')
            return 1
        if hashlib.sha256(open(ZIP, 'rb').read()).digest() != hashlib.sha256(blob).digest():
            print('build_starter_zip: FAIL - downloads/is2053-starter.zip is '
                  'out of date. Run python3 build_starter_zip.py')
            return 1
        print('build_starter_zip: PASS')
        return 0

    os.makedirs(os.path.dirname(ZIP), exist_ok=True)
    open(ZIP, 'wb').write(blob)
    print(f'build_starter_zip: wrote {os.path.relpath(ZIP, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
