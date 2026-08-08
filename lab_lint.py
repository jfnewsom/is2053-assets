#!/usr/bin/env python3
"""
lab_lint.py - Consistency checks across the lab assignment sheets.

Written 2026-08-08 after F-021, where Lab 1.3's Checkpoint 2 taught a method
that could not produce the sheet's own expected output. Nothing compared the
prose to the sample run, so the defect survived a full term and a student's
question about it.

This does NOT check whether a lab is pedagogically good. It checks whether a
lab contradicts ITSELF. Every finding is a suspicion for a human to confirm,
not a verdict. Findings are ranked:

  HIGH    the file states two things that cannot both be true
  REVIEW  a pattern that was a real bug once; worth eyes

Checks:
  1. ROLL MATH      "You rolled N ... gives you M miles" must satisfy M = N * 10
  2. MENU vs CONST  menu distances in the sample run must match namedConstants
  3. FRAMING        the architecture diagram and the checkpoint prose must
                    compare the same variable the same way (the F-021 bug)
  4. STATUS COVER   every status a branch sets must be handled by the summary
  5. DUP ROWS       identical rows inside one table
  6. REACHABILITY   a test case claiming a destination is reached when the
                    stated roll cannot cover the distance

Usage:  python3 lab_lint.py [lab-1-3]
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

MILES_PER_ROLL = 10


def strip_html(s):
    return re.sub(r'<[^>]+>', '', s or '')


def walk_strings(o, path='', out=None):
    if out is None:
        out = []
    if isinstance(o, dict):
        for k, v in o.items():
            walk_strings(v, f'{path}.{k}', out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk_strings(v, f'{path}[{i}]', out)
    elif isinstance(o, str):
        out.append((path, o))
    return out


def instructional_text(d):
    """Checkpoint prose that TELLS a student what to write.

    Excludes tips_and_pitfalls sections. Those exist to name the wrong way of
    doing something, so they legitimately contain code a student must not copy.
    Scanning them for correctness produces false positives on well-written
    warnings, which is the opposite of useful.
    """
    out = []
    for cp in d.get('checkpoints', []):
        label = None
        for b in cp.get('content', []):
            if b.get('type') == 'h3':
                label = b.get('label')
                continue
            if label == 'tips_and_pitfalls':
                continue
            out.extend(s for _, s in walk_strings(b))
    return out


def constants(d, add=None):
    """name -> int value.

    Two independent sources, which is itself a check:
      overview.namedConstants  {name, description} with the value in prose,
                               e.g. "Distance SA to Houston (200 miles)"
      beforeYouBegin.architecture   NAME = VALUE
    If both state a value and they disagree, that is a defect.
    """
    from_desc, from_arch = {}, {}

    for c in (d.get('overview', {}).get('namedConstants') or []):
        if isinstance(c, dict):
            name = c.get('name', '')
            desc = strip_html(c.get('description', ''))
        else:
            text = strip_html(c)
            m = re.match(r'\s*([A-Z][A-Z0-9_]{2,})', text)
            name, desc = (m.group(1) if m else ''), text
        if not re.fullmatch(r'[A-Z][A-Z0-9_]{2,}', name or ''):
            continue
        # The value is always the FIRST parenthesis: "(150 miles)", "(10)", "(30)".
        # Do NOT fall back to any "<n> miles" in the prose: descriptions carry
        # illustrative examples ("A roll of 15 becomes 150 miles") that a loose
        # pattern reads as the constant's value.
        m = re.search(r'\((\d+)[^)]*\)', desc)
        if m:
            from_desc[name] = int(m.group(1))

    arch = d.get('beforeYouBegin', {}).get('architecture', '')
    for m in re.finditer(r'^\s*([A-Z][A-Z0-9_]{2,})\s*=\s*(\d+)', arch, re.M):
        from_arch[m.group(1)] = int(m.group(2))

    if add:
        for name in set(from_desc) & set(from_arch):
            if from_desc[name] != from_arch[name]:
                add('HIGH', f'{name} is {from_arch[name]} in the architecture block '
                            f'but described as {from_desc[name]} miles in namedConstants',
                    'namedConstants vs architecture')

    vals = dict(from_desc)
    vals.update(from_arch)
    return vals


def check_roll_math(d, add):
    for path, s in walk_strings(d):
        for m in re.finditer(r'[Yy]ou rolled (?:a )?(\d+)[^.\n]{0,40}?gives you (\d+) miles', strip_html(s)):
            roll, miles = int(m.group(1)), int(m.group(2))
            if miles != roll * MILES_PER_ROLL:
                add('HIGH', f'roll {roll} shown as {miles} miles '
                            f'(expected {roll * MILES_PER_ROLL})', path)


def check_menu_vs_constants(d, add, consts):
    fc = (d.get('finalChecklist') or {}).get('finalCheck') or {}
    out = fc.get('expectedOutput', '')
    for m in re.finditer(r'^\s*\d[.)]\s*([A-Z][A-Za-z ]+?)\s*[-–]\s*(\d+) miles', out, re.M):
        city, miles = m.group(1).strip(), int(m.group(2))
        key = city.upper().split()[0]
        hits = {k: v for k, v in consts.items() if key in k}
        for k, v in hits.items():
            if v != miles:
                add('HIGH', f'sample run lists {city} at {miles} miles '
                            f'but {k} = {v}', 'finalCheck.expectedOutput')


def check_framing(d, add):
    """The F-021 signature: architecture compares VAR to 0, prose compares VAR
    to a constant (or the reverse). One of them is wrong."""
    arch = d.get('beforeYouBegin', {}).get('architecture', '')
    prose = ' '.join(strip_html(s) for s in instructional_text(d))
    pat = re.compile(r'([a-z_][a-z0-9_]{3,})\s*(?:&gt;=|>=)\s*([A-Z][A-Z0-9_]{2,}|0)\b')
    a = defaultdict(set)
    for m in pat.finditer(arch):
        a[m.group(1)].add(m.group(2))
    p = defaultdict(set)
    for m in pat.finditer(prose):
        p[m.group(1)].add(m.group(2))
    for var in set(a) & set(p):
        extra = p[var] - a[var]
        if not extra:
            continue
        # Complete disagreement: the diagram and the prose share no common form.
        if not (a[var] & p[var]):
            add('HIGH', f'architecture compares {var} to {sorted(a[var])} '
                        f'but checkpoint prose compares it to {sorted(p[var])}',
                'architecture vs checkpoints')
        else:
            # Partial: the prose uses forms the diagram never shows. This is what
            # a half-migrated sheet looks like, and it is how F-021 survived.
            # Requiring full disjointness missed it, so flag the mixture too.
            add('REVIEW', f'prose compares {var} to {sorted(extra)}, which the '
                          f'architecture diagram never does (diagram uses '
                          f'{sorted(a[var])}). One of them is stale',
                'architecture vs checkpoints')


def check_status_coverage(d, add):
    cps = d.get('checkpoints', [])
    if not cps:
        return
    allcp = ' '.join(strip_html(s) for _, s in walk_strings(cps))
    lit = re.compile(r"'([A-Z]{4,})'")
    # Only literals actually bound to a status variable. Matching every quoted
    # uppercase word swept in coin-flip results ('HEADS'), booleans ('TRUE'),
    # and prose, which buried the signal in noise.
    set_in = set(re.findall(r"status\w*\s*(?:=|==|to)\s*'([A-Z]{4,})'", allcp, re.I))
    set_in |= set(re.findall(r"status\s+to\s+'([A-Z]{4,})'", allcp, re.I))
    last = ' '.join(strip_html(s) for _, s in walk_strings(cps[-1]))
    # The final checkpoint names a status either as a quoted literal
    # ("status == 'STOPPED'") or bare in prose ("Status: STOPPED"). Only
    # checking the quoted form reports handled statuses as missing.
    handled = set(lit.findall(last)) | set(re.findall(r'\b([A-Z]{4,})\b', last))
    if not handled:
        return
    missing = {s for s in set_in - handled if s not in ('DEBUG', 'TESTING', 'NEW', 'REPLACED')}
    if missing:
        add('REVIEW', f'status value(s) {sorted(missing)} are set in earlier '
                      f'checkpoints but not named in the final checkpoint. '
                      f'Fine if an else branch catches them; a defect if not',
            'status coverage')


def check_dup_rows(d, add):
    def scan(o, path=''):
        if isinstance(o, dict):
            if o.get('type') == 'table' and isinstance(o.get('rows'), list):
                seen, dups = set(), []
                for r in o['rows']:
                    k = json.dumps(r)
                    if k in seen:
                        dups.append(strip_html(r[0]) if r else k)
                    seen.add(k)
                if dups:
                    add('REVIEW', f'duplicate table row(s): {dups}', path)
            for k, v in o.items():
                scan(v, f'{path}.{k}')
        elif isinstance(o, list):
            for i, v in enumerate(o):
                scan(v, f'{path}[{i}]')
    scan(d)


def check_reachability(d, add, consts):
    """Test items of the form 'Roll N, choice C: ... reached X'."""
    for path, s in walk_strings(d.get('checkpoints', [])):
        t = strip_html(s)
        m = re.search(r'Roll (\d+)\b', t)
        if not m:
            continue
        miles = int(m.group(1)) * MILES_PER_ROLL
        for name, val in consts.items():
            city = name.split('_')[-1].capitalize()
            # Negation matters. "Did not reach Houston" is a correct statement
            # about an unreachable city, not a claim that it was reached.
            claim = re.search(
                rf'(?<!not )(?<!n\'t )(?<!never )reach(?:ed|es)?\s+{city}', t, re.I)
            negated = re.search(
                rf'(?:did not|didn\'t|does not|doesn\'t|never|could not|couldn\'t|short of|out of reach)'
                rf'[^.]{{0,40}}{city}', t, re.I)
            if claim and not negated and miles < val:
                add('HIGH', f'claims {city} reached on roll {m.group(1)} '
                            f'({miles} miles) but {name} = {val}', path)


def lint(path):
    d = json.load(open(path, encoding='utf-8'))
    findings = []

    def add(sev, msg, where):
        findings.append((sev, msg, where))

    consts = constants(d, add)
    check_roll_math(d, add)
    check_menu_vs_constants(d, add, consts)
    check_framing(d, add)
    check_status_coverage(d, add)
    check_dup_rows(d, add)
    check_reachability(d, add, consts)
    return consts, findings


def main():
    targets = sys.argv[1:]
    files = sorted(glob.glob('pages/labs/json/lab-*.json'))
    if targets:
        files = [f for f in files if any(t in f for t in targets)]

    total = high = 0
    for f in files:
        consts, findings = lint(f)
        name = os.path.basename(f)
        if not findings:
            print(f'{name:16} clean   ({len(consts)} constants)')
            continue
        print(f'{name:16} {len(findings)} finding(s)')
        for sev, msg, where in findings:
            print(f'    [{sev:6}] {msg}')
            print(f'             at {where}')
            total += 1
            high += (sev == 'HIGH')
    print(f'\n{total} finding(s), {high} HIGH across {len(files)} labs')
    return 0


if __name__ == '__main__':
    sys.exit(main())
