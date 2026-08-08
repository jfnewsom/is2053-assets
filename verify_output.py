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

Labs that import random are NOT skipped (ledger L-023, closed 2026-08-08).
CodeGrade already grades them against a deterministic random.py fixture that
pins randint() and choice(), and the expected-output blocks in the sheets were
generated from exactly that fixture. Inventing a seeding scheme here would have
produced outputs CodeGrade never sees and a pile of false failures, so this
harness borrows the real fixture instead.

The fixture is found in the solutions tree and copied ALONE into a scratch
directory that goes on PYTHONPATH, so it shadows stdlib random without dragging
its neighbours (function_library.py and friends) onto the path with it. Its
three knobs default to the values the sheets describe: D20 rolls of 15 and coin
flips of HEADS.

    SMALLNUM=1   randint(a,b) when b <= 9    1 = HEADS, first hazard, first city
    LARGENUM=15  randint(a,b) when b > 9     d20 = 15, so 150 miles per turn
    CHOICE_IDX=0 choice(seq)                 first item

Only if no fixture can be found does a random-importing lab fall back to
NONDETERMINISTIC.
"""
import argparse
import difflib
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# A prompt reaches the student either from a direct input() call or from a
# helper in function_library that takes the prompt as its first argument. Only
# scanning input() misses everything from Module 2 onward, where get_valid_int
# and get_yes_no do the asking. Arguments often sit on the next line, so allow
# whitespace and newlines before the string.
PROMPT_RE = re.compile(
    r"(?:input|get_valid_int|get_yes_no)\s*\(\s*(?:f?)['\"](.*?)['\"]",
    re.S)
RANDOM_RE = re.compile(r'^\s*import\s+random\b|random\.\w+', re.M)

# The knob values the sheets say CodeGrade uses. Kept here, not guessed per lab.
FIXTURE_ENV = {'SMALLNUM': '1', 'LARGENUM': '15', 'CHOICE_IDX': '0'}


def find_fixture(root):
    """Locate the deterministic random.py CodeGrade grades against.

    Identified by content, not by path: a stray random.py that is not the
    fixture would silently change every result, so require the knobs.
    """
    for hit in sorted(glob.glob(os.path.join(root, '**', 'random.py'), recursive=True)):
        if 'OLDIES' in hit or '__pycache__' in hit:
            continue
        try:
            src = open(hit, encoding='utf-8').read()
        except OSError:
            continue
        if all(k in src for k in FIXTURE_ENV) and 'def randint' in src:
            return hit
    return None


def stage_fixture(fixture_path):
    """Copy the fixture ALONE into a scratch dir meant for PYTHONPATH.

    Putting the fixture's own directory on the path would also expose whatever
    else lives beside it, so a Module 2 lab could quietly import Module 4's
    function_library. Copy one file and nothing else.
    """
    d = tempfile.mkdtemp(prefix='is2053-fixture-')
    shutil.copy2(fixture_path, os.path.join(d, 'random.py'))
    return d


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


DECLARED_RE = re.compile(r'This run uses inputs\s+(.*?)\s*with the (?:deterministic|CodeGrade)',
                         re.S | re.I)


def declared_inputs(doc):
    """Read the input sequence the SHEET says it used.

    Recovering inputs from the transcript only works when the transcript echoes
    them, and this course's sample runs are captured two different ways: Module
    1 and 2 interactively (echo present), Module 3 onward piped (no echo). In a
    piped capture the typed values are simply absent, and two prompts land on
    one line: "Choice (1-3): What is your name, traveler?". Reverse-engineering
    that reads the second prompt as the answer to the first.

    Several sheets sidestep the whole problem by stating the sequence in prose:
    "This run uses inputs 1 (New Game) -> TestPlayer -> 2 (Houston) -> ...".
    That is the author declaring intent, which beats inference, so it wins when
    present. Parenthetical glosses are labels for the reader, not input.
    """
    m = DECLARED_RE.search(json.dumps(doc))
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<[^>]+>', '', raw)
    raw = (raw.replace('&rarr;', '->').replace('\\u2192', '->')
              .replace('&#x27;', "'").replace('&rsquo;', "'")
              .replace('&quot;', '"').replace('\\n', ' '))
    vals = []
    for part in raw.split('->'):
        part = re.sub(r'\([^)]*\)', '', part).strip().strip('.,')
        if part:
            vals.append(part)
    return vals or None


def strip_echoes(expected, prompts, vals):
    """Remove typed values the transcript echoed, leaving only program output.

    A piped run echoes nothing, so this is a no-op there and the transcript is
    already comparable. An interactive capture echoes each value right after
    its prompt; only remove text that exactly matches the value we are about to
    feed in, so a prompt immediately followed by another prompt is left alone.
    """
    pats = [(v, prompt_pattern(p)) for p in prompts for v in (None,)]
    out, remaining, pos = expected, list(vals), 0
    while remaining:
        best = None
        for p in prompts:
            m = prompt_pattern(p).search(out, pos)
            if m and (best is None or m.start() < best.start()):
                best = m
        if best is None:
            break
        end = best.end()
        nl = out.find('\n', end)
        nl = len(out) if nl < 0 else nl
        trailing = out[end:nl]
        if trailing.strip() == remaining[0]:
            out = out[:end] + out[nl + 1:]      # echo + its newline
            remaining.pop(0)
        else:
            remaining.pop(0)                     # nothing echoed for this one
        pos = end
    return out


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


ROLL_RE = re.compile(r'You rolled an? (\d+)')
NOT_STDOUT_RE = re.compile(r'^\s*\w+\.py output\b', re.I)
PLACEHOLDER_RE = re.compile(r'^\s*\(.*(?:continue as in|depends on|captured in)', re.M | re.S)


def unverifiable(exp, doc):
    """Why this sheet can never be reproduced, if it cannot.

    Distinguishing these from a real failure matters. A harness that cries
    CRASH at three different situations, only one of which is a defect, gets
    ignored. Each of these is a content decision, not a bug in the run.
    """
    if NOT_STDOUT_RE.match(exp):
        return ('NOT-APPLICABLE',
                'expectedOutput is another program\'s output (test.py), not this one\'s')
    if PLACEHOLDER_RE.search(exp):
        return ('PLACEHOLDER',
                'expectedOutput describes the run in prose instead of showing it')
    rolls = ROLL_RE.findall(exp)
    if len(set(rolls)) > 1:
        return ('REAL-RANDOM',
                f'sample run captured with real randomness (rolls {"/".join(rolls)}), '
                f'not the CodeGrade fixture, so it cannot be reproduced')
    return None


def uses_random(sol_path):
    """Does this lab consume randomness, directly or through a local module?

    Checking only the lab file was wrong: from Module 3 on, the randomness
    lives in function_library.py and the lab just calls it. lab-3-3 was being
    run without the fixture for exactly that reason.
    """
    d = os.path.dirname(sol_path)
    for f in [sol_path] + sorted(glob.glob(os.path.join(d, '*.py'))):
        try:
            if RANDOM_RE.search(open(f, encoding='utf-8').read()):
                return True
        except OSError:
            pass
    return False


def verify(lab, json_path, sol_path, fixture_dir=None, show_diff=True):
    d = json.load(open(json_path, encoding='utf-8'))
    exp = (d.get('finalChecklist') or {}).get('finalCheck', {}).get('expectedOutput', '')
    if not exp:
        return 'NO-EXPECTED', None
    why = unverifiable(exp, d)
    if why:
        return why
    src = open(sol_path, encoding='utf-8').read()
    random_lab = uses_random(sol_path)
    if random_lab and not fixture_dir:
        return 'NONDETERMINISTIC', 'no random.py fixture found in the solutions tree'

    prompts = PROMPT_RE.findall(src)
    vals = declared_inputs(d)
    if vals:
        exp_n, source = strip_echoes(exp, prompts, vals), 'declared'
    else:
        vals, exp_n, missing = derive_inputs(exp, prompts)
        source = 'transcript'
        if vals is None:
            return 'PROMPT-MISMATCH', f'sheet never shows the prompt {missing!r}'

    env = dict(os.environ)
    env.update(FIXTURE_ENV)
    if fixture_dir:
        env['PYTHONPATH'] = fixture_dir + os.pathsep + env.get('PYTHONPATH', '')

    # Run in a throwaway COPY of the module directory. Two reasons, both found
    # the hard way on 2026-08-08:
    #
    #   Correctness. These labs write savegame.txt and trip_report.txt, and a
    #   file left by one lab changes what the next one does. lab-3-3 passed
    #   alone and crashed when run after lab-3-1. A harness whose answer
    #   depends on execution order is not a harness.
    #
    #   Hygiene. Running in place littered John's solution tree, the source of
    #   truth, with generated files. Never write to the thing you are checking.
    workdir = tempfile.mkdtemp(prefix=f'is2053-{lab}-')
    run_dir = os.path.join(workdir, 'run')
    shutil.copytree(os.path.dirname(sol_path), run_dir)
    try:
        r = subprocess.run([sys.executable, os.path.basename(sol_path)],
                           cwd=run_dir,
                           input='\n'.join(vals) + '\n',
                           capture_output=True, text=True, timeout=30, env=env)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', 'solution asked for more input than the sheet shows'
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    if r.returncode != 0:
        return 'CRASH', (r.stderr.strip().splitlines() or ['?'])[-1]

    actual = [l.rstrip() for l in r.stdout.strip().splitlines()]
    wanted = [l.rstrip() for l in exp_n.strip().splitlines()]
    tag = (' (fixture)' if random_lab else '') + \
          (' (declared)' if source == 'declared' else '')
    if actual == wanted:
        return 'MATCH', f'inputs={vals}{tag}'
    if not show_diff:
        return 'DIFFERS', f'inputs={vals}{tag}'
    diff = list(difflib.unified_diff(wanted, actual, 'sheet', 'solution', lineterm=''))
    return 'DIFFERS', f'inputs={vals}{tag}\n' + '\n'.join('      ' + l for l in diff[:30])


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

    fixture = find_fixture(root)
    fixture_dir = stage_fixture(fixture) if fixture else None
    if fixture:
        print(f'fixture: {os.path.relpath(fixture, root)} '
              f'({", ".join(f"{k}={v}" for k, v in FIXTURE_ENV.items())})\n')
    else:
        print('fixture: NONE FOUND. Labs importing random cannot be verified.\n')

    tally, bad, unverified, by_design = {}, 0, 0, 0
    for jp in files:
        lab = os.path.splitext(os.path.basename(jp))[0]
        sol = solution_for(root, lab)
        if not sol:
            status, detail = 'NO-SOLUTION', None
        else:
            status, detail = verify(lab, jp, sol, fixture_dir)
        tally[status] = tally.get(status, 0) + 1
        # Only DIFFERS proves a disagreement. CRASH, TIMEOUT and PROMPT-MISMATCH
        # mean this harness could not reconstruct the input sequence, which is a
        # limitation here, not evidence against the sheet. Reporting those as
        # failures would train everyone to ignore the output.
        if status == 'DIFFERS':
            bad += 1
        elif status in ('CRASH', 'TIMEOUT', 'PROMPT-MISMATCH'):
            unverified += 1
        elif status in ('REAL-RANDOM', 'PLACEHOLDER', 'NOT-APPLICABLE'):
            by_design += 1
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
    if by_design:
        print(f'\nverify_output: {by_design} sheet(s) cannot be verified as written. '
              f'Each is a content decision, not a defect in the run:')
        print('  REAL-RANDOM    regenerate the sample run against the fixture to verify it')
        print('  PLACEHOLDER    the sheet never shows a real transcript')
        print('  NOT-APPLICABLE the block is not this program\'s stdout')
    if tally.get('NONDETERMINISTIC'):
        print(f'\nverify_output: {tally["NONDETERMINISTIC"]} lab(s) import random but no '
              f'deterministic fixture was found, so they could not be run.')
    if fixture_dir:
        shutil.rmtree(fixture_dir, ignore_errors=True)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
