#!/usr/bin/env python3
"""
render_assignment_overview.py — Renders pages/support/assignment-overview.html
from pages/support/json/assignments.json.

Single-card / sections-within layout (home-page pattern). One outer
purple card with five internal lc-named-section blocks:
  1. The Three-Stage Rhythm  (default yellow) — intro paragraphs
  2. BUILD     (blue)   — Lab X.1 / Foundation; What You Do, What's Due
  3. ENHANCE   (orange) — Lab X.2 / Add Features
  4. MASTER    (green)  — Lab X.3 / Polish & Complete
  5. Why This Works  (cyan) — intro + 4-card grid

The three stage sections share the same shape (label + subtitle + two
sub-headed lists) so they're emitted by a single render_section_stage
function parameterized by color and content.

Run with:
    python3 render_assignment_overview.py

Source:  pages/support/json/assignments.json
Output:  pages/support/assignment-overview.html
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
    descendants."""
    cls = 'lc-named-section'
    if color:
        cls += f' lc-named-section--{color}'
    return cls


# ── Section renderers ────────────────────────────────────────────────

def render_section_intro(intro):
    """Section 1: The Three-Stage Rhythm — intro paragraphs followed by
    a 3-up side-by-side grid of stage cards (BUILD / ENHANCE / MASTER).
    Each stage is parallel by design; showing them next to each other
    reinforces that pattern."""
    classes = section_div_classes(intro.get('labelColor'))
    label_html = render_section_label(intro['label'], intro.get('labelColor'))

    stage_cards_html = '\n'.join(render_stage_card(s) for s in intro['stages'])

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {intro["body_html"]}\n'
        f'\n'
        f'      <div class="lc-stage-grid">\n'
        f'{stage_cards_html}\n'
        f'      </div>\n'
        f'      </div>'
    )


def render_stage_card(stage):
    """A single stage card inside lc-stage-grid (BUILD / ENHANCE / MASTER).
    Shape: colored label + small italic subtitle + two sub-h3 blocks
    (What You Do / What's Due). The h3s pick up sub-banner styling via
    the `.lc-stage-card .lc-h3` rule in labs.css."""
    color = stage.get('labelColor', '')
    label_class = 'lc-stage-card__label'
    if color:
        label_class += f' lc-stage-card__label--{color}'
    h3_class = f' lc-h3--{color}' if color else ''
    return (
        f'        <div class="lc-stage-card">\n'
        f'          <div class="{label_class}">{stage["label"]}</div>\n'
        f'          <div class="lc-stage-card__subtitle">{stage["subtitle_html"]}</div>\n'
        f'\n'
        f'          <div class="lc-h3{h3_class}">What You Do</div>\n'
        f'          {stage["whatYouDo_html"]}\n'
        f'\n'
        f'          <div class="lc-h3{h3_class}">What&rsquo;s Due</div>\n'
        f'          {stage["whatsDue_html"]}\n'
        f'        </div>'
    )


def render_section_why(why):
    """Section 5: Why This Works — intro + 4-card lc-contact-grid."""
    classes = section_div_classes(why.get('labelColor'))
    label_html = render_section_label(why['label'], why.get('labelColor'))

    cards = []
    for c in why['cards']:
        cards.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label">{c["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">{c["value_html"]}</div>\n'
            f'        </div>'
        )
    cards_html = '\n'.join(cards)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {why["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-contact-grid">\n'
        f'{cards_html}\n'
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

    intro_section = render_section_intro(data['intro'])
    why_section = render_section_why(data['whyThisWorks'])

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
        '       Assignment Overview — single card, sections within (home-page pattern)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        f'{intro_section}\n\n'
        f'{why_section}\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'assignments.json'
    out = repo_root / 'pages' / 'support' / 'assignment-overview.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
