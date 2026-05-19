#!/usr/bin/env python3
"""
render_scenario.py — Renders pages/scenario/scenario.html
from pages/scenario/json/scenario.json.

Single-card / sections-within layout. One outer blue card with four
internal lc-named-section blocks:
  1. The Game        (default yellow) — game description + module bullets
                                        + payoff callout
  2. How to Play     (cyan)   — win condition, game loop, movement rules,
                                what we track, T-Bone closing quote
  3. Your Mission    (purple) — BUILD/ENHANCE/MASTER rhythm + table +
                                Danny closing quote
  4. Quick Reference (green)  — distance constants for early-module labs
                                (no fuel/money — those mechanics aren't
                                in the current game design)

Run with:
    python3 render_scenario.py

Source:  pages/scenario/json/scenario.json
Output:  pages/scenario/scenario.html
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


def render_callout(c):
    return (
        f'      <div class="lc-callout lc-callout--{c["variant"]}">\n'
        f'        <div class="lc-callout__icon">\n'
        f'          <span class="material-symbols-outlined">{c["icon"]}</span>\n'
        f'        </div>\n'
        f'        <div class="lc-callout__bubble">\n'
        f'          <div class="lc-callout__title">{c["title"]}</div>\n'
        f'          <div class="lc-callout__body">\n'
        f'            {c["body_html"]}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>'
    )


def render_mentor(m):
    """The lc-mentor avatar/quote/attribution block."""
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


# ── Section renderers ────────────────────────────────────────────────

def render_section_the_game(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    items = '\n'.join(f'        <li>{i}</li>' for i in s['whatYoureBuildingItems_html'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["about_html"]}\n'
        f'\n'
        f'      <div class="lc-h3">{s["whatYoureBuildingHeading"]}</div>\n'
        f'      {s["whatYoureBuildingIntro_html"]}\n'
        f'      <ul>\n'
        f'{items}\n'
        f'      </ul>\n'
        f'\n'
        f'{render_callout(s["payoffCallout"])}\n'
        f'      </div>'
    )


def render_section_how_to_play(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    color = s.get('labelColor', '')
    h3_class = f' lc-h3--{color}' if color else ''

    game_loop_items = '\n'.join(f'        <li>{i}</li>' for i in s['gameLoopSteps_html'])
    movement_items = '\n'.join(f'        <li>{i}</li>' for i in s['movementRules_html'])

    track_cells = []
    for t in s['whatWeTrack']:
        track_cells.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label" style="color: var(--lc-accent);">{t["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">{t["desc"]}</div>\n'
            f'        </div>'
        )
    track_grid = '      <div class="lc-contact-grid">\n' + '\n'.join(track_cells) + '\n      </div>'

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      <div class="lc-h3{h3_class}">{s["winConditionHeading"]}</div>\n'
        f'      {s["winCondition_html"]}\n'
        f'\n'
        f'      <div class="lc-h3{h3_class}">{s["gameLoopHeading"]}</div>\n'
        f'      {s["gameLoopIntro_html"]}\n'
        f'      <ol>\n'
        f'{game_loop_items}\n'
        f'      </ol>\n'
        f'\n'
        f'      <div class="lc-h3{h3_class}">{s["movementRulesHeading"]}</div>\n'
        f'      <ul>\n'
        f'{movement_items}\n'
        f'      </ul>\n'
        f'\n'
        f'      <div class="lc-h3{h3_class}">{s["whatWeTrackHeading"]}</div>\n'
        f'      {s["whatWeTrackIntro_html"]}\n'
        f'{track_grid}\n'
        f'\n'
        f'{render_mentor(s["closingMentor"])}\n'
        f'      </div>'
    )


def render_section_your_mission(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    color = s.get('labelColor', '')
    h3_class = f' lc-h3--{color}' if color else ''

    rt = s['rhythmTable']
    headers = '\n'.join(f'              <th>{h}</th>' for h in rt['headers'])
    rows = []
    for r in rt['rows']:
        tr_class = ' class="lc-table__total"' if r.get('highlight') else ''
        rows.append(
            f'            <tr{tr_class}>\n'
            f'              <td>{r["stage"]}</td>\n'
            f'              <td>{r["sprint"]}</td>\n'
            f'              <td>{r["goal"]}</td>\n'
            f'            </tr>'
        )
    rows_html = '\n'.join(rows)
    table_html = (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        f'{headers}\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        f'{rows_html}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      <div class="lc-h3{h3_class}">{s["rhythmHeading"]}</div>\n'
        f'      {s["rhythmIntro_html"]}\n'
        f'\n'
        f'{table_html}\n'
        f'\n'
        f'      {s["keyInsight_html"]}\n'
        f'\n'
        f'{render_mentor(s["closingMentor"])}\n'
        f'      </div>'
    )


def render_section_quick_reference(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    closing = s.get('closingNote_html', '')
    closing_block = f'\n\n      {closing}' if closing else ''
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'      {s["code_html"]}'
        f'{closing_block}\n'
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
        render_section_the_game(data['theGame']),
        render_section_how_to_play(data['howToPlay']),
        render_section_your_mission(data['yourMission']),
        render_section_quick_reference(data['quickReference']),
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
        '       Scenario — single card, sections within (home-page pattern)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        f'      {data["intro_html"]}\n\n'
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
    src = repo_root / 'pages' / 'scenario' / 'json' / 'scenario.json'
    out = repo_root / 'pages' / 'scenario' / 'scenario.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)
    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
