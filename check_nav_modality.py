#!/usr/bin/env python3
"""
check_nav_modality.py - nav.js and render_variant.py must agree on the list of
modalities.

WHY THIS EXISTS
Adding a modality is supposed to be a registry entry in render_variant.py. It
is not, quite: nav.js keeps its OWN copy of the same list, because it runs in
the browser and cannot import Python. Nothing checked that the two agreed.

The failure is silent and total. render_variant.py would happily build a third
tree, and every page in it would load a nav.js that does not recognise the new
directory, fall back to '/pages/', and send every student in that modality out
of their own tree on the first click. No error, no missing file, just the wrong
site.

So the duplication stays, since a browser cannot read the Python registry, but
it stops being unguarded. Two copies of a list with a check is a different
thing from two copies of a list.

Also asserts, for each declared modality:

  SYLLABUS KEY   nav.js's SYLLABUS map has an entry. A modality with no key
                 reads as `undefined`, which is falsy, so its Syllabus item
                 silently disappears rather than failing. Pending is `null`,
                 written on purpose; missing is a typo.
  TERM           any syllabus URL in nav.js names the current term. Duplicated
                 from check_syllabus_links.py deliberately: that file owns the
                 rule, this one owns nav.js, and the overlap costs nothing.

    python3 check_nav_modality.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
NAV = REPO / 'nav.js'
TERM = 'Fall-2026'


def nav_variants(src):
    m = re.search(r'const\s+VARIANTS\s*=\s*\[([^\]]*)\]', src)
    if not m:
        return None
    return [s.strip().strip('\'"') for s in m.group(1).split(',') if s.strip()]


def nav_syllabus_keys(src):
    m = re.search(r'const\s+SYLLABUS\s*=\s*\{(.*?)\n  \};?', src, re.S)
    if not m:
        return None
    return dict(re.findall(r'(\w+)\s*:\s*(null|\'[^\']*\')', m.group(1)))


def main():
    if not NAV.is_file():
        print(f'check_nav_modality: {NAV} not found')
        return 1
    src = NAV.read_text(encoding='utf-8')

    try:
        from render_variant import VARIANTS as REGISTRY
    except Exception as e:                              # pragma: no cover
        print(f'check_nav_modality: cannot import render_variant.py ({e})')
        return 1

    problems = []
    want = sorted(REGISTRY)

    got = nav_variants(src)
    if got is None:
        problems.append('nav.js has no `const VARIANTS = [...]`; the parser '
                        'below is guessing, so fix the name or fix this check')
    elif sorted(got) != want:
        problems.append(
            f'nav.js VARIANTS {sorted(got)} does not match the render_variant.py '
            f'registry {want}. Every page in a missing modality would fall back '
            f'to /pages/ and link students out of their own tree.')

    keys = nav_syllabus_keys(src)
    if keys is None:
        problems.append('nav.js has no SYLLABUS map to check')
    else:
        for v in want:
            if v not in keys:
                problems.append(
                    f'nav.js SYLLABUS has no "{v}" key. Undefined is falsy, so '
                    f'that modality would silently lose its Syllabus nav item. '
                    f'Write `{v}: null` if it is genuinely pending.')
        for v, val in keys.items():
            if v not in want:
                problems.append(f'nav.js SYLLABUS has key "{v}", which is not a '
                                f'registered modality')
            elif val != 'null' and TERM not in val:
                problems.append(f'nav.js SYLLABUS["{v}"] does not name {TERM}: {val}')

    if problems:
        print('check_nav_modality: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1

    pending = [v for v, val in (keys or {}).items() if val == 'null']
    note = f', {len(pending)} syllabus URL(s) pending ({", ".join(pending)})' if pending else ''
    print(f'check_nav_modality: PASS (nav.js and render_variant.py agree on '
          f'{want}{note})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
