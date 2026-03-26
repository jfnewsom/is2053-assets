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



# ============================================================
# Overview Card
# ============================================================

def render_overview_card(overview: dict, meta: dict) -> str:
    """Render the full blue Overview card."""

    body             = overview.get("body", "")
    mentor           = overview.get("mentorQuote", {})
    objectives       = overview.get("objectives", [])
    key_concepts     = overview.get("keyConceptsText", "")
    textbook_ref     = overview.get("textbookReference", "")
    prog_reqs        = overview.get("programRequirements", [])
    named_const      = overview.get("namedConstants", [])
    filename_note    = overview.get("filenameNote", "")
    additional_files_note = overview.get("additionalFilesNote", "")
    data_files       = overview.get("dataFiles", [])
    save_your_code   = overview.get("saveYourCode", "")

    week_type        = meta.get("weekType", "BUILD")
    module           = meta.get("module", "")
    week             = meta.get("week", "")
    chapters         = meta.get("chapters", "")
    chapter_topics   = meta.get("chapterTopics", "")
    title            = meta.get("title", "")
    filename         = meta.get("filename", "")
    additional_files = meta.get("additionalFiles", [])

    badge_num = f"{module}.{week}"

    sub_banner_text = f"MODULE {module} &bull; WEEK {week} &bull; {week_type}"
    if chapters:
        chapter_part = html_lib.escape(chapters)
        if chapter_topics:
            chapter_part += f": {html_lib.escape(chapter_topics).upper()}"
        sub_banner_text += f" &bull; CHAPTERS {chapter_part}"

    # 1. Overview — body narrative with logo floated right
    body_html = ""
    if body:
        logo_html = (
            '<img src="../../branding/AllMyEggses3D-Full.png" '
            'alt="All My Eggses Live in Texas" '
            'style="float: right; height: 110px; margin: 0 0 12px 20px;">\n'
        )
        body_html = (
            '    <div class="lc-h3 lc-h3--yellow">Overview</div>\n'
            f"    {logo_html}"
            f"    <p>{body}</p>\n"
            '    <div style="clear: both;"></div>\n'
        )

    # 2. Mentor quote
    mentor_html = render_mentor_quote(mentor) if mentor else ""

    # 3. Filename — primary submission file + any additional files listed inline
    filename_html = ""
    if filename_note or filename:
        display_note = filename_note if filename_note else f"Submit <code>{filename}</code> this week."
        filename_html = f'    <div class="lc-h3 lc-h3--yellow">Filename</div>\n    <p>{display_note}</p>\n'
    if additional_files_note:
        filename_html += f"    <p>{additional_files_note}</p>\n"
    elif additional_files and not data_files:
        # Fall back to inline list only when no dataFiles table is provided
        files_list = ", ".join(f"<code>{f}</code>" for f in additional_files)
        filename_html += f"    <p>Also required: {files_list}</p>\n"

    # 4. What You're Building — learning objectives
    objectives_html = ""
    if objectives:
        objectives_html = (
            '    <div class="lc-h3 lc-h3--yellow">What You\'re Building</div>\n'
            + render_objectives(objectives)
        )

    # 5. Key Concepts — may contain HTML inline code tags
    key_concepts_html = ""
    if key_concepts:
        key_concepts_html = (
            '    <div class="lc-h3 lc-h3--yellow">Key Concepts</div>\n'
            f"    <p>{key_concepts}</p>\n"
        )

    # 6. Textbook reference — plain text
    textbook_html = ""
    if textbook_ref:
        textbook_html = (
            '    <div class="lc-h3 lc-h3--yellow">Textbook Reference</div>\n'
            f"    <p>{html_lib.escape(textbook_ref)}</p>\n"
        )

    # 7. Program requirements — items may contain HTML
    prog_reqs_html = ""
    if prog_reqs:
        prog_reqs_html = (
            '    <div class="lc-h3 lc-h3--yellow">Program Requirements</div>\n'
            + render_program_requirements(prog_reqs)
        )

    # 8. Required Data Files — rendered as a table when dataFiles array is present
    data_files_html = ""
    if data_files:
        rows_html = ""
        for df in data_files:
            f_name = html_lib.escape(df.get("file", ""))
            f_fmt  = df.get("format", "")
            new_badge = ' <span style="color:#FFCC00; font-size:11px; font-weight:700;">NEW!</span>' if df.get("new") else ""
            if df.get("file", "").endswith(".txt"):
                download_cell = (
                    f'<td><a href="../../data/{f_name}" download '
                    f'style="color:#39FF14; font-family:var(--font-mono); font-size:12px;">'
                    f'&#11123; {f_name}</a></td>'
                )
            else:
                download_cell = '<td style="color:#555; font-size:12px;">—</td>'
            rows_html += f'      <tr><td><code>{f_name}</code>{new_badge}</td><td>{f_fmt}</td>{download_cell}</tr>\n'
        data_files_html = f"""    <div class="lc-h3 lc-h3--yellow">Required Data Files</div>
    <div class="lc-table-wrap">
      <table class="lc-table">
        <thead>
          <tr>
            <th>File</th>
            <th>Format</th>
            <th>Download</th>
          </tr>
        </thead>
        <tbody>
{rows_html}        </tbody>
      </table>
    </div>
"""

    # Named constants
    named_const_html = ""
    if named_const:
        named_const_html = (
            '    <div class="lc-h3 lc-h3--yellow">Named Constants</div>\n'
            + render_named_constants(named_const)
        )

    # 9. Save Your Code callout — may contain HTML
    save_html = ""
    if save_your_code:
        save_html = f"""    <div class="lc-callout lc-callout--success">
      <div class="lc-callout__icon">
        {CALLOUT_ICONS["success"].strip()}
      </div>
      <div class="lc-callout__bubble">
        <div class="lc-callout__title">Save Your Code</div>
        <div class="lc-callout__body">
          <p>{save_your_code}</p>
        </div>
      </div>
    </div>
"""

    return (
        card_open("blue")
        + topper_with_badge("LAB", badge_num, title, sub_banner_text)
        + panel_open()
        + body_html
        + mentor_html
        + filename_html
        + objectives_html
        + key_concepts_html
        + textbook_html
        + prog_reqs_html
        + data_files_html
        + named_const_html
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


if __name__ == "__main__":    main()
