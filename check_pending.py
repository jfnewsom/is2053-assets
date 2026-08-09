#!/usr/bin/env python3
"""
check_pending.py - Placeholders are allowed to exist. They are not allowed to
be forgotten.

Some content genuinely cannot be written yet. The face-to-face Simple Syllabus
URL does not exist until the online course is cloned, and the 904 welcome video
does not exist until it is recorded. Blocking the build on either would leave
render_all.sh red for weeks, which teaches you to ignore the output - the exact
failure mode already noted for verify_output.py. Staying silent instead means
the placeholder ships.

So: a placeholder is a WARNING now and a HARD FAILURE from HARD_FAIL_FROM, a
couple of days before students arrive. The deadline does the remembering.

Mark a placeholder by putting a NAME_PENDING token in the source. Nothing needs
registering here; the token is the registration. Two rules only:

  1. The token must never reach a student. Either the renderer omits the item
     (the syllabus link) or the whole block is an HTML comment (the 904 welcome
     video). This checks the BUILT trees to prove it.
  2. Every token is listed on every run, so the set of unfinished things is
     visible rather than remembered.

    python3 check_pending.py
"""
import datetime
import glob
import io
import re
import sys

# Classes start Wed Aug 19, 2026. Two days of buffer.
HARD_FAIL_FROM = datetime.date(2026, 8, 17)

TOKEN = re.compile(r'\b([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*_PENDING)\b')
BUILT_TREES = ('onl', 'f2f')

# What each token is waiting on, so the warning is actionable rather than a
# bare identifier. A token with no entry still works; it just reads worse.
CONTEXT = {
    'SYLLABUS_URL_PENDING':
        'the 904 Simple Syllabus doc, created by cloning the online course '
        '(ledger L-025). Paste the URL into pages/support/json/start-here.json.',
    'F2F_WELCOME_VIDEO_PENDING':
        'the 904 welcome video. Paste the embed into the F2F_ONLY block in '
        'pages/support/json/home.json and delete the comment wrapper.',
    'F2F_SYLLABUS_LINK_PENDING':
        'the same 904 Simple Syllabus URL as SYLLABUS_URL_PENDING, needed a '
        'second time for the home page Quick Links. Add the row to the f2f '
        'branch of the Quick Links block in pages/support/json/home.json. '
        'Until then f2f shows no syllabus row rather than a dead link, and '
        'the Canvas left-nav Syllabus link still works.',
}


def sources():
    return (sorted(glob.glob('pages/**/*.json', recursive=True))
            + sorted(glob.glob('pages/**/*.html', recursive=True)))


def visible_text(html):
    """What a student could actually see: markup minus HTML comments."""
    return re.sub(r'<!--.*?-->', '', html, flags=re.S)


def main():
    found = {}
    for path in sources():
        for m in TOKEN.finditer(io.open(path, encoding='utf-8').read()):
            found.setdefault(m.group(1), set()).add(path)

    problems = []
    # Rule 1: a placeholder must never be visible in a built tree.
    for tree in BUILT_TREES:
        for path in sorted(glob.glob(f'{tree}/**/*.html', recursive=True)):
            text = visible_text(io.open(path, encoding='utf-8').read())
            for m in TOKEN.finditer(text):
                problems.append(
                    f'{path} would SHOW "{m.group(1)}" to a student. A pending '
                    f'placeholder must be omitted by the renderer or wrapped in '
                    f'an HTML comment.')

    overdue = datetime.date.today() >= HARD_FAIL_FROM
    lines = []
    for tok in sorted(found):
        where = ', '.join(sorted(p for p in found[tok] if not p.startswith(BUILT_TREES)))
        lines.append(f'{tok} - waiting on {CONTEXT.get(tok, "(no context recorded)")} '
                     f'[{where}]')

    if not found and not problems:
        print('check_pending: PASS (nothing pending)')
        return 0

    for line in lines:
        label = 'OVERDUE' if overdue else 'WARNING'
        print(f'check_pending: {label} - {line}')
    if not overdue and lines:
        print(f'check_pending: {len(lines)} placeholder(s); these become a hard '
              f'failure on {HARD_FAIL_FROM.isoformat()}.')

    if overdue:
        problems += [f'{t} is still unresolved past {HARD_FAIL_FROM.isoformat()}'
                     for t in sorted(found)]
    if problems:
        print('check_pending: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('check_pending: PASS (placeholders present but none student-visible)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
