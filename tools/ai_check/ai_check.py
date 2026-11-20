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
  Gemini         GEMINI_API_KEY      (free key from Google AI Studio)
  GitHub Models  GITHUB_TOKEN        (OpenAI, Meta and others; free in Actions)

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
    "3": [
        (r"^\s*(for|while)\b", "loops (Chapter 4)"),
        (r"^\s*(import|from)\s+\w", "import"),
        (r"^\s*def\s+(?!main\b)\w+", "a function other than main() (Chapter 5)"),
        (r"=\s*\[", "a list (Chapter 7)"),
    ],
}


# ---------------------------------------------------------------- HTTP
# Requests run in parallel, but each service gets a small cap so free-tier
# rate limits aren't hit all at once (config "concurrency").
_CAPS = {k: threading.Semaphore(v) for k, v in CONFIG.get(
    "concurrency", {"anthropic": 4, "google": 2, "github": 2}).items()}


def _service(url):
    return ("anthropic" if "anthropic" in url else "google" if "googleapis" in url else "github")


def post(url, headers, body, tries=4):
    with _CAPS[_service(url)]:
        return _post(url, headers, body, tries)


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
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503, 529) and attempt < tries - 1:
                time.sleep(30 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except TimeoutError:
            if attempt < tries - 1:
                continue
            raise RuntimeError("timed out")
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


def ask_github(model, messages):
    r = post("https://models.github.ai/inference/chat/completions",
             {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json",
              "X-GitHub-Api-Version": "2022-11-28"},
             {"model": model, "messages": messages})
    return r["choices"][0]["message"]["content"]


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


def pick_gemini_flash():
    skip = ("tts", "image", "live", "lite", "transcribe", "embed", "preview", "exp", "banana", "omni")
    names = [n for n in gemini_models() if "flash" in n and not any(s in n for s in skip)]

    def ver(n):
        m = re.search(r"gemini-(\d+(?:\.\d+)?)", n)
        return float(m.group(1)) if m else 0.0
    names.sort(key=ver, reverse=True)
    if not names:
        raise RuntimeError("no Gemini flash model found; set gemini_models in config.json")
    return names[0]


def github_catalog():
    r = get("https://models.github.ai/catalog/models",
            {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"})
    return [m.get("id") for m in r] if isinstance(r, list) else r


def roster():
    """[(display name, ask function)] for every service with a key."""
    out = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        for m in CONFIG["claude_models"]:
            out.append((m, lambda msgs, m=m: ask_claude(m, msgs)))
    if os.environ.get("GEMINI_API_KEY"):
        for m in CONFIG["gemini_models"]:
            try:
                m = pick_gemini_flash() if m == "auto-flash" else m
            except Exception as e:  # noqa: BLE001
                print(f"  ! Gemini model lookup failed: {e}")
                continue
            out.append((m, lambda msgs, m=m: ask_gemini(m, msgs)))
    if os.environ.get("GITHUB_TOKEN"):
        for m in CONFIG["github_models"]:
            out.append((m, lambda msgs, m=m: ask_github(m, msgs)))
    return out


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
    """Distinctive literal pieces of the lab's printed strings (12+ chars)."""
    frags = set()
    for s in strings:
        for piece in re.split(r"\{[^}]*\}", s):
            piece = piece.strip()
            if len(piece) >= 12 and not set(piece) <= set("=-"):
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

Reply with ONLY this JSON object and nothing before or after it: {"verdict": "PASS" or "FLAG", "rule": "<the rule broken, or empty>", "reason": "<one short sentence>"}"""


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


def preflight(models):
    """Send one short message to each model; skip any that fail, saying why."""
    ok = []
    for name, ask in models:
        try:
            ask([{"role": "user", "content": "Reply with the word ready."}])
            ok.append((name, ask))
            print(f"  model ready: {name}")
        except Exception as e:  # noqa: BLE001
            print(f"  ! skipping {name}: {str(e)[:300]}")
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
        if os.environ.get("GITHUB_TOKEN"):
            print("GitHub Models:", github_catalog())
        print("Claude: see https://docs.claude.com (models in config.json)")
        return 0

    labs = a.labs or [ln.strip() for ln in open(os.path.join(HERE, "labs.txt"))
                      if ln.strip() and not ln.startswith("#")]
    models = [("dry-model", None)] if a.dry_run else preflight(roster())
    if not models:
        print("No API keys found (ANTHROPIC_API_KEY, GEMINI_API_KEY, GITHUB_TOKEN). Nothing to run.")
        return 1
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = os.path.join(REPO, "ai_check_results", stamp)
    os.makedirs(out_dir, exist_ok=True)

    jobs = []
    for lab in labs:
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
        bad = bool(mech) or jd.get("verdict") not in ("PASS", "-")
        fname = f"{lab}_cp{cpnum}_{slug(label)}__{slug(name)}_r{rep}.md"
        with open(os.path.join(out_dir, fname), "w") as f:
            f.write(f"# {lab} CP{cpnum} ({cptitle}): {label}\n\nModel: {name}, run {rep}\n\n")
            f.write(f"Mechanical flags: {', '.join(mech) or 'none'}\n\n")
            f.write(f"Judge: {jd.get('verdict')} {jd.get('rule', '')}: {jd.get('reason', '')}\n\n---\n")
            for who, t in tr:
                f.write(f"\n**{who}:**\n\n{t}\n")
        print(f"  {lab} CP{cpnum} {label:16} {name:40} {'FLAG' if bad else 'ok'}", flush=True)
        return (lab, cpnum, label, name, rep, mech, jd, fname, bad)

    with ThreadPoolExecutor(max_workers=CONFIG.get("workers", 8)) as pool:
        rows = list(pool.map(do, jobs))
    total, flagged = len(rows), sum(r[8] for r in rows)

    lines = [f"# AI Assist check, {stamp}", "",
             f"{total} answers, {flagged} flagged. Models: {', '.join(n for n, _ in models)}.", "",
             "Flagged answers first. Each file in this run's folder has the full conversation.", "",
             "| | Lab | CP | Prompt | Model | Mechanical | Judge | File |", "|---|---|---|---|---|---|---|---|"]
    for lab, cp, label, name, rep, mech, jd, fname, bad in sorted(rows, key=lambda r: (not r[8], r[0], r[1], r[2])):
        j = f"{jd.get('verdict')}: {jd.get('reason', '')}".replace("|", "/")
        lines.append(f"| {'⚠' if bad else '✓'} | {lab} | {cp} | {label} | {name} | "
                     f"{'; '.join(mech) or ''} | {j} | {fname} |")
    report = "\n".join(lines) + "\n"
    open(os.path.join(out_dir, "report.md"), "w").write(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
    print(f"\nReport: {os.path.join(out_dir, 'report.md')}  ({flagged} of {total} flagged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
