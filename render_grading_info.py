#!/usr/bin/env python3
"""
render_grading_info.py — Renders pages/support/grading-info.html
from pages/support/json/grading-info.json.

Single source of truth for the Grading Info page. Mirrors the architectural
pattern of render_modules.py and render_start_here.py.

Run with:
    python3 render_grading_info.py

Source:  pages/support/json/grading-info.json
Output:  pages/support/grading-info.html
"""
import json
from pathlib import Path


# ── Small renderers ──────────────────────────────────────────────────

def render_callout(callout):
    """An lc-callout block with icon + title + body_html.
    Multi-line form (matches the hand-written grading-info.html style)."""
    return (
        f'      <div class="lc-callout lc-callout--{callout["variant"]}">\n'
        f'        <div class="lc-callout__icon">\n'
        f'          <span class="material-symbols-outlined">{callout["icon"]}</span>\n'
        f'        </div>\n'
        f'        <div class="lc-callout__bubble">\n'
        f'          <div class="lc-callout__title">{callout["title"]}</div>\n'
        f'          <div class="lc-callout__body">\n'
        f'            {callout["body_html"]}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>'
    )


def render_weights_table(rows):
    """The Grade Weights table inside Card 1."""
    body_rows = []
    for row in rows:
        body_rows.append(
            f'            <tr>\n'
            f'              <td>{row["category"]}</td>\n'
            f'              <td>{row["count"]}</td>\n'
            f'              <td><strong>{row["weight"]}</strong></td>\n'
            f'            </tr>'
        )
    rows_html = '\n'.join(body_rows)
    return (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th>Category</th>\n'
        '              <th>Count</th>\n'
        '              <th>Weight</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        f'{rows_html}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def render_drop_table(rows, header_label='Drops'):
    """The Drop Policy / Sick Days table inside Card 2. The second column
    header defaults to 'Drops' but can be overridden via header_label
    (e.g., 'Sick Days')."""
    body_rows = []
    for row in rows:
        body_rows.append(
            f'            <tr>\n'
            f'              <td>{row["category"]}</td>\n'
            f'              <td><strong>{row["drops"]}</strong></td>\n'
            f'            </tr>'
        )
    rows_html = '\n'.join(body_rows)
    return (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th>Category</th>\n'
        f'              <th>{header_label}</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        f'{rows_html}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def render_grade_scale_table(rows):
    """The two-column letter-grade table inside Card 4.

    Each entry is a {left, right} pair. If 'left' is null, the row renders
    a <td colspan='2'></td> in the left half (used for the lone F row)."""
    body_rows = []
    for row in rows:
        if row['left'] is None:
            left_html = '              <td colspan="2"></td>'
        else:
            left = row['left']
            left_html = (
                f'              <td><strong>{left["letter"]}</strong></td>\n'
                f'              <td>{left["range"]}</td>'
            )
        right = row['right']
        right_html = (
            f'              <td><strong>{right["letter"]}</strong></td>\n'
            f'              <td>{right["range"]}</td>'
        )
        body_rows.append(
            f'            <tr>\n'
            f'{left_html}\n'
            f'{right_html}\n'
            f'            </tr>'
        )
    rows_html = '\n'.join(body_rows)
    return (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th>Letter Grade</th>\n'
        '              <th>Range</th>\n'
        '              <th>Letter Grade</th>\n'
        '              <th>Range</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        f'{rows_html}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


# ── Card renderers ───────────────────────────────────────────────────

def render_card1_weights(weights):
    """Card 1: Grade Weights — blue, with course-badge topper and table."""
    color = weights['card1Color']
    table_html = render_weights_table(weights['rows'])
    footer = weights.get('footer_html', '')
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 1 — Grade Weights ({color})\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
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
        f'            <div class="lc-topper-title">{weights["topperTitle"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="https://jfnewsom.github.io/is2053-assets/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{weights["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'{table_html}\n'
        f'\n'
        f'      {footer}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_card2_drop_policy(drop):
    """Card 2: Sick Days (formerly Drop Policy) — green. Anchor id from JSON
    so the Late Work card can link back to it; defaults to 'drop-policy' for
    back-compat if anchor_id is not specified."""
    anchor_id = drop.get('anchor_id', 'drop-policy')
    header_label = drop.get('rowsHeader', 'Drops')
    table_html = render_drop_table(drop['rows'], header_label=header_label)
    callout_html = render_callout(drop['callout'])
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 2 — {drop["topperTitle"]} (green)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--green" id="{anchor_id}">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{drop["topperTitle"]}</div>\n'
        f'      <div class="lc-sub-banner">{drop["subBanner"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      {drop["intro_html"]}\n'
        f'\n'
        f'{table_html}\n'
        f'\n'
        f'{callout_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_relief_valves(valves):
    """Render the 'Three relief valves' as an ordered list inside Card 3.
    Each item is rendered as: <li><strong>{title_html}</strong> &mdash; {body_html}</li>"""
    items = []
    for v in valves:
        items.append(
            f'        <li><strong>{v["title_html"]}</strong> &mdash; {v["body_html"]}</li>'
        )
    items_html = '\n'.join(items)
    return (
        '      <ol>\n'
        f'{items_html}\n'
        '      </ol>'
    )


def render_card3_late_work(late):
    """Card 3: Late Work — red.

    Standard structure (slim):
      - Warning callout (the headline "No Late Work")
      - body_html (one or more <p> tags)
      - closing_html (final paragraph)

    Optional expansion blocks (rendered if present, between body_html and closing_html):
      - relief_valves_intro_html
      - relief_valves list (rendered as <ol>)
      - discretion_callout

    All fields except callout are optional.
    """
    blocks = [render_callout(late['callout'])]

    if late.get('body_html'):
        blocks.append(f'      {late["body_html"]}')

    if late.get('relief_valves_intro_html'):
        blocks.append(f'      {late["relief_valves_intro_html"]}')

    if late.get('relief_valves'):
        blocks.append(render_relief_valves(late['relief_valves']))

    if late.get('discretion_callout'):
        blocks.append(render_callout(late['discretion_callout']))

    if late.get('closing_html'):
        blocks.append(f'      {late["closing_html"]}')

    body_html = '\n\n'.join(blocks)

    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 3 — Late Work (red)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--red">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{late["topperTitle"]}</div>\n'
        f'      <div class="lc-sub-banner">{late["subBanner"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'{body_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_card4_grade_scale(scale):
    """Card 4: Grade Scale — orange, two-column letter-grade table."""
    table_html = render_grade_scale_table(scale['rows'])
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 4 — Grade Scale (orange)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--orange">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{scale["topperTitle"]}</div>\n'
        f'      <div class="lc-sub-banner">{scale["subBanner"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'{table_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


# ── Top-level page renderer ──────────────────────────────────────────

def render_page(data):
    """Render the complete grading-info.html document."""
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
        + render_card1_weights(data['gradeWeights']) + '\n\n\n'
        + render_card2_drop_policy(data['dropPolicy']) + '\n\n\n'
        + render_card3_late_work(data['lateWork']) + '\n\n\n'
        + render_card4_grade_scale(data['gradeScale']) + '\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


# ── Entry point ──────────────────────────────────────────────────────

def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'grading-info.json'
    out = repo_root / 'pages' / 'support' / 'grading-info.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')

    # Sanity check: weights total to 100
    total = sum(int(r['weight'].rstrip('%')) for r in data['gradeWeights']['rows'])
    if total != 100:
        print(f'  WARNING: weights total {total}%, not 100%')


if __name__ == '__main__':
    main()
