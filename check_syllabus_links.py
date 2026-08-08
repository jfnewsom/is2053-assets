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

PLACEHOLDER. A variant whose URL is still SYLLABUS_URL_PENDING fails the build,
so a missing document cannot quietly ship as a broken link.

    python3 check_syllabus_links.py
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages' / 'support' / 'json' / 'start-here.json'

TERM = 'Fall-2026'
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
    found, problems = {}, []

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
                problems.append(
                    f'the {v} syllabus URL is still {PLACEHOLDER} (ledger L-025). '
                    f'Paste the real Simple Syllabus doc URL into start-here.json.')
            elif TERM not in url:
                problems.append(
                    f'the {v} syllabus URL does not name {TERM}: {url}')
    for v in sorted(set(found) - set(MODALITIES)):
        problems.append(f'syllabus link tagged with unknown modality "{v}"')
    return problems


def check_built():
    problems = []
    for v in sorted(MODALITIES):
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
        if len(urls) != 1:
            problems.append(
                f'{v}/support/start-here.html has {len(urls)} syllabus link(s), '
                f'expected exactly 1: {urls or "none"}')
        elif urls[0] != PLACEHOLDER and TERM not in urls[0]:
            # A pending URL is already reported once against the source.
            problems.append(f'{v}/ ships a syllabus link that is not {TERM}: {urls[0]}')

        for o in MODALITIES:
            if o != v and f'{o.upper()}_ONLY' in html:
                problems.append(
                    f'{v}/ still contains a {o.upper()}_ONLY sentinel, so it is '
                    f'carrying the {o} modality\'s content')
    return problems


def main():
    problems = check_source() + check_built()
    if problems:
        print('check_syllabus_links: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    print(f'check_syllabus_links: PASS ({TERM}; one correct link per modality tree)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
