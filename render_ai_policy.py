#!/usr/bin/env python3
"""
render_ai_policy.py — Renders pages/support/ai-policy.html
from pages/support/json/ai-policy.json.

Single-card / mixed-flow layout (home-page pattern). One outer purple
card. Content flows linearly inside the panel as a mix of free-standing
callouts and named sections — the same shape the IS3513 GenAI policy
uses. Top-to-bottom:

  1. intro paragraph
  2. opening purple callout — "learn or grade?"
  3. framing paragraphs — learn vs grade stakes
  4. green decision callout — "The Question That Decides Everything"
  5. cyan named section — Why Employers Care
  6. orange named section — Use AI / Don't Use AI  (2-col DO/DON'T grid)
  7. purple named section — Real Examples  (2-col OK/Not OK grid)
  8. blue tutor callout — "Tutor, Not Ghostwriter"
  9. cyan named section — The Bigger Picture  (3 sub-h3s)
 10. blue named section — Scope Compliance  (with warning callout)
 11. red named section — The Honest Test
 12. purple bottom-line callout
 13. footer line

Run with:
    python3 render_ai_policy.py

Source:  pages/support/json/ai-policy.json
Output:  pages/support/ai-policy.html
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
    """Free-standing callout (used both inside sections and in the panel
    flow). The 'variant' value maps to .lc-callout--{variant}."""
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


def render_stage_card(label_html, label_color, subtitle, list_items_html):
    """A single lc-stage-card for the 2-col comparison grids. Items can
    arrive as either {'title','desc'} dicts (DO/DON'T form) or raw HTML
    strings (Real Examples form)."""
    label_class = 'lc-stage-card__label'
    if label_color:
        label_class += f' lc-stage-card__label--{label_color}'

    subtitle_block = ''
    if subtitle:
        subtitle_block = f'          <div class="lc-stage-card__subtitle">{subtitle}</div>\n\n'

    # Build the <li>s
    li_lines = []
    for item in list_items_html:
        if isinstance(item, dict):
            li_lines.append(
                f'            <li><strong>{item["title"]}</strong> &mdash; {item["desc"]}</li>'
            )
        else:
            li_lines.append(f'            <li>{item}</li>')
    list_html = '\n'.join(li_lines)

    return (
        f'        <div class="lc-stage-card">\n'
        f'          <div class="{label_class}">{label_html}</div>\n'
        f'{subtitle_block}'
        f'          <ul>\n'
        f'{list_html}\n'
        f'          </ul>\n'
        f'        </div>'
    )


def render_2col_grid(left_card, right_card):
    """Wrap two stage-cards in a lc-stage-grid--2col."""
    return (
        f'      <div class="lc-stage-grid lc-stage-grid--2col">\n'
        f'{left_card}\n'
        f'{right_card}\n'
        f'      </div>'
    )


# ── Section renderers ────────────────────────────────────────────────

def render_section_why_employers_care(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {s["body_html"]}\n'
        f'      </div>'
    )


def render_section_use_ai_or_not(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''

    do_card = render_stage_card(
        s['do']['label'], s['do']['labelColor'], s['do'].get('subtitle'), s['do']['items']
    )
    dont_card = render_stage_card(
        s['dont']['label'], s['dont']['labelColor'], s['dont'].get('subtitle'), s['dont']['items']
    )
    grid_html = render_2col_grid(do_card, dont_card)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'{grid_html}\n'
        f'      </div>'
    )


def render_section_real_examples(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))

    ok_card = render_stage_card(
        s['ok']['label'], s['ok']['labelColor'], None, s['ok']['items_html']
    )
    not_ok_card = render_stage_card(
        s['notOk']['label'], s['notOk']['labelColor'], None, s['notOk']['items_html']
    )
    grid_html = render_2col_grid(ok_card, not_ok_card)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'\n'
        f'{grid_html}\n'
        f'      </div>'
    )


def render_section_bigger_picture(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    color = s.get('labelColor', '')
    h3_class = f' lc-h3--{color}' if color else ''

    blocks = []
    for sub in s['subSections']:
        blocks.append(
            f'      <div class="lc-h3{h3_class}">{sub["heading"]}</div>\n'
            f'      {sub["body_html"]}'
        )
    body = '\n\n'.join(blocks)
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'\n'
        f'{body}\n'
        f'      </div>'
    )


def render_section_scope_compliance(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    callout_html = render_callout(s['warningCallout'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["body_html"]}\n'
        f'\n'
        f'{callout_html}\n'
        f'      </div>'
    )


def render_section_honest_test(s):
    classes = section_div_classes(s.get('labelColor'))
    label_html = render_section_label(s['label'], s.get('labelColor'))
    subtitle_html = render_subtitle(s['subtitle_html']) if s.get('subtitle_html') else ''
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'{subtitle_html}\n'
        f'\n'
        f'      {s["body_html"]}\n'
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

    # Linear flow of blocks inside lc-panel
    blocks = [
        f'      {data["intro_html"]}',
        render_callout(data['openingCallout']),
        f'      {data["framing_html"]}',
        render_callout(data['decisionCallout']),
        render_section_why_employers_care(data['whyEmployersCare']),
        render_section_use_ai_or_not(data['useAiOrNot']),
        render_section_real_examples(data['realExamples']),
        render_callout(data['tutorCallout']),
        render_section_bigger_picture(data['biggerPicture']),
        render_section_scope_compliance(data['scopeCompliance']),
        render_section_honest_test(data['honestTest']),
        render_callout(data['bottomLineCallout']),
    ]

    if data.get('footer_html'):
        blocks.append(f'      {data["footer_html"]}')

    panel_body = '\n\n'.join(blocks)

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
        '       AI Policy — single card, mixed callout/section flow\n'
        '       (adapted from IS3513 GenAI policy to programming context)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
        f'{render_card_topper(card)}\n'
        '    <div class="lc-panel">\n\n'
        + panel_body + '\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'ai-policy.json'
    out = repo_root / 'pages' / 'support' / 'ai-policy.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
