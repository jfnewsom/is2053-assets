#!/usr/bin/env python3
"""
render_bat_city.py — Renders pages/scenario/bat-city.html
from pages/scenario/json/bat-city.json.

Single-card / sections-within layout. One outer purple card with two
internal lc-named-section blocks:
  1. About the Studio  (default yellow) — intro + Danny opening quote +
                                          Company Culture + Your Role
  2. Meet the Team     (purple)         — five mentor blocks (Danny,
                                          Sasha, T-Bone, Priya, Tyler),
                                          each with a quote and a bio

Run with:
    python3 render_bat_city.py

Source:  pages/scenario/json/bat-city.json
Output:  pages/scenario/bat-city.html
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


# ── Section renderers ────────────────────────────────────────────────

def render_section_about_studio(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    culture_items = '\n'.join(f'        <li>{i}</li>' for i in s['cultureItems_html'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{render_mentor(s["openingMentor"])}\n'
        f'\n'
        f'      <div class="lc-h3">{s["cultureHeading"]}</div>\n'
        f'      {s["cultureIntro_html"]}\n'
        f'      <ul>\n'
        f'{culture_items}\n'
        f'      </ul>\n'
        f'\n'
        f'      <div class="lc-h3">{s["yourRoleHeading"]}</div>\n'
        f'      {s["yourRole_html"]}\n'
        f'      </div>'
    )


def render_section_meet_the_team(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    member_blocks = []
    for m in s['members']:
        member_blocks.append(
            f'{render_mentor(m)}\n'
            f'      {m["bio_html"]}'
        )
    members_html = '\n\n'.join(member_blocks)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{members_html}\n'
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
        render_section_about_studio(data['aboutTheStudio']),
        render_section_meet_the_team(data['meetTheTeam']),
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
        '       Bat City Collective — single card, sections within\n'
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
    src = repo_root / 'pages' / 'scenario' / 'json' / 'bat-city.json'
    out = repo_root / 'pages' / 'scenario' / 'bat-city.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)
    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
