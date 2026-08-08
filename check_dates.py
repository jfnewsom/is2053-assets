#!/usr/bin/env python3
"""
check_dates.py - Every date on a student-facing page belongs to THIS term.

On 2026-08-08 the Grading Info page still told students the final cutoff was
"11:59 PM Tuesday, August 4" - a Summer 2026 date, live on the Fall site
(ledger F-022). Nothing caught it. check_style.py counts em-dashes, lab_lint.py
reads labs, verify_output.py runs solutions, check_syllabus_links.py checks one
URL. None of them look at dates, so the only thing standing between a stale term
date and a student was somebody reading the page. That is not a control.

Two checks, both cheap:

  WINDOW    Every Month+Day found in the sources must fall inside the term.
            August 4 is before Aug 19, so this is the check that would have
            caught it. Also catches a date rippled one week the wrong way, and
            anything left over from last term's calendar.

  WEEKDAY   Every "Tue Oct 20" pair must actually BE that weekday in the term
            year. Catches the far more likely error: a correct date typed with
            the wrong day name, or a date shifted without updating the day.

Ranges are parsed rather than fumbled. "Mon-Tue Oct 12-13" pairs the first
weekday with the first day and the second with the second; a naive scan reads it
as "Tue Oct 12" and reports a mismatch that is not there.

EACH TERM: update TERM, FIRST_DAY and LAST_DAY. That is the whole maintenance
burden, and getting it wrong fails loudly rather than silently passing.

    python3 check_dates.py
"""
import datetime
import glob
import io
import re
import sys

TERM = 'Fall 2026'
# Classes start Wed Aug 19, 2026; end of term Fri Dec 11; grades posted Mon Dec 14.
# The window runs to the last date a student could legitimately see, not the
# last class day, or every "grades posted" line would trip it.
FIRST_DAY = datetime.date(2026, 8, 19)
LAST_DAY = datetime.date(2026, 12, 14)

# Dates that are correct despite sitting outside the window. Empty today; add
# entries as (month, day, 'why'), never by widening the window, so each
# exception stays justified in writing.
ALLOWED_OUTSIDE = {}

MONTHS = {}
for _i, _m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                         'August', 'September', 'October', 'November', 'December'], 1):
    MONTHS[_m] = _i
    MONTHS[_m[:3]] = _i
MONTHS['Sept'] = 9

DOW = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DOWS = {}
for _i, _d in enumerate(DOW):
    DOWS[_d] = _i
    DOWS[_d[:3]] = _i
DOWS['Tues'] = 1
DOWS['Thur'] = DOWS['Thurs'] = 3

_M = '|'.join(sorted(MONTHS, key=len, reverse=True))
_D = '|'.join(sorted(DOWS, key=len, reverse=True))
# HTML entities are the real text here: &ndash; and &mdash; show up far more
# often than a literal hyphen.
_DASH = r'(?:&ndash;|&mdash;|[-–—])'

RANGE = re.compile(rf'\b({_D})\.?\s*{_DASH}\s*({_D})\.?,?\s+({_M})\.?\s+(\d{{1,2}})\s*{_DASH}\s*(\d{{1,2}})\b')
PAIR = re.compile(rf'\b({_D})\.?,?\s+({_M})\.?\s+(\d{{1,2}})\b')
BARE = re.compile(rf'\b({_M})\.?\s+(\d{{1,2}})\b')


def sources():
    return sorted(set(glob.glob('pages/**/json/*.json', recursive=True)
                      + glob.glob('pages/**/json/**/*.json', recursive=True)))


def make(month, day):
    try:
        return datetime.date(FIRST_DAY.year, MONTHS[month], int(day))
    except ValueError:
        return None


def main():
    problems, checked_pairs, checked_dates = [], 0, 0

    for path in sources():
        text = io.open(path, encoding='utf-8').read()

        # Consume ranges first so their inner dates are not re-read as pairs.
        def take_range(m):
            nonlocal checked_pairs
            d1, d2, mon, a, b = m.groups()
            for dow, day in ((d1, a), (d2, b)):
                date = make(mon, day)
                checked_pairs += 1
                if date is None:
                    problems.append(f'{path}: "{m.group(0)}" contains an impossible date')
                elif date.weekday() != DOWS[dow]:
                    problems.append(
                        f'{path}: "{m.group(0)}" says {dow} for {mon} {day}, '
                        f'which is a {DOW[date.weekday()]} in {FIRST_DAY.year}')
            return ' '

        text = RANGE.sub(take_range, text)

        for m in PAIR.finditer(text):
            dow, mon, day = m.groups()
            date = make(mon, day)
            checked_pairs += 1
            if date is None:
                problems.append(f'{path}: "{m.group(0)}" is not a real date')
            elif date.weekday() != DOWS[dow]:
                problems.append(
                    f'{path}: "{m.group(0)}" is a {DOW[date.weekday()]} in {FIRST_DAY.year}, '
                    f'not a {dow}day' if len(dow) > 3 else
                    f'{path}: "{m.group(0)}" is actually a {DOW[date.weekday()]}')

        for m in BARE.finditer(text):
            mon, day = m.groups()
            date = make(mon, day)
            if date is None:
                continue
            checked_dates += 1
            if (MONTHS[mon], int(day)) in ALLOWED_OUTSIDE:
                continue
            if not (FIRST_DAY <= date <= LAST_DAY):
                problems.append(
                    f'{path}: "{m.group(0)}" is outside {TERM} '
                    f'({FIRST_DAY.isoformat()} to {LAST_DAY.isoformat()}). '
                    f'Stale term date, or add it to ALLOWED_OUTSIDE with a reason.')

    print(f'check_dates: {checked_dates} date(s) and {checked_pairs} weekday+date '
          f'pair(s) across {len(sources())} source files, against {TERM}')
    if problems:
        print('check_dates: FAIL')
        for p in sorted(set(problems)):
            print(f'  - {p}')
        return 1
    print('check_dates: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
