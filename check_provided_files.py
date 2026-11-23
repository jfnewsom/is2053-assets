#!/usr/bin/env python3
"""
check_provided_files.py - The same provided file, from two places, must be the
same file.

Students can get a provided file two ways: the download button on the
assignment sheet (served from pages/labs/data/) or the starter zip from Start
Here (downloads/is2053-starter.zip). Nothing kept those in step, and on
2026-08-09 they had drifted: the page was serving a lab-5-2.py that was 25 lines
different from the one in the zip and in the solution tree. The differences
happened to be output-identical refactors, so nobody would ever have noticed
from behaviour, which is exactly why it needed a guard rather than a reader.

Since Nov 22, 2026 the starter zip is retired (John: students make their
folders from Start Here, and VS Code's settings come from the IS2053
profile), so there is one copy of each provided file, the sheet's. What's
checked now:

  TRUTH      provided .py files match the solution tree, when it is
             reachable. The solution is the source of truth.

Before Nov 22, three things were checked:

  SYNC       every file under pages/labs/data/ is byte-identical to its
             counterpart in the starter zip, unless allowlisted below.
  TRUTH      provided .py files also match the solution tree, when it is
             reachable. The solution is the source of truth; the other two are
             copies of it.
  SCAFFOLD   the zip's zero-byte files are intentional. It ships correctly
             named empty files for everything the student writes, which is what
             stops submissions being rejected for filename mismatches. So an
             empty file is only an error if the sheet calls it PROVIDED.

    python3 check_provided_files.py
    python3 check_provided_files.py --solutions ~/path/to/IS2053/code/Modules
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(REPO, 'pages', 'labs', 'data')

# Deliberate differences between the two channels. Each needs a reason, and the
# reason is the point: without it this file slowly becomes a list of things
# somebody once decided not to look at.
ALLOWED = {
    '5-2/city.py':
        'Lab 5.2 students bring their own City class from Lab 5.1. The page '
        'serves a reference copy as a fallback for anyone whose 5.1 class '
        'does not work, so it is not held to the solution tree.',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def zip_key(lab, name):
    mod = lab.split('-')[0]
    return f'is2053/code/modules/mod{mod}/lab-{lab}/{name}'


def provided_names():
    """Files the lab sheets describe as provided, per lab."""
    out = {}
    for f in sorted(glob.glob(os.path.join(REPO, 'pages/labs/json/lab-*.json'))):
        lab = os.path.basename(f)[4:-5]
        d = json.load(open(f, encoding='utf-8'))

        def walk(o):
            if isinstance(o, dict):
                if 'file' in o and 'path' in o:
                    fmt = str(o.get('format', '')).lower()
                    if 'provided' in fmt or 'harness' in fmt:
                        out.setdefault(lab, set()).add(
                            re.sub(r'<[^>]+>', '', str(o['file'])).strip())
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solutions', help='root of the solution tree (optional)')
    a = ap.parse_args()

    problems = []
    checked = len(glob.glob(os.path.join(DATA, '*', '*')))

    # TRUTH
    if a.solutions:
        root = os.path.expanduser(a.solutions)
        for path in sorted(glob.glob(os.path.join(DATA, '*', '*.py'))):
            name = os.path.basename(path)
            rel = f'{os.path.basename(os.path.dirname(path))}/{name}'
            if rel in ALLOWED:
                continue
            hits = [h for h in glob.glob(os.path.join(root, '**', name), recursive=True)
                    if 'OLDIES' not in h and '__pycache__' not in h]
            if len(hits) == 1 and sha(open(path, 'rb').read()) != sha(open(hits[0], 'rb').read()):
                problems.append(
                    f'{rel} does not match the solution tree copy. The solution is the '
                    f'source of truth; sync the page to it.')

    print(f'check_provided_files: {checked} provided file(s) served from the sheets'
          + (', checked against the solutions' if a.solutions else ''))
    if problems:
        print('check_provided_files: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('check_provided_files: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
