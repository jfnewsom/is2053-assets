#!/usr/bin/env python3
"""
render_support_page.py - The generic renderer. Cards, blocks, and modalities.

Ledger L-021, final tranche. Every other renderer in this repo is bespoke: it
knows its page's section names, and adding a page means writing a new script.
That is right when the page has real structure (a lab, a BookEx chapter, the
Flake8 guide's error blocks). It is waste for what most support pages actually
are, which is a topper followed by a stack of blocks with prose inside them.

WHY THIS IS NOT JUST DEDUPLICATION
Hand-maintained HTML cannot express "this sentence differs by modality", so on
2026-08-09 pages/support/home.html told face-to-face students the course was
"Asynchronous Online", because the only copy of that line was the online one and
there was nowhere else to put a second. Sourcing the page is what makes the
per-modality answer sayable at all. That is the point of the byModality key
below, and it is why John's ask was for everything to come from JSON rather than
just the pages that happened to be easy.

    _meta.renderer   must be "support_page". This is how the file is FOUND.
    _meta.output     path, relative to the repo root, of the page to write.
    pageTitle        <title> text.
    siteContext      the site-context meta value. Defaults to "support".
    extraHead        optional list of extra verbatim <head> lines.
    cards[]          the page body. See below.

A page is a list of CARDS. Each card has:

    color            the lc-card accent. Required unless the card is `raw`.
    comment          optional banner comment above it, for View Source.
    topper           optional: badgeWord, badgeNum, title, subBanner, logo.
                     A card with no topper emits none (the Recordings card).
    blocks[]         the card's panel contents.
    footer_html      optional lc-page-footer at the end of the panel.
    raw              verbatim card markup, used INSTEAD of everything above.
                     This exists for the one card another renderer owns: the
                     Recordings card is injected by render_modules.py between
                     its sentinels, so this file emits the empty markers and
                     stays out of the way.

A BLOCK is exactly one of:

    {"raw_html": ...}                    verbatim, for bespoke layout
    {"label": ..., "body_html": ...}     an lc-named-section
    {"row": [col, col]}                  an lc-home-row; each col is a bare
                                         label plus body, no section wrapper

Named sections and row columns also take labelColor (a palette accent), or
sectionStyle plus labelStyle (a one-off color not in the palette). labelColor
tints the label and the section border; "sectionColor": false tints the label
only.

MODALITY
Any block, or any row column, may carry either:

    "modality": "f2f"        emit once, fenced in that modality's sentinel
    "byModality": {...}      emit one fenced copy per key, each holding the
                             keys that differ. Everything not restated is
                             inherited from the block, so a per-modality
                             difference costs one line, not a second copy.

The fencing is what render_variant.py already understands, so adding a third
modality is a registry entry there plus one key here. No page is forked.

    python3 render_support_page.py                       every support_page JSON
    python3 render_support_page.py pages/support/json/home.json

Note the sorted(set(...)) in discover(). The globs pages/**/json/*.json and
pages/**/json/**/*.json overlap, and walking the tree twice has already caused
one wrong count in this repo. Do not remove it.
"""
import glob
import json
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
RENDERER = 'support_page'

# Imported rather than restated. A modality key that render_variant.py does not
# know is content that survives into every tree, which is the failure mode you
# cannot see by looking at one page.
try:
    from render_variant import VARIANTS
    KNOWN_MODALITIES = set(VARIANTS)
except Exception:                                   # pragma: no cover
    KNOWN_MODALITIES = {'onl', 'f2f'}


def fence(html, modality, where, what):
    if modality == 'all':
        # Explicitly every tree. See wrap_for_modality in render_start_here.py.
        return html
    if modality not in KNOWN_MODALITIES:
        raise ValueError(
            f'{where}: {what} has modality "{modality}", which is not in the '
            f'render_variant.py registry {sorted(KNOWN_MODALITIES)}. An unknown '
            f'sentinel is never stripped, so this would appear in every tree.')
    name = f'{modality.upper()}_ONLY'
    pad = ' ' * (len(html) - len(html.lstrip(' ')))
    return f'{pad}<!-- {name}:START -->\n{html}\n{pad}<!-- {name}:END -->'


def expand(item, where, what):
    """Resolve byModality into a list of (modality_or_None, item) pairs."""
    by = item.get('byModality')
    if not by:
        return [(item.get('modality'), item)]
    if item.get('modality'):
        raise ValueError(f'{where}: {what} sets both modality and byModality.')
    out = []
    for mod, override in by.items():
        merged = {k: v for k, v in item.items() if k != 'byModality'}
        merged.update(override)
        out.append((mod, merged))
    return out


def label_and_classes(item):
    color = item.get('labelColor')
    if color and item.get('sectionStyle'):
        raise ValueError(
            f'section "{item.get("label")}" sets both labelColor and '
            f'sectionStyle. Pick one; the CSS class wins silently, so the '
            f'inline color would look ignored.')
    # labelColor normally tints the label AND the section border, which is the
    # pattern on every colored section in the repo. home.html's Course
    # Resources section is the one exception: colored label, uncolored border.
    # "sectionColor": false preserves that rather than quietly restyling a live
    # page to make the data model tidier.
    wrap = color if item.get('sectionColor', True) else None
    div_cls = 'lc-named-section' + (f' lc-named-section--{wrap}' if wrap else '')
    lbl_cls = ('lc-named-section__label'
               + (f' lc-named-section__label--{color}' if color else ''))
    div_sty = f' style="{item["sectionStyle"]}"' if item.get('sectionStyle') else ''
    lbl_sty = f' style="{item["labelStyle"]}"' if item.get('labelStyle') else ''
    return div_cls, lbl_cls, div_sty, lbl_sty


def render_column(col, where):
    """One child of an lc-home-row: a bare label, then the body."""
    parts = []
    for mod, c in expand(col, where, f'row column "{col.get("label")}"'):
        _, lbl_cls, _, lbl_sty = label_and_classes(c)
        lbl = (f'          <div class="{lbl_cls}"{lbl_sty}>{c["label"]}</div>\n'
               if c.get('label') else '')
        html = (f'        <div>\n{lbl}'
                f'{c["body_html"].rstrip()}\n'
                f'        </div>')
        parts.append(fence(html, mod, where, 'row column') if mod else html)
    return '\n'.join(parts)


def render_block(block, where):
    parts = []
    for mod, b in expand(block, where, f'block "{b_label(block)}"'):
        if 'raw_html' in b:
            html = b['raw_html'].rstrip()
        elif 'row' in b:
            cols = '\n'.join(render_column(c, where) for c in b['row'])
            html = f'      <div class="lc-home-row">\n{cols}\n      </div>'
        elif 'label' in b:
            div_cls, lbl_cls, div_sty, lbl_sty = label_and_classes(b)
            html = (f'      <div class="{div_cls}"{div_sty}>\n'
                    f'      <div class="{lbl_cls}"{lbl_sty}>{b["label"]}</div>\n'
                    f'      {b["body_html"].rstrip()}\n'
                    f'      </div>')
        else:
            raise ValueError(
                f'{where}: a block must have raw_html, row, or label. Got keys '
                f'{sorted(b)}.')
        if mod:
            html = fence(html, mod, where, 'block')
        if b.get('comment'):
            html = f'      <!-- {b["comment"]} -->\n' + html
        parts.append(html)
    return '\n\n'.join(parts)


def b_label(block):
    return block.get('label') or block.get('comment') or 'unlabelled'


def render_topper(t):
    return (
        f'    <div class="lc-topper">\n'
        f'      <table style="width: 100%; border-collapse: collapse;">\n'
        f'        <tr>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0;">\n'
        f'            <div class="lc-course-badge">\n'
        f'              <div class="lc-course-badge__word">{t["badgeWord"]}</div>\n'
        f'              <div class="lc-course-badge__num">{t["badgeNum"]}</div>\n'
        f'            </div>\n'
        f'          </td>\n'
        f'          <td style="vertical-align: bottom; padding: 0 0 0 16px;">\n'
        f'            <div class="lc-topper-title">{t["title"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="{t["logo"]}"\n'
        f'                 alt="{t.get("logoAlt", "Bat City Collective")}" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{t["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>'
    )


def render_card(card, where):
    banner = ''
    if card.get('comment'):
        rule = '═' * 58
        banner = (f'  <!-- {rule}\n'
                  f'       {card["comment"]}\n'
                  f'  {rule} -->\n')

    if 'raw' in card:
        return banner + card['raw'].rstrip()

    blocks = '\n\n\n'.join(render_block(b, where) for b in card['blocks'])

    footer = ''
    if card.get('footer_html'):
        footer = ('\n\n      <div class="lc-page-footer">\n'
                  f'        {card["footer_html"].strip()}\n'
                  '      </div>')

    topper = (render_topper(card['topper']) + '\n') if card.get('topper') else ''

    return (banner
            + f'  <div class="lc-card lc-card--{card["color"]}">\n'
            + topper
            + '    <div class="lc-panel">\n\n\n'
            + blocks + footer + '\n\n'
            + '    </div>\n'
            + '  </div>')


def normalize(data):
    """The single-card shape is the common one; keep it sayable.

    A page with one card and a flat list of sections may write `card` and
    `sections` instead of `cards`. Normalizing here means there is exactly one
    code path below, so the simple shape cannot rot.
    """
    if 'cards' in data:
        return data['cards']
    card = dict(data['card'])
    card['blocks'] = data['sections']
    if data.get('footer_html'):
        card['footer_html'] = data['footer_html']
    if data.get('topper'):
        card['topper'] = data['topper']
    return [card]


def render_page(data, where):
    cards = [render_card(c, where) for c in normalize(data)]
    head_extra = ''.join(f'  {line}\n' for line in data.get('extraHead', []))
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        f'  <meta name="site-context" content="{data.get("siteContext", "support")}">\n'
        f'  <title>{data["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        + head_extra
        + '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        + '\n\n\n'.join(cards) + '\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def discover():
    """Every JSON in the tree that asks for this renderer.

    sorted(set(...)) is load-bearing: the two globs overlap.
    """
    found = []
    pats = ('pages/**/json/*.json', 'pages/**/json/**/*.json')
    for path in sorted(set(sum(
            (glob.glob(os.path.join(REPO, p), recursive=True) for p in pats), []))):
        try:
            with open(path, encoding='utf-8') as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(data, dict) and \
                data.get('_meta', {}).get('renderer') == RENDERER:
            found.append(path)
    return found


def build(path):
    rel = os.path.relpath(path, REPO)
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)

    out_rel = data.get('_meta', {}).get('output')
    if not out_rel:
        raise ValueError(f'{rel}: _meta.output is required; it names the page to write.')

    html = render_page(data, rel)
    with open(os.path.join(REPO, out_rel), 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f'  Rendered -> {out_rel}  ({len(html.splitlines())} lines)')


def main(argv):
    targets = [os.path.abspath(a) for a in argv[1:]] or discover()
    if not targets:
        print('render_support_page: no JSON declares _meta.renderer = '
              f'"{RENDERER}"; nothing to do.')
        return 0
    for path in targets:
        build(path)
    print(f'render_support_page: {len(targets)} page(s) rendered')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
