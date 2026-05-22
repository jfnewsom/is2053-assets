# IS2053 Slide Decks

This directory holds the build scripts for every IS2053 slide deck.

## Layout

```
slides/
├── build_lib.py          shared deck-assembly library
├── README.md             this file
├── m1_u1/
│   └── build_m1_u1.py    per-deck script (M1-U1, "The Chapter 2 Toolkit")
├── m1_u2/                future deck
│   └── build_m1_u2.py
├── ...
├── week10/               legacy per-week PNG render scripts (Spring 2026 M4-U1)
│   └── render_week10.py
└── week11/               legacy per-week PNG render scripts (Spring 2026 M4-U2)
    └── render_week11.py
```

The `weekNN/` folders are the legacy convention from M4/M5 last semester:
they render the PNGs only, with deck assembly handled separately. The
`m<N>_<unit>/` folders are the current convention: a single `build_*.py`
script that renders PNGs **and** assembles the full deck end-to-end.

## How to build a deck

```bash
python3 slides/m1_u1/build_m1_u1.py
```

The script writes the finished `.pptx` to `/home/claude/M<N>-<unit>.pptx`
and the rendered PNGs to `/home/claude/m<N>_<unit>_pngs/`. Both paths
are configurable at the top of the per-deck script.

## How to create a new deck

```bash
cp -r slides/m1_u1 slides/m1_u2
mv slides/m1_u2/build_m1_u1.py slides/m1_u2/build_m1_u2.py
```

Then in the new script:

1. Update the path constants at the top (`OUTPUT_PPTX`, `PNG_OUT`, `WORK_DIR`).
2. Replace every `deck.add_*_slide(...)` call's content with the new deck's
   content. The order of calls determines slide order in the final deck.
3. Run it.

The first call should always be `deck.add_title_slide(...)`. Per the locked
deck-build rules, every deck opens with the title-slide layout.

## What the library provides

`build_lib.py` exposes:

- `DeckBuilder(template, png_out, work)` - the orchestrator.
- `add_title_slide(main_title, subtitle, notes)` - template layout 1.
- `add_narrative_slide(title, section_label, bold_oneliner, body, notes)` - layout 33.
- `add_concept_slide(title, bullets, notes)` - layout 2 (up to 5 bullets).
- `add_demo_slide(title, code, png, notes)` - layout 3 (renders + inserts code PNG).
- `add_output_slide(title, output_text, png, notes)` - layout 4 (renders + inserts output PNG).
- `add_two_column_slide(title, left_label, left_bullets, right_label, right_bullets, notes)` - layout 23.
- `add_overview_slide(title, section1_label, section1_body, section2_body, section3_label, section3_body, notes)` - layout 20.
- `format_concept_notes(video_script, key_terms, think_about, source_url)` - composes speaker notes.
- `format_demo_notes(code, instructor_notes)` - composes demo speaker notes.
- `format_output_notes(output_text, instructor_notes)` - composes output speaker notes.
- `format_title_notes(deck_id, deck_title, opening_line)` - composes title speaker notes.

## How it works

1. **Unpack.** The template `.pptx` (default: `ppt/IS2053_Template_v2.pptx`)
   is unzipped into a working directory.
2. **Duplicate.** Each `add_*_slide` call uses `pptx/scripts/add_slide.py`
   to duplicate the appropriate template layout into the slide sequence.
3. **Populate.** Text is substituted into the duplicated slide's XML via
   targeted string replacements against known placeholder text. (The
   placeholder text strings are defined in `build_lib.PH`. If the template
   gets re-authored, update `PH` to match the new placeholder text.)
4. **Render PNGs.** Demo and output slides call `render_code()` /
   `render_output()` from `tools/render_slides.py` to produce the
   Bat City Noir code/output PNGs. Empty label string is used (no corner
   caption on the PNG).
5. **Pack.** The unpacked deck is re-zipped via `pptx/scripts/office/pack.py`.
6. **Inject notes and PNGs.** The packed deck is opened with `python-pptx`,
   speaker notes are written to the notes pane of each slide, and the
   rendered PNGs are placed on demo/output slides at the template's
   prescribed position (`x=0.90"`, `y=1.90"`, `w=11.53"`). Placeholder
   textboxes ("CODE DEMO", "EXPECTED OUTPUT", "[ PNG GOES HERE ]", and
   the placement-instruction text) are removed so they don't peek through
   the PNG's rounded corners.
7. **Save.** Final `.pptx` written to `OUTPUT_PPTX`.

## Conventions (locked)

- **Slide naming.** Filenames are `M<N>-<unit>_<deck_type>.pptx`. Examples:
  `M1-U1.pptx`, `M3-L2.pptx`. Student-facing references say "Module 1,
  Unit 1" and "Lab 1.1".
- **Slide titles.** Concept, narrative, two-column, and overview slides
  use just the topic title; no "Slide N:" prefix anywhere. Demo and output
  slides keep their `Demo:` and `Output:` prefix per template convention.
- **PNG labels.** Empty string. The slide title identifies the PNG; the
  template doesn't need an additional corner caption.
- **Speaker notes.** Mandatory on every slide. Composed from the slide
  guide markdown's Video Script, Key Terms, Think About This, and Source
  URL blocks via the `format_*_notes` helpers.
- **Em-dashes.** Banned in all slide content and speaker notes. Use colons.

## Slide guide markdown

The human-readable slide guide markdown (e.g.,
`IS2053_<YYYY-MM-DD>_M1-U1_Slide_Guide.md`) is the source-of-truth document
that gets reviewed before the script is written. The build script is a
direct Python translation of the slide guide. They are kept in sync
manually; the build script does not consume the markdown.

## Per-deck script anatomy

See `m1_u1/build_m1_u1.py` for the canonical example. The shape is:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build_lib import DeckBuilder, format_concept_notes, ...

def main():
    deck = DeckBuilder(png_out=..., work=...)
    deck.add_title_slide(...)
    deck.add_narrative_slide(...)
    deck.add_concept_slide(...)
    # ... etc ...
    deck.save('/home/claude/M1-U1.pptx')

if __name__ == '__main__':
    main()
```

Content (bullets, video scripts, code blocks, output text, key terms,
questions, source URLs) all live inline in the per-deck script as Python
string literals. The library does no parsing of external files.
