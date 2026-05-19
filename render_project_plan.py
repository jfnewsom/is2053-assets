#!/usr/bin/env python3
"""
render_project_plan.py — Renders pages/scenario/project-plan.html
from pages/scenario/json/project-plan.json.

Single-card / sections-within layout. One outer blue card with seven
internal lc-named-section blocks:
  1. Project Overview      (default yellow) — intro + executive
                                               summary of end state
  2. Module 1: Getting Started     (blue)   — intro + 3 lab cards
  3. Module 2: The Journey Begins  (orange) — intro + 3 lab cards
  4. Module 3: Keeping Track       (green)  — intro + 3 lab cards
  5. Module 4: Smarter Code        (purple) — intro + 3 lab cards
  6. Module 5: Ship It             (cyan)   — intro + 2 lab cards
                                              (2-col grid, no ENHANCE)
  7. The Final Product             (cyan)   — body + byTheNumbers
                                              stat grid + closing
                                              Danny quote

Each lab card uses the lc-stage-card pattern:
  • Stage label colored by stage (BUILD=blue, ENHANCE=orange, MASTER=green)
  • Subtitle: "Lab X.Y · Ch N · Title"
  • "What You Do" sub-h3 + bullet list (boiled from lab objectives)
  • "Result" sub-h3 + one-sentence game-state paragraph

Run with:
    python3 render_project_plan.py

Source:  pages/scenario/json/project-plan.json
Output:  pages/scenario/project-plan.html
"""
import json
from pathlib import Path

HEADSHOT_BASE = 'https://jfnewsom.github.io/is2053-assets/headshots/'


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
    return (
        f'      <p style="font-size: 13px; color: var(--color-text-muted); '
        f'margin-top: -4px; margin-bottom: 16px; font-style: italic;">{html}</p>'
    )


def render_mentor(m):
    return (
        f'      <div class="lc-mentor">\n'
        f'        <div class="lc-mentor__inner">\n'
        f'          <div class="lc-mentor__avatar">\n'
        f'            <img src="{HEADSHOT_BASE}{m["avatar"]}" alt="{m["name"]}">\n'
        f'          </div>\n'
        f'          <div class="lc-mentor__bubble">\n'
        f'            <p class="lc-mentor__quote">{m["quote_html"]}</p>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'        <div class="lc-mentor__attribution">\n'
        f'          <div class="lc-mentor__name">{m["name"]}</div>\n'
        f'          <div class="lc-mentor__role">{m["role"]}</div>\n'
        f'        </div>\n'
        f'      </div>'
    )


def render_lab_card(lab):
    stage_color = lab['stageColor']
    what_items = '\n'.join(f'          <li>{i}</li>' for i in lab['whatYouDo_html'])
    lab_url = lab.get('labUrl', '')
    cta_html = (
        f'\n\n          <p style="margin-top: 12px; margin-bottom: 0; font-size: 13px;">\n'
        f'            <a href="{lab_url}" style="font-weight: 600;">Open lab page &rarr;</a>\n'
        f'          </p>'
    ) if lab_url else ''
    return (
        f'        <div class="lc-stage-card">\n'
        f'          <div class="lc-stage-card__label lc-stage-card__label--{stage_color}">{lab["stage"]}</div>\n'
        f'          <p class="lc-stage-card__subtitle">{lab["subtitle_html"]}</p>\n'
        f'\n'
        f'          <div class="lc-h3">What You Do</div>\n'
        f'          <ul>\n'
        f'{what_items}\n'
        f'          </ul>\n'
        f'\n'
        f'          <div class="lc-h3">Result</div>\n'
        f'          {lab["result_html"]}'
        f'{cta_html}\n'
        f'        </div>'
    )


# ── Section renderers ────────────────────────────────────────────────

def render_section_overview(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    end_items = '\n'.join(f'        <li>{i}</li>' for i in s['endState_html'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-h3">{s["endStateHeading"]}</div>\n'
        f'      <ul>\n'
        f'{end_items}\n'
        f'      </ul>\n'
        f'      </div>'
    )


def render_module_section(m, two_col=False):
    classes = section_div_classes(m.get('labelColor'))
    label_html = render_section_label(m['label'], m.get('labelColor'))
    subtitle_html = render_subtitle(m['subtitle_html']) if m.get('subtitle_html') else ''
    grid_class = 'lc-stage-grid lc-stage-grid--2col' if two_col else 'lc-stage-grid'
    cards = '\n\n'.join(render_lab_card(l) for l in m['labs'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {m["intro_html"]}\n'
        f'\n'
        f'      <div class="{grid_class}">\n'
        f'{cards}\n'
        f'      </div>\n'
        f'      </div>'
    )


def render_section_final_product(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    stat_boxes = []
    for st in s['byTheNumbers']:
        stat_boxes.append(
            f'        <div class="lc-stat-box">\n'
            f'          <div class="lc-stat-box__num">{st["num"]}</div>\n'
            f'          <div class="lc-stat-box__label">{st["label"]}</div>\n'
            f'          <div class="lc-stat-box__sub">{st["sub"]}</div>\n'
            f'        </div>'
        )
    stats_html = '      <div class="lc-stat-grid">\n' + '\n'.join(stat_boxes) + '\n      </div>'

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["body_html"]}\n'
        f'\n'
        f'{stats_html}\n'
        f'\n'
        f'{render_mentor(s["closingMentor"])}\n'
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
        render_module_section(data['module1']),
        render_module_section(data['module2']),
        render_module_section(data['module3']),
        render_module_section(data['module4']),
        render_module_section(data['module5'], two_col=True),
        render_section_final_product(data['finalProduct']),
    ]
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        f'  <meta name="site-context" content="{data["siteContext"]}">\n'
        f'  <title>{data["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        '  <!-- ══════════════════════════════════════════════════════════\n'
        '       Project Plan — Module-by-Module Build Roadmap\n'
        '       Source of truth synthesized from pages/labs/json/lab-*.json\n'
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
    src = repo_root / 'pages' / 'scenario' / 'json' / 'project-plan.json'
    out = repo_root / 'pages' / 'scenario' / 'project-plan.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)
    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
