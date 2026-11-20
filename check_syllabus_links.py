#!/usr/bin/env python3
"""
check_syllabus_links.py - Every syllabus link names the current term, and every
place that lists the syllabi lists the same ones.

STALE TERM. On 2026-08-08 the Start Here page was still sending every student
to the Summer 2026 Simple Syllabus doc (ledger L-025). It is the first external
link a student clicks and nothing verified it. A syllabus URL naming a term
other than the current one fails, wherever it appears.

ONE SITE, BOTH SYLLABI (Nov 20, 2026). From Spring 2027 there is one version of
the site for every section, served from pages/. Online and in-person sections
still have separate Simple Syllabus documents, so Start Here, the Home page's
Quick Links, and the nav menu each list BOTH, labeled. This checks that the
three agree: the same set of URLs in each, so a term update that reaches one
file and misses another fails here instead of on the first day of class. The
old per-modality trees and their ONL_ONLY / F2F_ONLY sentinels are retired; a
sentinel that reappears in a built page fails too, because nothing strips it
anymore and the page would show both copies.

    python3 check_syllabus_links.py
"""
import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / 'pages' / 'support' / 'json' / 'start-here.json'

TERM = 'Fall-2026'
PLACEHOLDER = 'SYLLABUS_URL_PENDING'
SYLLABUS = re.compile(r'https?://[^"\'\s\\]*simplesyllabus[^"\'\s\\]*')  # \\ stops at a JSON-escaped quote
# The places that list the syllabi. Each must hold the same set of URLs.
LISTS = {
    'start-here.json': REPO / 'pages' / 'support' / 'json' / 'start-here.json',
    'home.json': REPO / 'pages' / 'support' / 'json' / 'home.json',
    'nav.js': REPO / 'nav.js',
}
EXPECTED = 2   # one online, one in person


def check_lists():
    problems, sets = [], {}
    for name, path in LISTS.items():
        text = path.read_text(encoding='utf-8')
        sets[name] = set(SYLLABUS.findall(text))
        if PLACEHOLDER in text:
            sets[name].add(PLACEHOLDER)
    first = sets['start-here.json']
    if len(first) != EXPECTED:
        problems.append(f'start-here.json lists {len(first)} syllabus link(s), '
                        f'expected {EXPECTED} (online and in person): {sorted(first)}')
    for name, urls in sets.items():
        if urls != first:
            problems.append(f'{name} lists different syllabus links than start-here.json: '
                            f'missing {sorted(first - urls)}, extra {sorted(urls - first)}')
    return problems, first


def check_built(source_urls):
    """The built Start Here shows every syllabus link, and no retired sentinel
    survives anywhere in the built site."""
    problems = []
    page = REPO / 'pages' / 'support' / 'start-here.html'
    if not page.is_file():
        return ['pages/support/start-here.html not built; run ./render_all.sh']
    html = page.read_text(encoding='utf-8')
    for url in sorted(source_urls - {PLACEHOLDER}):
        if url not in html:
            problems.append(f'pages/support/start-here.html is missing the syllabus link {url}')
    if PLACEHOLDER in html:
        problems.append(f'pages/support/start-here.html contains the literal {PLACEHOLDER}; '
                        f'a pending link must be omitted, never rendered')
    for f in sorted(glob.glob(str(REPO / 'pages' / '**' / '*.html'), recursive=True)):
        if '_to_delete' in f:
            continue
        if re.search(r'(ONL|F2F)_ONLY:START', Path(f).read_text(encoding='utf-8')):
            problems.append(f'{Path(f).relative_to(REPO)} still has a retired ONL_ONLY/F2F_ONLY '
                            f'block; nothing strips it now, so students would see both copies')
    return problems


def check_every_page():
    """Any syllabus URL anywhere, not just the one on Start Here.

    Added 2026-08-09 (F-047). Everything above this function reads
    start-here.json, because that is where L-025 was found. Meanwhile the HOME
    page linked the Summer 2026 doc for a full day of green builds, since it was
    never in scope. A guard scoped to the file that taught you the invariant is
    not guarding the invariant.

    This sweep is deliberately dumb and total: every source and every built
    page, one rule. A Simple Syllabus URL that does not name the current term
    fails, wherever it lives.
    """
    problems = []
    seen = set()
    # nav.js is in this list because leaving it out is exactly the mistake this
    # sweep was written to stop repeating. The first cut globbed pages/ and the
    # built trees, and nav.js is at the repo root and is neither .html nor
    # .json, so the Summer 2026 syllabus link in the LEFT NAV OF EVERY PAGE
    # survived a green run of this very check on 2026-08-09. Scope a guard to
    # the invariant, not to the shape of the files you happened to think of.
    for pat in ('pages/**/*.json', 'pages/**/*.html',
                '*.js', 'pages/**/*.js'):
        seen |= set(glob.glob(pat, recursive=True))
    for f in sorted(seen):
        if '_to_delete' in f:
            continue
        for url in set(SYLLABUS.findall(Path(f).read_text(encoding='utf-8'))):
            if TERM not in url:
                problems.append(
                    f'{f} links a syllabus URL that does not name {TERM}: {url}')
    return problems, len(seen)


def main():
    problems, source_urls = check_lists()
    problems += check_built(source_urls)
    sweep_problems, swept = check_every_page()
    problems += sweep_problems
    if problems:
        print('check_syllabus_links: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    live = len(source_urls - {PLACEHOLDER})
    print(f'check_syllabus_links: PASS ({TERM}; {live} syllabus links, the same in '
          f'Start Here, Home, and the nav; {swept} file(s) swept for stale-term '
          f'syllabus URLs)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
