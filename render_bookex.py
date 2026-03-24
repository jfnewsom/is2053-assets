"""
render_bookex.py — IS2053 BookEx Renderer
Bat City Noir v5.0 — Module 4+ Pipeline

Usage:
    python3 render_bookex.py pages/bookex/json/bookex-ch09.json
    → writes pages/bookex/BookExCH09.html

Source of truth: IS2053_JSON_Schema_Spec_v1.md

Key differences from render_lab.py:
    - No beforeYouBegin block
    - No mentorQuote in overview
    - No namedConstants in overview
    - No saveYourCode in overview
    - No mentor_quote content items in checkpoints
    - No test_your_code h3 in checkpoints
    - Output filename: BookExCH{XX}.html (capital convention, zero-padded)
    - Badge word: "BOOKEX", badge num: chapter number
"""

import json
import sys
import os
import html as html_lib

from components import (
    html_head,
    html_foot,
    card_open,
    card_close,
    topper,
    topper_with_badge,
    panel_open,
    panel_close,
    render_content_item,
    render_checkpoint,
    render_time_guide,
    render_objectives,
    render_program_requirements,
    render_final_checklist,
    render_need_help,
    CALLOUT_ICONS,
)


# ============================================================
# Overview Card (BookEx)
# ============================================================

def render_bookex_overview_card(overview: dict, meta: dict) -> str:
    """Render the full blue Overview card for a BookEx file."""

    body             = overview.get("body", "")
    objectives       = overview.get("objectives", [])
    key_concepts     = overview.get("keyConceptsText", "")
    textbook_ref     = overview.get("textbookReference", "")
    prog_reqs        = overview.get("programRequirements", [])
    filename_note    = overview.get("filenameNote", "")

    chapter          = meta.get("chapter", "")
    title            = meta.get("title", "")
    program_count    = meta.get("programCount", "")
    filename         = meta.get("filename", "")

    badge_num        = str(chapter)
    sub_banner_text  = f"Chapter {chapter} &nbsp;&mdash;&nbsp; {program_count} Program{'s' if program_count != 1 else ''}"

    # Body narrative
    body_html = f"    <p>{body}</p>\n" if body else ""

    # Objectives
    objectives_html = ""
    if objectives:
        objectives_html = (
            '    <div class="lc-h3 lc-h3--yellow">Learning Objectives</div>\n'
            + render_objectives(objectives)
        )

    # Key concepts
    key_concepts_html = ""
    if key_concepts:
        key_concepts_html = (
            '    <div class="lc-h3 lc-h3--yellow">Key Concepts</div>\n'
            f"    <p>{html_lib.escape(key_concepts)}</p>\n"
        )

    # Textbook reference
    textbook_html = ""
    if textbook_ref:
        textbook_html = (
            '    <div class="lc-h3 lc-h3--yellow">Textbook Reference</div>\n'
            f"    <p>{html_lib.escape(textbook_ref)}</p>\n"
        )

    # Program requirements
    prog_reqs_html = ""
    if prog_reqs:
        prog_reqs_html = (
            '    <div class="lc-h3 lc-h3--yellow">Program Requirements</div>\n'
            + render_program_requirements(prog_reqs)
        )

    # Filename note
    filename_html = ""
    if filename_note or filename:
        display_note = filename_note or f"Submit <code>{filename}</code> with all programs combined into one file."
        filename_html = (
            '    <div class="lc-h3 lc-h3--yellow">Filename</div>\n'
            f"    <p>{display_note}</p>\n"
        )

    return (
        card_open("blue")
        + topper_with_badge("BOOKEX", badge_num, title, sub_banner_text)
        + panel_open()
        + body_html
        + objectives_html
        + key_concepts_html
        + textbook_html
        + prog_reqs_html
        + filename_html
        + panel_close()
        + card_close()
    )


# ============================================================
# Checkpoints Card (BookEx)
# Each checkpoint = one Gaddis program
# ============================================================

def render_bookex_checkpoints_card(checkpoints: list) -> str:
    """Render the full green Checkpoints card for a BookEx file."""
    total = len(checkpoints)
    program_count_label = f"{total} Program{'s' if total != 1 else ''}"

    checkpoints_html = ""
    for i, cp in enumerate(checkpoints):
        checkpoints_html += render_checkpoint(cp, i, total)

    return (
        card_open("green")
        + topper("Programs", program_count_label)
        + panel_open()
        + checkpoints_html
        + panel_close()
        + card_close()
    )


# ============================================================
# Output Filename Derivation
# ============================================================

def derive_output_filename(chapter_id: str) -> str:
    """
    Convert 'bookex-ch09' → 'BookExCH09.html'
    Matches existing repo convention: capital B, capital E, capital CH.
    """
    # Extract the numeric part after 'bookex-ch'
    prefix = "bookex-ch"
    if chapter_id.lower().startswith(prefix):
        num_part = chapter_id[len(prefix):]
        return f"BookExCH{num_part}.html"
    # Fallback — shouldn't happen with valid JSON
    return f"{chapter_id}.html"


# ============================================================
# Main Renderer
# ============================================================

def render_bookex(data: dict, output_path: str) -> None:
    """
    Render a BookEx JSON dict to an HTML file at output_path.

    Card order:
        1. Overview         (blue)
        2. Time Guide       (orange)
        3. Checkpoints      (green)  — one per Gaddis program
        4. Final Checklist  (red)
        5. Need Help        (purple)
    """
    meta        = data.get("meta", {})
    overview    = data.get("overview", {})
    time_guide  = data.get("timeGuide", {})
    checkpoints = data.get("checkpoints", [])
    final       = data.get("finalChecklist", {})
    need_help   = data.get("needHelp", {})

    chapter = meta.get("chapter", "")
    title   = meta.get("title", "")
    page_title = f"BookEx Chapter {chapter}: {title} \u2014 IS2053"

    html = html_head(page_title)
    html += render_bookex_overview_card(overview, meta)
    html += render_time_guide(time_guide)
    html += render_bookex_checkpoints_card(checkpoints)
    html += render_final_checklist(final)
    html += render_need_help(need_help)
    html += html_foot()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Rendered \u2192 {output_path}")


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 render_bookex.py <path/to/bookex-chXX.json>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: file not found \u2014 {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapter_id = data.get("meta", {}).get("chapterId", "")
    if not chapter_id:
        print("Error: meta.chapterId is missing from JSON")
        sys.exit(1)

    # Output: pages/bookex/<BookExCHXX>.html
    json_dir    = os.path.dirname(os.path.abspath(json_path))   # .../pages/bookex/json
    bookex_dir  = os.path.dirname(json_dir)                     # .../pages/bookex
    out_file    = derive_output_filename(chapter_id)
    output_path = os.path.join(bookex_dir, out_file)

    print(f"Rendering {json_path}")
    render_bookex(data, output_path)


if __name__ == "__main__":
    main()
