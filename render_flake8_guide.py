#!/usr/bin/env python3
"""
render_flake8_guide.py — Renders pages/support/flake8-guide.html
from pages/support/json/flake8.json.

Single-card / sections-within layout (home-page pattern). One outer
purple card with five internal lc-named-section blocks:
  1. Overview         (default yellow) — what Flake8 is + grade note
  2. Reading Errors   (blue)   — error format + 4-cell anatomy grid +
                                 prefixes table
  3. Critical Errors  (red)    — F401 + F841 with problem/fix code
                                 callouts (−15 pts each)
  4. Style Errors     (orange) — 7-row table (E302, E303, E501,
                                 W291/W293, E111/E117, E225, E231)
  5. Quick Fixes      (green)  — 8-item pre-submission checklist

The Overview section links to grading-info.html#rubrics so students
can see how Code Style factors into their lab grade.

Run with:
    python3 render_flake8_guide.py

Source:  pages/support/json/flake8.json
Output:  pages/support/flake8-guide.html
"""
import json
from pathlib import Path


# ── Helpers ──────────────────────────────────────────────────────────

def render_section_label(label, color):
    cls = 'lc-named-section__label'
    if color:
        cls += f' lc-named-section__label--{color}'
    return f'      <div class="{cls}">{label}</div>'


def section_div_classes(color):
    cls = 'lc-named-section'
    if color:
        cls += f' lc-named-section--{color}'
    return cls


def render_subtitle(html):
    """Small italic muted subtitle line directly under a section label."""
    return (
        f'      <p style="font-size: 13px; color: var(--color-text-muted); '
        f'margin-top: -4px; margin-bottom: 16px; font-style: italic;">{html}</p>'
    )


def render_callout(variant, icon, title, body_inner_html):
    return (
        f'      <div class="lc-callout lc-callout--{variant}">\n'
        f'        <div class="lc-callout__icon">\n'
        f'          <span class="material-symbols-outlined">{icon}</span>\n'
        f'        </div>\n'
        f'        <div class="lc-callout__bubble">\n'
        f'          <div class="lc-callout__title">{title}</div>\n'
        f'          <div class="lc-callout__body">\n'
        f'            {body_inner_html}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>'
    )


# ── Section renderers ────────────────────────────────────────────────

def render_section_overview(s):
    """Section 1: Overview — intro paragraphs."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["body_html"]}\n'
        f'      </div>'
    )


def render_section_reading_errors(s):
    """Section 2: Reading Errors — intro + code-block example + 4-cell
    anatomy grid (using lc-contact-grid pattern) + sub-banner h3 with
    prefixes table."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    # 4-cell anatomy grid
    cells = []
    for cell in s['anatomy']:
        color_var = f'var(--neon-{cell["color"]})'
        cells.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label" style="color: {color_var};">{cell["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">{cell["desc"]}</div>\n'
            f'        </div>'
        )
    anatomy_html = (
        '      <div class="lc-contact-grid">\n'
        + '\n'.join(cells)
        + '\n      </div>'
    )

    # Prefixes table with sub-banner h3
    pt = s['prefixesTable']
    h3_color = pt.get('headingColor', '')
    h3_class = f' lc-h3--{h3_color}' if h3_color else ''
    rows = []
    for r in pt['rows']:
        rows.append(
            f'            <tr>\n'
            f'              <td><strong>{r["prefix"]}</strong></td>\n'
            f'              <td>{r["category"]}</td>\n'
            f'            </tr>'
        )
    prefixes_table_html = (
        f'      <div class="lc-h3{h3_class}">{pt["heading"]}</div>\n'
        f'      <div class="lc-table-wrap">\n'
        f'        <table class="lc-table">\n'
        f'          <thead>\n'
        f'            <tr>\n'
        f'              <th>Prefix</th>\n'
        f'              <th>Category</th>\n'
        f'            </tr>\n'
        f'          </thead>\n'
        f'          <tbody>\n'
        + '\n'.join(rows) + '\n'
        f'          </tbody>\n'
        f'        </table>\n'
        f'      </div>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'      {s["errorFormat_html"]}\n'
        f'\n'
        f'{anatomy_html}\n'
        f'\n'
        f'{prefixes_table_html}\n'
        f'      </div>'
    )


def render_section_critical_errors(s):
    """Section 3: Critical Errors — subtitle + repeated error blocks
    (F401, F841 …). Each error: lc-h3 sub-banner heading + intro
    paragraph + Problem callout (warning) + Fix callout (success)."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    blocks = []
    for i, err in enumerate(s['errors']):
        color = err.get('color', '')
        h3_class = f' lc-h3--{color}' if color else ''
        heading = f'{err["code"]} &mdash; {err["title"]}'
        problem_callout = render_callout('warning', 'close', 'Problem', err['problem_html'])
        fix_callout = render_callout('success', 'check', 'Fix', err['fix_html'])

        block = (
            f'      <div class="lc-h3{h3_class}">{heading}</div>\n'
            f'      {err["intro_html"]}\n'
            f'{problem_callout}\n'
            f'{fix_callout}'
        )
        blocks.append(block)

    # Subtle separator between consecutive error blocks
    body = '\n\n      <hr class="lc-cp-sep">\n\n'.join(blocks)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'{body}\n'
        f'      </div>'
    )


def render_section_style_errors(s):
    """Section 4: Style Errors — subtitle + 3-col code/problem/fix table."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    rows = []
    for r in s['rows']:
        rows.append(
            f'            <tr>\n'
            f'              <td><code>{r["code"]}</code></td>\n'
            f'              <td>{r["problem"]}</td>\n'
            f'              <td>{r["fix"]}</td>\n'
            f'            </tr>'
        )
    table_html = (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th>Code</th>\n'
        '              <th>Problem</th>\n'
        '              <th>Fix</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        + '\n'.join(rows) + '\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'{table_html}\n'
        f'      </div>'
    )


def render_section_quick_fixes(s):
    """Section 5: Quick Fixes — intro + lc-checklist of items."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    items = []
    for item_html in s['items_html']:
        items.append(
            f'        <li>\n'
            f'          <div class="lc-checklist__box"></div>\n'
            f'          <div class="lc-checklist__label">{item_html}</div>\n'
            f'        </li>'
        )
    checklist_html = (
        '      <ul class="lc-checklist">\n'
        + '\n'.join(items) + '\n'
        '      </ul>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{checklist_html}\n'
        f'      </div>'
    )


# ── Top-level ────────────────────────────────────────────────────────

def render_card_topper(card_meta):
    return (
        f'    <div class="lc-topper">\n'
        f'      <table style="width: 100%; border-collapse: collapse;">\n'
        f'        <tr>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0;">\n'
        f'            <div class="lc-course-badge">\n'
        f'              <div class="lc-course-badge__word">Information Systems</div>\n'
        f'              <div class="lc-course-badge__num">2053</div>\n'
        f'            </div>\n'
        f'          </td>\n'
        f'          <td style="vertical-align: bottom; padding: 0 0 0 16px;">\n'
        f'            <div class="lc-topper-title">{card_meta["topperTitle"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="https://jfnewsom.github.io/is2053-assets/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{card_meta["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>'
    )


def render_page(data):
    card = data['card']
    color = card['color']

    sections = [
        render_section_overview(data['overview']),
        render_section_reading_errors(data['readingErrors']),
        render_section_critical_errors(data['criticalErrors']),
        render_section_style_errors(data['styleErrors']),
        render_section_quick_fixes(data['quickFixes']),
    ]

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        '  <meta name="site-context" content="support">\n'
        f'  <title>{data["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        '  <!-- ══════════════════════════════════════════════════════════\n'
        '       Flake8 Guide — single card, sections within (home-page pattern)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        + '\n\n'.join(sections) + '\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'flake8.json'
    out = repo_root / 'pages' / 'support' / 'flake8-guide.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
