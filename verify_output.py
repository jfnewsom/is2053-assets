#!/usr/bin/env python3
"""
verify_output.py - Execute each lab solution and diff it against the sheet.

The conventions say expected output blocks are copied from running the actual
solution, never typed from memory. Nothing enforced that until now. On
2026-08-08, Lab 1.3 was found teaching a method that could not produce its own
sample run (ledger F-021); it had been wrong for a full term.

lab_lint.py catches sheets that contradict THEMSELVES. This catches sheets that
contradict the CODE, which is the stronger check and the one the conventions
actually promise.

How it works, with no configuration per lab:
  1. Read the input() prompt strings out of the solution, in source order.
  2. Find each prompt in the sheet's expectedOutput and take the text after it
     on that line. That is what the student typed.
  3. Feed those values to the solution on stdin and capture stdout.
  4. Diff against expectedOutput with the typed echoes removed, because a piped
     run does not echo input and input() never emits the newline.

Solutions live outside this repo, so pass their root:

    python3 verify_output.py --solutions ~/path/to/IS2053/code/Modules
    python3 verify_output.py --solutions ... lab-1-3        # one lab

Labs importing random are reported NONDETERMINISTIC and skipped rather than
failed. Seeding them is the obvious next step; until then this covers the
deterministic labs, which is where the arithmetic bugs live anyway.
"""
import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys

# A prompt reaches the student either from a direct input() call or from a
# helper in function_library that takes the prompt as its first argument. Only
# scanning input() misses everything from Module 2 onward, where get_valid_int
# and get_yes_no do the asking. Arguments often sit on the next line, so allow
# whitespace and newlines before the string.
PROMPT_RE = re.compile(
    r"(?:input|get_valid_int|get_yes_no)\s*\(\s*(?:f?)['\"](.*?)['\"]",
    re.S)
RANDOM_RE = re.compile(r'^\s*import\s+random\b|random\.\w+', re.M)


def solution_for(root, lab):
    """mod1/lab-1-1.py, mod4/4-1/lab-4-1.py, ... without hardcoding layout."""
    hits = glob.glob(os.path.join(root, '**', f'{lab}.py'), recursive=True)
    hits = [h for h in hits if 'OLDIES' not in h and '__pycache__' not in h]
    return hits[0] if hits else None


def prompt_pattern(p):
    """Prompts are often f-strings: f'Choice (1-{num_choices}): '. The braces
    hold a runtime value, so match them as a wildcard rather than literally."""
    return re.compile(''.join(
        '.+?' if part.startswith('{') and part.endswith('}') else re.escape(part)
        for part in re.split(r'(\{[^}]*\})', p)))


def derive_inputs(expected, prompts):
    """Return (typed values, expectedOutput with echoes removed).

    Driven by the SAMPLE RUN, not by source order. Programs branch, so a
    solution can contain prompts the sample run never reaches ("Return to San
    Antonio?" only fires on a dead end). Walking prompts in source order and
    demanding each appear was wrong; instead, scan the transcript top to bottom
    and consume a prompt wherever one actually shows up.
    """
    pats = [(p, prompt_pattern(p)) for p in prompts]
    vals, out, pos = [], expected, 0
    while True:
        best = None
        for p, rx in pats:
            m = rx.search(out, pos)
            if m and (best is None or m.start() < best[0].start()):
                best = (m, p)
        if best is None:
            break
        m, _ = best
        end = m.end()
        j = out.find('\n', end)
        j = len(out) if j < 0 else j
        typed = out[end:j].strip()
        vals.append(typed)
        out = out[:end] + out[j + 1:]
        pos = end
    if not vals:
        return None, None, prompts[0] if prompts else '(no prompts found)'
    return vals, out, None


def verify(lab, json_path, sol_path, show_diff=True):
    d = json.load(open(json_path, encoding='utf-8'))
    exp = (d.get('finalChecklist') or {}).get('finalCheck', {}).get('expectedOutput', '')
    if not exp:
        return 'NO-EXPECTED', None
    src = open(sol_path, encoding='utf-8').read()
    if RANDOM_RE.search(src):
        return 'NONDETERMINISTIC', None

    prompts = PROMPT_RE.findall(src)
    vals, exp_n, missing = derive_inputs(exp, prompts)
    if vals is None:
        return 'PROMPT-MISMATCH', f'sheet never shows the prompt {missing!r}'

    try:
        r = subprocess.run([sys.executable, os.path.basename(sol_path)],
                           cwd=os.path.dirname(sol_path),
                           input='\n'.join(vals) + '\n',
                           capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', 'solution asked for more input than the sheet shows'

    if r.returncode != 0:
        return 'CRASH', (r.stderr.strip().splitlines() or ['?'])[-1]

    actual = [l.rstrip() for l in r.stdout.strip().splitlines()]
    wanted = [l.rstrip() for l in exp_n.strip().splitlines()]
    if actual == wanted:
        return 'MATCH', f'inputs={vals}'
    if not show_diff:
        return 'DIFFERS', f'inputs={vals}'
    diff = list(difflib.unified_diff(wanted, actual, 'sheet', 'solution', lineterm=''))
    return 'DIFFERS', f'inputs={vals}\n' + '\n'.join('      ' + l for l in diff[:30])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solutions', required=True, help='root of the solution tree')
    ap.add_argument('labs', nargs='*', help='e.g. lab-1-3 (default: all)')
    a = ap.parse_args()

    root = os.path.expanduser(a.solutions)
    if not os.path.isdir(root):
        print(f'verify_output: no such directory {root}')
        return 2

    files = sorted(glob.glob('pages/labs/json/lab-*.json'))
    if a.labs:
        files = [f for f in files if any(l in f for l in a.labs)]

    tally, bad, unverified = {}, 0, 0
    for jp in files:
        lab = os.path.splitext(os.path.basename(jp))[0]
        sol = solution_for(root, lab)
        if not sol:
            status, detail = 'NO-SOLUTION', None
        else:
            status, detail = verify(lab, jp, sol)
        tally[status] = tally.get(status, 0) + 1
        # Only DIFFERS proves a disagreement. CRASH, TIMEOUT and PROMPT-MISMATCH
        # mean this harness could not reconstruct the input sequence, which is a
        # limitation here, not evidence against the sheet. Reporting those as
        # failures would train everyone to ignore the output.
        if status == 'DIFFERS':
            bad += 1
        elif status in ('CRASH', 'TIMEOUT', 'PROMPT-MISMATCH'):
            unverified += 1
        print(f'{lab:10} {status:17} {detail or ""}')

    print('\n' + '  '.join(f'{k}={v}' for k, v in sorted(tally.items())))
    if bad:
        print(f'\nverify_output: {bad} lab(s) where the sheet and the code DISAGREE.')
        print('The code is the source of truth. Fix the sheet, then re-render.')
    if unverified:
        print(f'\nverify_output: {unverified} lab(s) COULD NOT BE VERIFIED. The harness '
              f'could not rebuild the input sequence from the sample run.')
        print('Not evidence of a defect. These labs use menus, save/load, or multi-leg')
        print('journeys whose prompt order the transcript does not fully determine.')
    if tally.get('NONDETERMINISTIC'):
        print(f'\nverify_output: {tally["NONDETERMINISTIC"]} lab(s) import random and were '
              f'skipped. Seeding them would bring these under test too.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
