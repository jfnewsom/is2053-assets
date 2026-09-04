#!/usr/bin/env python3
"""
message_digest.py - Keep every official string in one place, and keep it true.

Why this exists
---------------
On 2026-09-03, mid-lecture, Lab 1.2 turned out to tell students to set a
`message` variable to "a fun message" and then grade them, character by
character, against a fixed string. Corpus and Austin's wording leaked into
CP3 and CP4 output blocks, so the students who passed were the ones who
reverse-engineered it. Houston's message and the invalid-choice message
appeared NOWHERE in the sheet. Lab 1.3 was worse: its CP4 table asked for a
"Beach celebration message" and the callout directly beneath it said
CodeGrade compares output character by character.

The fix is the `finalChecklist.messageDigest` block: every prompt and every
printed string, in the exact form it appears, in one section at the bottom of
the sheet. This tool keeps that block honest.

    lab_lint.py        catches a sheet contradicting ITSELF.
    verify_output.py   catches a sheet contradicting the SOLUTION's output.
    message_digest.py  catches a sheet that never states a string at all.

The third is the gap the first two could not see: a sheet can be perfectly
self-consistent, and its expectedOutput can match the solution exactly, while
still leaving a required string undocumented. Nothing prints what is missing.

Usage
-----
    python3 message_digest.py --solutions ~/path/to/IS2053/code/Modules
    python3 message_digest.py --solutions ... lab-1-3          # one lab
    python3 message_digest.py --solutions ... --generate lab-2-1 > rows.json

--generate emits a messageDigest skeleton with every string pulled from the
solution in source order, each with an empty "when" for the author to fill.
It never writes to the JSON; authoring the "where it appears" column is a
human job, and a digest full of blanks is worse than none.
"""
import argparse
import ast
import glob
import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(REPO, 'pages', 'labs', 'json')

# Calls whose string arguments reach the student's screen. get_valid_int and
# get_yes_no take the prompt as their first argument from Module 2 onward;
# scanning input() alone goes blind at exactly the point the labs get harder.
USER_FACING = {'print', 'input', 'get_valid_int', 'get_yes_no'}


def solution_for(root, lab):
    """mod1/lab-1-1.py, mod4/4-1/lab-4-1.py, ... without hardcoding layout.

    Same lookup verify_output.py uses, deliberately: two tools disagreeing
    about which file is the solution would be its own bug.
    """
    hits = glob.glob(os.path.join(root, '**', f'{lab}.py'), recursive=True)
    hits = [h for h in hits if 'OLDIES' not in h and '__pycache__' not in h]
    return hits[0] if hits else None


def module_constants(tree):
    """UPPER_SNAKE_CASE = <literal> at module scope.

    Needed because the solutions build menu lines out of their constants:

        f'  1. Corpus Christi - {SAT_TO_CORPUS} miles (BEACH!)'

    A student reading the digest sees `150` on their screen, not the constant
    name, and the digest's promise is "exactly as it appears." So resolve the
    constant rather than making the author choose between a row that matches
    the source and a row that matches the terminal.
    """
    consts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    consts[target.id] = node.value.value
    return consts


def _fold(node, consts):
    """Evaluate a constant-only string expression, or return None.

    Handles the shapes the course writes: '=' * 50 for banners and 'a' + 'b'
    for split lines, with module constants resolved.

    By hand and not eval(): this runs over solution files, and a linter that
    executes expressions out of a source file is a bad habit to build into a
    repo that student code eventually passes through.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in consts:
        return consts[node.id]

    if isinstance(node, ast.BinOp):
        left, right = _fold(node.left, consts), _fold(node.right, consts)

        if isinstance(node.op, ast.Add):
            if isinstance(left, str) and isinstance(right, str):
                return left + right

        if isinstance(node.op, ast.Mult):
            # '=' * 50 or 50 * '='
            for text, count in ((left, right), (right, left)):
                if isinstance(text, str) and isinstance(count, int) \
                        and 0 <= count <= 500:
                    return text * count

    return None


def visible_text(node, src, consts):
    """The characters a student actually sees, or None if undeterminable.

    Built from the AST rather than by unquoting a source segment. The digest
    column is the STRING, not the Python literal, and an f-string's braces,
    a constant's value, and a banner's repetition all have to be resolved the
    same way the interpreter resolves them before a comparison means anything.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value

    if isinstance(node, ast.JoinedStr):
        out = []
        for part in node.values:
            if isinstance(part, ast.Constant) and isinstance(part.value, str):
                out.append(part.value)
            elif isinstance(part, ast.FormattedValue):
                inner = part.value
                # A constant resolves to its value; anything else stays a
                # {placeholder} carrying the student's own variable name.
                if isinstance(inner, ast.Name) and inner.id in consts:
                    out.append(str(consts[inner.id]))
                    continue
                seg = ast.get_source_segment(src, inner)
                if seg is None:
                    return None
                spec = ''
                if part.format_spec is not None:
                    spec_src = ast.get_source_segment(src, part.format_spec)
                    if spec_src:
                        spec = ':' + spec_src
                out.append('{' + ' '.join(seg.split()) + spec + '}')
            else:
                return None
        return ''.join(out)

    if isinstance(node, ast.BinOp):
        folded = _fold(node, consts)
        return folded if isinstance(folded, str) else None

    return None


def extract_strings(src):
    """Every user-facing argument in the solution, in source order.

    Returns [(kind, text, lineno)] where kind is:
      'string'   text a student sees, f-strings and banners already resolved
      'variable' a bare name or attribute, e.g. print(message)
    """
    tree = ast.parse(src)
    consts = module_constants(tree)
    found = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, 'id', None) or getattr(fn, 'attr', None)
        if name not in USER_FACING:
            continue

        for arg in node.args:
            text = visible_text(arg, src, consts)
            if text is not None:
                found.append(('string', text, arg.lineno))
            elif isinstance(arg, (ast.Name, ast.Attribute)):
                seg = ast.get_source_segment(src, arg)
                if seg:
                    found.append(('variable', seg, arg.lineno))

    found.sort(key=lambda t: t[2])
    return found


def assigned_strings(src):
    """Every string literal assigned to a variable anywhere in the solution.

    A `status` of 'BEACH' and a `message` of 'Invalid choice!' never appear
    inside a print() call, but they reach the screen through the variable that
    prints them, and CodeGrade sees them. They belong in the digest, so the
    check has to be able to find them.
    """
    out = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            out.add(node.value.value)
    return out


def digest_texts(doc):
    """Every `text` in the sheet's messageDigest."""
    digest = doc.get('finalChecklist', {}).get('messageDigest', {})
    rows = digest.get('rows', [])
    if isinstance(rows, str):
        return []
    return [r.get('text', '') for r in rows if r.get('text')]


def check_lab(lab, doc, sol_path):
    """Diff the solution's strings against the sheet's digest, both ways."""
    src = open(sol_path, encoding='utf-8').read()
    found = extract_strings(src)
    declared = digest_texts(doc)

    printed = [t for kind, t, _ in found if kind == 'string']
    printed_vars = {t for kind, t, _ in found if kind == 'variable'}
    assigned = assigned_strings(src)

    # Direction 1: the solution prints something the sheet never states.
    # This is the failure that started all of this.
    undocumented = [t for t in printed if t not in declared]

    def documented(t):
        if t in printed or t in assigned:
            return True
        # A row whose text is exactly {name} documents `print(name)` — the
        # line whose wording lives in a variable.
        if t.startswith('{') and t.endswith('}') and t[1:-1] in printed_vars:
            return True
        return False

    # Direction 2: the sheet states something the solution never produces.
    # Usually a stale digest left behind after the solution was edited.
    stale = [t for t in declared if not documented(t)]

    return undocumented, stale, len(printed)


def is_section_header(text):
    """Is this comment a section label, or just prose?

    Module 1 and 2 solutions are sectioned with headers (`# Welcome banner`,
    `# Get player name`). Module 3 onward comment in full sentences and wrap
    them across lines, so the naive "nearest comment" gives fragments like
    "-- no return value needed (player handles its own state)". A fragment in
    the Purpose column is worse than an empty cell, because an empty cell
    reads as unfinished and a fragment reads as wrong.
    """
    if not text or len(text) > 55:
        return False
    if not text[0].isupper() and not text[0].isdigit():
        return False
    if text[0] in '-*' or text.endswith((',', ':', 'and', 'or', 'the')):
        return False
    # Sentence prose, as opposed to a label.
    if text.count(' ') > 7 or text.endswith('.') and ' ' in text.rstrip('.'):
        return False
    return True


def source_comments(src):
    """Map line number -> the nearest section-header comment at or above it.

    Where a solution labels its sections, those labels are the author's own
    description of what each block is for, which is exactly what the Purpose
    column wants and beats anything this tool could invent. Where it does not,
    this returns nothing and the author fills the column in.
    """
    nearest = {}
    current = ''
    for i, line in enumerate(src.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith('#'):
            text = stripped.lstrip('#').strip()
            if 'DEBUG' in text or set(text) <= set('=-# '):
                continue
            current = text if is_section_header(text) else ''
        nearest[i] = current
    return nearest


def checkpoints_mentioning(doc, text):
    """Which checkpoints already contain this string, for the Shown In column.

    A string found in no checkpoint is the interesting case: it is one the
    sheet never states, which is the whole defect. Those come back as TODO so
    a human has to look at them rather than having a plausible number filled
    in for them.
    """
    # Compare on the longest literal run outside any {placeholder}, so an
    # f-string still matches the sample output it was rendered into. Falling
    # back to the whole braced string would never match anything, which reads
    # as "undocumented" for a line that is in fact documented.
    needle = max(re.split(r'\{[^}]*\}', text), key=len).strip()
    if len(needle) < 4:
        return []

    escaped = html.escape(needle)
    hits = []
    # Not every checkpoint carries an explicit `number`; fall back to position
    # so a lab with one unnumbered CP does not crash the whole run.
    for i, cp in enumerate(doc.get('checkpoints', []), start=1):
        blob = json.dumps(cp, ensure_ascii=False)
        if needle in blob or escaped in blob:
            number = cp.get('number')
            hits.append(number if isinstance(number, int) else i)
    return hits


def shown_in(cps):
    """Format the Shown In cell the way the course's sheets always have.

    The checkpoint where the student WRITES the line is the useful answer, so
    take the earliest and mark a trailing + when it recurs later. Listing
    every checkpoint that happens to quote it (a sample run near the end
    quotes most of the program) produces a column nobody can read.
    """
    if not cps:
        return 'TODO'
    first = min(cps)
    return f'CP{first}+' if len(cps) > 1 else f'CP{first}'


LABEL_LINE = re.compile(r'^([A-Z][A-Za-z ]{1,24}):\s')


def dedupe_purposes(rows):
    """Number repeated Purpose values so a table of them stays readable.

    A block of six report lines all share one section comment, and six rows
    reading "Display final summary" is a column carrying no information.
    Numbering them in order restores what a human would have written.
    """
    counts = {}
    for row in rows:
        if row['purpose']:
            counts[row['purpose']] = counts.get(row['purpose'], 0) + 1

    seen = {}
    for row in rows:
        purpose = row['purpose']
        if counts.get(purpose, 0) > 1:
            seen[purpose] = seen.get(purpose, 0) + 1
            row['purpose'] = f'{purpose} {seen[purpose]}'
    return rows


def generate(lab, sol_path, doc=None):
    """Emit a messageDigest skeleton from the solution, for a human to finish.

    Purpose is seeded from the solution's own section comments and Shown In
    from the checkpoint that already mentions the string. Both are seeds, not
    answers: anything the tool could not derive comes back as TODO, and a row
    whose Shown In is TODO is a string the sheet never states anywhere, which
    is precisely the row a human needs to look at.
    """
    src = open(sol_path, encoding='utf-8').read()
    found = extract_strings(src)
    comments = source_comments(src)

    def row_for(text, lineno, label=None):
        note = comments.get(lineno, '')

        # A report line names itself better than its section comment does:
        # "Driver: {player_name}" is the Driver line, not "Display final
        # summary" for the fourth row running.
        m = LABEL_LINE.match(text)
        # An all-caps banner is a title, not a labelled report line.
        if m and not label and not m.group(1).isupper():
            return {'purpose': f'{m.group(1)} line',
                    'text': text,
                    'shownIn': shown_in(checkpoints_mentioning(doc, text) if doc else [])}

        if label and note:
            purpose = f'<code>{label}</code>, {note[0].lower()}{note[1:]}'
        elif label:
            purpose = f'<code>{label}</code>'
        elif note:
            purpose = note
        else:
            purpose = ''

        cps = checkpoints_mentioning(doc, text) if doc else []
        shown = shown_in(cps)
        return {'purpose': purpose, 'text': text, 'shownIn': shown}

    seen = set()
    rows = []
    for kind, text, lineno in found:
        key = text if kind == 'string' else '{' + text + '}'
        if key in seen or not key:
            continue
        seen.add(key)
        rows.append(row_for(key, lineno))

    # Assigned-but-printed-by-variable strings, in source order.
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            text = node.value.value
            var = getattr(node.targets[0], 'id', '?')
            if text in seen or not text.strip() or var.isupper():
                continue
            seen.add(text)
            rows.append(row_for(text, node.lineno, label=var))

    rows = dedupe_purposes(rows)

    todo = sum(1 for r in rows if r['shownIn'] == 'TODO')
    print(f'  {lab}: {len(rows)} rows, {todo} with no checkpoint mention '
          f'(these are the undocumented ones)', file=sys.stderr)

    return {'intro': '', 'rows': rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--solutions', required=True,
                    help='root of the solutions tree (outside this repo)')
    ap.add_argument('--generate', action='store_true',
                    help='print a digest skeleton instead of checking')
    ap.add_argument('labs', nargs='*',
                    help='lab ids, e.g. lab-1-2. Default: every lab JSON.')
    args = ap.parse_args()

    root = os.path.expanduser(args.solutions)
    if not os.path.isdir(root):
        sys.exit(f'Not a directory: {root}')

    labs = args.labs or sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(JSON_DIR, 'lab-*.json'))
    )

    failures = 0
    for lab in labs:
        json_path = os.path.join(JSON_DIR, f'{lab}.json')
        if not os.path.exists(json_path):
            print(f'{lab}: no JSON at {json_path}')
            failures += 1
            continue

        sol = solution_for(root, lab)
        if not sol:
            print(f'{lab}: SKIP, no solution found under {root}')
            continue

        if args.generate:
            doc = json.load(open(json_path, encoding='utf-8'))
            print(json.dumps(generate(lab, sol, doc), indent=2, ensure_ascii=False))
            continue

        doc = json.load(open(json_path, encoding='utf-8'))
        if not doc.get('finalChecklist', {}).get('messageDigest'):
            print(f'{lab}: NO DIGEST — sheet has no messageDigest block')
            failures += 1
            continue

        undocumented, stale, total = check_lab(lab, doc, sol)

        if not undocumented and not stale:
            print(f'{lab}: OK ({total} strings, all documented)')
            continue

        failures += 1
        print(f'{lab}: {len(undocumented)} undocumented, {len(stale)} stale')
        for s in undocumented:
            print(f'    MISSING FROM SHEET   {s}')
        for s in stale:
            print(f'    NOT IN SOLUTION      {s}')

    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
