#!/usr/bin/env python3
"""
render_how_to_get_help.py — Renders pages/support/how-to-get-help.html
from pages/support/json/help.json.

This page absorbs the deleted zoom-sessions.html. All help-channel
content lives here: Discord, Tuesday office hours, Calendly bookings,
and email — each as a section within a single outer card (home-page
pattern).

Page structure: one outer purple card with five internal
lc-named-section blocks:
  1. Quick Reference  (default yellow) — intro + 4-channel contact grid
  2. Discord          (purple) — when/how to use, code blocks tip
  3. Tuesday Office Hours  (cyan) — when/where, what to expect, recording note
  4. Book a 1-on-1    (green) — Calendly when/why
  5. Email            (orange) — when to email, contact card, pro tip

Run with:
    python3 render_how_to_get_help.py

Source:  pages/support/json/help.json
Output:  pages/support/how-to-get-help.html
"""
import json
from pathlib import Path


# ── Helpers ──────────────────────────────────────────────────────────

def render_section_label(label, color):
    """Yellow-by-default named-section label."""
    cls = 'lc-named-section__label'
    if color:
        cls += f' lc-named-section__label--{color}'
    return f'      <div class="{cls}">{label}</div>'


def section_div_classes(color):
    """CSS class list for the lc-named-section div given an optional color.
    Drives the section-scoped --lc-accent override that propagates to
    descendants (table headers, etc.)."""
    cls = 'lc-named-section'
    if color:
        cls += f' lc-named-section--{color}'
    return cls


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


# ── Section renderers ────────────────────────────────────────────────

def render_section_quick_ref(qr):
    """Section 1: Quick Reference — intro + 4-channel lc-contact-grid."""
    classes = section_div_classes(qr.get('labelColor'))
    label_html = render_section_label(qr['label'], qr.get('labelColor'))

    cards = []
    for ch in qr['channels']:
        cards.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label" style="color: var({ch["labelColorVar"]});">{ch["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">\n'
            f'            {ch["value_html"]}\n'
            f'          </div>\n'
            f'        </div>'
        )
    cards_html = '\n'.join(cards)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {qr["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-contact-grid">\n'
        f'{cards_html}\n'
        f'      </div>\n'
        f'      </div>'
    )


def render_section_channel(ch):
    """Render a channel section (Discord / Office Hours / Calendly / Email).

    Each channel has: label + labelColor, list of sub-sections (h3 + body),
    optional callout, optional contactCard, optional closing_html."""
    classes = section_div_classes(ch.get('labelColor'))
    label_html = render_section_label(ch['label'], ch.get('labelColor'))
    sub_color = ch.get('labelColor', '')
    h3_class = f' lc-h3--{sub_color}' if sub_color else ''

    blocks = []
    for section in ch.get('sections', []):
        sub_block = (
            f'      <div class="lc-h3{h3_class}">{section["heading"]}</div>\n'
            f'      {section["body_html"]}'
        )
        blocks.append(sub_block)

    # Optional contact-card subgrid (used by Email section)
    if ch.get('contactCard'):
        cc = ch['contactCard']
        contact_block = (
            f'      <div class="lc-contact-grid">\n'
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label" style="color: var({cc["labelColorVar"]});">{cc["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">\n'
            f'            {cc["value_html"]}\n'
            f'          </div>\n'
            f'        </div>\n'
            f'      </div>'
        )
        blocks.append(contact_block)

    # Optional callout
    if ch.get('callout'):
        blocks.append(render_callout(ch['callout']))

    # Optional closing link/paragraph (used by Discord section)
    if ch.get('closing_html'):
        blocks.append(f'      {ch["closing_html"]}')

    body = '\n\n'.join(blocks)
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{body}\n'
        f'      </div>'
    )


# ── Top-level renderer ───────────────────────────────────────────────

def render_card_topper(card_meta):
    """Course-badge topper at the top of the outer card."""
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
    """Render how-to-get-help.html — one outer purple card with five sections."""
    card = data['card']
    color = card['color']

    quick_ref_section = render_section_quick_ref(data['quickRef'])
    discord_section = render_section_channel(data['discord'])
    office_hours_section = render_section_channel(data['officeHours'])
    calendly_section = render_section_channel(data['calendly'])
    email_section = render_section_channel(data['email'])

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
        '       How to Get Help — single card, sections within (home-page pattern)\n'
        '       Absorbs the former zoom-sessions.html\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        f'{quick_ref_section}\n\n'
        f'{discord_section}\n\n'
        f'{office_hours_section}\n\n'
        f'{calendly_section}\n\n'
        f'{email_section}\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'help.json'
    out = repo_root / 'pages' / 'support' / 'how-to-get-help.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
