"""
components.py — IS2053 Shared Rendering Utilities
Bat City Noir v5.0 — Module 4+ Pipeline

Used by: render_lab.py, render_bookex.py
Source of truth: IS2053_JSON_Schema_Spec_v1.md
"""

import html as html_lib
import re


# ============================================================
# H3 Label Map — label → display text
# ============================================================

H3_LABELS = {
    "what_youre_building":   "What You're Building",
    "why_this_matters":      "Why This Matters",
    "step_by_step":          "Step-by-Step Instructions",
    "pro_tip":               "Pro Tip",
    "tips_and_pitfalls":     "Tips &amp; Pitfalls",
    "test_your_code":        "Test Your Code",
    "what_you_should_have":  "What You Should Have",
    "bookex_patterns":       "BookEx Patterns",
    "expected_output":       "Expected Output",
    "named_constants":       "Named Constants",
    "warning":               "Warning",
    "before_you_submit":     "Before You Submit",
    "permitted_techniques":  "Permitted Techniques",
    "academic_integrity":    "Academic Integrity",
    "save_your_code":        "Save Your Code",
    "if_you_get_stuck":      "If You Get Stuck",
    "codegrade_tip":         "CodeGrade Tip",
    "contact_and_resources": "Contact &amp; Resources",
    "overview":              "Overview",
    "filename":              "Filename",
    "key_concepts":          "Key Concepts",
    "textbook_reference":    "Textbook Reference",
    "program_requirements":  "Program Requirements",
}

# H3 background color per card context
# Card context key → CSS modifier class
H3_COLOR_FOR_CARD = {
    "blue":   "lc-h3--yellow",
    "orange": "lc-h3--yellow",
    "green":  "lc-h3--yellow",
    "red":    "lc-h3--yellow",
    "purple": "lc-h3--yellow",
}


# ============================================================
# Callout Icons — inline SVG per variant
# ============================================================

CALLOUT_ICONS = {
    "pitfall": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 4 L27 25 L3 25 Z" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
        <line x1="15" y1="12" x2="15" y2="19" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="15" cy="22.5" r="1.5" fill="#000"/>
    </svg>""",

    "success": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="15" cy="15" r="11" stroke="#000" stroke-width="2.5"/>
        <polyline points="9,15 13,19 21,11" stroke="#000" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    "tip": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 4 C10 4 6 8 6 13 C6 17 9 20 11 22 L11 24 L19 24 L19 22
                 C21 20 24 17 24 13 C24 8 20 4 15 4 Z"
              stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
        <line x1="11" y1="26" x2="19" y2="26" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="15" y1="8" x2="15" y2="16" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="15" cy="19" r="1.5" fill="#000"/>
    </svg>""",

    "info": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="15" cy="15" r="11" stroke="#000" stroke-width="2.5"/>
        <line x1="15" y1="13" x2="15" y2="21" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="15" cy="9.5" r="1.5" fill="#000"/>
    </svg>""",

    "bookex": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 5 L6 25 L22 25 C23 25 24 24 24 23 L24 7 C24 6 23 5 22 5 Z"
              stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
        <line x1="6" y1="5" x2="22" y2="5" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="10" y1="11" x2="20" y2="11" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="10" y1="15" x2="20" y2="15" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="10" y1="19" x2="16" y2="19" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
    </svg>""",

    "warning": """<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="5" y="5" width="20" height="20" rx="3"
              stroke="#000" stroke-width="2.5" stroke-linejoin="round"/>
        <line x1="15" y1="10" x2="15" y2="17" stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="15" cy="21" r="1.5" fill="#000"/>
    </svg>""",
}

CALLOUT_ACCENT = {
    "pitfall": "#FF6B1A",
    "success": "#39FF14",
    "tip":     "#00FFFF",
    "info":    "#0055FF",
    "bookex":  "#BF40FF",
    "warning": "#FF1744",
}


# ============================================================
# HTML Document Shell
# ============================================================

def html_head(title: str, css_path: str = "../../labs.css") -> str:
    """Return the opening <html> through <body> tags."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="lc-wrapper">
"""


def html_foot(logo_path: str = "../../branding/BatCity-logo-on-black.svg") -> str:
    """Return the footer and closing tags."""
    return f"""
    <footer class="lc-footer">
        <img src="{logo_path}" alt="Bat City Collective">
        <p class="lc-footer__course">IS2053: Programming I (Python) — The University of Texas at San Antonio</p>
        <p class="lc-footer__detail">Starting Out with Python, 6th Edition — Tony Gaddis — Pearson</p>
    </footer>

</div>
</body>
</html>
"""


# ============================================================
# Card Shell
# ============================================================

def card_open(color: str) -> str:
    """Open a card div. color: blue | orange | green | red | purple"""
    return f'<div class="lc-card lc-card--{color}">\n'


def card_close() -> str:
    return '</div>\n'


def topper(title: str, sub_banner: str = "") -> str:
    """Render a card topper with title and optional sub-banner."""
    sub = f'\n    <div class="lc-sub-banner">{sub_banner}</div>' if sub_banner else ""
    return f"""  <div class="lc-topper">
    <div class="lc-topper-title">{title}</div>{sub}
  </div>
"""


def topper_with_badge(badge_word: str, badge_num: str,
                      title: str, sub_banner: str = "") -> str:
    """Render a card topper with a lab/bookex badge + title side by side."""
    sub = f'\n    <div class="lc-sub-banner">{sub_banner}</div>' if sub_banner else ""
    return f"""  <div class="lc-topper">
    <div class="lc-card-header">
      <div class="lc-lab-badge">
        <div class="lc-lab-badge__word">{badge_word}</div>
        <div class="lc-lab-badge__num">{badge_num}</div>
      </div>
      <div class="lc-topper-title">{title}</div>
    </div>{sub}
  </div>
"""


def panel_open() -> str:
    return '  <div class="lc-panel">\n'


def panel_close() -> str:
    return '  </div>\n'


# ============================================================
# Content Item Renderers
# ============================================================

def render_content_item(item: dict, card_color: str = "green",
                        headshot_path: str = "../../headshots/") -> str:
    """
    Dispatch a single content item to its renderer.
    card_color is used to select h3 color variant.
    headshot_path is the relative path prefix for mentor images.
    """
    t = item.get("type", "")

    if t == "instructions":
        return render_instructions(item)
    elif t == "text":
        return render_text(item)
    elif t == "h3":
        return render_h3(item, card_color)
    elif t == "callout":
        return render_callout(item)
    elif t == "code_block":
        return render_code_block(item)
    elif t == "output_block":
        return render_output_block(item)
    elif t == "table":
        return render_table(item)
    elif t == "mentor_quote":
        return render_mentor_quote(item, headshot_path)
    else:
        # Unknown type — emit a comment so it's visible during audit
        return f'<!-- UNKNOWN CONTENT TYPE: {html_lib.escape(t)} -->\n'


def render_instructions(item: dict) -> str:
    """Render an ordered list of instruction steps."""
    items_html = ""
    for step in item.get("items", []):
        items_html += f"      <li>{step}</li>\n"
    return f"""    <ol>
{items_html}    </ol>
"""


def render_text(item: dict) -> str:
    """Render a plain paragraph."""
    return f'    <p>{item.get("body", "")}</p>\n'


def render_h3(item: dict, card_color: str = "green") -> str:
    """Render a named section header — Roboto Slab, color inherited from card accent."""
    label = item.get("label", "")
    display = H3_LABELS.get(label, label.replace("_", " ").title())
    return f'    <div class="lc-h3">{display}</div>\n'


def render_callout(item: dict) -> str:
    """Render a styled callout box with icon, title, body, and optional items."""
    variant = item.get("variant", "info")

    # bookex variant has a special references layout
    if variant == "bookex" and "references" in item:
        return render_bookex_callout(item)

    icon_svg = CALLOUT_ICONS.get(variant, CALLOUT_ICONS["info"])
    title = item.get("title", "")
    body = item.get("body", "")
    items = item.get("items", [])

    body_html = f'        <p>{body}</p>\n' if body else ""

    items_html = ""
    if items:
        items_html = "        <ul>\n"
        for i in items:
            items_html += f"          <li>{i}</li>\n"
        items_html += "        </ul>\n"

    title_html = f'        <div class="lc-callout__title">{title}</div>\n' if title else ""

    return f"""    <div class="lc-callout lc-callout--{variant}">
      <div class="lc-callout__icon">
        {icon_svg.strip()}
      </div>
      <div class="lc-callout__bubble">
{title_html}        <div class="lc-callout__body">
{body_html}{items_html}        </div>
      </div>
    </div>
"""


def render_bookex_callout(item: dict) -> str:
    """Render the bookex callout variant with program reference list."""
    references = item.get("references", [])
    icon_svg = CALLOUT_ICONS["bookex"]

    refs_html = ""
    for ref in references:
        program_id = ref.get("programId", "")
        filename = ref.get("filename", "")
        step = ref.get("step", "")
        description = ref.get("description", "")
        refs_html += f"""          <li>
            <strong>Program {program_id}</strong>
            {f'— <code>{filename}</code>' if filename else ""}
            {f'(Step {step})' if step else ""}
            {f'— {description}' if description else ""}
          </li>
"""

    return f"""    <div class="lc-callout lc-callout--bookex">
      <div class="lc-callout__icon">
        {icon_svg.strip()}
      </div>
      <div class="lc-callout__bubble">
        <div class="lc-callout__title">Textbook Reference</div>
        <div class="lc-callout__body">
          <ul>
{refs_html}          </ul>
        </div>
      </div>
    </div>
"""


def render_code_block(item: dict) -> str:
    """Render a pre-formatted code block."""
    code = html_lib.escape(item.get("code", ""))
    return f"""    <div class="lc-code-block">
      <pre><code>{code}</code></pre>
    </div>
"""


def render_output_block(item: dict) -> str:
    """Render an expected terminal output block."""
    output = html_lib.escape(item.get("output", ""))
    return f"""    <div class="lc-output">
      <div class="lc-output__label">Expected Output</div>
      <pre>{output}</pre>
    </div>
"""


def render_table(item: dict, card_color: str = "green") -> str:
    """Render a data table with optional accent override."""
    headers = item.get("headers", [])
    rows = item.get("rows", [])
    accent_key = item.get("accent", "")

    accent_map = {
        "red":    "#FF1744",
        "orange": "#FF6B1A",
        "green":  "#39FF14",
        "blue":   "#0055FF",
        "purple": "#BF40FF",
        "yellow": "#FFCC00",
        "cyan":   "#00FFFF",
    }

    # Build style override only if an explicit accent was specified
    style_attr = ""
    if accent_key and accent_key in accent_map:
        style_attr = f' style="--lc-accent: {accent_map[accent_key]};"'

    thead = "".join(f"        <th>{h}</th>\n" for h in headers)
    tbody = ""
    for row in rows:
        cells = "".join(f"        <td>{cell}</td>\n" for cell in row)
        tbody += f"      <tr>\n{cells}      </tr>\n"

    return f"""    <div class="lc-table-wrap"{style_attr}>
      <table class="lc-table">
        <thead>
          <tr>
{thead}          </tr>
        </thead>
        <tbody>
{tbody}        </tbody>
      </table>
    </div>
"""


def render_mentor_quote(item: dict,
                        headshot_path: str = "../../headshots/") -> str:
    """Render a mentor quote with headshot, bubble, and attribution."""
    character = item.get("character", "")
    role = item.get("role", "")
    headshot = item.get("headshot", "")
    quote = item.get("quote", "")

    img_src = f"{headshot_path}{headshot}"

    return f"""    <div class="lc-mentor">
      <div class="lc-mentor__inner">
        <div class="lc-mentor__avatar">
          <img src="{img_src}" alt="{html_lib.escape(character)}">
        </div>
        <div class="lc-mentor__bubble">
          <div class="lc-mentor__quote">"{html_lib.escape(quote)}"</div>
        </div>
      </div>
      <div class="lc-mentor__attribution">
        <div class="lc-mentor__name">{html_lib.escape(character)}</div>
        <div class="lc-mentor__role">{html_lib.escape(role)}</div>
      </div>
    </div>
"""


# ============================================================
# Checkpoint Renderer
# ============================================================

def render_checkpoint(cp: dict, index: int, total: int,
                      headshot_path: str = "../../headshots/") -> str:
    """
    Render a single checkpoint — separator (if not first), badge+title row,
    then all content items.
    index is 0-based. total is len(checkpoints).
    """
    number = cp.get("number", index + 1)
    title = cp.get("title", f"Checkpoint {number}")
    content = cp.get("content", [])

    separator = '    <hr class="lc-cp-sep">\n' if index > 0 else ""

    content_html = ""
    for item in content:
        content_html += render_content_item(item, card_color="green",
                                            headshot_path=headshot_path)

    return f"""{separator}    <div class="lc-cp-row">
      <div class="lc-cp-badge">
        <div class="lc-cp-badge__word">Checkpoint</div>
        <div class="lc-cp-badge__num">{number}</div>
      </div>
      <div class="lc-cp-content">
        <div class="lc-cp-title">{html_lib.escape(title)}</div>
      </div>
    </div>
    <div class="lc-cp-body">
{content_html}    </div>
"""


# ============================================================
# Time Guide Card
# ============================================================

def render_time_guide(time_guide: dict) -> str:
    """Render the full orange Time Guide card."""
    total_time = time_guide.get("totalTime", "")
    rows = time_guide.get("rows", [])

    rows_html = ""
    for row in rows:
        cp = row.get("checkpoint", "")
        time = row.get("time", "")
        task = row.get("task", "")
        rows_html += f"""      <tr>
        <td><strong>{html_lib.escape(cp)}</strong></td>
        <td>{html_lib.escape(time)}</td>
        <td>{html_lib.escape(task)}</td>
      </tr>
"""

    return f"""{card_open("orange")}
{topper("Time Guide", f"Plan Your Session &nbsp;&mdash;&nbsp; {html_lib.escape(total_time)}")}
{panel_open()}
    <div class="lc-table-wrap">
      <table class="lc-table">
        <thead>
          <tr>
            <th>Checkpoint</th>
            <th>Time</th>
            <th>Task</th>
          </tr>
        </thead>
        <tbody>
{rows_html}        </tbody>
      </table>
    </div>
{panel_close()}{card_close()}"""


# ============================================================
# Before You Begin Card (labs only)
# ============================================================

def render_before_you_begin(byb: dict) -> str:
    """
    Render the Before You Begin architecture block.
    Wraps in a green-tinted card section. [NEW] and [REPLACED]
    tags are replaced with colored spans.
    """
    intro = byb.get("intro", "")
    architecture = byb.get("architecture", "")

    # HTML-escape the raw architecture string, then restore our special tags
    escaped = html_lib.escape(architecture)
    escaped = escaped.replace(
        "[NEW]",
        '<span class="lc-arch-new">[NEW]</span>'
    )
    escaped = escaped.replace(
        "[REPLACED]",
        '<span class="lc-arch-replaced">[REPLACED]</span>'
    )
    # Also handle inline [NEW — ...] and [REPLACED — ...] patterns
    escaped = re.sub(
        r'\[NEW(&#x2014;[^\]]*)\]',
        r'<span class="lc-arch-new">[NEW\1]</span>',
        escaped
    )
    escaped = re.sub(
        r'\[REPLACED(&#x2014;[^\]]*)\]',
        r'<span class="lc-arch-replaced">[REPLACED\1]</span>',
        escaped
    )
    # Handle [NEW — ...] and [REPLACED — ...] with Unicode em dash
    # (escaped as &#8212; or literal) — catch remaining patterns
    escaped = re.sub(
        r'\[NEW([^\]]+)\]',
        r'<span class="lc-arch-new">[NEW\1]</span>',
        escaped
    )
    escaped = re.sub(
        r'\[REPLACED([^\]]+)\]',
        r'<span class="lc-arch-replaced">[REPLACED\1]</span>',
        escaped
    )

    intro_html = f'    <p class="lc-arch-intro">{html_lib.escape(intro)}</p>\n' if intro else ""

    return (
        card_open("cyan")
        + topper("Before You Begin", "Program Architecture")
        + panel_open()
        + intro_html
        + f"""    <div class="lc-arch">
      <pre>{escaped}</pre>
    </div>
"""
        + panel_close()
        + card_close()
    )


# ============================================================
# Overview Card Sections (shared)
# ============================================================

def render_objectives(objectives: list) -> str:
    """Render the learning objectives list."""
    items = "".join(
        f'      <li>{html_lib.escape(obj)}</li>\n'
        for obj in objectives
    )
    return f"""    <ul class="lc-objectives">
{items}    </ul>
"""


def render_named_constants(constants: list) -> str:
    """Render the named constants table."""
    rows = ""
    for c in constants:
        name = c.get("name", "")
        desc = c.get("description", "")
        rows += f"""      <tr>
        <td><code>{html_lib.escape(name)}</code></td>
        <td>{html_lib.escape(desc)}</td>
      </tr>
"""
    return f"""    <div class="lc-table-wrap">
      <table class="lc-table lc-named-constants__table">
        <thead>
          <tr>
            <th>Constant</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
{rows}        </tbody>
      </table>
    </div>
"""


def render_program_requirements(requirements: list) -> str:
    """Render the program requirements checklist."""
    items = "".join(
        f'      <li>{html_lib.escape(req)}</li>\n'
        for req in requirements
    )
    return f"""    <ul>
{items}    </ul>
"""


# ============================================================
# Final Checklist Card
# ============================================================

ACADEMIC_INTEGRITY_DEFAULT = (
    "All submitted code must be your own work. You may use your textbook, "
    "class notes, the BookEx reference guides, and course-provided resources. "
    "Do not share code with other students or submit AI-generated solutions "
    "as your own. If you are unsure whether a resource is permitted, ask first."
)


def render_final_checklist(checklist: dict) -> str:
    """Render the full red Final Checklist card."""
    before_you_submit = checklist.get("beforeYouSubmit", [])
    scope_reminder = checklist.get("scopeReminder", "")
    permitted = checklist.get("permittedTechniques", {})
    warnings = checklist.get("warnings", [])
    save_your_code = checklist.get("saveYourCode", "")
    academic_integrity = checklist.get(
        "academicIntegrity", ACADEMIC_INTEGRITY_DEFAULT
    )

    # Before You Submit checklist
    checklist_items = ""
    for item in before_you_submit:
        checklist_items += f"""      <li class="lc-checklist-item">
        <span class="lc-checklist__box"></span>
        <span class="lc-checklist__label">{html_lib.escape(item)}</span>
      </li>
"""

    submit_block = f"""    <div class="lc-h3">Before You Submit</div>
    <ul class="lc-checklist">
{checklist_items}    </ul>
""" if checklist_items else ""

    # Scope reminder
    scope_block = f"""    <div class="lc-h3">Scope Reminder</div>
    <p>{html_lib.escape(scope_reminder)}</p>
""" if scope_reminder else ""

    # Permitted techniques
    permitted_block = ""
    if permitted:
        chapters = permitted.get("chapters", "")
        specific = permitted.get("specific", [])
        not_permitted = permitted.get("notPermitted", "")

        specific_items = "".join(
            f'      <li>{html_lib.escape(s)}</li>\n' for s in specific
        )
        not_permitted_html = (
            f'    <p class="lc-permitted__not-permitted">'
            f'<strong>Not permitted:</strong> {html_lib.escape(not_permitted)}</p>\n'
        ) if not_permitted else ""

        permitted_block = f"""    <div class="lc-h3">Permitted Techniques</div>
    <div class="lc-permitted">
      <p class="lc-permitted__chapters"><strong>Chapters in scope:</strong> {html_lib.escape(chapters)}</p>
      <ul class="lc-permitted__list">
{specific_items}      </ul>
{not_permitted_html}    </div>
"""

    # Warnings
    warnings_html = ""
    for w in warnings:
        warnings_html += f"""    <div class="lc-callout lc-callout--warning">
      <div class="lc-callout__icon">
        {CALLOUT_ICONS["warning"].strip()}
      </div>
      <div class="lc-callout__bubble">
        <div class="lc-callout__body">
          <p>{html_lib.escape(w)}</p>
        </div>
      </div>
    </div>
"""

    # Save Your Code
    save_block = f"""    <div class="lc-callout lc-callout--success">
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
""" if save_your_code else ""

    # Academic Integrity
    integrity_block = f"""    <div class="lc-h3">Academic Integrity</div>
    <p>{html_lib.escape(academic_integrity)}</p>
"""

    return f"""{card_open("red")}
{topper("Final Checklist", "Check It Before You Wreck It")}
{panel_open()}
{submit_block}{scope_block}{permitted_block}{warnings_html}{save_block}{integrity_block}{panel_close()}{card_close()}"""


# ============================================================
# Need Help Card
# ============================================================

CONTACT_GRID_HTML = """    <div class="lc-contact-grid">
      <div class="lc-contact-card">
        <div class="lc-contact-card__label">Zoom Office Hours</div>
        <div class="lc-contact-card__value">Tuesdays 6&ndash;7 PM<br>
          <a href="https://utsa.zoom.us/j/97617245124" target="_blank">Join Meeting</a>
        </div>
      </div>
      <div class="lc-contact-card">
        <div class="lc-contact-card__label">Schedule a Meeting</div>
        <div class="lc-contact-card__value">
          <a href="https://calendly.com/john-newsom-utsa/student-meeting" target="_blank">Book via Calendly</a>
        </div>
      </div>
      <div class="lc-contact-card">
        <div class="lc-contact-card__label">Course Discord</div>
        <div class="lc-contact-card__value">Post questions in <strong>#help</strong> &mdash; check if your question has already been answered</div>
      </div>
      <div class="lc-contact-card">
        <div class="lc-contact-card__label">Email</div>
        <div class="lc-contact-card__value">
          <a href="mailto:john.newsom@utsa.edu">john.newsom@utsa.edu</a><br>
          Include your section number and abc123
        </div>
      </div>
      <div class="lc-contact-card">
        <div class="lc-contact-card__label">CodeGrade</div>
        <div class="lc-contact-card__value">Submit early and often &mdash; feedback is instant and submissions are unlimited</div>
      </div>
    </div>
"""


def render_need_help(need_help: dict) -> str:
    """Render the full purple Need Help card."""
    if_you_get_stuck = need_help.get("ifYouGetStuck", [])
    bookex_note = need_help.get("bookexResourceNote", "")

    stuck_items = "".join(
        f'      <li>{html_lib.escape(item)}</li>\n'
        for item in if_you_get_stuck
    )
    stuck_block = f"""    <div class="lc-h3">If You Get Stuck</div>
    <ul>
{stuck_items}    </ul>
""" if stuck_items else ""

    bookex_block = f"""    <div class="lc-callout lc-callout--bookex">
      <div class="lc-callout__icon">
        {CALLOUT_ICONS["bookex"].strip()}
      </div>
      <div class="lc-callout__bubble">
        <div class="lc-callout__title">BookEx Reference Guides</div>
        <div class="lc-callout__body">
          <p>{html_lib.escape(bookex_note)}</p>
        </div>
      </div>
    </div>
""" if bookex_note else ""

    return f"""{card_open("purple")}
{topper("Need Help?", "Look No Further!")}
{panel_open()}
{stuck_block}{bookex_block}    <div class="lc-h3">Contact &amp; Resources</div>
{CONTACT_GRID_HTML}{panel_close()}{card_close()}"""
