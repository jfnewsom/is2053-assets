#!/usr/bin/env python3
"""
render_codegrade_guide.py — Renders pages/support/codegrade-guide.html
from pages/support/json/codegrade.json.

Single-card / sections-within layout (home-page pattern). One outer
blue card with four internal lc-named-section blocks:
  1. What Is CodeGrade  (default yellow) — intro + unlimited-subs callout
  2. How to Submit      (green)  — 5-step process + filename warning
  3. Reading Feedback   (orange) — 5 category sub-headings + cross-ref
                                   to grading-info.html#rubrics
  4. Common Issues      (red)    — troubleshooting table

This page is intentionally separate from Grading Info — different
student moments (submission workflow vs. grade calculation). Cross-
links between the two pages handle the natural traffic both ways:
  - this page → grading-info.html#rubrics  (point values per category)
  - grading-info.html → codegrade-guide.html  (submission workflow)

Run with:
    python3 render_codegrade_guide.py

Source:  pages/support/json/codegrade.json
Output:  pages/support/codegrade-guide.html
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


def render_callout(callout):
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


# ── Section renderers ────────────────────────────────────────────────

def render_section_what_is_it(s):
    """Section 1: What Is CodeGrade — intro paragraph + callout."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    callout_html = render_callout(s['callout']) if s.get('callout') else ''
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["body_html"]}\n'
        f'\n'
        f'{callout_html}\n'
        f'      </div>'
    )


def render_section_how_to_submit(s):
    """Section 2: How to Submit — intro + ordered list of steps + warning callout."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    steps = '\n'.join(f'        <li>{step}</li>' for step in s['steps_html'])
    callout_html = render_callout(s['callout']) if s.get('callout') else ''
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'      <ol>\n'
        f'{steps}\n'
        f'      </ol>\n'
        f'\n'
        f'{callout_html}\n'
        f'      </div>'
    )


def render_section_reading_feedback(s):
    """Section 3: Reading Feedback — intro + 5 colored category h3 sub-banners +
    cross-ref pointer to grading-info.html#rubrics."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    categories_html = []
    for cat in s['categories']:
        color = cat.get('color', '')
        h3_class = f' lc-h3--{color}' if color else ''
        categories_html.append(
            f'      <div class="lc-h3{h3_class}">{cat["heading"]}</div>\n'
            f'      {cat["body_html"]}'
        )
    cats_block = '\n\n'.join(categories_html)

    cross_ref = f'\n\n{s["crossRef_html"]}' if s.get('crossRef_html') else ''

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{cats_block}'
        f'{cross_ref}\n'
        f'      </div>'
    )


def render_section_common_issues(s):
    """Section 4: Common Issues — intro + two-column error/fix table."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    rows = []
    for row in s['rows']:
        rows.append(
            f'            <tr>\n'
            f'              <td>{row["error_html"]}</td>\n'
            f'              <td>{row["fix_html"]}</td>\n'
            f'            </tr>'
        )
    rows_html = '\n'.join(rows)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-table-wrap">\n'
        f'        <table class="lc-table">\n'
        f'          <thead>\n'
        f'            <tr>\n'
        f'              <th>Error</th>\n'
        f'              <th>What It Means &amp; How to Fix It</th>\n'
        f'            </tr>\n'
        f'          </thead>\n'
        f'          <tbody>\n'
        f'{rows_html}\n'
        f'          </tbody>\n'
        f'        </table>\n'
        f'      </div>\n'
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
        render_section_what_is_it(data['whatIsIt']),
        render_section_how_to_submit(data['howToSubmit']),
        render_section_reading_feedback(data['readingFeedback']),
        render_section_common_issues(data['commonIssues']),
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
        '       CodeGrade Guide — single card, sections within (home-page pattern)\n'
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
    src = repo_root / 'pages' / 'support' / 'json' / 'codegrade.json'
    out = repo_root / 'pages' / 'support' / 'codegrade-guide.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
