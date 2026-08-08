#!/usr/bin/env python3
"""
voice_pass.py - Remove em-dashes from lab sheets by rewriting, not substituting.

Ledger L-013. The no-em-dash rule is old; the debt is AI-drafting drift. A blanket
swap to commas would produce comma splices and lose the emphasis the dash carried,
so each occurrence is classified by what follows it and repunctuated accordingly.

CONFIDENT rules (applied silently):
  A  after </strong>, </code>, </em>     label, then explanation      -> colon
  B  after Edition / Gaddis / Guide      citation                     -> comma
  C  followed by a pronoun               independent clause           -> period
  D  followed by even/but/so/which/...   connective aside             -> comma

HEURISTIC rules (applied, but listed for review with --review):
  E  followed by a gerund or a list      appositive                   -> colon
  F  followed by an imperative verb      independent clause           -> period
  G  followed by <code> or a quote       definition                   -> colon
  H  anything else                       safest reading               -> comma

NEVER TOUCHED: code_block and output_block content, expectedOutput, and the
architecture diagram. Those must stay byte-identical to what the solution prints,
or CodeGrade's exact-match tests break. verify_output.py is the backstop.

    python3 voice_pass.py --dry-run            # counts only
    python3 voice_pass.py --review lab-2-1     # show every change
    python3 voice_pass.py                      # apply to all labs
"""
import argparse
import collections
import glob
import io
import json
import os
import re
import sys

PROTECTED_TYPES = {'code_block', 'output_block'}
PROTECTED_KEYS = {'expectedOutput', 'architecture', 'code', 'output'}
DASH = re.compile(r'\s*(?:—|&mdash;)\s*')

PRONOUN = r"(?:you|we|they|it|that|this|there|here|I)\b"
CONNECTIVE = r"(?:even|especially|but|and|or|so|which|often|usually|unless|because)\b"
IMPERATIVE = (r"(?:copy|use|check|add|save|run|delete|keep|make|put|write|read|test|"
              r"pick|start|stop|open|close|remove|verify|trace|note|remember|confirm|"
              r"type|compare|enter|try|look|submit|download|extract|install|re-read|"
              r"initialize|declare|define|create|build|set|reset|call|import|convert|"
              r"compare|update|display|print|store|track|count|loop|wrap|indent|"
              r"replace|rename|move|name|pass|return|assign|include|follow|watch)\b")
GERUND = r"[a-z]+ing\b"


DETERMINER = r"(?:the|a|an|your|its|my|our|no|none|every|these|those|this|that)\b"
# A finite verb near the start means the clause can stand alone and wants a
# period. Without this, "— the patterns are there" becomes a comma splice while
# "— carried over from Lab 1.1" correctly stays an appositive.
FINITE = (r"\b(?:is|are|was|were|has|have|had|does|do|don't|doesn't|will|won't|can|"
          r"can't|must|should|shows?|means?|tells?|gets?|goes|comes?|matters?|works?|"
          r"happens?|holds?|keeps?|needs?|lives?|starts?|ends?|makes?|takes?|gives?|"
          r"decreases?|increases?|becomes?|stays?|fails?|passes?|serves?|returns?|"
          r"prints?|adds?|subtracts?|stores?|tracks?|counts?|loops?|runs?|executes?|"
          r"converts?|checks?|compares?|updates?|sets?|resets?|calls?|imports?|opens?|"
          r"reads?|writes?|saves?|loads?|displays?|contains?|includes?|requires?|"
          r"expects?|accepts?|produces?|causes?|breaks?|crashes?|throws?|raises?|"
          r"lets?|allows?|prevents?|ensures?|handles?|feeds?|belongs?|differs?|differ|"
          r"depends?|depend|gives?|give|hits?|hit|stops?|stop|appears?|appear|"
          r"strips?|parses?|receives?|wraps?|includes?|introduces?|controls?)\b")
# Leading adverbs hide the real head of the clause.
LEAD_ADVERB = r"^(?:just|simply|now|then|always|never|only|still|already)\s+"


def classify(before, after):
    b, a = before.rstrip(), after.lstrip()
    a = re.sub(LEAD_ADVERB, '', a, flags=re.I)

    if re.search(r'</(?:strong|code|em)>\s*$', b):
        return 'A', ': '
    if re.search(r'\b(?:Edition|Gaddis|Guide|Reference)\s*$', b):
        return 'B', ', '
    if re.match(PRONOUN, a, re.I):
        return 'C', '. '
    if re.match(CONNECTIVE, a, re.I):
        return 'D', ', '
    # Short label with no sentence punctuation on the left: "Style violation — ..."
    if len(b) < 42 and not re.search(r'[.!?]', b) and re.match(r'[a-z]', a):
        return 'I', ': '
    # Any noun phrase owning a finite verb within the first few words is an
    # independent clause and needs a period. Requiring a determiner missed
    # "indentation errors are..." and "only the program number differs", which
    # a comma turns into a splice. Appositives ("the value being passed",
    # "carried over from Lab 1.1") have no finite verb, so they stay commas.
    if len(a.split()) >= 3 and re.search(FINITE, ' '.join(a.split()[:7]), re.I):
        return 'J', '. '
    if re.match(GERUND, a) or (',' in a[:60] and re.match(r'[a-z]', a)):
        return 'E', ': '
    if re.match(IMPERATIVE, a, re.I):
        return 'F', '. '
    if a.startswith('<code>') or a.startswith('"') or a.startswith('&ldquo;'):
        return 'G', ': '
    return 'H', ', '


def capitalize_after(s, at):
    """After turning a dash into a period, the next word starts a sentence.

    Two things must not be capitalized, and both were shipped before being
    caught:

      code    "readline()" became "Readline()" on a BookEx page, which is
              simply wrong in Python. If the token is followed by '(', skip.
      markup  "<strong>NEW this unit</strong>" became "<Strong>...". HTML is
              case-insensitive so it still rendered, but it is a defect and it
              defeats every tag-matching grep. Step over the whole tag and
              capitalize the first real word inside it instead.
    """
    import re as _re
    while at < len(s):
        tag = _re.match(r'\s*<[^>]*>', s[at:])
        if not tag:
            break
        # Inside <code> the next word is an identifier, not a sentence.
        if _re.match(r'\s*<code\b', s[at:], _re.I):
            return s
        at += tag.end()
    for i in range(at, min(at + 12, len(s))):
        if s[i].isalpha():
            m = _re.match(r'[A-Za-z_][A-Za-z0-9_]*', s[i:])
            if m and s[i + m.end():i + m.end() + 1] == '(':
                return s
            return s[:i] + s[i].upper() + s[i + 1:]
        if s[i] not in 'abcdefghijklmnopqrstuvwxyz':
            break
    return s


def rewrite(text, tally, log, where):
    out, pos = text, 0
    while True:
        m = DASH.search(out, pos)
        if not m:
            return out
        rule, repl = classify(out[:m.start()], out[m.end():])
        before_ctx = re.sub(r'\s+', ' ', out[max(0, m.start() - 60):m.end() + 60])
        out = out[:m.start()] + repl + out[m.end():]
        if repl == '. ':
            out = capitalize_after(out, m.start() + len(repl))
        tally[rule] += 1
        if rule in 'EFGHIJ':
            after_ctx = re.sub(r'\s+', ' ',
                               out[max(0, m.start() - 60):m.start() + len(repl) + 60])
            log.append((rule, where, before_ctx, after_ctx))
        pos = m.start() + len(repl)


def process(path, tally, log, dry):
    d = json.load(open(path, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    lab = os.path.basename(path)

    def walk(o, key=None, intype=None):
        if isinstance(o, dict):
            t = o.get('type')
            return collections.OrderedDict((k, walk(v, k, t or intype)) for k, v in o.items())
        if isinstance(o, list):
            return [walk(v, key, intype) for v in o]
        if isinstance(o, str):
            if key in PROTECTED_KEYS or intype in PROTECTED_TYPES:
                return o
            return rewrite(o, tally, log, f'{lab}:{key}')
        return o

    new = walk(d)
    if not dry:
        io.open(path, 'w', encoding='utf-8').write(json.dumps(new, indent=2, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--review', action='store_true', help='print every heuristic change')
    ap.add_argument('labs', nargs='*', help='filter by filename fragment')
    a = ap.parse_args()

    # Every JSON source, not just labs. BookEx, scenario, support and exam
    # pages carry the same debt and the same rules apply.
    files = sorted(glob.glob('pages/**/json/*.json', recursive=True))
    files += sorted(glob.glob('pages/**/json/**/*.json', recursive=True))
    files = sorted(set(files))
    if a.labs:
        files = [f for f in files if any(l in f for l in a.labs)]

    tally, log = collections.Counter(), []
    for f in files:
        process(f, tally, log, a.dry_run)

    names = {'A': 'label -> colon', 'B': 'citation -> comma', 'C': 'clause -> period',
             'D': 'aside -> comma', 'I': 'short label -> colon', 'J': 'NP+verb -> period',
             'E': 'appositive -> colon', 'F': 'imperative -> period',
             'G': 'definition -> colon', 'H': 'fallback -> comma'}
    print(('DRY RUN, ' if a.dry_run else '') + f'{sum(tally.values())} em-dashes across {len(files)} source files')
    for r in 'ABCDIJEFGH':
        if tally[r]:
            kind = 'confident' if r in 'ABCDIJ' else 'HEURISTIC'
            print(f'  {r} {names[r]:24} {tally[r]:4}   {kind}')
    if a.review:
        print(f'\n{len(log)} heuristic change(s) to review:')
        for rule, where, b, af in log:
            print(f'\n  [{rule}] {where}')
            print(f'    was: {b}')
            print(f'    now: {af}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
