#!/usr/bin/env python3
"""
check_scope.py - Run CodeGrade's Scope Compliance rules against the solutions,
here, before anything reaches CodeGrade.

WHY THIS EXISTS
On 2026-08-10 a change was made to mod4/4-1/lab-4-1.py that added `.upper()`.
Every guard in this repo passed. `verify_output.py` went to 13 MATCH. The
reasoning behind the change cited six sibling labs and fourteen assignment
sheets, all of which agreed. All of it was wrong, and it was caught only when
John ran the file through CodeGrade and the Scope Check failed with
`FAIL: {'.upper()'}` (ledger R-008).

The reason no guard could catch it: every check in this repo compares repo
artifacts to each other. The rule that actually governed that file lived in a
CodeGrade AutoTest step, which nothing here can see. Repo-internal agreement is
worthless when the deciding authority is outside the repo.

So the rules move in here. This file is a TRANSCRIPTION of the CodeGrade scope
scripts, and its only job is to fail the build the moment a solution stops
complying with the scope its assignment enforces.

WHAT THE RULES ENCODE
Not arbitrary restriction. Deliberate staging, so each tool lands as a payoff:

    .upper() / .lower()   withheld until Lab 4.2, whose docstring reads
                          ".upper() finally arrives: clean_input() strips
                          whitespace and uppercases user input". Lab 4.1 must
                          feel the y/Y/n/N comparisons first.
    set / set()           withheld until Lab 4.3. Lab 3.3 and Lab 4.1 build
                          unique-city lists by hand with `in`, which is the
                          work that makes a set feel like a gift later.
    class                 Module 5 only.

KEEPING THIS HONEST
A rule set that drifts from CodeGrade is worse than none, because it grants
false confidence. Two defences:

  1. Every entry records the assignment it was transcribed from and the date.
  2. An assignment with no entry is reported as UNKNOWN, never as passing.
     Silence here means "nobody has looked", and it says so out loud.

    python3 check_scope.py
    python3 check_scope.py --solutions ~/path/to/IS2053/code/Modules
"""
import argparse
import ast
import glob
import os
import sys

# ── Transcribed rules ────────────────────────────────────────────────
# Keys are lab ids. Each value lists what that assignment PROHIBITS.
# Verbatim from the CodeGrade custom-test scripts; do not "tidy" them.
#
#   banned_methods  attribute calls, e.g. 'upper' catches x.upper()
#   ban_sets        set literals, set comprehensions, and set()
#   ban_classes     any class definition
#   files           which uploaded files the CodeGrade script actually reads.
#                   4.1's script opens ONLY lab-4-1.py, so function_library.py
#                   is NOT scope-checked there. Mirroring that exactly matters:
#                   a guard stricter than the real one fails honest solutions.
SCOPE = {
    'lab-4-1': {
        'source': 'CodeGrade "Scope Check" custom-test, transcribed 2026-08-10',
        'files': ['lab-4-1.py'],
        'banned_methods': ('upper', 'lower'),
        'ban_sets': True,
        'ban_classes': True,
    },
}

# Assignments known to exist but whose scope script has not been read yet.
# Listing them is the point: an empty dict would quietly imply "all clear".
NOT_YET_TRANSCRIBED = [
    'lab-1-1', 'lab-1-2', 'lab-1-3', 'lab-2-1', 'lab-2-2', 'lab-2-3',
    'lab-3-1', 'lab-3-2', 'lab-3-3', 'lab-4-2', 'lab-4-3', 'lab-5-1', 'lab-5-2',
]


def violations(path, rule):
    """The same AST walk CodeGrade performs, same node types, same order."""
    found = []
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except SyntaxError as e:
        return [f'syntax error: {e}']
    for node in ast.walk(tree):
        if rule.get('ban_sets'):
            if isinstance(node, ast.Set):
                found.append('set literal')
            if isinstance(node, ast.SetComp):
                found.append('set comprehension')
        if rule.get('ban_classes') and isinstance(node, ast.ClassDef):
            found.append(f'class: {node.name}')
        if isinstance(node, ast.Call):
            if rule.get('ban_sets') and isinstance(node.func, ast.Name) \
                    and node.func.id == 'set':
                found.append('set()')
            if isinstance(node.func, ast.Attribute) \
                    and node.func.attr in rule.get('banned_methods', ()):
                found.append(f'.{node.func.attr}()')
    return sorted(set(found))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solutions', default=os.environ.get('IS2053_SOLUTIONS'),
                    help='root of the solution tree')
    a = ap.parse_args()
    if not a.solutions:
        print('check_scope: SKIPPED (no solutions tree; set IS2053_SOLUTIONS '
              'or pass --solutions)')
        return 0
    root = os.path.expanduser(a.solutions)
    if not os.path.isdir(root):
        print(f'check_scope: SKIPPED (solutions tree not found at {root})')
        return 0

    problems, checked = [], 0
    for lab, rule in sorted(SCOPE.items()):
        for name in rule['files']:
            hits = [h for h in glob.glob(os.path.join(root, '**', name), recursive=True)
                    if 'OLDIES' not in h and '__pycache__' not in h]
            if not hits:
                problems.append(f'{lab}: {name} not found under {root}')
                continue
            for path in hits:
                checked += 1
                bad = violations(path, rule)
                if bad:
                    problems.append(
                        f'{lab}: {name} uses {", ".join(bad)}, which its CodeGrade '
                        f'Scope Check PROHIBITS. This scores 0 of 15 and the '
                        f'student sees only "FAIL". Source: {rule["source"]}')

    print(f'check_scope: {checked} file(s) checked against '
          f'{len(SCOPE)} transcribed scope rule(s)')
    if NOT_YET_TRANSCRIBED:
        print(f'check_scope: {len(NOT_YET_TRANSCRIBED)} assignment(s) have NO '
              f'transcribed rule and are therefore UNCHECKED, not passing:')
        print('  ' + ', '.join(NOT_YET_TRANSCRIBED))
        print('  Paste each CodeGrade Scope Check script into SCOPE to close '
              'the gap (ledger L-030).')
    if problems:
        print('check_scope: FAIL')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('check_scope: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
