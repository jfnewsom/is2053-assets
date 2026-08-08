#!/usr/bin/env python3
"""
render_reading.py - Renders pages/support/reading-ch*.html from reading.json.

Created 2026-08-08 to close ledger L-016. Before this, the nine chapter reading
pages were hand-maintained HTML with no JSON source. That put them outside the
source-of-truth chain and outside check_style.py's SOURCE scan, and it let three
of them carry retired lab titles ("Where Have We Been?", "Save Your Progress",
"The City Class") for a full term while every other surface was correct.

Source:  pages/support/json/reading.json
Outputs: pages/support/reading-ch{NN}.html  (one per entry in chapters[])

Run before render_variant.py, like every other content renderer.
"""
import json
from pathlib import Path

BADGE_WORD = 'Information Systems'
BADGE_NUM = '2053'
BASE = 'https://jfnewsom.github.io/is2053-assets'


def render_topper(ch):
    return (
        '    <div class="lc-topper">\n'
        '      <table style="width: 100%; border-collapse: collapse;">\n'
        '        <tr>\n'
        '          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0;">\n'
        '            <div class="lc-course-badge">\n'
        f'              <div class="lc-course-badge__word">{BADGE_WORD}</div>\n'
        f'              <div class="lc-course-badge__num">{BADGE_NUM}</div>\n'
        '            </div>\n'
        '          </td>\n'
        '          <td style="vertical-align: bottom; padding: 0 0 0 16px;">\n'
        f'            <div class="lc-topper-title">{ch["topperTitle"]}</div>\n'
        '          </td>\n'
        '          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; '
        'padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="{BASE}/branding/BatCity-logo-3D.png"\n'
        '                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        '          </td>\n'
        '        </tr>\n'
        '        <tr>\n'
        '          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{ch["subBanner"]}</div>\n'
        '          </td>\n'
        '        </tr>\n'
        '      </table>\n'
        '    </div>'
    )


def render_sections(ch):
    rows = '\n'.join(
        f'            <tr><td><strong>{s["num"]}</strong></td><td>{s["title"]}</td></tr>'
        for s in ch['sections']
    )
    return (
        f'      <div class="lc-h3 lc-h3--{ch["color"]}">{ch["sectionsLabel"]}</div>\n'
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <tbody>\n'
        f'{rows}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def render_callout(c):
    return (
        f'      <div class="lc-callout lc-callout--{c["variant"]}">\n'
        f'        <div class="lc-callout__icon"><span class="material-symbols-outlined">'
        f'{c["icon"]}</span></div>\n'
        '        <div class="lc-callout__bubble">\n'
        f'          <div class="lc-callout__title">{c["title"]}</div>\n'
        '          <div class="lc-callout__body">\n'
        f'            {c["body_html"]}\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>'
    )


def render_after(ch):
    items = '\n'.join(f'        <li>{i}</li>' for i in ch['afterReading'])
    return (
        f'      <div class="lc-h3 lc-h3--{ch["color"]}">{ch["afterReadingLabel"]}</div>\n'
        '      <ul>\n'
        f'{items}\n'
        '      </ul>'
    )


def render_page(ch):
    bar = '═' * 58
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <link rel="icon" type="image/png" href="{BASE}/favicon.png">\n'
        f'  <title>{ch["topperTitle"]} | IS2053 Programming I</title>\n'
        f'  <link rel="stylesheet" href="{BASE}/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n'
        '\n'
        '\n'
        f'  <!-- {bar}\n'
        f'       CARD 1 — Chapter {ch["chapter"]} ({ch["color"]})\n'
        f'  {bar} -->\n'
        f'  <div class="lc-card lc-card--{ch["color"]}">\n'
        f'{render_topper(ch)}\n'
        '    <div class="lc-panel">\n'
        '\n'
        f'{render_sections(ch)}\n'
        '\n'
        f'{render_callout(ch["callout"])}\n'
        '\n'
        f'{render_after(ch)}\n'
        '\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '\n'
        '</div><!-- /lc-wrapper -->\n'
        f'<script src="{BASE}/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'reading.json'

    print(f'Reading {src}')
    with open(src, encoding='utf-8') as f:
        data = json.load(f)

    for ch in data['chapters']:
        out = repo_root / 'pages' / 'support' / f'reading-ch{ch["chapter"]}.html'
        html = render_page(ch)
        out.write_text(html, encoding='utf-8')
        print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
