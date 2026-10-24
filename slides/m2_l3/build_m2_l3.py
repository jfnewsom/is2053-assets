"""
build_m2_l3.py - M2-L3 ("Lab 2.3: Road Trip Ready") walkthrough deck.

Module 2, Lab 3 (MASTER) | walks six checkpoints.

Source-of-truth chain (do not invert):
  1. Modules/mod2/lab-2-3.py          - bedrock main game code
  2. Modules/mod2/function_library.py - bedrock library code
  3. pages/labs/json/lab-2-3.json     - student-facing assignment
  4. This deck (downstream)

Checkpoint plan (Oct 22, 2026, John's call): the deck follows the Spring
2027 Build List Addendum, items A.1 to A.3, not the five checkpoints on
the current sheet.
  - A.1: a new CP4 "Keep the Trip Going" sits between Validate Menu Input
    and Play Again. It builds the multi-leg game the Final Check, the
    Message Digest, the solution, and Lab 3.1 all assume. The current
    sheet's checkpoints build a one-trip game (Lab 2.3 findings D-1).
  - A.2: the menu prompt is 'Choice (1-3): ' everywhere.
  - A.3: no claim that the title-case beach line "fails a test", and no
    Austin menu (its 'Choice (1-1): ' branch is unreachable).
  Until the sheet gets the same changes, this deck is one checkpoint
  ahead of it.

Deck conventions (Oct 2026):
  - Every slide carries a VIDEO SCRIPT. Scripts are written to be spoken:
    contractions, no em-dashes, Oxford comma, no dates, no grading-weight
    claims, and code narrated per the Code Narration Standard.
  - Code and output panels hold at most 13 lines. Code lines are at most
    79 characters, output lines at most 100. The build stops if not.
  - Demo notes say "CODE ON SCREEN (complete as shown):". Nothing tells
    the instructor to type live.
  - Every output panel is a verbatim slice of a real run. CP1 and CP2 come
    from the library's test bench; CP4 to CP6 come from the solution run
    under the CodeGrade fixture (randint gives 1 when its upper bound is
    9 or less, otherwise 15) with inputs
    TestPlayer, 2, y, 1, y, 1, n.
  - The build also writes the narration file: one paragraph per slide,
    each starting with "[short pause]", no slide numbers. ElevenLabs
    exports one MP3 per paragraph, so MP3 N is slide N.

USAGE
-----
    python3 slides/m2_l3/build_m2_l3.py

Set IS2053_OUT to choose the output folder (default /home/claude).
"""
import os
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu

# ----- Bootstrap: make slides/build_lib.py importable -----
SLIDES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SLIDES_DIR))

from build_lib import (  # noqa: E402
    DeckBuilder,
    format_concept_notes,
    format_output_notes,
)

# ----- Outputs -----
OUT_DIR = Path(os.environ.get('IS2053_OUT', '/home/claude'))
OUTPUT_PPTX = str(OUT_DIR / 'IS2053_2026-10-22_M2-L3_Deck.pptx')
OUTPUT_TTS = str(OUT_DIR / 'IS2053_2026-10-22_M2-L3_TTS.txt')
PNG_OUT = str(OUT_DIR / 'm2_l3_pngs')
WORK_DIR = '/tmp/build_m2_l3'

# ----- Panel limits -----
MAX_LINES = 13
MAX_CODE_COLS = 79
MAX_OUTPUT_COLS = 100
MAX_STORY_WORDS = 75

TTS = []


def say(script):
    """Record one slide's narration for the TTS file and return it."""
    TTS.append('[short pause] ' + ' '.join(script.split()))
    return script


def check_panel(kind, title, text):
    lines = text.rstrip('\n').split('\n')
    cols = MAX_CODE_COLS if kind == 'code' else MAX_OUTPUT_COLS
    if len(lines) > MAX_LINES:
        raise SystemExit(f'{title}: {len(lines)} lines (max {MAX_LINES})')
    wide = [ln for ln in lines if len(ln) > cols]
    if wide:
        raise SystemExit(f'{title}: line over {cols} chars: {wide[0]!r}')


def code_notes(code, instructor_notes):
    """Demo-slide notes. The code on screen is complete as shown."""
    return (
        f'CODE ON SCREEN (complete as shown):\n\n{code.strip()}\n\n\n'
        f'INSTRUCTOR NOTES\n\n{instructor_notes.strip()}'
    )


def title_notes(deck_id, deck_title, opening_line):
    return (
        f'TITLE SLIDE: {deck_id}: {deck_title}\n\n'
        'This is the cold open. Brief greeting, name the unit, then '
        'advance.\n\n'
        f'Suggested opening line:\n{opening_line}'
    )


def demo(deck, title, code, png, script, instructor, key_terms=None,
         think=None):
    check_panel('code', title, code)
    notes = (format_concept_notes(say(script), key_terms, think)
             + '\n\n\n' + code_notes(code, instructor))
    deck.add_demo_slide(title=title, code=code, png=png, notes=notes)


def output(deck, title, text, png, script, instructor, key_terms=None,
           think=None):
    check_panel('output', title, text)
    notes = (format_concept_notes(say(script), key_terms, think)
             + '\n\n\n' + format_output_notes(text, instructor))
    deck.add_output_slide(title=title, output_text=text, png=png,
                          notes=notes)


def concept(deck, title, bullets, script, key_terms=None, think=None,
            source_url=None):
    if not 3 <= len(bullets) <= 5:
        raise SystemExit(f'{title}: {len(bullets)} key points')
    deck.add_concept_slide(
        title=title, bullets=bullets,
        notes=format_concept_notes(say(script), key_terms, think,
                                   source_url))


# ----- Post-processing (same fixes as the Module 4 pipeline) -----
GREEN = RGBColor(0x39, 0xFF, 0x14)
MONO = 'Roboto Mono'


def _restyle_backticks(p):
    """Render `code` spans in green Roboto Mono and drop the backticks."""
    full = ''.join(r.text for r in p.runs)
    if '`' not in full:
        return
    base = p.runs[0].font
    name, size, bold = base.name, base.size, base.bold
    try:
        color = base.color.rgb
    except Exception:
        color = None
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    for i, seg in enumerate(full.split('`')):
        if seg == '':
            continue
        run = p.add_run()
        run.text = seg
        f = run.font
        if size is not None:
            f.size = size
        if bold is not None:
            f.bold = bold
        if i % 2 == 1:
            f.name = MONO
            f.color.rgb = GREEN
        else:
            if name:
                f.name = name
            if color is not None:
                f.color.rgb = color


def _fix_narrative(slide):
    """Template v2 overlaps the story one-liner and body. Separate them."""
    labels = [sh.text_frame.text.strip() for sh in slide.shapes
              if sh.has_text_frame]
    if 'THE STORY' not in labels:
        return
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        top_in = sh.top / 914400 if sh.top is not None else 0
        if 2.5 < top_in < 2.95:
            sh.height = Emu(int(0.95 * 914400))
        elif 3.1 < top_in < 3.5:
            sh.top = Emu(int(3.78 * 914400))
            sh.height = Emu(int(2.95 * 914400))


def postprocess(path):
    prs = Presentation(path)
    for s in prs.slides:
        _fix_narrative(s)
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if 'Spring 2026' in r.text:
                        r.text = r.text.split('Spring 2026')[0].rstrip(
                            ' •')
                _restyle_backticks(p)
    prs.save(path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 2.3: Road Trip Ready',
        subtitle='IS2053 Programming I  •  Module 2  •  Lab Walkthrough',
        notes=title_notes('M2-L3', 'Lab 2.3: Road Trip Ready', say(
            "Welcome to your Lab 2.3 walkthrough. This is the MASTER lab for "
            "Module 2, and it's where your road trip grows up. The game stops "
            "trusting whatever the player types, it keeps going after the "
            "first city, and it lets you play as many trips as you want. Six "
            "checkpoints. Let's take them one at a time."
        )),
    )

    # =========================================================================
    # SLIDE 2: The story
    # =========================================================================
    story_body = (
        "Everything from Lab 2.2 stays: the menu, the coin flip gate, the D20 "
        "travel, and the hazards. Two library functions make the input "
        "trustworthy. Then the game learns to keep going: arrive in Houston "
        "and you can drive on to Galveston. Finally, the whole game repeats "
        "for as long as you want to play, and a session report adds up every "
        "trip."
    )
    if len(story_body.split()) > MAX_STORY_WORDS:
        raise SystemExit('Story body is over the word limit')
    deck.add_narrative_slide(
        title='One Trip Becomes a Road Trip',
        section_label='THE STORY',
        bold_oneliner='Lab 2.2 drove one leg. Lab 2.3 drives the whole trip.',
        body=story_body,
        notes=format_concept_notes(
            say(
                "Here's the shape of the finished program, because the shape "
                "is really the lesson. There are three loops, each one inside "
                "the next. The outer loop is the session. It runs one game "
                "after another until you say you're done. Inside it is one "
                "game, and a game can have several legs, like San Antonio to "
                "Houston and then Houston to Galveston. And inside each leg is "
                "the travel loop you already built, rolling the die turn by "
                "turn. The first two checkpoints add two small functions to "
                "your library. Checkpoint 3 puts the first one to work at the "
                "menu. Checkpoint 4 builds the in-game loop, Checkpoint 5 "
                "wraps everything in a play-again loop, and Checkpoint 6 keeps "
                "score across the whole session. Hold on to that picture of "
                "three loops, one inside the next, and every checkpoint has an "
                "obvious home."
            ),
            key_terms=[
                ('Nested loop', 'A loop that runs inside the body of another '
                 'loop. The inner loop finishes all of its passes for each '
                 'single pass of the outer loop.'),
                ('Leg', 'One drive between two cities. A game can have '
                 'several legs.'),
            ],
            think_about=[
                "Where in your Lab 2.2 game does the program just trust "
                "whatever the player types?",
                "What's the difference between one game and one session?",
            ],
            source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
        ),
    )

    # =========================================================================
    # SLIDE 3: CP1 and CP2 concept
    # =========================================================================
    concept(
        deck, 'Checkpoints 1 and 2: Expand the Library',
        [
            "Two new functions join `function_library.py`: `get_valid_int` "
            "and `get_yes_no`.",
            "Each one asks once, then loops until the answer is acceptable.",
            "`get_valid_int` hands back a whole number inside the range you "
            "pass in.",
            "`get_yes_no` hands back `True` or `False`, never the letter "
            "typed.",
            "A `main()` test bench lets you try both before the game uses "
            "them.",
        ],
        "The first two checkpoints both happen in your function library, "
        "and they use the same pattern, so let's take them together. It's "
        "the input validation loop from Chapter 4. You ask once before the "
        "loop, which is called the priming read. Then a while loop checks "
        "the answer, and as long as it isn't acceptable, the loop prints an "
        "error and asks again. When the answer's finally good, the loop ends "
        "and the function hands it back. The get valid int function protects "
        "the number menus. The get yes no function protects every yes or no "
        "question. Why put them in the library instead of in the game? "
        "Because the game needs them in several places, and anything you'll "
        "reuse belongs in the library from day one. Your game stays "
        "readable, and the fussy re-asking stays tucked out of sight.",
        key_terms=[
            ('Priming read', 'The first input, taken before a validation loop '
             'starts, so the loop has something to check.'),
            ('Input validation loop', 'A loop that keeps asking until the '
             'input meets a condition.'),
            ('Boolean', 'A value that is either True or False.'),
        ],
        think=[
            "What does a validation function promise about the value it hands "
            "back?",
            "Why is it easier to test these functions on their own than inside "
            "the game's menu?",
        ],
        source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
    )

    # =========================================================================
    # SLIDE 4: CP1 demo - get_valid_int
    # =========================================================================
    demo(
        deck, 'Demo: get_valid_int()',
        r'''def get_valid_int(prompt, min_val, max_val):
    """Get a valid integer from the user within a range."""
    value = int(input(prompt))

    while value < min_val or value > max_val:
        print(f'ERROR: Enter a number between {min_val} and {max_val}.')
        value = int(input(prompt))

    return value
''',
        'slide04_get_valid_int.png',
        "Here's the get valid int function. It takes three things: the "
        "prompt to show, the smallest number allowed, and the largest. First "
        "comes the priming read. We ask with the prompt, convert the answer "
        "to a whole number, and assign it to value. Then the while loop asks "
        "a question: is the value below the minimum, or above the maximum? "
        "If either one is true, the number's out of range, so we print an "
        "error that names the allowed range, and ask again. Notice that "
        "second read inside the loop. Without it, value never changes and "
        "the loop never ends. The moment the value lands in range, the "
        "condition's false, we drop out of the loop, and the function hands "
        "back value. And if the very first answer is fine? The loop body "
        "never runs at all. Give the function a docstring that explains all "
        "three parameters, the same way your other library functions do.",
        "The one-line docstring fits the panel. The sheet asks for a "
        "docstring that explains each parameter, and the solution uses the "
        "Args and Returns form. Point at the re-read inside the loop: "
        "forgetting it is the infinite-loop bug in the sheet's pitfalls "
        "table. The or matters too: and would require a number to be below "
        "the minimum and above the maximum at the same time.",
    )

    # =========================================================================
    # SLIDE 5: CP1 output - the test bench
    # =========================================================================
    output(
        deck, 'Output: Out-of-Range Numbers Bounce',
        r'''Testing get_valid_int()
Pick a number (1-5): 7
ERROR: Enter a number between 1 and 5.
Pick a number (1-5): 0
ERROR: Enter a number between 1 and 5.
Pick a number (1-5): 3
You picked: 3
''',
        'slide05_get_valid_int_output.png',
        "To try the function before the game ever calls it, the sheet has "
        "you add a small main function at the bottom of the library, with "
        "the if name is main guard under it. When you run the library file "
        "directly, the test runs. When your game imports the library, it "
        "doesn't. Here's that test in action. We typed seven, which is too "
        "high, so the function complained and asked again. Zero is too low, "
        "same thing. Three is in range, so it came back, and main printed "
        "it. The program never moved on with a bad number, and it never "
        "crashed. That's the whole job.",
        "Real run of the CP1 test bench from the sheet (main() with the "
        "get_valid_int test, plus the if __name__ == '__main__': guard), "
        "inputs 7, 0, 3. The test bench stays in the file for good; the "
        "Final Check list asks for main() and the guard.",
        key_terms=[
            ('Main guard', "if __name__ == '__main__': runs main() only when "
             'the file is run directly, not when another file imports it.'),
        ],
    )

    # =========================================================================
    # SLIDE 6: CP2 demo - get_yes_no
    # =========================================================================
    demo(
        deck, 'Demo: get_yes_no()',
        r'''def get_yes_no(prompt):
    """Get a yes or no response from the user."""
    answer = input(prompt)

    while answer != 'y' and answer != 'Y' and answer != 'n' and answer != 'N':
        print("ERROR: Please enter 'y' or 'n'.")
        answer = input(prompt)

    if answer == 'y' or answer == 'Y':
        return True
    else:
        return False
''',
        'slide06_get_yes_no.png',
        "Same shape, different test. The get yes no function takes one "
        "thing, the prompt. The priming read takes the answer just as it was "
        "typed. The while condition reads a little backward at first: keep "
        "looping while the answer isn't a lowercase y, and isn't a capital Y, "
        "and isn't a lowercase n, and isn't a capital N. That's and, not or, "
        "because a bad answer has to miss all four. Write or, and every "
        "answer misses at least one of them, so the loop never lets anybody "
        "out. Once we have a clean letter, the if at the bottom turns it into "
        "a Boolean. Yes comes back as True, and no comes back as False. "
        "That's the part to notice. The game never gets a letter back. It "
        "gets True or False, which is exactly what a while loop wants to "
        "check.",
        "Matches the solution line for line except the shorter docstring. "
        "The while line is exactly 79 characters, the style limit. The "
        "and-versus-or mix-up is the first If Something Breaks row on the "
        "sheet.",
    )

    # =========================================================================
    # SLIDE 7: CP2 output - both tests
    # =========================================================================
    output(
        deck, 'Output: A Real True or False',
        r'''Testing get_valid_int()
Pick a number (1-5): 3
You picked: 3

Testing get_yes_no()
Play again? (y/n): maybe
ERROR: Please enter 'y' or 'n'.
Play again? (y/n): Y
Result: True
Type: <class 'bool'>
''',
        'slide07_get_yes_no_output.png',
        "Here's the test bench with a second test added under the first: a "
        "heading, a call to get yes no, and two prints, one for the result "
        "and one for its type. The number test runs first, and three goes "
        "straight through. Then the yes or no test. We typed maybe, and it "
        "bounced. Then a capital Y, and the function handed back True. The "
        "last line is the proof that matters: the type is bool, not a "
        "string. Leave the test bench in the library. It doesn't run when "
        "the game imports the file, so there's nothing to delete.",
        "Real run of the sheet's CP2 test bench, inputs 3, maybe, Y. The "
        "sheet's own CP2 block shows only the get_yes_no half.",
    )

    # =========================================================================
    # SLIDE 8: CP3 concept
    # =========================================================================
    concept(
        deck, 'Checkpoint 3: Validate Menu Input',
        [
            "Copy `lab-2-2.py` to `lab-2-3.py` and update the docstring.",
            "The menu's `int(input(...))` becomes a call to `get_valid_int`.",
            "The prompt becomes `Choice (1-3): ` for the rest of the course.",
            "The beach line goes all caps: `CONGRATULATIONS! YOU REACHED THE "
            "BEACH!`",
            "Out-of-range picks re-ask. Letters still crash until Module 4.",
        ],
        "Checkpoint 3 is where the library pays off in the game. Copy your "
        "Lab 2.2 file to lab dash two dash three dot p-y, and update the "
        "docstring's title and description. Then find the one line that "
        "reads the menu choice. It used to convert the input straight to a "
        "number. Now it calls get valid int with a prompt and the range one "
        "to three. The prompt changes too, to the shorter Choice one through "
        "three, which is the wording every later lab uses. While you're in "
        "there, change the beach message to all capitals. Then try to break "
        "it. Type nine, and it asks again. Type banana, though, and it still "
        "crashes, because the conversion to a number fails before our range "
        "check ever sees the value. Fixing that takes the string methods in "
        "Chapter 8, so it's a Module 4 job. For now, range protection is the "
        "win.",
        key_terms=[
            ('Module function call', 'function_library.get_valid_int(...) '
             'runs the function that lives in your library file.'),
        ],
        think=[
            "Once the menu is validated, what can the rest of the turn assume "
            "about choice?",
            "Why does banana still crash even though get_valid_int is in "
            "place?",
        ],
        source_url='https://docs.python.org/3/tutorial/modules.html',
    )

    # =========================================================================
    # SLIDE 9: CP3 demo - the validated menu
    # =========================================================================
    demo(
        deck, 'Demo: The Menu Calls the Library',
        r'''print('Where would you like to go?')
print(f'  1. Corpus Christi - {SAT_TO_CORPUS} miles (BEACH!)')
print(f'  2. Houston - {SAT_TO_HOUSTON} miles')
print(f'  3. Austin - {SAT_TO_AUSTIN} miles')
print()

# Validated input!
choice = function_library.get_valid_int('Choice (1-3): ', 1, 3)
print()

# further down, the beach line goes all caps
print('CONGRATULATIONS! YOU REACHED THE BEACH!')
''',
        'slide09_validated_menu.png',
        "Here's the menu after the change. The four menu lines don't change "
        "at all. The one that does is the choice. We call get valid int from "
        "the function library with the prompt, one as the smallest choice, "
        "and three as the largest, and whatever comes back is assigned to "
        "choice. Don't wrap it in int. The function already hands back a "
        "whole number. Run it, type seven and then zero, and you'll see the "
        "same bounce you saw in the library test, right at the menu, until "
        "you give it a two. Down at the bottom, the beach message is now in "
        "capitals. Copy that line from the Message Digest so every character "
        "matches.",
        "Lab 2.2 used 'Enter your choice (1-3): '. The Final Check, the "
        "Message Digest, and every later lab use 'Choice (1-3): ' (Spring "
        "Build List A.2). The deck does not repeat the sheet's claim that "
        "the title-case beach line fails a test; the Lab 2.3 data falsified "
        "it (A.3). A run of this stage with inputs 7, 0, 2 bounces twice and "
        "accepts 2, the same as the sheet's CP3 block with the new prompt.",
    )

    # =========================================================================
    # SLIDE 10: CP4 concept - Keep the Trip Going (Spring Build List A.1)
    # =========================================================================
    concept(
        deck, 'Checkpoint 4: Keep the Trip Going',
        [
            "Arriving in Houston no longer ends the game. You can keep "
            "driving.",
            "`current_city` and the game totals are set once, before "
            "`while playing:`.",
            "The menu and the gate both check `current_city`, so Houston gets "
            "options.",
            "Each leg counts its own turns and hazards, then adds them to the "
            "game.",
            "The game ends at a beach, or when the player says no.",
        ],
        "This is the big one, and it's the checkpoint that turns your game "
        "into a real road trip. In Lab 2.2, the game ended the moment you "
        "arrived anywhere. Now, if you land in Houston, the game asks whether "
        "you want to keep going, and if you say yes, you get a Houston menu "
        "with Galveston on it. To make that work, the game has to remember "
        "where you are, so a current city variable takes over from the fixed "
        "start in San Antonio. A new loop, while playing, wraps the menu, the "
        "gate, and the travel loop, so each pass through it is one leg. The "
        "counting splits in two. Each leg counts its own turns and hazards, "
        "and when the leg ends, those numbers get added into the totals for "
        "the whole game. And the game stops in one of two ways: you reach a "
        "beach, or you tell it you're done. It's several small changes, and "
        "we'll walk through every one of them.",
        key_terms=[
            ('Flag', 'A Boolean variable that controls a loop. Here playing '
             'stays True until the game should end.'),
            ('Game total', 'A count that keeps growing across every leg of '
             'one game, like total_turns.'),
        ],
        think=[
            "Why can't the menu stay fixed on San Antonio once the game can "
            "continue?",
            "What would Total Turns show if a leg's turns were never added to "
            "the game total?",
        ],
        source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
    )

    # =========================================================================
    # SLIDE 11: CP4 demo - one game's state and the in-game loop
    # =========================================================================
    demo(
        deck, 'Demo: One Game, Many Legs',
        r'''# per-game state: set once, before the in-game loop
current_city = 'San Antonio'
total_miles = 0
total_turns = 0
total_hazards = 0
total_escaped = 0
reached_beach = False

# in-game loop: ends at a beach, or when the player stops
playing = True
while playing:
    # menu, gate, travel loop, and outcome check, indented
''',
        'slide11_in_game_loop.png',
        "Start right after the welcome lines. These six lines are one game's "
        "state. We set current city to San Antonio, the four game totals to "
        "zero, and reached beach to False, because nobody's there yet. "
        "They're set once, before the new loop, so they keep their values "
        "from one leg to the next. Then we set playing to True and start the "
        "loop, while playing. Everything that made up one trip in Lab 2.2, "
        "the menu, the gate, the travel loop, and the ending, moves inside "
        "it and gets indented one level. Each pass through this loop is one "
        "leg of the trip. One more thing: total miles used to start at zero "
        "right before the travel loop. Delete that line. Total miles belongs "
        "to the whole game now, not to one leg.",
        "Solution lines 61 to 71, minus the outer play-again indent, which "
        "arrives in CP5. The placeholder comment stands for the code on the "
        "next six demo slides. Lab 2.2's total_miles = 0 before the travel "
        "loop must go, or Total Miles in the summary shows only the last leg.",
    )

    # =========================================================================
    # SLIDE 12: CP4 demo - the Houston menu
    # =========================================================================
    demo(
        deck, 'Demo: Houston Gets a Menu',
        r'''HOU_TO_GALVESTON = 50  # beside the other distance constants
HOU_TO_SAN_ANTONIO = 200

# inside while playing: the menu follows current_city
if current_city == 'San Antonio':
    # the San Antonio menu and Choice (1-3) from Checkpoint 3
elif current_city == 'Houston':
    print('From Houston, where would you like to go?')
    print(f'  1. Galveston - {HOU_TO_GALVESTON} miles (BEACH!)')
    print(f'  2. San Antonio - {HOU_TO_SAN_ANTONIO} miles')
    print()
    choice = function_library.get_valid_int('Choice (1-2): ', 1, 2)
print()
''',
        'slide12_houston_menu.png',
        "First, two new constants for the Houston routes: fifty miles to "
        "Galveston, and two hundred back to San Antonio. Put them with your "
        "other distance constants. Inside the loop, the menu now depends on "
        "where you are. If the current city is San Antonio, it's the same "
        "three-option menu from Checkpoint 3. If it's Houston, we print the "
        "Houston heading and two options, then call get valid int with the "
        "prompt Choice one through two and the range one to two. Same "
        "function, different bounds, and it doesn't care which city it's "
        "serving. The blank print after the menu moves out to the end, so it "
        "runs for either city.",
        "The solution also has an else branch that prints an Austin menu "
        "with 'Choice (1-1): '. It can't run: arriving in Austin either sends "
        "you back to San Antonio or ends the game. Spring Build List A.3 "
        "removes it from the sheet and the Digest, so the deck leaves it out. "
        "The solution splits the get_valid_int call over two lines; one line "
        "fits the 79-character limit here.",
    )

    # =========================================================================
    # SLIDE 13: CP4 demo - the gate on HEADS
    # =========================================================================
    demo(
        deck, 'Demo: Houston on HEADS',
        r'''if gate_result == 'HEADS':
    print('Texas says: "Y\'all come on through!"')
    if current_city == 'San Antonio':
        # your three San Antonio choices from Lab 2.2, one level
        # deeper; the last one is now a plain else for Austin
    elif current_city == 'Houston':
        if choice == 1:
            destination = 'Galveston'
            distance = HOU_TO_GALVESTON
        else:
            destination = 'San Antonio'
            distance = HOU_TO_SAN_ANTONIO
''',
        'slide13_gate_heads.png',
        "The gate needs the same idea. On heads, Texas lets you go where you "
        "asked, but what you asked for depends on where you are. So the San "
        "Antonio choices you already have from Lab 2.2 move inside an if "
        "that checks for San Antonio, one level deeper. Since choice is "
        "always one to three now, the last of those choices can be a plain "
        "else for Austin, and the old fallback to Corpus Christi can go. "
        "Then add the Houston branch. If the choice is one, we set "
        "destination to Galveston and distance to the Houston to Galveston "
        "constant. Otherwise, we set destination to San Antonio and distance "
        "to two hundred miles.",
        "In the solution the San Antonio HEADS block is if choice == 1 "
        "Corpus Christi, elif choice == 2 Houston, else Austin. Lab 2.2 had "
        "elif choice == 3 plus an else that defaulted to Corpus Christi; "
        "validation makes that fallback dead code (T-Bone's Patch Note in "
        "CP1). Keeping it changes nothing in the output.",
    )

    # =========================================================================
    # SLIDE 14: CP4 demo - the gate on TAILS
    # =========================================================================
    demo(
        deck, 'Demo: Houston on TAILS',
        r'''else:
    print('Texas has other plans for you...')
    if current_city == 'San Antonio':
        # your three San Antonio redirects from Lab 2.2,
        # one level deeper
    elif current_city == 'Houston':
        # Flip the choice
        if choice == 1:
            destination = 'San Antonio'
            distance = HOU_TO_SAN_ANTONIO
        else:
            destination = 'Galveston'
            distance = HOU_TO_GALVESTON
''',
        'slide14_gate_tails.png',
        "Tails works the same way. The San Antonio redirects you built in "
        "Lab 2.2, with their random picks, move inside an if that checks for "
        "San Antonio. Then Houston gets its own branch, and it's a simple "
        "one: tails flips the choice. Ask for Galveston, choice one, and "
        "Texas sends you back to San Antonio. Ask for San Antonio, and you "
        "end up on the beach in Galveston. Sometimes Texas has other plans, "
        "and they work out fine.",
        "Matches the solution's TAILS block for Houston, including its "
        "Flip the choice comment. The solution's trailing else for Austin is "
        "unreachable for the same reason as the Austin menu, so it isn't "
        "shown.",
    )

    # =========================================================================
    # SLIDE 15: CP4 demo - each leg starts fresh
    # =========================================================================
    demo(
        deck, 'Demo: Every Leg Starts Fresh',
        r'''print('=' * 50)
print(f'TRAVELING TO {destination.upper()}!')
print('=' * 50)
print()

miles_remaining = distance
leg_turns = 0
hazards_faced = 0
hazards_escaped = 0

while miles_remaining > 0:
    leg_turns = leg_turns + 1
    print(f'--- Turn {leg_turns} ---')
''',
        'slide15_leg_counters.png',
        "After the gate, the banner changes. Instead of let the journey "
        "begin, it names the destination in capital letters, like traveling "
        "to Houston. Then four values reset at the start of every leg. Miles "
        "remaining starts at this leg's distance, and leg turns, hazards "
        "faced, and hazards escaped all start at zero. Inside the travel "
        "loop, the first thing we do is add one to leg turns, then print the "
        "turn number from it. That replaces the old turn counter from Lab "
        "2.2, so delete the line that started it at one and the line at the "
        "bottom of the loop that added to it. The rest of the turn, the "
        "roll, the miles, and the hazard check, stays exactly as it was.",
        "Solution lines 191 to 203. The rest of the travel loop body is the "
        "Lab 2.2 turn, unchanged. LET THE JOURNEY BEGIN! becomes TRAVELING "
        "TO {destination.upper()}! on every leg.",
    )

    # =========================================================================
    # SLIDE 16: CP4 demo - fold the leg in, check for a beach
    # =========================================================================
    demo(
        deck, 'Demo: The Beach Ends the Game',
        r'''# after the travel loop: fold this leg into the game
total_turns = total_turns + leg_turns
total_hazards = total_hazards + hazards_faced
total_escaped = total_escaped + hazards_escaped
current_city = destination

if current_city == 'Corpus Christi' or current_city == 'Galveston':
    print('=' * 50)
    print('CONGRATULATIONS! YOU REACHED THE BEACH!')
    print('=' * 50)
    print()
    reached_beach = True
    playing = False
''',
        'slide16_beach_ends_game.png',
        "When the travel loop finishes, the leg is over, so we fold it into "
        "the game. We add leg turns to total turns, hazards faced to total "
        "hazards, and hazards escaped to total escaped. Then we set current "
        "city to the destination, because you've arrived. Now we check "
        "where. If the current city is Corpus Christi or Galveston, it's a "
        "beach. We print the congratulations message between two banner "
        "lines, set reached beach to True, and set playing to False, so the "
        "in-game loop ends after this pass. The Lab 2.2 trip summary and its "
        "arrival messages at the bottom of the file go away. The new summary "
        "is coming up shortly.",
        "Solution lines 254 to 267. Total miles is already added inside the "
        "travel loop each turn, so it isn't folded in here.",
    )

    # =========================================================================
    # SLIDE 17: CP4 demo - Austin, or keep going
    # =========================================================================
    demo(
        deck, 'Demo: Austin, or Keep Going',
        r'''elif current_city == 'Austin':
    print('Austin is fun, but no beach here!')
    if function_library.get_yes_no('Return to San Antonio? (y/n): '):
        current_city = 'San Antonio'
        print()
    else:
        playing = False

else:
    # Houston or San Antonio - can continue this leg
    if not function_library.get_yes_no('Keep going this trip? (y/n): '):
        playing = False
    print()
''',
        'slide17_austin_keep_going.png',
        "Austin's not a beach, and from Austin the only road leads back, so "
        "the game asks whether you want to return to San Antonio. That "
        "question goes through get yes no, and since it hands back True or "
        "False, the call can sit right in the if. Yes sets current city back "
        "to San Antonio, and the next pass of the loop shows the San Antonio "
        "menu. No sets playing to False and ends the game. Anywhere else, "
        "meaning Houston or San Antonio, we ask whether you want to keep "
        "going this trip. Read that if carefully: if not, so when the player "
        "says no, playing becomes False. Say yes, and the loop comes back "
        "around with the menu for wherever you are.",
        "Solution lines 269 to 283, with each get_yes_no call on one line. "
        "This is where CP2's Boolean return earns its keep: no comparison "
        "to 'y' anywhere.",
    )

    # =========================================================================
    # SLIDE 18: CP4 output - Houston isn't the end
    # =========================================================================
    output(
        deck, "Output: Houston Isn't the End Anymore",
        r'''You made it to Houston!

Keep going this trip? (y/n): y

From Houston, where would you like to go?
  1. Galveston - 50 miles (BEACH!)
  2. San Antonio - 200 miles

Choice (1-2): 1

Flipping to see if Texas cooperates...
Result: HEADS!
''',
        'slide18_houston_output.png',
        "Here's the payoff. We picked Houston and made it in two turns. "
        "Before, that was the end of the game. Now it asks whether we want "
        "to keep going this trip, and we said y. The menu that comes up is "
        "the Houston menu, with Galveston as option one, and the prompt is "
        "Choice one through two. We picked one, and the gate flips again for "
        "this new leg. This is the exact path the Full Check takes, so if "
        "your game can't get here, this checkpoint is the place to look.",
        "Verbatim slice of a solution run under the CodeGrade fixture "
        "(D20 rolls 15, coin flips HEADS), inputs TestPlayer, 2, y, 1. The "
        "same lines appear in the sheet's Final Check.",
    )

    # =========================================================================
    # SLIDE 19: CP4 output - one summary for the whole trip
    # =========================================================================
    output(
        deck, 'Output: One Summary for the Whole Trip',
        r'''--------------------------------------------------
TRIP SUMMARY
--------------------------------------------------
Driver: TestPlayer
Final City: Galveston
Total Miles: 450
Total Turns: 3
Hazards Faced: 1
Hazards Escaped: 1
Status: BEACH WINNER!
--------------------------------------------------
''',
        'slide19_trip_summary_output.png',
        "When the in-game loop ends, the trip summary prints once for the "
        "whole game, after the loop, not inside it. It's framed in dashes "
        "now, with a blank line above it. Driver is the player's name. Final "
        "City is where the game ended, Galveston here. Total Miles and Total "
        "Turns cover both legs: three turns, two to Houston and one more to "
        "Galveston. The hazard counts are game totals too. The last line "
        "depends on reached beach. True prints BEACH WINNER, and False "
        "prints Trip Incomplete. Every one of these lines is in the Message "
        "Digest, so copy them from there.",
        "Solution lines 288 to 303: print(), the dash line, the heading, the "
        "six f-string lines, if reached_beach: Status: BEACH WINNER! else "
        "Status: Trip Incomplete, the dash line, print(). It replaces the "
        "Lab 2.2 summary (Destination, Distance) and its arrival messages.",
    )

    # =========================================================================
    # SLIDE 20: CP5 concept - Play Again Loop
    # =========================================================================
    concept(
        deck, 'Checkpoint 5: Play Again Loop',
        [
            "A `while play_again:` loop wraps the whole game.",
            "The per-game state moves inside it, so every game starts clean.",
            "After each trip summary, `get_yes_no` decides whether to play "
            "again.",
            "Three loops now nest: games, then legs, then turns.",
            "The goodbye prints once, after the last game.",
        ],
        "Checkpoint 5 is a wrap, not a rewrite. Your game from Checkpoint 4 "
        "goes inside one more loop, the play-again loop. It's the sentinel "
        "pattern from Chapter 4. We set play again to True, loop while it's "
        "True, and at the bottom of each game, we let get yes no decide "
        "whether it stays that way. The one placement that really matters is "
        "the per-game state. Current city, the four totals, and reached "
        "beach have to reset at the start of every game, so they move inside "
        "the new loop, at the top. Leave them outside, and the second game "
        "starts in Galveston with the first game's miles already on the "
        "board.",
        key_terms=[
            ('Sentinel', 'A value that signals a loop to stop. Here, '
             'play_again stays True until the player says no.'),
        ],
        think=[
            "What would the second game look like if current_city were set "
            "before the play-again loop?",
            "How is this the same pattern as a loop that stops when you enter "
            "a sentinel number?",
        ],
        source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
    )

    # =========================================================================
    # SLIDE 21: CP5 demo - wrap the whole game
    # =========================================================================
    demo(
        deck, 'Demo: Wrap the Whole Game',
        r'''play_again = True
while play_again:
    # the per-game state from Checkpoint 4 moves in here,
    # so every game starts with fresh totals
    playing = True
    while playing:
        # one leg per pass, just as in Checkpoint 4

    # the TRIP SUMMARY prints here, once per game
    play_again = function_library.get_yes_no('Play again? (y/n): ')
    print()

print(f'Thanks for playing, {player_name}!')
''',
        'slide21_play_again.png',
        "Here's the structure. We set play again to True and loop while it's "
        "True. At the top of each game, the per-game state from Checkpoint 4 "
        "sits right here, inside the loop. Then the in-game loop runs one leg "
        "per pass, just like before. When it ends, the trip summary prints, "
        "and then we call get yes no with the prompt Play again, and whatever "
        "comes back is assigned to play again. Yes keeps the outer loop "
        "going, and the next game starts fresh in San Antonio. No ends it. "
        "The goodbye sits after the loop, all the way out at the left, so it "
        "prints once, at the very end, and now it greets the player by name. "
        "Indentation is doing all the work here, so take your time with it.",
        "Placeholders stand for code shown on slides 11 to 19. The goodbye "
        "line here is the CP5 version from the sheet's skeleton; CP6 puts "
        "the session report above it and adds the production credit line "
        "below it. Run with inputs TestPlayer, 2, y, 1, y, 1, n: the second "
        "game opens on the San Antonio menu.",
    )

    # =========================================================================
    # SLIDE 22: CP6 concept - Session Statistics
    # =========================================================================
    concept(
        deck, 'Checkpoint 6: Session Statistics',
        [
            "Three accumulators: `games_played`, `session_miles`, and "
            "`session_hazards`.",
            "They start at zero once, before the play-again loop.",
            "Each one grows after every trip summary.",
            "SESSION STATISTICS prints once, after the last game.",
        ],
        "Checkpoint 6 keeps score across the whole session. It's the "
        "accumulator pattern again, and the trick, like last time, is where "
        "things live. The session totals start at zero once, before the "
        "play-again loop, so they survive from game to game. After each trip "
        "summary, we add to them: one more game played, this game's miles, "
        "and this game's hazards. And when the player finally says no, the "
        "session report prints once, below the loop. Get the placement right, "
        "and the numbers take care of themselves.",
        key_terms=[
            ('Accumulator', 'A variable that starts at zero before a loop and '
             'grows inside it.'),
        ],
        think=[
            "What would Games Played show if games_played were set to zero "
            "inside the play-again loop?",
            "Why does the session report print after the loop instead of "
            "inside it?",
        ],
        source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
    )

    # =========================================================================
    # SLIDE 23: CP6 demo - the session accumulators
    # =========================================================================
    demo(
        deck, 'Demo: Session Accumulators',
        r'''# before play_again = True: set once for the whole session
games_played = 0
session_miles = 0
session_hazards = 0

# inside the play-again loop, right after the TRIP SUMMARY
games_played = games_played + 1
session_miles = session_miles + total_miles
session_hazards = session_hazards + total_hazards
''',
        'slide23_session_accumulators.png',
        "Here are the two halves. Up top, before the play-again loop starts, "
        "we set games played, session miles, and session hazards to zero. "
        "Once. Then, inside the loop, right after the trip summary prints, "
        "we add one to games played, add this game's total miles to session "
        "miles, and add this game's total hazards to session hazards. Watch "
        "the names. Total miles is this game's number, and it resets every "
        "game. Session miles is the running total, and it never resets. "
        "Mixing those two up is the classic mistake on this checkpoint.",
        "Solution lines 51 to 54 and 305 to 308. The update goes after the "
        "summary and before the play-again prompt.",
    )

    # =========================================================================
    # SLIDE 24: CP6 demo - the session report
    # =========================================================================
    demo(
        deck, 'Demo: The Session Report',
        r'''print('=' * 50)
print('SESSION STATISTICS')
print('=' * 50)
print(f'Games Played: {games_played}')
print(f'Total Miles: {session_miles}')
print(f'Total Hazards: {session_hazards}')
print('=' * 50)
print()
print(f'Thanks for playing, {player_name}!')
print('An All My Eggses Live in Texas Production')
''',
        'slide24_session_report.png',
        "After the play-again loop ends, the report prints. A banner line, "
        "the heading SESSION STATISTICS, another banner line, then the three "
        "totals: games played, total miles from session miles, and total "
        "hazards from session hazards. One more banner and a blank line, "
        "then the goodbye with the player's name, and the closing credit: "
        "An All My Eggses Live in Texas Production. This block sits at the "
        "left margin, below the loop, and it replaces the plain goodbye from "
        "Checkpoint 5.",
        "Solution lines 317 to 326, all outside the play-again loop.",
    )

    # =========================================================================
    # SLIDE 25: CP6 output - two games, one report
    # =========================================================================
    output(
        deck, 'Output: Two Games, One Report',
        r'''Play again? (y/n): n

==================================================
SESSION STATISTICS
==================================================
Games Played: 2
Total Miles: 600
Total Hazards: 1
==================================================

Thanks for playing, TestPlayer!
An All My Eggses Live in Texas Production
''',
        'slide25_session_output.png',
        "Here's a session of two games. The first was the Houston then "
        "Galveston trip, four hundred fifty miles. The second went straight "
        "to Corpus Christi, one hundred fifty more. At the play-again prompt "
        "we said n, and the report shows two games played and six hundred "
        "total miles. That's the proof the accumulators survived from one "
        "game to the next. If Games Played says one after two games, check "
        "where you set it to zero.",
        "Verbatim end of a solution run under the CodeGrade fixture, inputs "
        "TestPlayer, 2, y, 1, y, 1, n. Game 1: 450 miles, 1 hazard. Game 2 "
        "(Corpus Christi): 150 miles, 0 hazards.",
    )

    # =========================================================================
    # SLIDE 26: Final Check and Submit
    # =========================================================================
    concept(
        deck, 'Final Check and Submit',
        [
            "Run the Full Check inputs: `TestPlayer`, `2`, `y`, `1`, `n`.",
            "Match the structure line for line: banners, prompts, and blank "
            "lines.",
            "Try to break it: `9` at a menu, `maybe` at a yes or no question.",
            "Submit `lab-2-3.py` and `function_library.py` together.",
            "Submissions are unlimited, so submit early and use the feedback.",
        ],
        "Before you submit, run the Full Check. Enter TestPlayer as your "
        "name, pick two for Houston, say y to keep going, pick one for "
        "Galveston, and say n when it asks to play again. Your rolls will "
        "differ from the sheet's, because CodeGrade runs with fixed dice, so "
        "compare the structure: every banner, every prompt, and every blank "
        "line. Then try to break it. Type nine at a menu, type maybe at a yes "
        "or no question, and play two games so you can watch the session "
        "numbers add up. Submit both files together: your lab two three file "
        "and the function library. Submissions are unlimited, so "
        "submit early and let the feedback point you to what needs fixing. "
        "That wraps up Module 2. In Module 3, your game learns to save a "
        "trip and pick it back up, starting right where this in-game loop "
        "leaves off.",
        think=[
            "What's the strangest input you can throw at your game, and does "
            "it survive?",
            "Which loop would you check first if Games Played came out wrong?",
        ],
    )

    deck.save(OUTPUT_PPTX)
    postprocess(OUTPUT_PPTX)
    if len(TTS) != len(deck.slides):
        raise SystemExit(f'{len(TTS)} narration paragraphs for '
                         f'{len(deck.slides)} slides')
    Path(OUTPUT_TTS).write_text('\n\n'.join(TTS) + '\n', encoding='utf-8')
    print(f'OK {OUTPUT_PPTX}: {len(deck.slides)} slides; '
          f'TTS {OUTPUT_TTS}: {len(TTS)} paragraphs')


if __name__ == '__main__':
    main()

