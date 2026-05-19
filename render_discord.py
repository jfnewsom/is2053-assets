#!/usr/bin/env python3
"""
render_discord.py — Renders pages/support/discord.html
from pages/support/json/discord.json.

Single-card / sections-within layout (home-page pattern). One outer
purple card with five internal lc-named-section blocks:
  1. Overview              (default yellow) — intro + Is For / Is NOT For table
  2. Platform Disclaimer   (orange) — warning callout + implications h3 + list
  3. Server Rules          (blue)   — 5 colored rule sub-h3s + Enforcement
                                      warning callout
  4. Server Channels       (green)  — intro + 6-cell channel grid + code-blocks
                                      tip callout
  5. Join the Server       (purple) — agreement checklist + join link + welcome

Run with:
    python3 render_discord.py

Source:  pages/support/json/discord.json
Output:  pages/support/discord.html
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


# ── Section renderers ────────────────────────────────────────────────

def render_section_overview(s):
    """Section 1: Overview — intro + 2-col 'Is For / Is NOT For' table."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    tbl = s['isForTable']
    rows = []
    for r in tbl['rows']:
        rows.append(
            f'            <tr>\n'
            f'              <td>{r["left"]}</td>\n'
            f'              <td>{r["right"]}</td>\n'
            f'            </tr>'
        )
    table_html = (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        f'              <th>{tbl["leftHeader"]}</th>\n'
        f'              <th>{tbl["rightHeader"]}</th>\n'
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
        f'      {s["body_html"]}\n'
        f'\n'
        f'{table_html}\n'
        f'      </div>'
    )


def render_section_platform_disclaimer(s):
    """Section 2: Platform Disclaimer — subtitle + warning callout +
    implications sub-h3 + bullet list."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    color = s.get('labelColor', '')
    h3_class = f' lc-h3--{color}' if color else ''

    callout_html = render_callout(s['warningCallout'])

    imp = s['implications']
    items = '\n'.join(f'        <li>{i}</li>' for i in imp['items_html'])
    impl_block = (
        f'      <div class="lc-h3{h3_class}">{imp["heading"]}</div>\n'
        f'      <ul>\n'
        f'{items}\n'
        f'      </ul>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'{callout_html}\n'
        f'\n'
        f'{impl_block}\n'
        f'      </div>'
    )


def render_section_server_rules(s):
    """Section 3: Server Rules — subtitle + 5 colored rule sub-h3s
    (each with a body paragraph or list) + Enforcement warning callout."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    color = s.get('labelColor', '')
    h3_class = f' lc-h3--{color}' if color else ''

    rule_blocks = []
    for rule in s['rules']:
        rule_blocks.append(
            f'      <div class="lc-h3{h3_class}">{rule["heading"]}</div>\n'
            f'      {rule["body_html"]}'
        )
    rules_html = '\n\n'.join(rule_blocks)

    enforcement_html = render_callout(s['enforcementCallout'])

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'{rules_html}\n'
        f'\n'
        f'{enforcement_html}\n'
        f'      </div>'
    )


def render_section_server_channels(s):
    """Section 4: Server Channels — subtitle + intro + 6-cell channel
    grid (lc-contact-grid) + tip callout. Channel labels are colored
    green inline (matches section accent)."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    cells = []
    for ch in s['channels']:
        cells.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label" style="color: var(--neon-green);">{ch["name"]}</div>\n'
            f'          <div class="lc-contact-card__value">{ch["desc"]}</div>\n'
            f'        </div>'
        )
    grid_html = (
        '      <div class="lc-contact-grid">\n'
        + '\n'.join(cells) + '\n'
        '      </div>'
    )

    tip_html = render_callout(s['tipCallout'])

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{grid_html}\n'
        f'\n'
        f'{tip_html}\n'
        f'      </div>'
    )


def render_section_join(s):
    """Section 5: Join the Server — subtitle + intro + agreement checklist +
    join link + welcome line."""
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    items = '\n'.join(f'        <li>{i}</li>' for i in s['agreement_items_html'])
    items_html = (
        '      <ul>\n'
        f'{items}\n'
        '      </ul>'
    )

    join_link_html = (
        f'      <p>\n'
        f'        <a href="{s["joinUrl"]}" target="_blank" rel="noopener">\n'
        f'          {s["joinLabel_html"]}\n'
        f'        </a>\n'
        f'      </p>'
    )

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["intro_html"]}\n'
        f'\n'
        f'{items_html}\n'
        f'\n'
        f'{join_link_html}\n'
        f'\n'
        f'      {s["welcome_html"]}\n'
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
        render_section_platform_disclaimer(data['platformDisclaimer']),
        render_section_server_rules(data['serverRules']),
        render_section_server_channels(data['serverChannels']),
        render_section_join(data['joinTheServer']),
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
        '       Discord — single card, sections within (home-page pattern)\n'
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
    src = repo_root / 'pages' / 'support' / 'json' / 'discord.json'
    out = repo_root / 'pages' / 'support' / 'discord.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
