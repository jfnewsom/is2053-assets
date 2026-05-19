#!/usr/bin/env python3
"""
render_study_worksheet.py — Renders pages/support/module-N-study-worksheet.html
from pages/support/json/study_worksheets/module_N_worksheet.json.

Each worksheet page is a stack of cards: a header card + one card per
numbered section + a closing footer block. Each section's card body holds
content blocks dispatched through BLOCK_RENDERERS — bullet lists, fill-in
tables, prompts, key questions, concept questions, subheadings, and section
intros.

Visual language: standard IS2053 lc-* classes (lc-card / lc-topper /
lc-panel / lc-h3 / lc-table) plus worksheet-specific ws-* classes
(ws-blank, ws-key-question, ws-answer-cell, ws-concept-question,
ws-section-intro, ws-footer-callout). All worksheet pages open with
<body class="ws-page"> so the @media print rules in labs.css know to apply.

Two clipboard buttons (Copy as Rich Text, Copy as Plain Text) ship with
every worksheet via worksheet-copy.js, hosted on the assets domain.

Run with:
    python3 render_study_worksheet.py                                   # all worksheets
    python3 render_study_worksheet.py <src.json> <out.html>             # single file

Source filename convention: module_N_worksheet.json
Output filename convention: module-N-study-worksheet.html
"""
import json
import sys
import glob
import os
from pathlib import Path


ASSETS_BASE = "https://jfnewsom.github.io/is2053-assets"


# ── Inline-blank token replacement ───────────────────────────────────

BLANK_HTML = '<span class="ws-blank">&nbsp;</span>'


def replace_blanks(text):
    """Replace `___` tokens in text with ws-blank spans."""
    return text.replace('___', BLANK_HTML)


# ── Content block renderers ──────────────────────────────────────────

def render_section_intro(b, color):
    return f'      <p class="ws-section-intro">{b["text"]}</p>'


def render_subheading(b, color):
    return f'      <div class="lc-h3 lc-h3--{color}">{b["text"]}</div>'


def render_bullet_list(b, color):
    items = '\n'.join(f'        <li>{replace_blanks(item)}</li>' for item in b['items'])
    return (
        '      <ul class="ws-bullets">\n'
        f'{items}\n'
        '      </ul>'
    )


def render_fill_table(b, color):
    """Generic fill table. Each row is a list of cells; a `null` cell
    renders as a blank answer cell (ws-answer-cell). Last row is
    visually emphasized with lc-table__total to make the worksheet
    rhythm consistent with the rest of the site."""
    headers = b.get('headers', ['Question', 'Answer'])
    header_html = '\n'.join(f'              <th>{h}</th>' for h in headers)

    rows_html = []
    rows = b['rows']
    last_idx = len(rows) - 1
    for i, cells in enumerate(rows):
        tr_class = ' class="lc-table__total"' if i == last_idx else ''
        cell_parts = []
        for cell in cells:
            if cell is None:
                cell_parts.append('              <td class="ws-answer-cell"></td>')
            else:
                cell_parts.append(f'              <td>{replace_blanks(cell)}</td>')
        rows_html.append(f'            <tr{tr_class}>\n' + '\n'.join(cell_parts) + '\n            </tr>')

    return (
        '      <div class="lc-table-wrap">\n'
        '        <table class="lc-table">\n'
        '          <thead>\n'
        '            <tr>\n'
        f'{header_html}\n'
        '            </tr>\n'
        '          </thead>\n'
        '          <tbody>\n'
        + '\n'.join(rows_html) + '\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def render_key_question(b, color):
    label = b.get('label', 'Key question:')
    text = replace_blanks(b['text'])
    return (
        f'      <div class="ws-key-question"><strong>{label}</strong> {text}</div>'
    )


def render_concept_questions(b, color):
    start = b.get('start', 1)
    lines = []
    for i, q in enumerate(b['items']):
        n = start + i
        text = replace_blanks(q)
        lines.append(f'      <div class="ws-concept-question"><strong>{n}.</strong> {text}</div>')
    return '\n'.join(lines)


def render_prompt(b, color):
    """Free-form inline-fill paragraph. `___` tokens become ws-blank spans."""
    text = replace_blanks(b['text'])
    return f'      <p class="ws-prompt">{text}</p>'


def render_code_block(b, color):
    """Raw HTML code block. Pass through pre-formatted HTML — useful when
    the source needs syntax-highlighting spans (lc-syn-*) or multi-line
    code that wouldn't fit in a single string."""
    return (
        '      <div class="lc-code-block"><pre>'
        + b['html']
        + '</pre></div>'
    )


def render_paragraph(b, color):
    """Plain paragraph (no blank substitution)."""
    return f'      <p>{b["text"]}</p>'


BLOCK_RENDERERS = {
    'section_intro':     render_section_intro,
    'subheading':        render_subheading,
    'bullet_list':       render_bullet_list,
    'fill_table':        render_fill_table,
    'key_question':      render_key_question,
    'concept_questions': render_concept_questions,
    'prompt':            render_prompt,
    'code_block':        render_code_block,
    'paragraph':         render_paragraph,
}


def render_content_blocks(blocks, color):
    out = []
    for b in blocks:
        t = b.get('type')
        fn = BLOCK_RENDERERS.get(t)
        if fn is None:
            out.append(f'      <!-- UNKNOWN BLOCK TYPE: {t} -->')
        else:
            out.append(fn(b, color))
    return '\n\n'.join(out)


# ── Card renderers ───────────────────────────────────────────────────

def render_header_card(data):
    """Top-of-page header card: course badge + topper title + Bat City
    logo + sub-banner, with the 'How to Use' intro callout below."""
    color = data['moduleColor']
    intro = data['intro']
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       Header Card\n'
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
        f'            <div class="lc-topper-title">{data["topperTitle"]}</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="{ASSETS_BASE}/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{data["subBanner"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'      <div class="ws-copy-bar">\n'
        f'        <button type="button" class="ws-copy-btn" data-ws-copy="rich">Copy as Rich Text</button>\n'
        f'        <button type="button" class="ws-copy-btn" data-ws-copy="plain">Copy as Plain Text</button>\n'
        f'        <button type="button" class="ws-copy-btn" data-ws-copy="print">Print</button>\n'
        f'      </div>\n'
        f'\n'
        f'      <div class="lc-callout lc-callout--tip">\n'
        f'        <div class="lc-callout__icon"><span class="material-symbols-outlined">school</span></div>\n'
        f'        <div class="lc-callout__bubble">\n'
        f'          <div class="lc-callout__title">{intro["title"]}</div>\n'
        f'          <div class="lc-callout__body">\n'
        f'            {intro["body_html"]}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_section_card(sec, num, total):
    """One numbered section card. Color comes from sec['color']."""
    color = sec['color']
    content_html = render_content_blocks(sec.get('content', []), color)
    return (
        f'  <!-- ══════════════════════════════════════════════════════════\n'
        f'       Section {num} of {total}\n'
        f'  ══════════════════════════════════════════════════════════ -->\n'
        f'  <div class="lc-card lc-card--{color} ws-section-card">\n'
        f'    <div class="lc-topper">\n'
        f'      <div class="lc-topper-title">{sec["title"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'\n'
        f'{content_html}\n'
        f'\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_closing_block(data):
    """Optional closing footer callout below the last section."""
    closing = data.get('closing')
    if not closing:
        return ''
    return (
        f'  <div class="ws-footer-callout">\n'
        f'    {closing["body_html"]}\n'
        f'  </div>'
    )


# ── Top-level page renderer ──────────────────────────────────────────

def render_worksheet_page(data):
    """Render a complete module-N-study-worksheet.html document."""
    sections = data.get('sections', [])
    total = len(sections)

    header = render_header_card(data)
    section_blocks = [render_section_card(sec, i + 1, total) for i, sec in enumerate(sections)]
    closing = render_closing_block(data)

    body_parts = [header] + section_blocks
    if closing:
        body_parts.append(closing)
    body = '\n\n'.join(body_parts)

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <link rel="icon" type="image/png" href="{ASSETS_BASE}/favicon.png">\n'
        f'  <title>{data["htmlTitle"]}</title>\n'
        f'  <link rel="stylesheet" href="{ASSETS_BASE}/labs.css">\n'
        '</head>\n'
        '<body class="ws-page">\n'
        '<div class="lc-wrapper">\n\n'
        + body + '\n\n'
        '</div><!-- /lc-wrapper -->\n'
        f'<script src="{ASSETS_BASE}/nav.js"></script>\n'
        f'<script src="{ASSETS_BASE}/worksheet-copy.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


# ── Entry point ──────────────────────────────────────────────────────

def render_one(src_path, out_path):
    with open(src_path) as f:
        data = json.load(f)
    html = render_worksheet_page(data)
    Path(out_path).write_text(html, encoding='utf-8')
    return len(html.splitlines())


def main():
    if len(sys.argv) == 3:
        src, dst = sys.argv[1], sys.argv[2]
        n = render_one(src, dst)
        print(f'Rendered: {dst}  ({n} lines)')
        return

    repo_root = Path(__file__).resolve().parent
    src_dir = repo_root / 'pages' / 'support' / 'json' / 'study_worksheets'
    out_dir = repo_root / 'pages' / 'support'
    pattern = str(src_dir / 'module_*_worksheet.json')

    for src in sorted(glob.glob(pattern)):
        # module_1_worksheet.json → module-1-study-worksheet.html
        stem = os.path.basename(src)
        num = stem.replace('module_', '').replace('_worksheet.json', '')
        dst = out_dir / f'module-{num}-study-worksheet.html'
        n = render_one(src, dst)
        print(f'Rendered: pages/support/module-{num}-study-worksheet.html  ({n} lines)')


if __name__ == '__main__':
    main()
