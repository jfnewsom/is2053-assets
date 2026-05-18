#!/usr/bin/env python3
"""
render_grading_info.py — Renders pages/support/grading-info.html
from pages/support/json/grading-info.json.

Single source of truth for the Grading Info page.

Schema: One outer lc-card with internal lc-named-section blocks.
This is the home-page pattern (tight, one frame) rather than the
4-cards-stacked assignment-sheet pattern.

Run with:
    python3 render_grading_info.py

Source:  pages/support/json/grading-info.json
Output:  pages/support/grading-info.html
"""
import json
from pathlib import Path


# ── Small renderers ──────────────────────────────────────────────────

def render_callout(callout):
    """An lc-callout block with icon + title + body_html."""
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


def render_section_label(label, color):
    """Yellow-by-default named-section label. color is a string like
    'green', 'orange', 'red', 'cyan', 'purple', or None (default yellow)."""
    cls = 'lc-named-section__label'
    if color:
        cls += f' lc-named-section__label--{color}'
    return f'      <div class="{cls}">{label}</div>'


def render_weights_table(rows):
    """Grade Weights table."""
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
    """Sick Days / drops table. header_label overrides the second column."""
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
    """Two-column letter-grade table. left:null → <td colspan='2'></td>
    in left half (used for the lone F row)."""
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


# ── Section renderers ────────────────────────────────────────────────

def render_section_weights(weights):
    """Section 1: Grade Weights — table + optional footer paragraph."""
    label_html = render_section_label(weights['label'], weights.get('labelColor'))
    table_html = render_weights_table(weights['rows'])
    footer = weights.get('footer_html', '')
    return (
        f'      <div class="lc-named-section">\n'
        f'{label_html}\n'
        f'{table_html}\n'
        f'\n'
        f'      {footer}\n'
        f'      </div>'
    )


def render_section_sick_days(drop):
    """Section 2: Sick Days — intro + table + workplace metaphor callout.

    The named-section gets an id (anchor target for cross-links from
    Late Work)."""
    anchor_id = drop.get('anchor_id', 'drop-policy')
    header_label = drop.get('rowsHeader', 'Drops')
    label_html = render_section_label(drop['label'], drop.get('labelColor'))
    table_html = render_drop_table(drop['rows'], header_label=header_label)
    callout_html = render_callout(drop['callout'])
    return (
        f'      <div class="lc-named-section" id="{anchor_id}">\n'
        f'{label_html}\n'
        f'      {drop["intro_html"]}\n'
        f'\n'
        f'{table_html}\n'
        f'\n'
        f'{callout_html}\n'
        f'      </div>'
    )


def render_section_late_work(late):
    """Section 3: Late Work — warning callout + sub-sections (each with
    lc-h3 sub-heading) + closing paragraph."""
    label_html = render_section_label(late['label'], late.get('labelColor'))
    sub_color = late.get('labelColor', '')
    h3_class = f' lc-h3--{sub_color}' if sub_color else ''

    blocks = [render_callout(late['callout'])]

    for section in late.get('sections', []):
        sub_block = (
            f'      <div class="lc-h3{h3_class}">{section["heading"]}</div>\n'
            f'      {section["body_html"]}'
        )
        blocks.append(sub_block)

    if late.get('closing_html'):
        blocks.append(f'      {late["closing_html"]}')

    body = '\n\n'.join(blocks)

    return (
        f'      <div class="lc-named-section">\n'
        f'{label_html}\n'
        f'{body}\n'
        f'      </div>'
    )


def render_section_grade_scale(scale):
    """Section 4: Grade Scale — two-column letter-grade table only."""
    label_html = render_section_label(scale['label'], scale.get('labelColor'))
    table_html = render_grade_scale_table(scale['rows'])
    return (
        f'      <div class="lc-named-section">\n'
        f'{label_html}\n'
        f'{table_html}\n'
        f'      </div>'
    )


# ── Top-level page renderer ──────────────────────────────────────────

def render_card_topper(card_meta):
    """The course-badge topper at the top of the outer card.
    Same shape as the module overview pages."""
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
    """Render the complete grading-info.html — one outer card with four
    internal lc-named-section blocks (home-page pattern)."""
    card = data['card']
    color = card['color']

    weights_section = render_section_weights(data['gradeWeights'])
    drops_section = render_section_sick_days(data['dropPolicy'])
    late_section = render_section_late_work(data['lateWork'])
    scale_section = render_section_grade_scale(data['gradeScale'])

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
        '       Grading Info — single card, sections within (home-page pattern)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        f'{weights_section}\n\n'
        f'{drops_section}\n\n'
        f'{late_section}\n\n'
        f'{scale_section}\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
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

    # Sanity: weights sum to 100
    total = sum(int(r['weight'].rstrip('%')) for r in data['gradeWeights']['rows'])
    if total != 100:
        print(f'  WARNING: weights total {total}%, not 100%')


if __name__ == '__main__':
    main()
