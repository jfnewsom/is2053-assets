#!/usr/bin/env python3
"""
check_zoom_room.py - One course, one Zoom room.

WHY THIS EXISTS
On 2026-08-09 the repo held two different room IDs. 96542097913 was on the home
page, Start Here, How to Get Help, and the footer of every lab and BookEx sheet:
34 references. 97617245124 was in exactly one place that matters more than all
of them, the floating **Join Zoom** button nav.js pops up on Tuesdays between
6:00 and 7:30, which is the button a student actually clicks at the moment
office hours start. So the one link used under time pressure was the one
pointing at the wrong room, and everything a student would have read earlier in
the week was right. John confirmed 96542097913.

Nothing had caught it because every existing guard asked whether a link was
well-formed or current, and both IDs are well-formed and neither names a term.
The invariant here is not shape, it is AGREEMENT: a course has one office-hours
room, so every reference to one must be the same string.

If a second room is ever legitimate, for instance a separate exam-proctoring
room, add it to ALLOWED with the reason. Do not delete the check. The point is
that a second ID has to be a decision somebody wrote down, not a paste.

    python3 check_zoom_room.py
"""
import glob
import re
import sys

ROOM = '96542097913'

# Room IDs that are deliberately not the office-hours room. Each needs a reason.
ALLOWED = {}

ZOOM = re.compile(r'utsa\.zoom\.us/j/(\d+)')


def sources():
    seen = set()
    for pat in ('*.js', 'pages/**/*.json', 'pages/**/*.html', 'pages/**/*.js',
                'onl/**/*.html', 'f2f/**/*.html'):
        seen |= set(glob.glob(pat, recursive=True))
    return sorted(f for f in seen if '_to_delete' not in f)


def main():
    problems, hits, files = [], 0, sources()
    for f in files:
        with open(f, encoding='utf-8', errors='ignore') as fh:
            for rid in ZOOM.findall(fh.read()):
                hits += 1
                if rid == ROOM or rid in ALLOWED:
                    continue
                problems.append(
                    f'{f} links Zoom room {rid}, not the office-hours room {ROOM}. '
                    f'If that is deliberate, add it to ALLOWED with a reason.')

    if problems:
        print('check_zoom_room: FAIL')
        for p in sorted(set(problems)):
            print(f'  - {p}')
        return 1
    print(f'check_zoom_room: PASS ({hits} Zoom link(s) across {len(files)} file(s), '
          f'all room {ROOM})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
