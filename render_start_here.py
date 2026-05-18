#!/usr/bin/env python3
"""
render_start_here.py — Renders pages/support/start-here.html from start-here.json.

Architecture B: JSON is the single source of truth for the Start Here page.
A future render of pages/support/hello-world.html will pull from the same CP9
content + its own hello-world.json for the standalone-page framing.

Output is byte-identical to the hand-written start-here.html as of Round 10.
Run with:
    python3 render_start_here.py

Source:  pages/support/json/start-here.json
Output:  pages/support/start-here.html
"""
import json
import sys
from pathlib import Path


# ── Content-item renderers ────────────────────────────────────────────

def render_paragraph(item):
    """A <p> with HTML body, with optional inline style."""
    style_attr = f' style="{item["style"]}"' if item.get('style') else ''
    return f'        <p{style_attr}>\n          {item["html"]}\n        </p>'


def render_link_paragraph(item):
    """A <p> wrapping a single anchor — common pattern in start-here."""
    attrs = ''
    if item.get('external', False):
        attrs = '\n             target="_blank" rel="noopener"'
    return (
        f'        <p>\n'
        f'          <a href="{item["url"]}"{attrs}>{item["text"]}</a>\n'
        f'        </p>'
    )


def render_ordered_list(item):
    """An <ol> with HTML <li> items."""
    lines = ['        <ol>']
    for li in item['items']:
        lines.append(f'          <li>{li}</li>')
    lines.append('        </ol>')
    return '\n'.join(lines)


def render_unordered_list(item):
    """A <ul> with HTML <li> items."""
    lines = ['        <ul>']
    for li in item['items']:
        lines.append(f'          <li>{li}</li>')
    lines.append('        </ul>')
    return '\n'.join(lines)


def render_callout(item):
    """A lc-callout block with icon, title, body_html."""
    return (
        f'        <div class="lc-callout lc-callout--{item["variant"]}">\n'
        f'          <div class="lc-callout__icon">\n'
        f'            <span class="material-symbols-outlined">{item["icon"]}</span>\n'
        f'          </div>\n'
        f'          <div class="lc-callout__bubble">\n'
        f'            <div class="lc-callout__title">{item["title"]}</div>\n'
        f'            <div class="lc-callout__body">\n'
        f'              {item["body_html"]}\n'
        f'            </div>\n'
        f'          </div>\n'
        f'        </div>'
    )


def render_h3(item, indent='        '):
    """Section heading. Optional color variant."""
    color_class = f' lc-h3--{item["color"]}' if item.get('color') else ''
    return f'{indent}<div class="lc-h3{color_class}">{item["text"]}</div>'


def render_code_block(item):
    """A lc-code-block with raw HTML inside <pre>."""
    raw = item['raw_html']
    return f'        <div class="lc-code-block"><pre>{raw}</pre></div>'


def render_cta_button(item):
    """A large CTA button (lc-cta-btn) wrapping a Material icon + text.

    Supports optional 'id' for JS hooks (e.g., Fall section-aware link rewriting).
    """
    id_attr = f' id="{item["id"]}"' if item.get('id') else ''
    return (
        f'        <p>\n'
        f'          <a href="{item["url"]}"{id_attr}\n'
        f'             class="lc-cta-btn">\n'
        f'            <span class="material-symbols-outlined" style="vertical-align: middle; margin-right: 6px;">{item["icon"]}</span>\n'
        f'            {item["text"]}\n'
        f'          </a>\n'
        f'        </p>'
    )


def render_mentor(item):
    """Mentor quote block — used in Card 1 Overview."""
    return (
        f'      <div class="lc-mentor">\n'
        f'        <div class="lc-mentor__inner">\n'
        f'          <div class="lc-mentor__avatar">\n'
        f'            <img src="{item["avatar"]}"\n'
        f'                 alt="{item["name"]}">\n'
        f'          </div>\n'
        f'          <div class="lc-mentor__bubble">\n'
        f'            <p class="lc-mentor__quote">\n'
        f'              {item["quote"]}\n'
        f'            </p>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'        <div class="lc-mentor__attribution">\n'
        f'          <div class="lc-mentor__name">{item["name"]}</div>\n'
        f'          <div class="lc-mentor__role">{item["role"]}</div>\n'
        f'        </div>\n'
        f'      </div>'
    )


def render_contact_grid(item):
    """Contact grid block — used in Need Help card."""
    cards_html = []
    for card in item['cards']:
        cards_html.append(
            f'        <div class="lc-contact-card">\n'
            f'          <div class="lc-contact-card__label">{card["label"]}</div>\n'
            f'          <div class="lc-contact-card__value">\n'
            f'            {card["value_html"]}\n'
            f'          </div>\n'
            f'        </div>'
        )
    return (
        '      <div class="lc-contact-grid">\n'
        + '\n'.join(cards_html) + '\n'
        + '      </div>'
    )


# ── Dispatch table ─────────────────────────────────────────────────────

# Content-item types that go INSIDE a checkpoint body (indent: 8 spaces)
CP_RENDERERS = {
    'paragraph': render_paragraph,
    'link_paragraph': render_link_paragraph,
    'ordered_list': render_ordered_list,
    'unordered_list': render_unordered_list,
    'callout': render_callout,
    'h3': render_h3,
    'code_block': render_code_block,
    'cta_button': render_cta_button,
}


def render_cp_body_item(item):
    rtype = item['type']
    if rtype not in CP_RENDERERS:
        raise ValueError(f"Unknown CP body type: {rtype}")
    return CP_RENDERERS[rtype](item)


# Section types that go inside top-level card panels (indent: 6 spaces)
def render_card_section(item):
    """For sections inside Overview / Need Help cards (6-space indent)."""
    rtype = item['type']
    if rtype == 'h3':
        return render_h3(item, indent='      ')
    elif rtype == 'paragraph':
        # 6-space indent variant
        style_attr = f' style="{item["style"]}"' if item.get('style') else ''
        return f'      <p{style_attr}>\n        {item["html"]}\n      </p>'
    elif rtype == 'mentor':
        return render_mentor(item)
    elif rtype == 'ordered_list':
        lines = ['      <ol>']
        for li in item['items']:
            lines.append(f'        <li>{li}</li>')
        lines.append('      </ol>')
        return '\n'.join(lines)
    elif rtype == 'contact_grid':
        return render_contact_grid(item)
    elif rtype == 'callout':
        # Callouts in card sections use 6-space indent vs 8-space in CP bodies
        return (
            f'      <div class="lc-callout lc-callout--{item["variant"]}">\n'
            f'        <div class="lc-callout__icon">\n'
            f'          <span class="material-symbols-outlined">{item["icon"]}</span>\n'
            f'        </div>\n'
            f'        <div class="lc-callout__bubble">\n'
            f'          <div class="lc-callout__title">{item["title"]}</div>\n'
            f'          <div class="lc-callout__body">\n'
            f'            {item["body_html"]}\n'
            f'          </div>\n'
            f'        </div>\n'
            f'      </div>'
        )
    else:
        raise ValueError(f"Unknown card section type: {rtype}")


# ── Card-level renderers ──────────────────────────────────────────────

def render_topper_with_badge(meta):
    """Render the Card 1 topper with course badge + title + logo."""
    badge = meta['courseBadge']
    logo = meta['topperLogo']
    return (
        f'    <div class="lc-topper">\n'
        f'      <table style="width: 100%; border-collapse: collapse;">\n'
        f'        <tr>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0;">\n'
        f'            <div class="lc-course-badge">\n'
        f'              <div class="lc-course-badge__word">{badge["word"]}</div>\n'
        f'              <div class="lc-course-badge__num">{badge["num"]}</div>\n'
        f'            </div>\n'
        f'          </td>\n'
        f'          <td style="vertical-align: bottom; padding: 0 0 0 16px;">\n'
        f'            <div class="lc-topper-title">{meta["title"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="{logo["src"]}"\n'
        f'                 alt="{logo["alt"]}" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{meta["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>'
    )


def render_simple_topper(title, sub_banner):
    """Render a plain topper (no badge) for Cards 3 and 4."""
    return (
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{title}</div>\n'
        f'      <div class="lc-sub-banner">{sub_banner}</div>\n'
        f'    </div>'
    )


def render_overview_card(meta, card):
    """Card 1 — Overview (blue, with course-badge topper)."""
    sections_html = '\n\n'.join(
        render_card_section(s) for s in card['sections']
    )
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 1 — Overview ({card["color"]})\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{card["color"]}">\n'
        f'{render_topper_with_badge(meta)}\n'
        f'    <div class="lc-panel">\n\n'
        f'{sections_html}\n\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_checkpoint(cp):
    """Render a single checkpoint row + body + separator."""
    num = cp['num']
    title = cp['title']
    sub = cp['subBanner']

    # Comment marker — match the original hand-rolled width
    if num < 10:
        comment = f'<!-- CP {num} ─────────────────────────────────────────────── -->'
    elif num == 10 or num == 11:
        # Original had varying widths; CP10 used "─" * 19, CP11 used 18
        if num == 10:
            comment = f'<!-- CP 10 ─────────────────────────────────────────────── -->'
        else:
            comment = f'<!-- CP 11 ────────────────────────────────────────────── -->'
    else:
        # CP12 used 18 dashes (one less than CP10)
        comment = f'<!-- CP 12 ────────────────────────────────────────────── -->'

    body_items_html = '\n'.join(render_cp_body_item(item) for item in cp['body'])

    return (
        f'      {comment}\n'
        f'      <div class="lc-cp-row">\n'
        f'        <div class="lc-cp-badge">\n'
        f'          <div class="lc-cp-badge__word">CHECKPOINT</div>\n'
        f'          <div class="lc-cp-badge__num">{num}</div>\n'
        f'        </div>\n'
        f'        <div class="lc-cp-content">\n'
        f'          <div class="lc-cp-title">{title}</div>\n'
        f'          <div class="lc-sub-banner">{sub}</div>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'      <div class="lc-cp-body">\n'
        f'{body_items_html}\n'
        f'      </div>'
    )


def render_checkpoints_card(card, checkpoints):
    """Card 3 — Checkpoints (green, with intro + 12 CPs)."""
    pre_html = '\n\n'.join(render_card_section(s) for s in card['preContent'])

    # Render all 12 CPs, separated by hr.lc-cp-sep
    cp_blocks = []
    for i, cp in enumerate(checkpoints):
        cp_html = render_checkpoint(cp)
        is_last = (i == len(checkpoints) - 1)
        if is_last:
            # Last CP — no separator
            cp_blocks.append(cp_html)
        else:
            cp_blocks.append(cp_html + '\n      <hr class="lc-cp-sep">')

    # Original spacing: TWO blank lines between CPs after the hr
    cps_html = '\n\n\n'.join(cp_blocks)

    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 3 — Checkpoints ({card["color"]})\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{card["color"]}">\n'
        f'{render_simple_topper(card["title"], card["subBanner"])}\n'
        f'    <div class="lc-panel">\n\n'
        f'{pre_html}\n\n\n'
        f'{cps_html}\n\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_need_help_card(card):
    """Card 4 — Need Help? (purple)."""
    sections_html = '\n\n'.join(
        render_card_section(s) for s in card['sections']
    )
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       CARD 4 — Need Help? ({card["color"]})\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{card["color"]}">\n'
        f'{render_simple_topper(card["title"], card["subBanner"])}\n'
        f'    <div class="lc-panel">\n\n'
        f'{sections_html}\n\n'
        f'    </div>\n'
        f'  </div>'
    )


# ── Page renderer ─────────────────────────────────────────────────────

def render_page(data):
    """Render the complete start-here.html from JSON data."""
    meta = data['meta']
    cards = data['cards']
    checkpoints = data['checkpoints']

    html_doc = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        '  <meta name="site-context" content="support">\n'
        f'  <title>{meta["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        + render_overview_card(meta, cards['overview']) + '\n\n\n'
        + render_checkpoints_card(cards['checkpointsCard'], checkpoints) + '\n\n\n'
        + render_need_help_card(cards['needHelp']) + '\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )
    return html_doc


# ── $ref resolver ─────────────────────────────────────────────────────

def resolve_ref(ref_str, repo_root):
    """Resolve a $ref like 'start-here.json#/checkpoints[num=9]/body'.

    Supports a single non-standard extension over JSON Pointer: array element
    selection by field-value like [num=9] instead of zero-indexed array
    positions. That makes refs readable and stable across reorderings.

    Returns the resolved value.
    """
    if '#' not in ref_str:
        raise ValueError(f"Bad $ref (no fragment): {ref_str}")
    file_part, frag = ref_str.split('#', 1)
    json_file = repo_root / 'pages' / 'support' / 'json' / file_part
    with open(json_file) as f:
        data = json.load(f)

    # Walk the pointer fragments
    if not frag.startswith('/'):
        raise ValueError(f"Bad fragment (must start with /): {frag}")
    parts = frag.lstrip('/').split('/')
    node = data
    for part in parts:
        if part == '':
            continue
        # Field-value selector: e.g. checkpoints[num=9]
        # Format: <key>[<field>=<value>]
        if '[' in part and part.endswith(']'):
            key, selector = part.split('[', 1)
            selector = selector[:-1]  # drop trailing ]
            field, value = selector.split('=', 1)
            arr = node[key]
            if not isinstance(arr, list):
                raise ValueError(f"Selector applied to non-list: {key}")
            # Try numeric coercion for the value
            try:
                value_typed = int(value)
            except ValueError:
                value_typed = value
            matches = [item for item in arr if item.get(field) == value_typed]
            if not matches:
                raise ValueError(f"No element with {field}={value_typed!r} in {key}")
            if len(matches) > 1:
                raise ValueError(f"Multiple elements with {field}={value_typed!r} in {key}")
            node = matches[0]
        else:
            # Plain key or numeric index
            if isinstance(node, list):
                node = node[int(part)]
            else:
                node = node[part]
    return node


def resolve_refs(obj, repo_root):
    """Recursively resolve $ref entries in a JSON tree.

    If obj is a dict with exactly one key '$ref', replace it with the
    resolved value. Otherwise, walk children.
    """
    if isinstance(obj, dict):
        if list(obj.keys()) == ['$ref']:
            return resolve_ref(obj['$ref'], repo_root)
        return {k: resolve_refs(v, repo_root) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_refs(item, repo_root) for item in obj]
    return obj


# ── hello-world.html renderer ─────────────────────────────────────────

def render_hero_card_with_intro_body_outro(meta, card):
    """Render the BookEx-style hero card for the standalone hello-world page.

    Layout: course-badge topper → intro paragraphs → body (shared from CP9) → outro.
    """
    intro_html = '\n'.join(render_cp_body_item(item) for item in card['intro'])
    body_html = '\n'.join(render_cp_body_item(item) for item in card['body'])
    outro_html = '\n'.join(render_cp_body_item(item) for item in card['outro'])

    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       Hello World — Standalone assignment page ({card["color"]})\n'
        f'       Body shared via $ref from start-here.json#/checkpoints[num=9]/body\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{card["color"]}">\n'
        f'{render_topper_with_badge(meta)}\n'
        f'    <div class="lc-panel">\n\n'
        f'{intro_html}\n\n'
        f'{body_html}\n\n'
        f'{outro_html}\n\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_hello_world_page(data):
    """Render the standalone hello-world.html from JSON data (post-ref-resolution)."""
    meta = data['meta']
    cards = data['cards']

    html_doc = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        '  <meta name="site-context" content="support">\n'
        f'  <title>{meta["pageTitle"]}</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        + render_hero_card_with_intro_body_outro(meta, cards['hero']) + '\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )
    return html_doc


# ── Entry point ───────────────────────────────────────────────────────

def main():
    repo_root = Path(__file__).resolve().parent

    # 1. Render start-here.html
    sh_json = repo_root / 'pages' / 'support' / 'json' / 'start-here.json'
    sh_out = repo_root / 'pages' / 'support' / 'start-here.html'
    print(f'Rendering {sh_json}')
    with open(sh_json) as f:
        sh_data = json.load(f)
    sh_html = render_page(sh_data)
    sh_out.write_text(sh_html, encoding='utf-8')
    print(f'  Rendered → {sh_out}  ({len(sh_html.splitlines())} lines)')

    # 2. Render hello-world.html (resolves $ref against start-here.json)
    hw_json = repo_root / 'pages' / 'support' / 'json' / 'hello-world.json'
    hw_out = repo_root / 'pages' / 'support' / 'hello-world.html'
    if hw_json.exists():
        print(f'Rendering {hw_json}')
        with open(hw_json) as f:
            hw_data = json.load(f)
        hw_data = resolve_refs(hw_data, repo_root)
        hw_html = render_hello_world_page(hw_data)
        hw_out.write_text(hw_html, encoding='utf-8')
        print(f'  Rendered → {hw_out}  ({len(hw_html.splitlines())} lines)')


if __name__ == '__main__':
    main()
