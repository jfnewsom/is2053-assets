#!/usr/bin/env python3
"""
render_bookex_overview.py — Renders pages/support/bookex-overview.html
from pages/support/json/bookex.json.

Single-card / sections-within layout with three named sections:
  - Workflow      (blue accent)   — ordered list of 5 steps
  - Chapters      (green accent)  — chapter-to-key-concepts table
  - Scoring       (orange accent) — scoring rubric table

Note: this is the OVERVIEW landing page. The per-chapter BookEx pages
(pages/bookex/BookExCH{N}.html) are rendered separately by render_bookex.py
from their own JSON SoTs in pages/bookex/json/.

Run with:
    python3 render_bookex_overview.py

Source:  pages/support/json/bookex.json
Output:  pages/support/bookex-overview.html
"""
import json
from pathlib import Path


ASSETS_BASE = "https://jfnewsom.github.io/is2053-assets"


# ── Topper (course badge + title + Bat City logo + sub-banner) ────────

def render_topper(card):
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
        f'            <div class="lc-topper-title">{card["topperTitle"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="{ASSETS_BASE}/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{card["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>'
    )


# ── Lead-in (bare content, no named-section wrapper) ──────────────────

def render_intro(intro):
    """Intro paragraphs + a callout. No named-section wrapper."""
    paras = '\n'.join(
        f'      <p>\n        {p}\n      </p>' for p in intro['paragraphs_html']
    )
    callout = intro.get('callout')
    callout_html = ''
    if callout:
        callout_html = (
            f'\n\n'
            f'      <div class="lc-callout lc-callout--{callout["variant"]}">\n'
            f'        <div class="lc-callout__icon"><span class="material-symbols-outlined">{callout["icon"]}</span></div>\n'
            f'        <div class="lc-callout__bubble">\n'
            f'          <div class="lc-callout__title">{callout["title"]}</div>\n'
            f'          <div class="lc-callout__body">\n'
            f'            {callout["body_html"]}\n'
            f'          </div>\n'
            f'        </div>\n'
            f'      </div>'
        )
    return paras + callout_html


# ── Section header (label + italic sub-label) ─────────────────────────

def render_section_header(label, sub_label, color):
    return (
        f'      <div class="lc-named-section lc-named-section--{color}">\n'
        f'      <div class="lc-named-section__label lc-named-section__label--{color}">{label}</div>\n'
        f'      <p style="font-size: 13px; color: var(--color-text-muted); margin-top: -4px; margin-bottom: 16px; font-style: italic;">{sub_label}</p>'
    )


# ── Section 1: Workflow (ordered list) ────────────────────────────────

def render_workflow(workflow):
    color = workflow['labelColor']
    header = render_section_header(workflow['label'], workflow['subLabel'], color)
    steps = '\n'.join(f'        <li>{s}</li>' for s in workflow['steps_html'])
    return (
        f'\n\n'
        f'{header}\n'
        f'\n'
        f'      <ol>\n'
        f'{steps}\n'
        f'      </ol>\n'
        f'      </div>'
    )


# ── Section 2: Chapter reference table ────────────────────────────────

def render_chapters(chapters):
    color = chapters['labelColor']
    header = render_section_header(chapters['label'], chapters['subLabel'], color)
    rows = chapters['rows']
    highlight_last = chapters.get('highlightLast', False)
    last_idx = len(rows) - 1
    row_lines = []
    for i, row in enumerate(rows):
        tr_class = ' class="lc-table__total"' if (highlight_last and i == last_idx) else ''
        row_lines.append(
            f'            <tr{tr_class}><td><strong>{row["chapter_html"]}</strong></td><td>{row["concepts_html"]}</td></tr>'
        )
    rows_html = '\n'.join(row_lines)
    return (
        f'\n\n'
        f'{header}\n'
        f'\n'
        f'      <div class="lc-table-wrap">\n'
        f'        <table class="lc-table">\n'
        f'          <thead>\n'
        f'            <tr>\n'
        f'              <th>Chapter</th>\n'
        f'              <th>Key Concepts</th>\n'
        f'            </tr>\n'
        f'          </thead>\n'
        f'          <tbody>\n'
        f'{rows_html}\n'
        f'          </tbody>\n'
        f'        </table>\n'
        f'      </div>\n'
        f'      </div>'
    )


# ── Section 3: Scoring (binary grading — paragraph + callout) ─────────

def render_scoring(scoring):
    """Binary-grading section. Lead paragraph stating the 100/0 rule,
    followed by an explanatory callout about the troubleshooting
    pedagogy and unlimited submissions."""
    color = scoring['labelColor']
    header = render_section_header(scoring['label'], scoring['subLabel'], color)
    body = scoring['body_html']

    callout = scoring.get('callout')
    callout_html = ''
    if callout:
        callout_html = (
            f'\n\n'
            f'      <div class="lc-callout lc-callout--{callout["variant"]}">\n'
            f'        <div class="lc-callout__icon"><span class="material-symbols-outlined">{callout["icon"]}</span></div>\n'
            f'        <div class="lc-callout__bubble">\n'
            f'          <div class="lc-callout__title">{callout["title"]}</div>\n'
            f'          <div class="lc-callout__body">\n'
            f'            {callout["body_html"]}\n'
            f'          </div>\n'
            f'        </div>\n'
            f'      </div>'
        )

    return (
        f'\n\n'
        f'{header}\n'
        f'\n'
        f'      {body}'
        f'{callout_html}\n'
        f'      </div>'
    )


# ── Page renderer ─────────────────────────────────────────────────────

def render_page(data):
    card = data['card']
    color = card['color']
    topper = render_topper(card)
    intro = render_intro(data['intro'])
    workflow = render_workflow(data['workflow'])
    chapters = render_chapters(data['chapters'])
    scoring = render_scoring(data['scoring'])

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <link rel="icon" type="image/png" href="{ASSETS_BASE}/favicon.png">\n'
        f'  <title>{data["pageTitle"]}</title>\n'
        f'  <link rel="stylesheet" href="{ASSETS_BASE}/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       BookEx Overview — single card, sections within\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{topper}\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'{intro}'
        f'{workflow}'
        f'{chapters}'
        f'{scoring}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>\n'
        '\n\n'
        '</div><!-- /lc-wrapper -->\n'
        f'<script src="{ASSETS_BASE}/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'bookex.json'
    out = repo_root / 'pages' / 'support' / 'bookex-overview.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
