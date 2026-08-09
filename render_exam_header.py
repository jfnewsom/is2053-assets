#!/usr/bin/env python3
"""
render_exam_header.py - Generate the five Canvas exam header pages.

Ledger L-021 tranche two. These five pages were the last hand-maintained
student-facing HTML in the repo, and they had already drifted: the voice pass
rewrote the tips in exams.json (em-dash to colon), but nothing regenerated the
pages, so the HTML still carried the old wording. A page with a source that
nothing reads is not a source, it is a second copy.

They are also 90% identical to each other. Every difference between module 1
and module 4 is data (question count, chapters, tips), and module 5 adds one
optional element, the points breakdown, which is already flagged in the JSON as
`showPointsBreakdown`.

Source:  pages/exams/json/exams.json  (same file render_grading_info.py reads)
Output:  pages/exams/exam-header-module-{1..5}.html

    python3 render_exam_header.py
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages' / 'exams' / 'json' / 'exams.json'
OUT = REPO / 'pages' / 'exams'

# Module N gets the same accent as everywhere else in the course.
CARD_COLOR = 'red'


def stat(num, label):
    return (f'            <div class="lc-stat-block">\n'
            f'                <div class="lc-stat-block__num">{num}</div>\n'
            f'                <div class="lc-stat-block__label">{label}</div>\n'
            f'            </div>')


def render_format_card(exam, common):
    """Top card: title, sub-banner, the stat grid, and the format sentence."""
    intro = (f'This exam contains <strong>multiple choice</strong>, '
             f'<strong>true/false</strong>, and <strong>code tracing</strong> questions. '
             f'{common["questionPoolNote"]}')

    # Order matches the hand-authored pages this replaced: the points pair sits
    # between Questions and Minutes, not appended at the end.
    stats = [stat(exam['questions'], 'Questions')]
    if exam.get('showPointsBreakdown'):
        total = exam.get('pointsTotal') or 100
        # Derive rather than hardcode, so changing the question count in the
        # JSON cannot leave the arithmetic on the page saying something else.
        per = exam.get('pointsEach') or (total // exam['questions'] if exam['questions'] else 0)
        stats += [stat(per, 'Points Each'), stat(total, 'Points Total')]
        intro += (f' Each question is worth <strong>{per} points</strong> '
                  f'for a total of <strong>{total} points</strong>.')
    stats += [stat(exam['timeLimitMinutes'], 'Minutes'),
              stat(exam['attempts'], 'Attempt' if exam['attempts'] == 1 else 'Attempts')]

    return (
        f'<div class="lc-card lc-card--{CARD_COLOR}">\n'
        f'    <div class="lc-topper">\n'
        f'        <div class="lc-topper-title">Module {exam["num"]} Exam</div>\n'
        f'        <div class="lc-sub-banner">{exam["subtitle"]}</div>\n'
        f'    </div>\n'
        f'    <div class="lc-panel">\n'
        f'        <div class="lc-h3 lc-h3--{CARD_COLOR}">Exam Format</div>\n'
        f'        <div class="lc-stat-grid">\n'
        + '\n'.join(stats) + '\n'
        f'        </div>\n'
        f'        <p>{intro}</p>\n'
        f'    </div>\n'
        f'</div>'
    )


def render_two_col(exam, common):
    """Time Limit and Allowed Materials, side by side."""
    rules = list(common['timeLimitRules'])
    rules.append(f'<strong>Budget {exam["timePerQuestion"]}</strong>')
    time_items = '\n'.join(f'                <li>{r}</li>' for r in rules)

    mats = []
    for m in common['allowedMaterials']:
        mark = ('<span class="lc-allow">&#10003;</span>' if m['allowed']
                else '<span class="lc-deny">&#10007;</span>')
        mats.append(f'                <li>{mark} {m["text"]}</li>')

    return (
        f'<div class="lc-two-col">\n'
        f'    <div class="lc-card lc-card--orange">\n'
        f'        <div class="lc-panel">\n'
        f'            <div class="lc-h3 lc-h3--orange">Time Limit</div>\n'
        f'            <ul>\n{time_items}\n            </ul>\n'
        f'        </div>\n'
        f'    </div>\n'
        f'    <div class="lc-card lc-card--green">\n'
        f'        <div class="lc-panel">\n'
        f'            <div class="lc-h3 lc-h3--green">Allowed Materials</div>\n'
        f'            <ul>\n' + '\n'.join(mats) + '\n            </ul>\n'
        f'        </div>\n'
        f'    </div>\n'
        f'</div>'
    )


def render_chapters(exam):
    rows = '\n'.join(
        f'                    <tr>\n'
        f'                        <td><strong>Chapter {c["num"]}</strong></td>\n'
        f'                        <td>{c["topics"]}</td>\n'
        f'                    </tr>'
        for c in exam['chapters'])
    return (
        f'<div class="lc-card lc-card--purple">\n'
        f'    <div class="lc-panel">\n'
        f'        <div class="lc-h3 lc-h3--purple">Chapters Covered</div>\n'
        f'        <div class="lc-table-wrap">\n'
        f'            <table class="lc-table">\n'
        f'                <thead>\n'
        f'                    <tr>\n'
        f'                        <th>Chapter</th>\n'
        f'                        <th>Key Topics</th>\n'
        f'                    </tr>\n'
        f'                </thead>\n'
        f'                <tbody>\n{rows}\n                </tbody>\n'
        f'            </table>\n'
        f'        </div>\n'
        f'    </div>\n'
        f'</div>'
    )


def render_tips(exam):
    items = '\n'.join(f'            <li>{t}</li>' for t in exam['tips'])
    return (
        f'<div class="lc-card lc-card--cyan">\n'
        f'    <div class="lc-panel">\n'
        f'        <div class="lc-h3 lc-h3--cyan">Tips for Success</div>\n'
        f'        <ul>\n{items}\n        </ul>\n'
        f'    </div>\n'
        f'</div>'
    )


def render_footer(common):
    return (
        f'<div class="lc-integrity">\n'
        f'    <div class="lc-integrity__icon">&#9888;&#65039;</div>\n'
        f'    <div>\n'
        f'        <div class="lc-integrity__heading">Academic Integrity</div>\n'
        f'        <p>{common["integrityStatement"]}</p>\n'
        f'    </div>\n'
        f'</div>\n\n'
        f'<div class="lc-ready">\n'
        f'    <p class="lc-ready__prompt">{common["readyPrompt"]}</p>\n'
        f'    <p class="lc-ready__note">{common["canvasNote"]}</p>\n'
        f'</div>'
    )


def render_page(exam, common):
    body = '\n\n'.join([
        render_format_card(exam, common),
        render_two_col(exam, common),
        render_chapters(exam),
        render_tips(exam),
        render_footer(common),
    ])
    return (
        f'<!DOCTYPE html>\n'
        f'<html lang="en">\n'
        f'<head>\n'
        f'    <meta charset="UTF-8">\n'
        f'    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'    <title>Module {exam["num"]} Exam | IS2053</title>\n'
        f'    <link rel="stylesheet" href="../../labs.css">\n'
        f'</head>\n'
        f'<body>\n'
        f'<div class="lc-wrapper">\n\n'
        f'{body}\n\n'
        f'</div>\n'
        f'<script src="https://jfnewsom.github.io/is2053-assets/nav.js"></script>\n'
        f'</body>\n'
        f'</html>\n'
    )


def main():
    if not SRC.is_file():
        sys.exit(f'render_exam_header.py: {SRC} not found; run from the repo root.')
    data = json.loads(SRC.read_text(encoding='utf-8'))
    common = data['common']
    for exam in data['exams']:
        out = OUT / f'exam-header-module-{exam["num"]}.html'
        out.write_text(render_page(exam, common), encoding='utf-8')
        print(f'  Rendered -> {out.relative_to(REPO)}')
    print(f'render_exam_header: {len(data["exams"])} exam header page(s) from exams.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
