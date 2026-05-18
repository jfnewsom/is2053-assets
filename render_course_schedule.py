#!/usr/bin/env python3
"""
render_course_schedule.py — Renders pages/support/course-schedule.html
from pages/support/json/calendar.json.

Single source of truth for all term-schedule data. The companion markdown
calendar (IS2053_2026-05-11_Summer_2026_Calendar.md in project knowledge)
is the human reference; calendar.json mirrors its tables in machine form.

Page structure: one outer orange card (home-page pattern) with four
internal lc-named-section blocks:
  1. Weekly Cadence  (default yellow label)
  2. 10-Week Schedule  (orange label)
  3. How Module 5 Differs  (purple label)
  4. Term Dates  (cyan label) — boundaries / holidays / registrar deadlines

Drop policy is NOT on this page — it lives on grading-info.html (Drops
section). Per the site design principle, each page is self-contained
within its own topic; cross-topic content stays where it canonically
belongs.

Run with:
    python3 render_course_schedule.py

Source:  pages/support/json/calendar.json
Output:  pages/support/course-schedule.html
"""
import json
from pathlib import Path


# ── Small renderers ──────────────────────────────────────────────────

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


def render_info_bar(cadence):
    """The weekly cadence info bar. Adds lc-info-bar--5col modifier when
    there are 5+ stats (so they don't pack into the default 4-column grid)."""
    cells = []
    for stat in cadence['stats']:
        cells.append(
            f'        <div class="lc-info-stat">\n'
            f'          <div class="lc-info-stat__label lc-info-stat__label--{stat["labelColor"]}">{stat["label"]}</div>\n'
            f'          <div class="lc-info-stat__value lc-info-stat__value--lg">{stat["value_html"]}</div>\n'
            f'        </div>'
        )
    cells_html = '\n'.join(cells)
    bar_classes = 'lc-info-bar'
    if len(cadence['stats']) >= 5:
        bar_classes += ' lc-info-bar--5col'
    return (
        f'      <div class="{bar_classes}">\n'
        f'{cells_html}\n'
        f'      </div>'
    )


# ── Section renderers ────────────────────────────────────────────────

def render_section_cadence(term, cadence):
    """Section 1: Weekly Cadence — term intro + info bar + footer note."""
    classes = section_div_classes(None)
    label_html = render_section_label('Weekly Cadence', None)
    info_bar_html = render_info_bar(cadence)
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {term["intro_html"]}\n'
        f'\n'
        f'{info_bar_html}\n'
        f'\n'
        f'      {cadence["footer_html"]}\n'
        f'      </div>'
    )


def render_section_schedule(schedule):
    """Section 2: 10-Week Schedule — the dense data table."""
    classes = section_div_classes('orange')
    label_html = render_section_label('10-Week Schedule', 'orange')

    # Headers
    headers_html = []
    for h in schedule['headers']:
        style_attr = f' style="{h["style"]}"' if h['style'] else ''
        headers_html.append(f'              <th{style_attr}>{h["label"]}</th>')
    headers_block = '\n'.join(headers_html)

    # Rows
    em_dash_cell = '<td style="color: #6c7a8c; font-style: italic;">&mdash;</td>'

    def cell(html, css_class=None):
        if html is None:
            return f'              {em_dash_cell}'
        cls_attr = f' class="{css_class}"' if css_class else ''
        return f'              <td{cls_attr}>{html}</td>'

    rows_html = []
    for row in schedule['rows']:
        tr_class = ' class="lc-st-m5-row"' if row['isM5'] else ''
        rows_html.append(
            f'            <tr{tr_class}>\n'
            f'{cell(row["module_html"], "lc-st-module")}\n'
            f'{cell(row["window_html"])}\n'
            f'{cell(row["bookex1_html"])}\n'
            f'{cell(row["lab1_html"])}\n'
            f'{cell(row["bookex2_html"])}\n'
            f'{cell(row["lab2_html"])}\n'
            f'{cell(row["lab3_html"], "lc-st-highlight") if row["lab3_html"] else cell(None)}\n'
            f'{cell(row["exam_html"])}\n'
            f'            </tr>'
        )

    # Closing row (last-day banner)
    closing_row = (
        f'            <tr class="lc-st-final-row">\n'
        f'              <td colspan="8">{schedule["closingRow_html"]}</td>\n'
        f'            </tr>'
    )
    rows_html.append(closing_row)
    rows_block = '\n'.join(rows_html)

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'        <table class="lc-schedule-table">\n'
        f'          <thead>\n'
        f'            <tr>\n'
        f'{headers_block}\n'
        f'            </tr>\n'
        f'          </thead>\n'
        f'          <tbody>\n'
        f'{rows_block}\n'
        f'          </tbody>\n'
        f'        </table>\n'
        f'        <p style="font-size: 13px; color: var(--color-text-muted); margin-top: 14px;">Worried about turning stuff in late? See the <a href="grading-info.html#late-work">late policy</a>.</p>\n'
        f'      </div>'
    )


def render_section_module5(m5):
    """Section 3: How Module 5 Differs — intro + lab bullets + explanation."""
    classes = section_div_classes('purple')
    label_html = render_section_label('How Module 5 Differs', 'purple')
    labs_lis = '\n'.join(f'        <li>{lab}</li>' for lab in m5['labs_html'])
    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'      {m5["intro_html"]}\n'
        f'\n'
        f'      <ul>\n'
        f'{labs_lis}\n'
        f'      </ul>\n'
        f'\n'
        f'      {m5["explanation_html"]}\n'
        f'      </div>'
    )


def render_section_term_dates(td):
    """Section 4: Term Dates — three lc-h3 sub-blocks (Boundaries / Holidays
    / Registrar) + a due-times callout at the end."""
    classes = section_div_classes('cyan')
    label_html = render_section_label('Term Dates', 'cyan')

    # Holidays list
    holidays_lis = '\n'.join(
        f'        <li><strong>{h["date_html"]}</strong> &mdash; {h["name_html"]}</li>'
        for h in td['holidays']
    )

    # Registrar list
    reg_lis = '\n'.join(
        f'        <li><strong>{r["date_html"]}</strong> &mdash; {r["event_html"]}</li>'
        for r in td['registrarDeadlines']
    )

    callout_html = render_callout(td['dueTimesCallout'])

    return (
        f'      <div class="{classes}">\n'
        f'{label_html}\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--cyan">Term Boundaries</div>\n'
        f'      {td["termBoundaries_html"]}\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--cyan">University Holidays</div>\n'
        f'      <ul>\n'
        f'{holidays_lis}\n'
        f'      </ul>\n'
        f'      {td["holidaysFooter_html"]}\n'
        f'\n'
        f'      <div class="lc-h3 lc-h3--cyan">Registrar Deadlines</div>\n'
        f'      <ul>\n'
        f'{reg_lis}\n'
        f'      </ul>\n'
        f'\n'
        f'{callout_html}\n'
        f'      </div>'
    )


# ── Top-level renderer ───────────────────────────────────────────────

def render_card_topper(term):
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
        f'            <div class="lc-topper-title">Course Schedule</div>\n'
        f'          </td>\n'
        f'          <td style="width: 1%; white-space: nowrap; vertical-align: bottom; padding: 0 0 0 16px; text-align: right;">\n'
        f'            <img src="https://jfnewsom.github.io/is2053-assets/branding/BatCity-logo-3D.png"\n'
        f'                 alt="Bat City Collective" style="height: 84px; width: auto; display: block;">\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'        <tr>\n'
        f'          <td colspan="3" style="padding: 10px 0 0 0;">\n'
        f'            <div class="lc-sub-banner">{term["subBanner_html"]}</div>\n'
        f'          </td>\n'
        f'        </tr>\n'
        f'      </table>\n'
        f'    </div>'
    )


def render_page(data):
    """Render course-schedule.html — one outer orange card with four sections."""
    term = data['term']
    cadence_section = render_section_cadence(term, data['cadence'])
    schedule_section = render_section_schedule(data['schedule'])
    m5_section = render_section_module5(data['module5Differs'])
    term_dates_section = render_section_term_dates(data['termDates'])

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">\n'
        '  <meta name="site-context" content="support">\n'
        '  <title>Course Schedule | IS2053 Programming I</title>\n'
        '  <link rel="stylesheet" href="https://jfnewsom.github.io/is2053-assets/labs.css">\n'
        '</head>\n'
        '<body>\n'
        '<div class="lc-wrapper">\n\n\n'
        '  <!-- ══════════════════════════════════════════════════════════\n'
        '       Course Schedule — single card, sections within (home-page pattern)\n'
        '  ══════════════════════════════════════════════════════════ -->\n'
        '  <div class="lc-card lc-card--orange">\n'
        f'{render_card_topper(term)}\n'
        '    <div class="lc-panel">\n\n'
        f'{cadence_section}\n\n'
        f'{schedule_section}\n\n'
        f'{m5_section}\n\n'
        f'{term_dates_section}\n\n'
        '    </div>\n'
        '  </div>\n\n\n'
        '</div><!-- /lc-wrapper -->\n'
        '<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / 'pages' / 'support' / 'json' / 'calendar.json'
    out = repo_root / 'pages' / 'support' / 'course-schedule.html'

    print(f'Reading {src}')
    with open(src) as f:
        data = json.load(f)

    html = render_page(data)
    out.write_text(html, encoding='utf-8')
    print(f'  Rendered → {out}  ({len(html.splitlines())} lines)')


if __name__ == '__main__':
    main()
