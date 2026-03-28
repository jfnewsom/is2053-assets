"""
render_week10.py — Week 10 slide PNGs
Module 4, Week 1 | Chapter 8: More About Strings

HOW TO USE THIS TEMPLATE FOR FUTURE WEEKS
------------------------------------------
1. Copy this file into slides/weekNN/
2. Update OUT_DIR
3. Replace the render_code() / render_output() calls with your content
4. Run:  python3 slides/weekNN/render_weekNN.py
5. PNGs appear in OUT_DIR — drag into Keynote

The engine (render_slides.py) and fonts live in tools/.
This script fetches them automatically from the repo if not present locally.
"""

import os
import sys
import urllib.request
import json
import base64

# ── Bootstrap: locate tools/ two levels up (repo root → tools/) ──
_REPO      = "jfnewsom/is2053-assets"
_TOOLS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools")
)
_ENGINE    = os.path.join(_TOOLS_DIR, "render_slides.py")


def _fetch_file(repo_path, local_path):
    url = f"https://api.github.com/repos/{_REPO}/contents/{repo_path}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(base64.b64decode(data["content"]))
    print(f"  fetched {os.path.basename(local_path)} from repo")


if not os.path.exists(_ENGINE):
    _fetch_file("tools/render_slides.py", _ENGINE)

sys.path.insert(0, _TOOLS_DIR)
from render_slides import render_code, render_output  # noqa: E402

# ── Output directory ───────────────────────────────────────────────
OUT = "/home/claude/week10_pngs"

# ═══════════════════════════════════════════════════════════════════
# SLIDE CONTENT
# ═══════════════════════════════════════════════════════════════════

def main():
    print("Rendering Week 10 PNGs...\n")

    # ── Slide 4a: Input Handling — Before ───────────────────────
    render_code(
        code="""\
# BEFORE: checking both cases manually, every single time

answer = input('Keep playing? (y/n): ')
if answer == 'y' or answer == 'Y':
    keep_playing = True

choice = input('A) Dallas  B) Houston: ')
if choice == 'A' or choice == 'a':
    destination = 'Dallas'
elif choice == 'B' or choice == 'b':
    destination = 'Houston'

confirm = input('Are you sure? (yes/no): ')
if confirm == 'yes' or confirm == 'Yes' or confirm == 'YES':
    print('Confirmed!')
""",
        label="Slide 4a – Input Handling: Before (.upper() doesn't exist yet)",
        filename="slide04a_input_before.png",
        out_dir=OUT,
    )

    # ── Slide 4b: Input Handling — After ────────────────────────
    render_code(
        code="""\
# AFTER: .upper() normalizes the input — one check each

answer = input('Keep playing? (y/n): ').upper()
if answer == 'Y':
    keep_playing = True

choice = input('A) Dallas  B) Houston: ').upper()
if choice == 'A':
    destination = 'Dallas'
elif choice == 'B':
    destination = 'Houston'

confirm = input('Are you sure? (yes/no): ').upper()
if confirm == 'YES':
    print('Confirmed!')
""",
        label="Slide 4b – Input Handling: After (.upper() to the rescue)",
        filename="slide04b_input_after.png",
        out_dir=OUT,
    )

    # ── Slide 4c: Output ─────────────────────────────────────────
    render_output(
        text="""\
Keep playing? (y/n): Y
A) Dallas  B) Houston: a
Are you sure? (yes/no): yes
Confirmed!

Keep playing? (y/n): y
A) Dallas  B) Houston: A
Are you sure? (yes/no): YES
Confirmed!
""",
        label="Slide 4c – Expected Output (both versions, same result)",
        filename="slide04c_input_output.png",
        out_dir=OUT,
    )

    # ── Slide 6: .strip() ───────────────────────────────────────
    render_code(
        code="""\
# .strip() removes leading and trailing whitespace

raw   = '   San Antonio   '
clean = raw.strip()
print(f'Before: "{raw}"')
print(f'After:  "{clean}"')

# lstrip / rstrip — one side only
left_only  = raw.lstrip()   # 'San Antonio   '
right_only = raw.rstrip()   # '   San Antonio'

# Always strip user input before comparing
city = input('Enter city: ').strip()
if city == 'Austin':
    print('Heading to the capital!')
""",
        label="Slide 6 – .strip(), .lstrip(), .rstrip()",
        filename="slide06_strip.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Before: "   San Antonio   "
After:  "San Antonio"

Enter city:  Austin 
Heading to the capital!
""",
        label="Slide 6b – Expected Output",
        filename="slide06b_strip_output.png",
        out_dir=OUT,
    )

    # ── Slide 8: String Testing Methods ─────────────────────────
    render_code(
        code="""\
# Testing methods — each returns True or False

samples = ['Austin', '42', '3.14', 'abc123', '   ']

for s in samples:
    print(f'"{s}"')
    print(f'  isalpha():  {s.isalpha()}')
    print(f'  isdigit():  {s.isdigit()}')
    print(f'  isalnum():  {s.isalnum()}')
    print(f'  isspace():  {s.isspace()}')
    print()
""",
        label="Slide 8 – String Testing Methods",
        filename="slide08_testing.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
"Austin"
  isalpha():  True
  isdigit():  False
  isalnum():  True
  isspace():  False

"42"
  isalpha():  False
  isdigit():  True
  isalnum.:  True
  isspace():  False

"3.14"
  isalpha():  False
  isdigit():  False
  isalnum():  False
  isspace():  False
""",
        label="Slide 8b – Expected Output",
        filename="slide08b_testing_output.png",
        out_dir=OUT,
    )

    # ── Slide 10: Searching ──────────────────────────────────────
    render_code(
        code="""\
city = 'San Antonio, Texas'

# in — True/False substring check
print('Antonio' in city)        # True
print('Houston' in city)        # False

# .find() — returns index, or -1 if not found
print(city.find('Texas'))       # 13
print(city.find('Dallas'))      # -1

# .startswith() / .endswith()
print(city.startswith('San'))   # True
print(city.endswith('Texas'))   # True

# .count() — how many times does it appear?
print(city.count('a'))          # 3
""",
        label="Slide 10 – Searching: in, .find(), .startswith(), .endswith(), .count()",
        filename="slide10_searching.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
True
False
13
-1
True
True
3
""",
        label="Slide 10b – Expected Output",
        filename="slide10b_searching_output.png",
        out_dir=OUT,
    )

    # ── Slide 12: .replace() and Character Iteration ─────────────
    render_code(
        code="""\
# .replace(old, new) — returns a NEW string every time

route    = 'SAT -> HOU -> GAL'
expanded = route.replace('SAT', 'San Antonio')
expanded = expanded.replace('HOU', 'Houston')
expanded = expanded.replace('GAL', 'Galveston')
print(expanded)

# Iterate character by character — count vowels in a city name
city        = 'Galveston'
vowel_count = 0
for ch in city:
    if ch.lower() in 'aeiou':
        vowel_count += 1
print(f'{city} has {vowel_count} vowels')
""",
        label="Slide 12 – .replace() and Character Iteration",
        filename="slide12_replace_iterate.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
San Antonio -> Houston -> Galveston
Galveston has 3 vowels
""",
        label="Slide 12b – Expected Output",
        filename="slide12b_replace_iterate_output.png",
        out_dir=OUT,
    )

    # ── Slide 14a: .split() ──────────────────────────────────────
    render_code(
        code="""\
# .split() — no argument splits on whitespace
sentence = 'Deep in the Heart of Texas'
words    = sentence.split()
print(words)
print(f'Word count: {len(words)}')

# .split(delimiter) — split on a specific character
route  = 'San Antonio,Houston,Galveston'
cities = route.split(',')
print(cities)
print(f'First city: {cities[0]}')
print(f'Last city:  {cities[2]}')
""",
        label="Slide 14a – .split() and .split(delimiter)",
        filename="slide14a_split.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
['Deep', 'in', 'the', 'Heart', 'of', 'Texas']
Word count: 6
['San Antonio', 'Houston', 'Galveston']
First city: San Antonio
Last city:  Galveston
""",
        label="Slide 14b – Expected Output",
        filename="slide14b_split_output.png",
        out_dir=OUT,
    )

    # ── Slide 16: CSV Parsing ─────────────────────────────────────
    render_code(
        code="""\
# The full CSV parsing pattern — strip, split, convert

trip_data = [
    'Maria,San Antonio,Galveston,356,5',
    'Carlos,San Antonio,Corpus Christi,150,3',
    'Priya,San Antonio,Dallas,280,4',
]

for line in trip_data:
    fields      = line.strip().split(',')
    name        = fields[0]
    start       = fields[1]
    destination = fields[2]
    miles       = int(fields[3])
    turns       = int(fields[4])
    print(f'{name}: {start} to {destination} — {miles} miles in {turns} turns')
""",
        label="Slide 16 – CSV Parsing Pattern",
        filename="slide16_csv.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Maria: San Antonio to Galveston — 356 miles in 5 turns
Carlos: San Antonio to Corpus Christi — 150 miles in 3 turns
Priya: San Antonio to Dallas — 280 miles in 4 turns
""",
        label="Slide 16b – Expected Output",
        filename="slide16b_csv_output.png",
        out_dir=OUT,
    )

    # ── Slide 18: Method Chaining / clean_input() ────────────────
    render_code(
        code="""\
# Method chaining — the clean_input() function
# This goes in function_library.py

def clean_input(prompt):
    return input(prompt).strip().upper()

# Now every input check in the game is clean
answer  = clean_input('Keep playing? (y/n): ')
choice  = clean_input('A) Dallas  B) Houston: ')
confirm = clean_input('Are you sure? (yes/no): ')

if answer == 'Y':
    print('Continuing the trip!')
if choice == 'A':
    print('Heading to Dallas!')
if confirm == 'YES':
    print('All confirmed. Buckle up.')
""",
        label="Slide 18 – Method Chaining and clean_input()",
        filename="slide18_chaining.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Keep playing? (y/n):  y 
A) Dallas  B) Houston:  a 
Are you sure? (yes/no):  yes 
Continuing the trip!
Heading to Dallas!
All confirmed. Buckle up.
""",
        label="Slide 18b – Expected Output (spaces and lowercase handled automatically)",
        filename="slide18b_chaining_output.png",
        out_dir=OUT,
    )

    print(f"\nDone. {len(os.listdir(OUT))} PNGs in {OUT}")


if __name__ == "__main__":
    main()
