#!/usr/bin/env python3
"""
render_modules.py — Renders pages/support/module-N-overview.html (N=1..5)
from pages/support/json/modules.json.

Single source of truth for the five Module Overview pages. Mirrors the
architectural pattern used by render_start_here.py.

Each module page has four cards:
  1. Module Overview (color varies per module)
  2. Client Context (always orange)
  3. Skills & End State (always green)
  4. Recordings (always orange)

Run with:
    python3 render_modules.py

Source:  pages/support/json/modules.json
Output:  pages/support/module-1-overview.html
         pages/support/module-2-overview.html
         pages/support/module-3-overview.html
         pages/support/module-4-overview.html
         pages/support/module-5-overview.html
"""
import json
from pathlib import Path


# ── Tier-to-color mapping for lab table badges ────────────────────────

TIER_COLORS = {
    'BUILD': 'var(--neon-cyan)',
    'ENHANCE': 'var(--neon-orange)',
    'MASTER': 'var(--neon-purple)',
}


# ── Small renderers ──────────────────────────────────────────────────

def render_tier_badge(tier):
    """Inline BUILD/ENHANCE/MASTER badge used inside the lab-table 'Assignment' cell."""
    color = TIER_COLORS[tier]
    return (
        f'<span class="lc-cp-badge" style="display:inline-flex;vertical-align:middle;margin-right:8px;">'
        f'<span class="lc-cp-badge__word" style="background:{color};color:#000;font-size:8px;padding:2px 5px;">'
        f'{tier}</span></span>'
    )


def render_lab_row(lab, is_last):
    """One <tr> in the 'This Module' table. The last row gets the
    lc-table__total class on the <tr> for the highlighted master row."""
    tr_class = ' class="lc-table__total"' if is_last else ''
    badge = render_tier_badge(lab['tier'])
    return (
        f'            <tr{tr_class}>\n'
        f'              <td><strong>{lab["week"]}</strong></td>\n'
        f'              <td>{badge}<strong>Lab {lab["id"]}: {lab["title"]}</strong></td>\n'
        f'              <td>{lab["focus_html"]}</td>\n'
        f'            </tr>'
    )


def render_lab_table(card1):
    """Full lab table inside Card 1."""
    rows = []
    labs = card1['labs']
    for i, lab in enumerate(labs):
        is_last = (i == len(labs) - 1)
        rows.append(render_lab_row(lab, is_last))
    rows_html = '\n'.join(rows)
    return (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th>Week</th>\n'
        '              <th>Assignment</th>\n'
        '              <th>Focus</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        f'{rows_html}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def render_callout(callout):
    """An inline lc-callout block (single line, matching M5 source style)."""
    return (
        f'<div class="lc-callout lc-callout--{callout["variant"]}">'
        f'<div class="lc-callout__icon">'
        f'<span class="material-symbols-outlined">{callout["icon"]}</span>'
        f'</div>'
        f'<div class="lc-callout__bubble">'
        f'<div class="lc-callout__title">{callout["title"]}</div>'
        f'<div class="lc-callout__body">{callout["body_html"]}</div>'
        f'</div>'
        f'</div>'
    )


def render_recording_button(url, label):
    """Render one Chapter Notes / Lab Walkthrough button.

    If url is set, render as a real <a class="sp-rec-btn"> linking out.
    If url is null/missing, render as a disabled <span class="sp-rec-btn sp-rec-btn--placeholder">.
    """
    if url:
        return (
            f'        <a class="sp-rec-btn sp-rec-btn--active" href="{url}" '
            f'target="_blank" rel="noopener">{label}</a>'
        )
    return (
        f'        <span class="sp-rec-btn sp-rec-btn--placeholder" '
        f'title="Recording will be posted after the session.">{label}</span>'
    )


def render_recording_row(row):
    """One row in the recordings card: a label + Chapter Notes + Lab Walkthrough."""
    chapter_btn = render_recording_button(row.get('chapter_notes_url'), 'Chapter Notes')
    walkthrough_btn = render_recording_button(row.get('lab_walkthrough_url'), 'Lab Walkthrough')
    return (
        f'      <div class="sp-rec-row">\n'
        f'        <span class="sp-rec-lab-label">{row["label"]}</span>\n'
        f'{chapter_btn}\n'
        f'{walkthrough_btn}\n'
        f'      </div>'
    )


# ── Card renderers ───────────────────────────────────────────────────

def render_card1_overview(module):
    """Card 1: Module Overview, with course-badge topper + lab table.
    Color varies per module."""
    color = module['card1Color']
    card1 = module['card1']
    table_html = render_lab_table(card1)
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 1 — Module Overview ({color})\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color}">\n'
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
        f'            <div class="lc-topper-title">{card1["topperTitle"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="https://jfnewsom.github.io/is2053-assets/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{card1["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      {card1["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--{color}">{card1["tableTitle"]}</div>\n'
        f'{table_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_card2_client_context(module):
    """Card 2: Client Context — always orange. Includes mentor block."""
    card2 = module['card2']
    mentor = card2['mentor']
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 2 — Client Context (orange)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--orange">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{card2["topperTitle"]}</div>\n'
        f'      <div class="lc-sub-banner">{card2["subBanner"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      {card2["intro_html"]}\n'
        f'\n'
        f'      <div class="lc-mentor">\n'
        f'        <div class="lc-mentor__inner">\n'
        f'          <div class="lc-mentor__avatar">\n'
        f'            <img src="{mentor["avatar_url"]}" alt="{mentor["avatar_alt"]}">\n'
        f'          </div>\n'
        f'          <div class="lc-mentor__bubble">\n'
        f'            <p class="lc-mentor__quote">{mentor["quote_html"]}</p>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'        <div class="lc-mentor__attribution">\n'
        f'          <div class="lc-mentor__name">{mentor["name"]}</div>\n'
        f'          <div class="lc-mentor__role">{mentor["role"]}</div>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_card3_skills(module):
    """Card 3: Skills & End State — always green."""
    card3 = module['card3']
    skill_lis = '\n'.join(f'        <li>{s}</li>' for s in card3['skills_html'])

    # Optional celebrate-style callout
    if card3.get('callout'):
        callout_block = (
            f'\n      {render_callout(card3["callout"])}\n'
        )
    else:
        callout_block = '\n      \n'

    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 3 — Skills and End State (green)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--green">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{card3["topperTitle"]}</div>\n'
        f'      <div class="lc-sub-banner">{card3["subBanner"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--green">Skills You&rsquo;ll Build</div>\n'
        f'      <ul>\n'
        f'{skill_lis}\n'
        f'      </ul>\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--green">End State</div>\n'
        f'      {card3["end_state_html"]}\n'
        f'{callout_block}\n'
        f'      <p style="margin-top: 20px;">\n'
        f'        {card3["next_step_html"]}\n'
        f'      </p>\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_card4_recordings(module):
    """Card 4: Recordings — always orange. Rows of buttons (real anchors when
    URL is present, disabled spans otherwise)."""
    rec = module['card4_recordings']
    rows_html = '\n'.join(render_recording_row(r) for r in rec['rows'])
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD — Recordings (orange)\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--orange">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">Recordings</div>\n'
        f'      <div class="lc-sub-banner">Chapter Notes &bull; Lab Walkthroughs</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      {rec["intro_html"]}\n'
        f'\n'
        f'{rows_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


# ── Top-level page renderer ──────────────────────────────────────────

def render_module_page(module):
    """Render a complete module-N-overview.html document."""
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        f'  <title>{module["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        + render_card1_overview(module) + '\n\n\n'
        + render_card2_client_context(module) + '\n\n\n'
        + render_card3_skills(module) + '\n\n\n\n'
        + render_card4_recordings(module) + '\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


# ── Home page recordings card (cross-page, sentinel-marker injection) ─

HOME_RECORDINGS_START = '<!-- RECORDINGS:START -->'
HOME_RECORDINGS_END = '<!-- RECORDINGS:END -->'


def render_home_recordings_card(modules):
    """Render the orange Session Recordings card for home.html.

    Layout: one card containing all 5 modules. Each module gets a yellow
    `.sp-rec-mod-label` header (Module N: <thematic title>) followed by its
    lab rows. Same button rendering as the per-module Recordings card —
    active anchors for set URLs, disabled placeholder spans otherwise.

    Rendered between sentinel markers in home.html so the rest of the home
    page stays hand-edited.
    """
    blocks = []
    for module in modules:
        # Header label: "Module N: <title-without-prefix>"
        # topperTitle is like "Module 1: Getting Started" — use it as-is.
        header_label = module['card1']['topperTitle']
        blocks.append(f'      <div class="sp-rec-mod-label">{header_label}</div>')

        rec = module['card4_recordings']
        for row in rec['rows']:
            blocks.append(render_recording_row(row))

    rows_html = '\n'.join(blocks)

    return (
        '  <div class="lc-card lc-card--orange">\n'
        '    <div class="lc-topper">\n'
        '      <div class="lc-topper-title">Recordings</div>\n'
        '      <div class="lc-sub-banner">Chapter Notes &bull; Lab Walkthroughs</div>\n'
        '    </div>\n'
        '    <div class="lc-panel">\n'
        '\n'
        '      <p>Recordings will be posted here after each Tuesday office hours session. Same buttons live on each module overview page.</p>\n'
        '\n'
        f'{rows_html}\n'
        '\n'
        '    </div>\n'
        '  </div>'
    )


def update_home_recordings(home_path, card_html):
    """Rewrite the block between RECORDINGS:START and RECORDINGS:END in home.html.

    Raises ValueError if either marker is missing — the renderer never
    silently writes past a damaged home.html.
    """
    text = home_path.read_text(encoding='utf-8')

    start_idx = text.find(HOME_RECORDINGS_START)
    end_idx = text.find(HOME_RECORDINGS_END)
    if start_idx == -1:
        raise ValueError(
            f'Missing {HOME_RECORDINGS_START} marker in {home_path}. '
            f'Cannot safely inject recordings card.'
        )
    if end_idx == -1:
        raise ValueError(
            f'Missing {HOME_RECORDINGS_END} marker in {home_path}. '
            f'Cannot safely inject recordings card.'
        )
    if end_idx < start_idx:
        raise ValueError(
            f'Marker order reversed in {home_path}: END appears before START.'
        )

    # text[:start_idx] keeps everything up to (and including) the indentation
    # before the START marker. text[end_idx + len(END):] keeps everything from
    # after the END marker to EOF. Between them: marker, card, indent, marker.
    new_block = (
        HOME_RECORDINGS_START + '\n'
        + card_html + '\n'
        + '  '  # 2-space indent to match marker indentation in home.html
        + HOME_RECORDINGS_END
    )
    new_text = (
        text[:start_idx]
        + new_block
        + text[end_idx + len(HOME_RECORDINGS_END):]
    )
    home_path.write_text(new_text, encoding='utf-8')


# ── Entry point ──────────────────────────────────────────────────────

def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'modules.json'
    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    # 1. Render each module-N-overview.html
    for module in data['modules']:
        out = repo_root / 'pages' / 'support' / f'module-{module["num"]}-overview.html'
        html = render_module_page(module)
        out.write_text(html, encoding='utf-8')
        print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')

    # 2. Inject aggregated Recordings card into home.html between sentinel markers
    home_path = repo_root / 'pages' / 'support' / 'home.html'
    if home_path.exists():
        card_html = render_home_recordings_card(data['modules'])
        update_home_recordings(home_path, card_html)
        print(f'  Updated → {home_path}  (recordings block injected between sentinels)')
    else:
        print(f'  Skipped home.html (not found at {home_path})')


if __name__ == '__main__':
    main()
