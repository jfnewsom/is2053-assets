#!/usr/bin/env python3
"""
check_syllabus_links.py - The syllabus link is per-modality and per-term.

Two failure modes have both already happened, so both are checked here.

STALE TERM. On 2026-08-08 the Start Here page was still sending every student
to the Summer 2026 Simple Syllabus doc (ledger L-025). It is the first external
link a student clicks and nothing verified it, because check_style.py counts
em-dashes and lab_lint.py reads labs. A syllabus URL naming a term other than
the current one fails.

WRONG MODALITY. Online and face-to-face are different Simple Syllabus documents
(2026-08-08 decision). The two links live side by side in start-here.json,
fenced by ONL_ONLY / F2F_ONLY sentinels, and render_variant.py strips the one
that does not belong. This asserts the outcome rather than trusting it: each
built tree must contain exactly one syllabus link, and it must be that
modality's. A tree with two means a strip entry is missing; a tree with zero
means the sentinel names disagree.

PENDING. The face-to-face Simple Syllabus does not exist yet: it is created by
CLONING the perfected online Canvas course, so its URL is unknowable until the
clone batch, the last step before term start. A pending URL is therefore NORMAL
for now and only a WARNING, and the renderer omits the link entirely rather than
emitting a dead href. It becomes a hard failure from HARD_FAIL_FROM, so it
cannot be forgotten in the last week. A permanently red build is worse than no
build check at all, because it teaches you to skip the output.

    python3 check_syllabus_links.py
"""
import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages' / 'support' / 'json' / 'start-here.json'

TERM = 'Fall-2026'
# Classes start Wed Aug 19, 2026. Two days of buffer: from this date a pending
# syllabus URL stops being a warning and fails the build.
HARD_FAIL_FROM = datetime.date(2026, 8, 17)
PLACEHOLDER = 'SYLLABUS_URL_PENDING'
SYLLABUS = re.compile(r'https?://[^"\'\s]*simplesyllabus[^"\'\s]*')
# The modality trees, which are also the values the "modality" key may take.
#
# Deliberately NOT asserting anything about the doc slug. The first cut required
# 'ON1' in the online URL, which is the slug UTSA happened to mint for the Fall
# online doc; the section is ONL. Pinning a guard to a vendor's slug spelling
# buys nothing here (each tree already holds exactly one link and the term is
# checked) and would fail the build on a cosmetic rename.
MODALITIES = ('onl', 'f2f')


def check_source():
    d = json.loads(SRC.read_text(encoding='utf-8'))
    found, problems, warnings = {}, [], []

    def walk(o):
        if isinstance(o, dict):
            url = o.get('url', '')
            if isinstance(url, str) and ('simplesyllabus' in url
                                         or url == PLACEHOLDER):
                v = o.get('modality')
                if not v:
                    problems.append(
                        'a syllabus link in start-here.json has no "modality" key, '
                        'so it would render into BOTH modality trees')
                else:
                    found.setdefault(v, []).append(url)
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(d)

    for v in sorted(MODALITIES):
        urls = found.get(v, [])
        if not urls:
            problems.append(f'no syllabus link tagged "modality": "{v}" in start-here.json')
        elif len(urls) > 1:
            problems.append(f'{len(urls)} syllabus links tagged "{v}"; expected exactly 1')
        else:
            url = urls[0]
            if url == PLACEHOLDER:
                overdue = datetime.date.today() >= HARD_FAIL_FROM
                msg = (f'the {v} syllabus URL is still pending (ledger L-025). It is '
                       f'created by cloning the online course, so it is expected to '
                       f'land with the clone batch. The link is omitted from {v}/ '
                       f'until then, not rendered dead. Paste it into start-here.json '
                       f'and re-render.')
                (problems if overdue else warnings).append(
                    msg + (f' HARD FAILURE: past {HARD_FAIL_FROM.isoformat()}.'
                           if overdue else
                           f' Becomes a hard failure on {HARD_FAIL_FROM.isoformat()}.'))
            elif TERM not in url:
                problems.append(
                    f'the {v} syllabus URL does not name {TERM}: {url}')
    for v in sorted(set(found) - set(MODALITIES)):
        problems.append(f'syllabus link tagged with unknown modality "{v}"')
    return problems, warnings, {v: (found.get(v) or [None])[0] for v in MODALITIES}


def check_built(source_urls):
    """A modality with a known URL must ship exactly one link; a pending one
    must ship ZERO, because the renderer drops it rather than emit a dead href."""
    problems = []
    for v in sorted(MODALITIES):
        want = 0 if source_urls.get(v) in (None, PLACEHOLDER) else 1
        page = REPO / v / 'support' / 'start-here.html'
        if not page.is_file():
            problems.append(f'{v}/support/start-here.html not built; run ./render_all.sh')
            continue
        html = page.read_text(encoding='utf-8')
        urls = sorted(set(SYLLABUS.findall(html)) | set(
            [PLACEHOLDER] if PLACEHOLDER in html else []))

        # Every check below is independent. An early `continue` here once made
        # the cross-modality sentinel check unreachable for any tree whose URL
        # was still pending, which is exactly the tree most likely to be wrong.
        if len(urls) != want:
            problems.append(
                f'{v}/support/start-here.html has {len(urls)} syllabus link(s), '
                f'expected {want}: {urls or "none"}')
        elif want and TERM not in urls[0]:
            problems.append(f'{v}/ ships a syllabus link that is not {TERM}: {urls[0]}')
        if PLACEHOLDER in html:
            problems.append(
                f'{v}/ contains the literal {PLACEHOLDER}; a pending link must be '
                f'omitted, never rendered')

        for o in MODALITIES:
            if o != v and f'{o.upper()}_ONLY' in html:
                problems.append(
                    f'{v}/ still contains a {o.upper()}_ONLY sentinel, so it is '
                    f'carrying the {o} modality\'s content')
    return problems


def main():
    problems, warnings, source_urls = check_source()
    problems += check_built(source_urls)
    for w in warnings:
        print(f'check_syllabus_links: WARNING - {w}')
    if problems:
        print('check_syllabus_links: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    live = sum(1 for v in MODALITIES if source_urls.get(v) not in (None, PLACEHOLDER))
    print(f'check_syllabus_links: PASS ({TERM}; {live}/{len(MODALITIES)} modality '
          f'links live, each in exactly one tree)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
