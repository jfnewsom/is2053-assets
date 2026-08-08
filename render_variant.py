#!/usr/bin/env python3
"""
render_variant.py - Generate per-modality variants of the course site.

Replaces render_904.py (2026-08-08). The old name encoded a section number,
which churns every term, into a directory path, a script name, nav.js, and every
Canvas iframe URL. Modality does not churn; section numbers do. Variants are now
named for what they are, and adding one is a config entry rather than a fork of
this script.

    pages/   the single source of truth. AUTHORING ONLY. No Canvas shell should
             point at it, so its layout can change without touching Canvas.
    onl/     the online variant, generated. A full copy; nothing is stripped.
    f2f/     the face-to-face variant, generated. Recordings and video removed.

WHY onl/ EXISTS WHEN IT IS IDENTICAL TO pages/
Until 2026-08-08 the online sections pointed straight at /pages/, which welded
every online Canvas URL to the name of the authoring directory. Giving online
its own build output decouples the two: the winter move to content/ plus build/
becomes invisible to Canvas instead of requiring a URL migration across three
shells. The duplication is the price of that decoupling, and it is cheap.

WHAT A VARIANT IS TODAY
Every difference is a REMOVAL. Regions wrapped in sentinel comments are stripped:

    <!-- RECORDINGS:START --> ... <!-- RECORDINGS:END -->
    <!-- VIDEO:START -->      ... <!-- VIDEO:END -->

As of 2026-08-08 that is 7 pages of real difference (home, start-here, and the
five module overviews) out of 79 that are byte-identical. If a variant ever needs
to REPLACE content rather than remove it, sentinels stop being enough and this
grows an overlay directory of per-variant override sources. See the winter target
in the ops Decisions Log before adding that.

WHY THE WHOLE TREE IS MIRRORED
Only a handful of pages differ, but every page is emitted so that relative links
keep working and every Canvas URL for a modality shares one prefix. Authoring the
diff and serving the whole tree are different problems; this script serves.

Run AFTER all content renderers, from the repo root:

    python3 render_variant.py            # all variants
    python3 render_variant.py f2f        # just one

Each variant directory is fully regenerated on every run (safe to delete).
Non-HTML files (data files) are copied unchanged. JSON sources and images are
never mirrored: sources live only in pages/, and images load by absolute URL
from the single pages/ copy.
"""
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages'

# ── Variant registry ─────────────────────────────────────────────────
# Add a modality by adding an entry. Nothing else in this file changes.
# 'dir'    output directory at the repo root, and the URL prefix
# 'strip'  sentinel names removed for this variant
# 'label'  human name, used only in output
#
# Keys are three letters on purpose (onl, f2f, and hyb if it ever lands). They
# are also directory names and URL prefixes, so equal width keeps the registry,
# the sentinel names, and every Canvas URL aligned. Match it when adding one.
VARIANTS = {
    'onl': {
        'dir': 'onl',
        'label': 'online',
        'strip': ['F2F_ONLY'],
    },
    'f2f': {
        'dir': 'f2f',
        'label': 'face-to-face',
        'strip': ['RECORDINGS', 'VIDEO', 'ONL_ONLY'],
    },
    # 'hyb': {'dir': 'hyb', 'label': 'hybrid',
    #         'strip': ['RECORDINGS', 'ONL_ONLY', 'F2F_ONLY']},
}

# Every variant must strip every other variant's ONLY block, or a page ends up
# showing two modalities' worth of content. Deriving that here means adding a
# variant cannot silently forget one.
for _name, _cfg in VARIANTS.items():
    for _other, _sentinel in (('onl', 'ONL_ONLY'), ('f2f', 'F2F_ONLY')):
        if _name != _other and _sentinel not in _cfg['strip']:
            _cfg['strip'].append(_sentinel)

SENTINEL_NAMES = ['RECORDINGS', 'VIDEO', 'ONL_ONLY', 'F2F_ONLY']
SENTINEL_PATTERNS = {
    name: re.compile(rf'\s*<!-- {name}:START -->.*?<!-- {name}:END -->', re.DOTALL)
    for name in SENTINEL_NAMES
}
# A sentinel this variant was told to strip must not survive into its tree; if
# one does, the pattern and the emitted comment disagree and a student sees the
# other modality's content. Sentinels NOT in the strip list are supposed to
# remain: onl/ keeps RECORDINGS and VIDEO because online sees the full site.
ANY_SENTINEL = re.compile(r'<!-- ([A-Z_]+):(?:START|END) -->')


def build(name, cfg):
    dst_root = REPO / cfg['dir']

    # Preferred path: wipe and regenerate, so deleted source pages cannot
    # survive as ghosts in the variant tree.
    #
    # Fallback: some environments cannot delete files at all. A Cowork cloud
    # session reaching this repo over the device bridge is one: rm is denied,
    # so rmtree raises PermissionError and the old script died here. Rather
    # than fail, overwrite in place and report anything stale so a human can
    # remove it. Overwriting is safe; only stale-file removal is lost.
    clean_wipe = True
    if dst_root.exists():
        try:
            shutil.rmtree(dst_root)
        except PermissionError:
            clean_wipe = False
            print(f'render_variant [{name}]: cannot delete in this environment; '
                  f'overwriting {cfg["dir"]}/ in place instead.')

    patterns = [SENTINEL_PATTERNS[s] for s in cfg['strip']]
    stripped_files = 0
    leaked, escaped, survivors = [], [], set()
    written = set()

    for src_file in sorted(SRC.rglob('*')):
        rel = src_file.relative_to(SRC)
        # Authoring sources and shared assets are never mirrored.
        if 'json' in rel.parts or 'images' in rel.parts or '_to_delete' in rel.parts:
            continue
        dst_file = dst_root / rel
        if src_file.is_dir():
            dst_file.mkdir(parents=True, exist_ok=True)
            continue
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        if src_file.suffix.lower() == '.html':
            text = original = src_file.read_text(encoding='utf-8')
            for pattern in patterns:
                text = pattern.sub('', text)
            # Absolute PAGE links into pages/ must stay inside this variant, or
            # one click sends a student back to the online site. Asset URLs are
            # NOT rewritten: assets are identical and load from the pages/ copy.
            text = re.sub(
                r'is2053-assets/pages/([^"\')\s]*?\.html(?:[#?][^"\')\s]*)?)',
                rf'is2053-assets/{cfg["dir"]}/\1',
                text)
            if text != original:
                stripped_files += 1
            # A variant that strips VIDEO must not carry video it did not author.
            # It MAY carry its own: as of 2026-08-08 the welcome video is per
            # modality, so f2f gets its own recording rather than nothing, fenced
            # in an F2F_ONLY block that survives into this tree by design. So the
            # check is "no Panopto OUTSIDE my own ONLY block", not "no Panopto".
            if 'VIDEO' in cfg['strip']:
                own = re.compile(rf'<!-- {name.upper()}_ONLY:START -->.*?'
                                 rf'<!-- {name.upper()}_ONLY:END -->', re.DOTALL)
                if 'panopto' in own.sub('', text).lower():
                    leaked.append(str(rel))
            if re.search(r'is2053-assets/pages/[^"\')\s]*\.html', text) \
                    or re.search(r'\.\./+pages/', text):
                escaped.append(str(rel))
            for m in ANY_SENTINEL.finditer(text):
                if m.group(1) in cfg['strip']:
                    survivors.add((str(rel), m.group(1)))
            dst_file.write_text(text, encoding='utf-8')
        else:
            shutil.copy2(src_file, dst_file)
        written.add(dst_file.resolve())

    print(f'render_variant [{name}]: mirrored pages/ -> {cfg["dir"]}/ '
          f'({stripped_files} files changed for the {cfg["label"]} modality)')

    ok = True

    if not clean_wipe:
        stale = [p for p in sorted(dst_root.rglob('*'))
                 if p.is_file() and p.resolve() not in written
                 and p.name != '.DS_Store']
        if stale:
            print(f'render_variant [{name}]: {len(stale)} STALE file(s) left behind '
                  f'(the tree could not be wiped). Delete these by hand:')
            for p in stale:
                print(f'  {p.relative_to(REPO)}')
            ok = False
        else:
            print(f'render_variant [{name}]: no stale files; '
                  f'in-place tree matches the source.')
    if survivors:
        ok = False
        print(f'render_variant [{name}]: FAIL - blocks this variant strips '
              f'survived into the built tree:')
        for f, s in sorted(survivors):
            print(f'  {cfg["dir"]}/{f}  <!-- {s} -->')
    if leaked:
        ok = False
        print(f'render_variant [{name}]: FAIL - unfenced Panopto references in:')
        for f in leaked:
            print(f'  {cfg["dir"]}/{f}')
        print(f'Fence them: VIDEO:START/END to remove them from this variant, or '
              f'{name.upper()}_ONLY:START/END if this modality should keep its own.')
    if escaped:
        ok = False
        print(f'render_variant [{name}]: FAIL - links escaping to /pages/ found in:')
        for f in escaped:
            print(f'  {cfg["dir"]}/{f}')
        print('These bypass the URL rewrite; investigate the source pages.')
    if ok:
        checked = 'zero /pages/ escape links'
        if 'VIDEO' in cfg['strip']:
            checked = (f'no Panopto outside this modality\'s own '
                       f'{name.upper()}_ONLY block, and ') + checked
        else:
            checked += ' (Panopto check not applicable: this variant keeps video)'
        print(f'render_variant [{name}]: verified {checked}.')
    return ok


def main():
    if not SRC.is_dir():
        sys.exit('render_variant.py: pages/ not found; run from the repo root.')

    wanted = sys.argv[1:] or list(VARIANTS)
    unknown = [w for w in wanted if w not in VARIANTS]
    if unknown:
        sys.exit(f'render_variant.py: unknown variant(s) {unknown}. '
                 f'Known: {list(VARIANTS)}')

    if not all(build(name, VARIANTS[name]) for name in wanted):
        sys.exit(1)


if __name__ == '__main__':
    main()
