#!/usr/bin/env python3
"""
render_904.py - Generate the section-904 (in-person) variant of the course site.

Mirrors the entire pages/ tree into 904/ at the repo root, stripping every
region delimited by sentinel comments:

    <!-- RECORDINGS:START --> ... <!-- RECORDINGS:END -->
    <!-- VIDEO:START -->      ... <!-- VIDEO:END -->

Because the whole tree is mirrored, all relative links between pages keep
working with no rewriting. The 904 Canvas shell points its iframes at
/904/... paths; every other shell uses /pages/... paths.

Run AFTER render_modules.py and any render_lab.py calls, from the repo root:

    python3 render_904.py

The 904/ directory is fully regenerated on every run (safe to delete).
Non-HTML files (data files, images) are copied unchanged.
"""
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages'
DST = REPO / '904'

SENTINELS = [
    (re.compile(r'\s*<!-- RECORDINGS:START -->.*?<!-- RECORDINGS:END -->', re.DOTALL), 'RECORDINGS'),
    (re.compile(r'\s*<!-- VIDEO:START -->.*?<!-- VIDEO:END -->', re.DOTALL), 'VIDEO'),
]


def main():
    if not SRC.is_dir():
        sys.exit('render_904.py: pages/ not found; run from the repo root.')

    if DST.exists():
        shutil.rmtree(DST)

    stripped_files = 0
    leaked = []
    escaped = []

    for src_file in sorted(SRC.rglob('*')):
        rel = src_file.relative_to(SRC)
        # Source-of-truth folders (JSON authoring sources) are never mirrored.
        # 904/ contains rendered output only; the single source lives in pages/.
        # Image assets are also skipped: they are linked by absolute URL and
        # load from the single pages/ copy in both trees.
        if 'json' in rel.parts or 'images' in rel.parts:
            continue
        dst_file = DST / rel
        if src_file.is_dir():
            dst_file.mkdir(parents=True, exist_ok=True)
            continue
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        if src_file.suffix.lower() == '.html':
            text = src_file.read_text(encoding='utf-8')
            original = text
            for pattern, _name in SENTINELS:
                text = pattern.sub('', text)
            # Absolute PAGE links into the pages/ tree must stay inside the
            # 904/ mirror, or one click sends a 904 student back to the main
            # site. Asset URLs (images, data files, scripts) are NOT rewritten:
            # assets are identical across sections and load from the single
            # pages/ copy.
            text = re.sub(
                r'is2053-assets/pages/([^"\')\s]*?\.html(?:[#?][^"\')\s]*)?)',
                r'is2053-assets/904/\1',
                text)
            if text != original:
                stripped_files += 1
            # Safety net: no Panopto reference may survive in the 904 tree.
            if 'panopto' in text.lower():
                leaked.append(str(rel))
            # Safety net: no PAGE link may escape back into the pages/ tree.
            # Asset URLs into pages/ are intentional (single asset copy);
            # .html links and relative ../pages/ climbs are escapes.
            # (Guards baked HTML; runtime-generated links live in nav.js.)
            if re.search(r'is2053-assets/pages/[^"\')\s]*\.html', text) \
                    or re.search(r'\.\./+pages/', text):
                escaped.append(str(rel))
            dst_file.write_text(text, encoding='utf-8')
        else:
            shutil.copy2(src_file, dst_file)

    print(f'render_904: mirrored pages/ -> 904/ ({stripped_files} files had video content stripped)')
    if leaked:
        print('render_904: WARNING - Panopto references survived stripping in:')
        for f in leaked:
            print(f'  904/{f}')
        print('Wrap those embeds in VIDEO:START/END sentinels and re-run.')
        sys.exit(1)
    if escaped:
        print('render_904: WARNING - links escaping to /pages/ found in:')
        for f in escaped:
            print(f'  904/{f}')
        print('These bypass the URL rewrite; investigate the source pages.')
        sys.exit(1)
    print('render_904: verified zero Panopto references and zero /pages/ escape links in 904/ tree.')


if __name__ == '__main__':
    main()
