#!/usr/bin/env python3
"""ai_check.py - Run every AI Assist prompt through several AI models and flag
answers that break the prompt's rules.

Why: each lab checkpoint offers copy-ready prompts (Explain it, Quiz me, Decode
my error). They only help if the AIs students use stay inside the chapter's
toolbox, don't hand back lab code, and actually ask, wait, and explain. This
tests that, per lab, before the prompts reach students. Design input only; it
never looks at student work. See IS2053_2026-11-20_AI_Assist_Prompts.md.

Services (keys come from environment variables; a missing key skips that one):
  Claude         ANTHROPIC_API_KEY   (Claude Ultra plan's monthly API credits)
  Gemini         GEMINI_API_KEY      (free key from Google AI Studio; tries each
                                      Flash model, newest first, until one answers)
  OpenAI         OPENAI_API_KEY      (optional; pay-as-you-go API key, separate
                                      from a ChatGPT subscription)
  GitHub Models was retired on July 30, 2026, and was removed from this script.

For each prompt and model:
  Explain it       one turn
  Quiz me          two turns: a simulated student answers the first question
                   wrong, so the reply shows whether the AI waits and hints
  Decode my error  the placeholder is filled with a real error for that
                   checkpoint (config.json "errors")

Checks:
  mechanical  code outside the chapter's toolbox, the lab's own printed
              strings appearing in the answer, length
  judge       Claude reads the transcript against the prompt's rules and
              returns PASS or FLAG with one reason

Usage:
  python3 tools/ai_check/ai_check.py                 # labs in labs.txt
  python3 tools/ai_check/ai_check.py lab-1-1         # one lab
  python3 tools/ai_check/ai_check.py --list-models   # what each service offers
  python3 tools/ai_check/ai_check.py --dry-run       # no network; fake answers
Writes ai_check_results/<timestamp>/ (transcripts + report.md) and, in GitHub
Actions, the report to the run's Summary page. Standard library only.
"""
import argparse
import datetime
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import http.client
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
JSON_DIR = os.path.join(REPO, "pages", "labs", "json")
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
PLACEHOLDER = "[paste the whole error message here]"

# Tools a chapter's labs may NOT use, as patterns over code the AI wrote.
# Keyed by the lab's meta.chapters. Extend as later labs get AI Assist.
FORBIDDEN = {
    "2": [
        (r"^\s*(if|elif|else)\b(?!\s+__name__)", "if/elif/else (Chapter 3)"),
        (r"^\s*(for|while)\b", "loops (Chapter 4)"),
        (r"^\s*(import|from)\s+\w", "import"),
        (r"^\s*def\s+(?!main\b)\w+", "a function other than main() (Chapter 5)"),
        (r"=\s*\[", "a list (Chapter 7)"),
    ],
    # Chapter 4 (Lab 2.1 on): .upper() is allowed, in the travel banner only.
    "4": [
        (r"\.(lower|strip|title|capitalize|split|isdigit)\(", "a string method other than .upper() (Chapter 8)"),
        (r"^\s*(import|from)\s+\w", "import"),
        (r"^\s*def\s+(?!main\b)\w+", "a function other than main() (Chapter 5)"),
        (r"=\s*\[", "a list (Chapter 7)"),
    ],
    # Chapters 4-5 (Lab 2.3): .strip() and .isdigit() join .upper(), each used
    # in one place in the lab, so the AI may use them too. Key matches the
    # sheet's meta.chapters, which uses an en dash.
    "4\u20135": [
        (r"\.(lower|title|capitalize|split|startswith|endswith|replace)\(", "a string method other than .upper(), .strip(), .isdigit() (Chapter 8)"),
        (r"=\s*\[", "a list (Chapter 7)"),
        (r"^\s*(try|except)\b", "try/except (Chapter 6)"),
        (r"\bopen\(", "a file (Chapter 6)"),
    ],
    # Chapter 5 (Lab 2.2 on): functions and import are allowed now.
    "5": [
        (r"\.(lower|strip|title|capitalize|split|isdigit)\(", "a string method other than .upper() (Chapter 8)"),
        (r"=\s*\[", "a list (Chapter 7)"),
        (r"^\s*(try|except)\b", "try/except (Chapter 6)"),
        (r"\bopen\(", "a file (Chapter 6)"),
    ],
    # Chapter 7 (Lab 3.2 on): lists, for loops, append(), sort() are allowed now.
    "7": [
        (r"\.(lower|title|capitalize|split|startswith|endswith|replace|find|join)\(", "a string method other than .upper(), .strip(), .rstrip(), .isdigit() (Chapter 8)"),
        (r"=\s*\{", "a dictionary or set (Chapter 9)"),
    ],
    # Chapter 6 (Lab 3.1): files and try/except are allowed now, and .rstrip()
    # joins the string methods the labs use. Lists still wait for Chapter 7.
    "6": [
        (r"\.(lower|title|capitalize|split|startswith|endswith|replace|find|join|readlines)\(", "a string method other than .upper(), .strip(), .rstrip(), .isdigit() (Chapter 8)"),
        (r"=\s*\[", "a list (Chapter 7)"),
    ],
    # Chapters 8-9 (Module 4): everything from Chapters 2 to 9 is allowed;
    # classes wait for Module 5. Key matches meta.chapters (en dash).
    "8\u20139": [
        (r"^\s*class\b", "a class (Chapter 10)"),
    ],
    # Chapter 10 (Module 5): classes are allowed now; inheritance waits
    # for Chapter 11, which the course doesn't cover.
    "10": [
        (r"^\s*class\s+\w+\s*\(\s*\w", "inheritance (Chapter 11)"),
    ],
    "3": [
        (r"\.(lower|upper|strip|title|capitalize)\(", "a string method (Chapter 8)"),
        (r"^\s*(for|while)\b", "loops (Chapter 4)"),
        (r"^\s*(import|from)\s+\w", "import"),
        (r"^\s*def\s+(?!main\b)\w+", "a function other than main() (Chapter 5)"),
        (r"=\s*\[", "a list (Chapter 7)"),
    ],
}


# ---------------------------------------------------------------- HTTP
# Requests run in parallel, but each service gets a small cap so free-tier
# rate limits aren't hit all at once (config "concurrency").
_CAPS = {k: threading.Semaphore(v) for k, v in {
    "anthropic": 4, "google": 2, "openai": 2, **CONFIG.get("concurrency", {})}.items()}


def _service(url):
    return ("anthropic" if "anthropic" in url else "google" if "googleapis" in url
            else "openai")


_TRIES = {"n": 4}   # preflight drops this to 1 so a dead model is skipped fast
# A service still answering 429 after every retry has used up its quota (Gemini's
# free tier has a daily cap), and 402 means prepaid credits ran out. Either way
# its remaining requests are skipped, not retried.
_DEAD = {}


def post(url, headers, body, tries=None):
    svc = _service(url)
    if svc in _DEAD:
        raise RuntimeError(f"not run: {_DEAD[svc]}")
    with _CAPS[svc]:
        try:
            return _post(url, headers, body, tries or _TRIES["n"])
        except RuntimeError as e:
            if str(e).startswith("HTTP 402"):
                _DEAD[svc] = f"{svc} prepaid credits used up (HTTP 402)"
            elif str(e).startswith("HTTP 429") and (tries or _TRIES["n"]) > 1:
                _DEAD[svc] = f"{svc} quota used up earlier in this run"
            raise


def _post(url, headers, body, tries=4):
    data = json.dumps(body).encode()
    for attempt in range(tries):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                raw = r.read().decode(errors="replace")
                try:
                    return json.loads(raw)
                except ValueError:
                    raise RuntimeError(f"HTTP {r.status} but not JSON: {raw[:200]!r}")
        except urllib.error.HTTPError as e:
            msg = " ".join(e.read().decode(errors="replace").split())[:900]
            if e.code in (429, 500, 502, 503, 529) and attempt < tries - 1:
                time.sleep(30 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except TimeoutError:
            if attempt < tries - 1:
                continue
            raise RuntimeError("timed out")
        except (ConnectionError, http.client.HTTPException) as e:
            # e.g. "Remote end closed connection without response"
            if attempt < tries - 1:
                time.sleep(10)
                continue
            raise RuntimeError(f"connection dropped: {e}")
        except urllib.error.URLError as e:
            if attempt < tries - 1:
                time.sleep(10)
                continue
            raise RuntimeError(f"network error: {e.reason}")


def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


# ---------------------------------------------------------------- services
def ask_claude(model, messages, max_tokens=4000, system=None):
    body = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        body["system"] = system
    r = post("https://api.anthropic.com/v1/messages",
             {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}, body)
    return "".join(b.get("text", "") for b in r.get("content", []))


def ask_openai(model, messages):
    r = post("https://api.openai.com/v1/chat/completions",
             {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
             {"model": model, "messages": messages})
    return r["choices"][0]["message"]["content"]


def openai_models():
    r = get("https://api.openai.com/v1/models", {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"})
    return sorted(m["id"] for m in r.get("data", []))


def ask_gemini(model, messages):
    contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                for m in messages]
    r = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
             {"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, {"contents": contents})
    parts = r["candidates"][0]["content"].get("parts", [])
    return "".join(p.get("text", "") for p in parts)


def gemini_models():
    r = get("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
            {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    return [m["name"].split("/", 1)[1] for m in r.get("models", [])
            if "generateContent" in m.get("supportedGenerationMethods", [])]


def gemini_flash_candidates():
    skip = ("tts", "image", "live", "lite", "transcribe", "embed", "preview", "exp", "banana", "omni")
    names = [n for n in gemini_models() if "flash" in n and not any(s in n for s in skip)]

    def ver(n):
        m = re.search(r"gemini-(\d+(?:\.\d+)?)", n)
        return float(m.group(1)) if m else 0.0
    names.sort(key=ver, reverse=True)
    if not names:
        raise RuntimeError("no Gemini flash model found; set gemini_models in config.json")
    return names


def roster():
    """Groups of [(display name, ask function)]. Preflight keeps the first model
    in each group that answers, so a group is one model slot with fallbacks."""
    groups = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        for m in CONFIG["claude_models"]:
            groups.append([(m, lambda msgs, m=m: ask_claude(m, msgs))])
    if os.environ.get("GEMINI_API_KEY"):
        for m in CONFIG["gemini_models"]:
            try:
                names = gemini_flash_candidates() if m == "auto-flash" else [m]
            except Exception as e:  # noqa: BLE001
                print(f"  ! Gemini model lookup failed: {e}")
                continue
            groups.append([(n, lambda msgs, n=n: ask_gemini(n, msgs)) for n in names])
    if os.environ.get("OPENAI_API_KEY"):
        for m in CONFIG.get("openai_models", []):
            groups.append([(m, lambda msgs, m=m: ask_openai(m, msgs))])
    return groups


# ---------------------------------------------------------------- lab data
def load_lab(lab):
    d = json.load(open(os.path.join(JSON_DIR, f"{lab}.json")))
    chapter = str(d["meta"].get("chapters", "")).split(",")[0].strip()
    strings = [r["text"] for r in d["finalChecklist"]["messageDigest"]["rows"]]
    scope = d["finalChecklist"].get("scopeReminder", "")
    prompts = []
    for cp in d["checkpoints"]:
        for item in cp["content"]:
            if item.get("type") == "ai_assist":
                for p in item["prompts"]:
                    prompts.append((cp["number"], cp["title"], p["label"], p["text"]))
    return chapter, strings, scope, prompts


def lab_fragments(strings):
    """Distinctive literal pieces of the lab's printed strings (15+ chars).

    15, not 12, since run 15 (Nov 20): short pieces like "You rolled a" and
    "Total Miles:" turn up in ordinary examples and flagged a passing answer.
    """
    frags = set()
    for s in strings:
        for piece in re.split(r"\{[^}]*\}", s):
            piece = piece.strip()
            if len(piece) >= 15 and not set(piece) <= set("=-"):
                frags.add(piece)
    return sorted(frags)


# ---------------------------------------------------------------- checks
def code_blocks(text):
    blocks = re.findall(r"```[a-zA-Z]*\n(.*?)```", text, flags=re.S)
    return "\n".join(blocks)


def mechanical(text, chapter, frags, label, turns, sent=""):
    flags = []
    code = code_blocks(text)
    for pat, name in FORBIDDEN.get(chapter, []):
        if re.search(pat, code, flags=re.M):
            flags.append(f"uses {name}")
    for f in frags:
        if f in text and f not in sent:
            flags.append(f'contains the lab\'s own line "{f}"')
            break
    words = len(text.split())
    if words > CONFIG["max_words"]:
        flags.append(f"long ({words} words)")
    if label == "Quiz me" and turns:
        first = turns[0]
        if len(re.findall(r"\?", first)) >= 3:
            flags.append("may have asked several questions at once")
    return flags


JUDGE_SYSTEM = """You check answers an AI gave to a beginner programming student. The student used a ready-made prompt from their course. Judge only whether the AI followed the prompt's rules; don't judge writing style.

Rules for every prompt:
1. SCOPE: stay inside the tools the prompt says the student may use. Any code example must use only those tools.
2. NO LAB CODE: don't write code for the student's assignment or anything they could paste into it. A small example on an unrelated topic is fine.
3. ACCURATE: no wrong statements about Python.
Extra rules by prompt:
- "Explain it": explain the concept and end with one question that checks understanding.
- "Quiz me": ask ONE question, then stop and wait. When the student answers wrong, give a hint before giving the answer.
- "Decode my error": explain what the error means and what kind of mistake causes it, and say what to look for. Don't rewrite or fix the student's code for them.
A count or total that starts at 0, or a comparison with 0, doesn't need a named constant: the course's own code writes those as 0.

If you FLAG, also say how serious it is, from a beginner's point of view:
- "serious": a wrong statement about Python that would mislead the student; telling the student a wrong answer is right, or giving the answer after a wrong answer with no hint; writing code for the assignment; or teaching a tool outside the student's list as the way to do it.
- "minor": everything else. For example: a bare number where the prompt asked for a named constant; in "Decode my error", naming the fix for a one-character mistake (like = instead of ==), or listing an extra cause that would give a closely related error instead (like NameError instead of UnboundLocalError); running a little long.

Reply with ONLY this JSON object and nothing before or after it: {"verdict": "PASS" or "FLAG", "severity": "serious" or "minor" (empty for PASS), "rule": "<the rule broken, or empty>", "reason": "<one short sentence>"}"""


def judge(prompt_label, prompt_text, transcript):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {"verdict": "-", "rule": "", "reason": "no judge (ANTHROPIC_API_KEY not set)"}
    convo = "\n\n".join(f"[{who}]\n{text}" for who, text in transcript)
    msg = (f'Prompt type: "{prompt_label}"\n\nPrompt the student sent:\n{prompt_text}\n\n'
           f"Conversation:\n{convo}")
    raw = ask_claude(CONFIG["judge_model"], [{"role": "user", "content": msg}], max_tokens=1500,
                     system=JUDGE_SYSTEM)
    for m in reversed(list(re.finditer(r"\{[^{}]*\}", raw, flags=re.S))):
        try:
            d = json.loads(m.group(0))
            if "verdict" in d:
                return d
        except ValueError:
            continue
    v = re.search(r'"verdict"\s*:\s*"(PASS|FLAG)"', raw)
    if v:
        return {"verdict": v.group(1), "rule": "", "reason": "(judge reply was cut short)"}
    return {"verdict": "?", "rule": "", "reason": f"judge reply not JSON: {raw[:120]}"}


# ---------------------------------------------------------------- one run
def run_prompt(ask, lab, cpnum, label, text, dry=False):
    """Return transcript [(speaker, text)] for one prompt on one model."""
    if label == "Decode my error":
        err = CONFIG["errors"].get(f"{lab}/{cpnum}", CONFIG["errors"]["default"])
        text = text.replace(PLACEHOLDER, err)
    msgs = [{"role": "user", "content": text}]
    if dry:
        return [("student", text), ("AI", "Here's an idea. ```python\nx = 5\nprint(x)\n``` What does it print?")]
    first = ask(msgs)
    transcript = [("student", text), ("AI", first)]
    if label == "Quiz me":
        # The simulated student sometimes returns nothing (Nov 20 run: HTTP 400,
        # "user messages must have non-empty content"). Ask again, then fall back.
        wrong = ""
        for _ in range(3):
            wrong = ask_claude(CONFIG["student_model"], [{"role": "user", "content":
                               CONFIG["wrong_answer_instruction"] + "\n\nQuestion:\n" + first}],
                               max_tokens=100).strip()
            if wrong:
                break
        if not wrong:
            wrong = CONFIG.get("fallback_wrong_answer", "I think it prints 0.")
        msgs += [{"role": "assistant", "content": first}, {"role": "user", "content": wrong}]
        second = ask(msgs)
        transcript += [("student", wrong), ("AI", second)]
    return transcript


def preflight(groups):
    """Send one short message per model; skip any that fail, saying why.
    In a group of fallbacks (Gemini's Flash models), stop at the first that works."""
    ok = []
    _TRIES["n"] = 1
    for group in groups:
        for name, ask in group:
            try:
                ask([{"role": "user", "content": "Reply with the word ready."}])
                ok.append((name, ask))
                print(f"  model ready: {name}")
                break
            except Exception as e:  # noqa: BLE001
                print(f"  ! skipping {name}: {str(e)[:600]}")
    _TRIES["n"] = 4
    return ok


def slug(s):
    return re.sub(r"[^A-Za-z0-9.]+", "-", s).strip("-").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("labs", nargs="*")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.list_models:
        if os.environ.get("GEMINI_API_KEY"):
            print("Gemini:", ", ".join(gemini_models()))
        if os.environ.get("OPENAI_API_KEY"):
            print("OpenAI:", ", ".join(openai_models()))
        print("Claude: see https://docs.claude.com (models in config.json)")
        return 0

    labs = a.labs or [ln.strip() for ln in open(os.path.join(HERE, "labs.txt"))
                      if ln.strip() and not ln.startswith("#")]
    models = [("dry-model", None)] if a.dry_run else preflight(roster())
    if not models:
        print("No model answered (keys: ANTHROPIC_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY). Nothing to run.")
        return 1
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = os.path.join(REPO, "ai_check_results", stamp)
    os.makedirs(out_dir, exist_ok=True)

    jobs = []
    # Newest lab first: if a service runs out of quota partway through, the
    # labs it misses are the older ones, already tested in earlier runs.
    for lab in reversed(labs):
        chapter, strings, scope, prompts = load_lab(lab)
        frags = lab_fragments(strings)
        print(f"{lab}: {len(prompts)} prompts x {len(models)} models x {CONFIG['repeats']} repeats")
        for cpnum, cptitle, label, text in prompts:
            for name, ask in models:
                for rep in range(1, CONFIG["repeats"] + 1):
                    jobs.append((lab, chapter, frags, cpnum, cptitle, label, text, name, ask, rep))

    def do(job):
        lab, chapter, frags, cpnum, cptitle, label, text, name, ask, rep = job
        try:
            tr = run_prompt(ask, lab, cpnum, label, text, dry=a.dry_run)
            ai_turns = [t for who, t in tr if who == "AI"]
            mech = mechanical("\n".join(ai_turns), chapter, frags, label, ai_turns, sent=tr[0][1] if tr else "")
            jd = ({"verdict": "-", "rule": "", "reason": "dry run"} if a.dry_run
                  else judge(label, text, tr))
        except Exception as e:  # noqa: BLE001
            tr, mech, jd = [], [], {"verdict": "ERROR", "rule": "", "reason": str(e)[:200]}
        skipped = jd.get("verdict") == "ERROR"
        bad = not skipped and (bool(mech) or jd.get("verdict") not in ("PASS", "-"))
        # Severity: length and question-count checks are minor; any other
        # mechanical hit (out-of-scope code, the lab's own strings) is serious.
        # A judge FLAG uses the judge's severity; an unreadable verdict counts
        # as serious so a person looks at it.
        sev = ""
        if bad:
            mech_serious = [m for m in mech if not (m.startswith("long") or "several questions" in m)]
            if mech_serious or jd.get("verdict") not in ("PASS", "-", "FLAG"):
                sev = "serious"
            elif jd.get("verdict") == "FLAG":
                sev = "minor" if str(jd.get("severity", "")).lower() == "minor" else "serious"
            else:
                sev = "minor"
        fname = f"{lab}_cp{cpnum}_{slug(label)}__{slug(name)}_r{rep}.md"
        with open(os.path.join(out_dir, fname), "w") as f:
            f.write(f"# {lab} CP{cpnum} ({cptitle}): {label}\n\nModel: {name}, run {rep}\n\n")
            f.write(f"Mechanical flags: {', '.join(mech) or 'none'}\n\n")
            f.write(f"Judge: {jd.get('verdict')} {jd.get('rule', '')}: {jd.get('reason', '')}\n\n---\n")
            for who, t in tr:
                f.write(f"\n**{who}:**\n\n{t}\n")
        print(f"  {lab} CP{cpnum} {label:16} {name:40} {sev.upper() if bad else 'not run' if skipped else 'ok'}",
              flush=True)
        return (lab, cpnum, label, name, rep, mech, jd, fname, bad, skipped, sev)

    with ThreadPoolExecutor(max_workers=CONFIG.get("workers", 8)) as pool:
        rows = list(pool.map(do, jobs))
    total = len(rows)
    serious = sum(1 for r in rows if r[10] == "serious")
    minor = sum(1 for r in rows if r[10] == "minor")
    flagged = serious + minor
    not_run = sum(r[9] for r in rows)
    passed = total - flagged - not_run

    lines = [f"# AI Assist check, {stamp}", "",
             f"{total} answers: {passed} passed, {serious} serious flags, {minor} minor flags, {not_run} not run "
             f"(service errors or quota). Models: {', '.join(n for n, _ in models)}.", "",
             "⚠ serious: wrong facts, wrong grading, lab code, or an off-limits tool taught as the way to do it. "
             "△ minor: style and near-misses (bare numbers, naming a one-character fix, an extra related cause, "
             "length). Serious flags first, then minor, then answers that didn't run. Each file in this run's "
             "folder has the full conversation.", "",
             "| | Lab | CP | Prompt | Model | Mechanical | Judge | File |", "|---|---|---|---|---|---|---|---|"]
    rank = {"serious": 0, "minor": 1}
    order = sorted(rows, key=lambda r: (rank.get(r[10], 2 if r[9] else 3), r[0], r[1], r[2]))
    for lab, cp, label, name, rep, mech, jd, fname, bad, skipped, sev in order:
        verdict = "NOT RUN" if skipped else jd.get("verdict")
        if sev:
            verdict = f"{verdict} ({sev})"
        j = f"{verdict}: {jd.get('reason', '')}".replace("|", "/")
        icon = "⚠" if sev == "serious" else "△" if sev == "minor" else "○" if skipped else "✓"
        lines.append(f"| {icon} | {lab} | {cp} | {label} | {name} | "
                     f"{'; '.join(mech) or ''} | {j} | {fname} |")
    report = "\n".join(lines) + "\n"
    open(os.path.join(out_dir, "report.md"), "w").write(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
    print(f"\nReport: {os.path.join(out_dir, 'report.md')}  ({serious} serious, {minor} minor, "
          f"{not_run} not run, of {total})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
