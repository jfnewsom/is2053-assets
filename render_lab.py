"""
render_lab.py — IS2053 Lab Renderer
Bat City Noir v5.0 — Module 4+ Pipeline

Usage:
    python3 render_lab.py pages/labs/json/lab-4-1.json
    → writes pages/labs/lab-4-1.html

Source of truth: IS2053_JSON_Schema_Spec_v1.md
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
    render_before_you_begin,
    render_objectives,
    render_named_constants,
    render_program_requirements,
    render_final_checklist,
    render_need_help,
    render_mentor_quote,
    H3_LABELS,
    CALLOUT_ICONS,
)


# ============================================================
# Week type badge text
# ============================================================

WEEK_TYPE_LABEL = {
    "BUILD":   "Module {module} &mdash; Week {week} &mdash; BUILD Week",
    "ENHANCE": "Module {module} &mdash; Week {week} &mdash; ENHANCE Week",
    "MASTER":  "Module {module} &mdash; Week {week} &mdash; MASTER Week",
}


# ============================================================
# Overview Card
# ============================================================

def render_overview_card(overview: dict, meta: dict) -> str:
    """Render the full blue Overview card."""

    body        = overview.get("body", "")
    mentor      = overview.get("mentorQuote", {})
    objectives  = overview.get("objectives", [])
    key_concepts = overview.get("keyConceptsText", "")
    textbook_ref = overview.get("textbookReference", "")
    prog_reqs   = overview.get("programRequirements", [])
    named_const = overview.get("namedConstants", [])
    filename_note = overview.get("filenameNote", "")
    additional_files_note = overview.get("additionalFilesNote", "")
    save_your_code = overview.get("saveYourCode", "")

    week_type   = meta.get("weekType", "BUILD")
    module      = meta.get("module", "")
    week        = meta.get("week", "")
    chapters    = meta.get("chapters", "")
    chapter_topics = meta.get("chapterTopics", "")
    title       = meta.get("title", "")
    lab_id      = meta.get("labId", "")
    filename    = meta.get("filename", "")
    additional_files = meta.get("additionalFiles", [])

    # Badge number: "1.1", "4.2", etc.
    badge_num = f"{module}.{week}"

    # Sub-banner: week type label
    sub_banner_text = WEEK_TYPE_LABEL.get(week_type, "").format(
        module=module, week=week
    )

    # Chapter info line
    chapter_line = ""
    if chapters:
        chapter_line = f"""    <p><strong>Chapters:</strong> {html_lib.escape(chapters)}
        {f"&mdash; {html_lib.escape(chapter_topics)}" if chapter_topics else ""}</p>
"""

    # Body narrative
    body_html = f"    <p>{body}</p>\n" if body else ""

    # Mentor quote
    mentor_html = render_mentor_quote(mentor) if mentor else ""

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

    # Named constants
    named_const_html = ""
    if named_const:
        named_const_html = (
            '    <div class="lc-h3 lc-h3--yellow">Named Constants</div>\n'
            + render_named_constants(named_const)
        )

    # Filename note
    filename_html = ""
    if filename_note or filename:
        display_note = filename_note or f"Submit <code>{filename}</code> this week."
        filename_html = f"""    <div class="lc-h3 lc-h3--yellow">Filename</div>
    <p>{display_note}</p>
"""
    # Additional files note
    if additional_files_note:
        filename_html += f"    <p>{html_lib.escape(additional_files_note)}</p>\n"
    elif additional_files:
        files_list = ", ".join(f"<code>{f}</code>" for f in additional_files)
        filename_html += f"    <p>Also submit: {files_list}</p>\n"

    # Save Your Code callout
    save_html = ""
    if save_your_code:
        save_html = f"""    <div class="lc-callout lc-callout--success">
      <div class="lc-callout__icon">
        {CALLOUT_ICONS["success"].strip()}
      </div>
      <div class="lc-callout__bubble">
        <div class="lc-callout__title">Save Your Code</div>
        <div class="lc-callout__body">
          <p>{html_lib.escape(save_your_code)}</p>
        </div>
      </div>
    </div>
"""

    return (
        card_open("blue")
        + topper_with_badge("LAB", badge_num, title, sub_banner_text)
        + panel_open()
        + chapter_line
        + body_html
        + mentor_html
        + objectives_html
        + key_concepts_html
        + textbook_html
        + prog_reqs_html
        + named_const_html
        + filename_html
        + save_html
        + panel_close()
        + card_close()
    )


# ============================================================
# Checkpoints Card
# ============================================================

def render_checkpoints_card(checkpoints: list) -> str:
    """Render the full green Checkpoints card."""
    total = len(checkpoints)
    cp_count_label = f"{total} Checkpoint{'s' if total != 1 else ''}"

    checkpoints_html = ""
    for i, cp in enumerate(checkpoints):
        checkpoints_html += render_checkpoint(cp, i, total)

    return (
        card_open("green")
        + topper("Checkpoints", cp_count_label)
        + panel_open()
        + checkpoints_html
        + panel_close()
        + card_close()
    )


# ============================================================
# Main Renderer
# ============================================================

def render_lab(data: dict, output_path: str) -> None:
    """
    Render a lab JSON dict to an HTML file at output_path.

    Card order:
        1. Overview     (blue)
        2. Time Guide   (orange)
        3. Before You Begin  (green — architecture block)
        4. Checkpoints  (green)
        5. Final Checklist  (red)
        6. Need Help    (purple)
    """
    meta          = data.get("meta", {})
    overview      = data.get("overview", {})
    time_guide    = data.get("timeGuide", {})
    before_begin  = data.get("beforeYouBegin", {})
    checkpoints   = data.get("checkpoints", [])
    final         = data.get("finalChecklist", {})
    need_help     = data.get("needHelp", {})

    title_str = meta.get("title", "Lab")
    page_title = f"{title_str} \u2014 IS2053"

    html = html_head(page_title)
    html += render_overview_card(overview, meta)
    html += render_time_guide(time_guide)

    if before_begin:
        html += render_before_you_begin(before_begin)

    html += render_checkpoints_card(checkpoints)
    html += render_final_checklist(final)
    html += render_need_help(need_help)
    html += html_foot()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Rendered → {output_path}")


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 render_lab.py <path/to/lab-X-X.json>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: file not found — {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Derive output path from labId
    lab_id = data.get("meta", {}).get("labId", "")
    if not lab_id:
        print("Error: meta.labId is missing from JSON")
        sys.exit(1)

    # Output: pages/labs/<labId>.html
    # Resolve relative to the directory containing the JSON file's parent
    json_dir = os.path.dirname(os.path.abspath(json_path))       # .../pages/labs/json
    labs_dir = os.path.dirname(json_dir)                          # .../pages/labs
    output_path = os.path.join(labs_dir, f"{lab_id}.html")

    print(f"Rendering {json_path}")
    render_lab(data, output_path)


if __name__ == "__main__":
    main()
