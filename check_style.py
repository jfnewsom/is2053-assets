#!/usr/bin/env python3
"""
check_style.py - Style guard for student-facing course content.

Enforces the no-em-dash rule (and other banned constructions). Ratchet design:
each baseline below is the known debt; the check FAILS if a count ever rises
above it. Lower a baseline as the debt is paid down (voice pass, ledger L-013).
At zero, each becomes a zero-tolerance gate.

Two ratchets, because they answer different questions:

  SOURCE  - em-dashes in pages/**/json/*.json. This is where authors type, so
            this is the ratchet that stops NEW debt at the point of entry.
  VISIBLE - em-dashes in rendered pages/**/*.html with HTML comments stripped.
            This is what a student actually sees. It excludes renderer
            docstrings and HTML comment banners, which inflate any raw count
            and are invisible on the page.

Known gap (ledger L-016): pages/support/reading-ch*.html are hand-maintained
HTML with no JSON source, so the SOURCE ratchet cannot see them. The VISIBLE
ratchet does cover them. Closing L-016 (a reading.json plus a renderer) also
closes this gap.

Run alongside the renderers, AFTER them so VISIBLE reflects current output:
    python3 render_*.py && python3 check_style.py
"""
import glob
import io
import re
import sys

BASELINE_SOURCE = 703    # pages/**/json/*.json, U+2014 plus &mdash;   (2026-08-08)
BASELINE_VISIBLE = 473   # rendered pages/**/*.html, comments stripped (2026-08-08)

BANNED_ZERO_TOLERANCE = [
    (re.compile(r"But here's the (truth|thing)", re.I), "AI-tell transition"),
    (re.compile(r"And honestly\?", re.I), "AI-tell transition"),
    (re.compile(r"(?:it'?s|is|are|was|you'?re)\s+not\s+just\b", re.I), "AI-tell: 'not just X, it's Y'"),
    (re.compile(r"that'?s\s+not\s+[^.,;]{2,40}[,.]\s*that'?s\b", re.I), "AI-tell: 'that's not X, that's Y'"),
    (re.compile(r"\bCalendy\b"), "product name typo (Calendly)"),
    (re.compile(r"\bUTSA\b"), "use 'UT San Antonio' (the credential 'myUTSA ID' is fine)"),
    (re.compile(r"weekly Zoom|course Zoom|Zoom session", re.I),
     "office-hours wording: the event is office hours, Zoom is only the room"),
    (re.compile(r"[Ss]essions are\s+(?:<[^>]+>\s*)?recorded"), "office hours are not recorded"),
]

COMMENT_RE = re.compile(r'<!--.*?-->', re.S)


def read(path):
    return io.open(path, encoding='utf-8', errors='ignore').read()


def count_source():
    total, hits = 0, []
    for f in sorted(glob.glob('pages/**/json/*.json', recursive=True)):
        text = read(f)
        total += text.count('—') + text.count('&mdash;')
        for pat, why in BANNED_ZERO_TOLERANCE:
            for m in pat.finditer(text):
                hits.append((f, m.group(0), why))
    return total, hits


def count_visible():
    total, per = 0, {}
    for f in sorted(glob.glob('pages/**/*.html', recursive=True)):
        n = COMMENT_RE.sub('', read(f)).count('—')
        if n:
            per[f] = n
            total += n
    return total, per


def ratchet(label, actual, baseline, ok):
    if actual > baseline:
        print(f'check_style: FAIL - {label} rose to {actual}, above baseline {baseline}. '
              f'New banned punctuation was introduced.')
        return False
    if actual < baseline:
        print(f'check_style: {label} {actual} (baseline {baseline}). '
              f'Debt reduced; lower the baseline to {actual} to lock it in.')
    else:
        print(f'check_style: {label} {actual} (baseline {baseline}). Holding.')
    return ok


def main():
    source, hits = count_source()
    visible, per = count_visible()

    ok = True
    ok = ratchet('SOURCE  em-dashes', source, BASELINE_SOURCE, ok)
    ok = ratchet('VISIBLE em-dashes', visible, BASELINE_VISIBLE, ok)

    if hits:
        ok = False
        print(f'check_style: FAIL - {len(hits)} zero-tolerance pattern(s) found:')
        for f, s, why in hits[:25]:
            print(f'  {f}: "{s}" ({why})')
        if len(hits) > 25:
            print(f'  ... and {len(hits) - 25} more')

    if per and '--top' in sys.argv:
        print('\nworst VISIBLE offenders:')
        for f, n in sorted(per.items(), key=lambda kv: -kv[1])[:12]:
            print(f'  {n:4}  {f}')

    print('check_style: PASS' if ok else 'check_style: FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
