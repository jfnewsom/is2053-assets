"""
render_week11.py — Week 11 slide PNGs
Module 4, Week 2 | Chapter 9: Dictionaries and Sets

HOW TO USE
----------
Run from the repo root:
    python3 slides/week11/render_week11.py

PNGs are written to OUT (default: ~/Desktop/week11_pngs).
Drag them into your Keynote deck.

CONTINUATION SLIDES
-------------------
Any demo with more than 13 lines of code is split across two slides.
The continuation slide filename ends in _cont.png and opens with
# (continued) so the split is clear in the deck.

The engine (render_slides.py) and fonts live in tools/.
This script locates them automatically via the repo structure.
"""

import os
import sys
import urllib.request
import json
import base64

# ── Bootstrap: locate tools/ two levels up (slides/week11/ → tools/) ──
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
OUT = os.path.expanduser("~/Desktop/week11_pngs")

# ═══════════════════════════════════════════════════════════════════
# SLIDE CONTENT
# ═══════════════════════════════════════════════════════════════════

def main():
    print("Rendering Week 11 PNGs...\n")

    # ── Slides 5 / 5-cont / 6 — Dictionary Basics ────────────────
    # 16 lines total → split after line 8 (after first print)

    render_code(
        code="""\
# Chapter 9 — Dictionary basics
city_taglines = {
    'San Antonio': 'Home of the Alamo',
    'Austin':      'Keep Austin Weird',
    'Houston':     'Space City',
}

print(city_taglines['Austin'])\
""",
        label="Slide 5 — Dictionary Basics",
        filename="slide05_dict_basics.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued)
city_taglines['El Paso'] = 'Sun City'
print(f'{len(city_taglines)} cities in dictionary')

if 'Dallas' in city_taglines:
    print('Dallas found.')
else:
    print('Dallas not here yet.')\
""",
        label="Slide 5 (cont.) — Dictionary Basics",
        filename="slide05_dict_basics_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Keep Austin Weird
4 cities in dictionary
Dallas not here yet.\
""",
        label="Slide 6 — Dictionary Basics Output",
        filename="slide05b_dict_basics_output.png",
        out_dir=OUT,
    )

    # ── Slides 8 / 8-cont / 9 — Nested Dictionary ────────────────
    # 15 lines total → split after line 9 (after first access pair)

    render_code(
        code="""\
# Chapter 9 — Nested dictionary
CITY_DISTANCES = {
    'San Antonio': {'Houston': 200, 'Austin': 80},
    'Houston':     {'Galveston': 50, 'Dallas': 240},
    'Austin':      {'Dallas': 200, 'Fort Worth': 190},
}

dist = CITY_DISTANCES['San Antonio']['Houston']
print(f'SA to Houston: {dist} miles')\
""",
        label="Slide 8 — Nested Dictionary",
        filename="slide08_nested_dict.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued)
dist2 = CITY_DISTANCES['Houston']['Dallas']
print(f'Houston to Dallas: {dist2} miles')

safe = CITY_DISTANCES['San Antonio'].get('Waco', -1)
print(f'SA to Waco: {safe}')\
""",
        label="Slide 8 (cont.) — Nested Dictionary",
        filename="slide08_nested_dict_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
SA to Houston: 200 miles
Houston to Dallas: 240 miles
SA to Waco: -1\
""",
        label="Slide 9 — Nested Dictionary Output",
        filename="slide08b_nested_dict_output.png",
        out_dir=OUT,
    )

    # ── Slides 11 / 11-cont / 12 — Dictionary Methods ────────────
    # 14 lines total → split after line 9 (after .keys() section)

    render_code(
        code="""\
# Chapter 9 — .keys()  .values()  .items()
CITY_DISTANCES = {
    'San Antonio': {'Houston': 200, 'Austin': 80},
    'Houston':     {'Galveston': 50, 'Dallas': 240},
}

print('Keys:')
for city in CITY_DISTANCES.keys():
    print(f'  {city}')\
""",
        label="Slide 11 — Dictionary Methods",
        filename="slide11_dict_methods.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued)
print()
print('All routes:')
for city, routes in CITY_DISTANCES.items():
    for dest, miles in routes.items():
        print(f'  {city} -> {dest}: {miles} miles')\
""",
        label="Slide 11 (cont.) — Dictionary Methods",
        filename="slide11_dict_methods_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Keys:
  San Antonio
  Houston

All routes:
  San Antonio -> Houston: 200 miles
  San Antonio -> Austin: 80 miles
  Houston -> Galveston: 50 miles
  Houston -> Dallas: 240 miles\
""",
        label="Slide 12 — Dictionary Methods Output",
        filename="slide11b_dict_methods_output.png",
        out_dir=OUT,
    )

    # ── Slides 14 / 14-cont / 15 — Dynamic Menu ──────────────────
    # 15 lines total → split after line 11 (after both dicts defined)

    render_code(
        code="""\
# Chapter 9 — Dynamic menu
CITY_DISTANCES = {
    'San Antonio': {'Houston': 200, 'Austin': 80,
                    'Corpus Christi': 150, 'Laredo': 160}
}
MARKERS = {
    'Houston':        '',
    'Austin':         '',
    'Corpus Christi': '  [BEACH!]',
    'Laredo':         '  [Dead End]',
}\
""",
        label="Slide 14 — Dynamic Menu",
        filename="slide14_dynamic_menu.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued — generate the menu)
option = 1
for dest, miles in CITY_DISTANCES['San Antonio'].items():
    print(f'  {option}. {dest} - {miles} miles{MARKERS[dest]}')
    option += 1\
""",
        label="Slide 14 (cont.) — Dynamic Menu",
        filename="slide14_dynamic_menu_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
  1. Houston - 200 miles
  2. Austin - 80 miles
  3. Corpus Christi - 150 miles  [BEACH!]
  4. Laredo - 160 miles  [Dead End]\
""",
        label="Slide 15 — Dynamic Menu Output",
        filename="slide14b_dynamic_menu_output.png",
        out_dir=OUT,
    )

    # ── Slides 17 / 17-cont / 18 — Safe .get() Lookups ──────────
    # 14 lines total → split after line 8 (after bracket access demo)

    render_code(
        code="""\
# Chapter 9 — Safe lookups with .get()
CITY_DISTANCES = {
    'San Antonio': {'Houston': 200, 'Austin': 80}
}

# Bracket notation — KeyError if key missing
dist = CITY_DISTANCES['San Antonio']['Houston']
print(f'SA to Houston: {dist} miles')\
""",
        label="Slide 17 — Safe .get() Lookups",
        filename="slide17_get_method.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued)
# .get() — returns default, no crash
known   = CITY_DISTANCES['San Antonio'].get('Austin', -1)
missing = CITY_DISTANCES['San Antonio'].get('Waco',   -1)
print(f'SA to Austin:  {known}')
print(f'SA to Waco:    {missing}  <- not found, no crash')\
""",
        label="Slide 17 (cont.) — Safe .get() Lookups",
        filename="slide17_get_method_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
SA to Houston: 200 miles
SA to Austin:  80
SA to Waco:    -1  <- not found, no crash\
""",
        label="Slide 18 — Safe .get() Output",
        filename="slide17b_get_method_output.png",
        out_dir=OUT,
    )

    # ── Slides 20 / 20-cont / 21 — Set Basics ────────────────────
    # 15 lines total → split after line 9 (after .add() + count)

    render_code(
        code="""\
# Chapter 9 — Set basics
visited = set()              # empty set — NOT {}
visited.add('San Antonio')
visited.add('Houston')
visited.add('Houston')       # duplicate — silently ignored
visited.add('Austin')
visited.add('Corpus Christi')

print(f'Unique city count: {len(visited)}')\
""",
        label="Slide 20 — Set Basics",
        filename="slide20_set_basics.png",
        out_dir=OUT,
    )

    render_code(
        code="""\
# (continued)
if 'Dallas' not in visited:
    print('Not been to Dallas.')

for city in sorted(visited):
    print(f'  - {city}')\
""",
        label="Slide 20 (cont.) — Set Basics",
        filename="slide20_set_basics_cont.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Unique city count: 4
Not been to Dallas.
  - Austin
  - Corpus Christi
  - Houston
  - San Antonio\
""",
        label="Slide 21 — Set Basics Output",
        filename="slide20b_set_basics_output.png",
        out_dir=OUT,
    )

    # ── Slides 23 / 24 — Set Operations (13 lines — fits in one) ─

    render_code(
        code="""\
# Chapter 9 — Set operations
baseball   = {'Jodi', 'Carmen', 'Aida', 'Alicia'}
basketball = {'Eva',  'Carmen', 'Alicia', 'Sarah'}

union = baseball.union(basketball)
inter = baseball.intersection(basketball)
diff  = baseball.difference(basketball)
sym   = baseball.symmetric_difference(basketball)

print('Union:    ', sorted(union))
print('Intersect:', sorted(inter))
print('Diff:     ', sorted(diff))
print('Sym diff: ', sorted(sym))\
""",
        label="Slide 23 — Set Operations",
        filename="slide23_set_operations.png",
        out_dir=OUT,
    )

    render_output(
        text="""\
Union:     ['Aida', 'Alicia', 'Carmen', 'Eva', 'Jodi', 'Sarah']
Intersect: ['Alicia', 'Carmen']
Diff:      ['Aida', 'Jodi']
Sym diff:  ['Aida', 'Eva', 'Jodi', 'Sarah']\
""",
        label="Slide 24 — Set Operations Output",
        filename="slide23b_set_operations_output.png",
        out_dir=OUT,
    )

    print(f"\nDone! 20 PNGs written to: {OUT}")


if __name__ == "__main__":
    main()
