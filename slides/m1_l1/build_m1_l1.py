"""
build_m1_l1.py - M1-L1 ("Lab 1.1: Welcome to San Antonio") slide deck.

Module 1, Lab 1 (BUILD) | Chapter 2 application
Pairs with: Lab 1.1 assignment sheet (lab-1-2.json scope is M1-U2)

PIPELINE FRAMING (locked May 24, 2026)
--------------------------------------
M1-L1 is a LAB WALKTHROUGH, not a concept introduction. M1-U1 already
taught the Chapter 2 toolkit (variables, input/int, arithmetic, f-strings,
named constants, def main() pattern). This deck WALKS THE CHECKPOINTS of
Lab 1.1 with explicit callbacks to U1 concepts. We do NOT re-teach.

SCOPE (verified against lab-1-1.py and lab-1-1.json)
- CP1: docstring, 4 named constants, def main() with welcome banner
- CP2: player_name via input(), roll via int(input()); REQUIRED PROMPT STRINGS
- CP3: miles_rolled = roll * 10; per-destination remaining; galveston via two-step
- CP4: formatted Travel Report using f-strings

OUT OF SCOPE
- Anything Chapter 3+ (if/elif/loops/lists/dicts/classes)
- Format specs (:.2f, :>N, etc.) -- not used in any M1 lab
- Re-teaching of U1 concepts

USAGE
-----
    python3 slides/m1_l1/build_m1_l1.py

The deck is written to /home/claude/IS2053_2026-05-24_M1-L1_Deck.pptx.
PNGs land in /home/claude/m1_l1_pngs/.
"""
import os
import sys
from pathlib import Path

# ----- Bootstrap: make slides/build_lib.py importable -----
SLIDES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SLIDES_DIR))

from build_lib import (  # noqa: E402
    DeckBuilder,
    format_concept_notes,
    format_demo_notes,
    format_output_notes,
    format_title_notes,
)

# ----- Outputs -----
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-24_M1-L1_Deck.pptx'
PNG_OUT = '/home/claude/m1_l1_pngs'
WORK_DIR = '/tmp/build_m1_l1'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 1.1: Welcome to San Antonio',
        subtitle='IS2053 Programming I  \u2022  Module 1  \u2022  Lab Walkthrough',
        notes=format_title_notes(
            deck_id='M1-L1',
            deck_title='Lab 1.1: Welcome to San Antonio',
            opening_line=(
                '"Welcome to your first lab walkthrough. You just finished M1-U1, '
                'the Chapter 2 toolkit. This hour we put that toolkit to work in '
                "Lab 1.1. We're going to walk all four checkpoints together. By "
                'the end you\'ll know exactly what to type."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro - the story + what we're building
    # =========================================================================
    deck.add_narrative_slide(
        title='Welcome to Bat City Collective',
        section_label='THE STORY',
        bold_oneliner='You just got hired. First assignment is on your desk.',
        body=(
            "You're a junior developer at an Austin indie game studio. Your "
            "first project is a Texas road trip game for the client All My "
            "Eggses Live in Texas. Lab 1.1 is the travel calculator: get the "
            "player's name, get a dice roll, calculate how far they can travel "
            "to each destination, and print a clean Travel Report. No decisions "
            "yet. No loops. Just the Chapter 2 toolkit you learned in U1, "
            "applied to a real problem with a real shape."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome back. In Unit 1 you learned the seven small ideas of "
                "Chapter 2. Variables, print, input, type conversion, "
                "arithmetic, string concatenation, and f-strings. You also "
                "learned the file shape: docstring on top, constants below, "
                "def main with all the work inside, if __name__ at the "
                "bottom. None of that needs reteaching today. Today we put "
                "all of it together in a single working program. Lab 1.1, "
                "Welcome to San Antonio. The premise is light. You're a "
                "junior developer at a fictional Austin indie game studio "
                "called Bat City Collective. Your client wants a Texas road "
                "trip game, and your first ticket is the travel calculator. "
                "Get the player's name, get a dice roll, calculate how far "
                "that roll will get them toward four different destinations, "
                "print a nicely formatted Travel Report. That's it. No "
                "decisions, no loops, no lists. Just Chapter 2, four "
                "checkpoints, about an hour of work. By the end of this "
                "video you'll have walked every checkpoint and seen the "
                "code shape. Then you go open VS Code and actually type it. "
                "Quick mental model. The whole program is three movements. "
                "Ask. Compute. Show. Same shape as the vending machine "
                "example from U1. Hold that picture."
            ),
            think_about=[
                "Before we walk the checkpoints, what's the part of this lab you expect to be the hardest? Why?",
                'When you read "calculate how far the player can travel to each destination," does the math approach come to mind, or do you need to see it first?',
            ],
            source_url='https://docs.python.org/3/tutorial/introduction.html',
        ),
    )

    # =========================================================================
    # SLIDE 3: CP1 Concept - Setup & Welcome Banner
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 1: Setup & Welcome Banner',
        bullets=[
            "Build the file shape from U1: docstring, named constants, def main(), if __name__.",
            "Define FOUR constants for distances: SAT_TO_CORPUS, SAT_TO_HOUSTON, SAT_TO_AUSTIN, HOU_TO_GALVESTON.",
            "Inside main(), print a welcome banner using string multiplication: print('=' * 50).",
            "Constants live at module level (top of file), NOT inside main().",
            "Run it and confirm the banner prints. That's your foundation for the next three checkpoints.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 1 is the foundation. You're not doing anything "
                "the player will see except the banner. You're setting the "
                "stage. Everything you learned in U1 about the file shape "
                "lands here. Docstring at the top with your name, abc123, "
                "section, and a one-line description. That's required, "
                "CodeGrade will check for it. Four named constants below "
                "the docstring, at module level. SAT_TO_CORPUS is 150 "
                "miles, SAT_TO_HOUSTON is 200, SAT_TO_AUSTIN is 80, and "
                "HOU_TO_GALVESTON is 50. The convention from U1 still "
                "applies, all caps with underscores. Then your def main "
                "function and your if __name__ block at the very bottom. "
                "All the work happens INSIDE main, indented four spaces. "
                "That's the rule. Constants outside, work inside. The "
                "banner itself uses the string multiplication trick from "
                "U1's BookEx, Program 2-8. Quote, equals sign, quote, "
                "star, fifty. Python repeats the equals sign fifty times "
                "and you get a clean line. Three prints make the banner: "
                "the top line of equals, the title in caps, the bottom "
                "line of equals. Add an empty print on either side for "
                "vertical breathing room. Run the file and confirm the "
                "banner shows. Nothing else happens yet."
            ),
            key_terms=[
                ('Module level', "Top of the file, outside any function. Constants and imports live here."),
                ('String multiplication', "Multiplying a string by an integer repeats it. '=' * 50 gives 50 equal signs."),
            ],
            think_about=[
                "Why do constants go OUTSIDE main() instead of inside? What would change if you moved them in?",
                "If you forgot the print() before and after the banner, what would the output look like? Would the program still 'work'?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#defining-functions',
        ),
    )

    # =========================================================================
    # SLIDE 4: CP1 Demo - constants + main + banner
    # =========================================================================
    cp1_code = '''"""Lab 1.1 - Name / abc123 / Section / Description"""

SAT_TO_CORPUS = 150
SAT_TO_HOUSTON = 200
SAT_TO_AUSTIN = 80
HOU_TO_GALVESTON = 50


def main():
    print()
    print('=' * 50)
    print('DEEP IN THE HEART: A LONE STAR JOURNEY')
    print('=' * 50)
    print()
'''

    deck.add_demo_slide(
        title='Demo: The CP1 Foundation',
        code=cp1_code,
        png='slide04_cp1.png',
        notes=format_demo_notes(
            code=cp1_code,
            instructor_notes=(
                "The docstring on screen is compacted for the slide. "
                "In their actual file, students write the full docstring "
                "with Name, abc123, Section, and Description on separate "
                "lines. CodeGrade checks for those four labels. Read the "
                "four constants out loud and explain what each "
                "represents. Note the blank line between SAT_TO_AUSTIN "
                "and HOU_TO_GALVESTON groups in their real code is "
                "optional but readable. Then def main. Tell students to "
                "add a one-line docstring inside main as a habit -- "
                'three quote three, Main function, three quote three. '
                "Not on this slide for space, but they should write it. "
                "Then the banner: blank print for spacing, fifty equals, "
                "the title in caps, fifty equals, blank print. The if "
                "__name__ block at the bottom is not shown here but tell "
                "students it goes after main closes. Mention that the "
                "title string DEEP IN THE HEART is exact, CodeGrade will "
                "check it character by character."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 5: CP1 Output - just the banner
    # =========================================================================
    cp1_output = """\

==================================================
DEEP IN THE HEART: A LONE STAR JOURNEY
=================================================="""

    deck.add_output_slide(
        title='Output: Banner Only (so far)',
        output_text=cp1_output,
        png='slide05_cp1_output.png',
        notes=format_output_notes(
            output_text=cp1_output,
            instructor_notes=(
                "Three lines of output for the entire program right now. "
                "That's correct. The program loads the constants into "
                "memory (you don't see them) and prints the banner. "
                "Nothing else. If you see anything different, the most "
                "likely cause is a typo in one of the prints. Pause and "
                "ask: did everyone get this exact output before moving on? "
                "If not, CP1 isn't done yet. Fix the typo first. "
                "Programming is built on layers. If CP1 is broken, CP2 "
                "stacking on top of it just hides the problem."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 6: CP2 Concept - Player Input
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 2: Player Input',
        bullets=[
            "Get player_name with input(). It's a string, no conversion needed.",
            "Get roll with int(input()). Wrap int() around the input call so the result is an integer.",
            "Required prompt strings are EXACT. CodeGrade checks them character by character.",
            "Display a welcome message in an f-string that uses {player_name}.",
            "Print the dice-roll instructions BEFORE asking for the roll, so the user knows what to enter.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 2 is where the program starts talking to the "
                "user. Two inputs to collect. The name first, then the "
                "roll. The name is a string so a plain input call is "
                "enough. The roll is going to be used in math next "
                "checkpoint, so it has to come back as an integer, not a "
                "string. That means wrapping int around the input call, "
                "exactly the pattern from U1 and BookEx Program 2-13. "
                "Two things to watch. First, the prompt strings are not "
                "suggestions. CodeGrade compares them character by "
                "character. The name prompt is What is your name, "
                "traveler, question mark, space. The roll prompt is What "
                "did you roll, open paren, 1 dash 20, close paren, "
                "colon, space. The trailing space inside the quotes is "
                "what keeps the cursor off the punctuation. Get those "
                "exactly right or your tests fail. Second, after you get "
                "the name, you greet the player with an f-string. "
                "Welcome, open brace, player_name, close brace, "
                "exclamation point. That's how you embed the value into "
                "the string. Pure U1 material, no surprises."
            ),
            key_terms=[
                ('input()', "Always returns a string. Always."),
                ('int(input(...))', "The pattern for getting a number from the user in one line."),
            ],
            think_about=[
                "If you typed input() but forgot the int() wrapper, the program runs and asks for the roll. When does the error happen?",
                'Why does the trailing space inside the prompt string ("? ") matter? What does the screen look like without it?',
            ],
            source_url='https://docs.python.org/3/library/functions.html#input',
        ),
    )

    # =========================================================================
    # SLIDE 7: CP2 Demo - input block
    # =========================================================================
    cp2_code = """    player_name = input('What is your name, traveler? ')
    print()

    print(f'Welcome, {player_name}!')
    print('You are in San Antonio. Your goal: reach the beach!')
    print()

    print('Roll to see how far you can travel.')
    print('Go to this link and click Generate:')
    print('https://www.calculator.net/random-number-generator.html')
    print()
    roll = int(input('What did you roll? (1-20): '))
"""

    deck.add_demo_slide(
        title='Demo: The CP2 Input Block',
        code=cp2_code,
        png='slide07_cp2.png',
        notes=format_demo_notes(
            code=cp2_code,
            instructor_notes=(
                "All twelve lines go INSIDE main, indented four spaces. "
                "The leading indent is critical, don't drop it. Walk top "
                "to bottom. Line 1, name input, plain input call. Blank "
                "print for spacing. Welcome line using an f-string with "
                "the player_name variable. Goal line, plain string, no "
                "f prefix needed because there's no variable. Blank "
                "print. Roll instructions, three plain prints. The URL "
                "for the random number generator is in there because "
                "students don't have dice. Click and generate is how "
                "they get a number. Then the blank print and the int "
                "input call. Stop and read the roll prompt out loud "
                "twice: 'What did you roll, open paren, 1 dash 20, "
                "close paren, colon, space.' Tell students CodeGrade is "
                "going to check this character by character."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: CP2 Output - partial run through CP2
    # =========================================================================
    cp2_output = """\
==================================================
DEEP IN THE HEART: A LONE STAR JOURNEY
==================================================

What is your name, traveler? Maria

Welcome, Maria!
You are in San Antonio. Your goal: reach the beach!

Roll to see how far you can travel.
Go to this link and click Generate:
https://www.calculator.net/random-number-generator.html

What did you roll? (1-20): 15"""

    deck.add_output_slide(
        title='Output: After CP2 (run through the second input)',
        output_text=cp2_output,
        png='slide08_cp2_output.png',
        notes=format_output_notes(
            output_text=cp2_output,
            instructor_notes=(
                "This is what the screen shows after running through "
                "both inputs. The banner is from CP1. The name prompt "
                "with Maria typed on the same line. Notice Maria is on "
                "the same line as the prompt, that's the trailing space "
                "doing its job. Then the welcome line shows the value "
                "of player_name embedded by the f-string. Then the goal "
                "line. Then the roll instructions and the roll prompt "
                "with 15 typed in. The program ends here for now, no "
                "calculations yet. If the output doesn't match this "
                "exactly, the issue is usually a missing print for "
                "spacing or a missing f prefix on the welcome line."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 9: CP3 Concept - Calculations
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 3: Calculations',
        bullets=[
            "Calculate miles_rolled = roll * 10 first. Every other number depends on this.",
            "Subtract miles_rolled from each destination's distance to get how far is left.",
            "Galveston is a two-step calculation: total first (SAT_TO_HOUSTON + HOU_TO_GALVESTON), then subtract.",
            "Store EVERY intermediate value in a named variable. Don't try to do math inline in print().",
            "Negative remaining is GOOD: it means the player made it with miles to spare.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 3 is the math engine. Six variables to "
                "compute in order. First, miles_rolled. The roll times "
                "ten. If they rolled a 15, miles_rolled is 150. Then "
                "three remaining variables, one for each direct "
                "destination. Corpus remaining is SAT_TO_CORPUS minus "
                "miles_rolled. Houston remaining is SAT_TO_HOUSTON "
                "minus miles_rolled. Austin remaining is SAT_TO_AUSTIN "
                "minus miles_rolled. Then Galveston, which is a two-step "
                "because Galveston is reached through Houston. First "
                "compute galveston_total as SAT_TO_HOUSTON plus "
                "HOU_TO_GALVESTON. That's 250. Then galveston_remaining "
                "is galveston_total minus miles_rolled. Two lines, not "
                "one. The temptation is to try to do the math inline in "
                "the print statement, like print f Corpus remaining is "
                "SAT_TO_CORPUS minus miles_rolled. Resist that. Tyler "
                "from the mentor team will tell you the same thing in "
                "the lab sheet. Named intermediate variables are how "
                "real codebases stay readable. About signs. The math "
                "here is destination minus what you rolled, so if you "
                "rolled MORE than you needed, you get a negative number. "
                "That's good. The legend at the bottom of the Travel "
                "Report explains it: negative means you made it. "
                "Positive means you still have miles to go. Don't try "
                "to flip the math to make positives mean made it. The "
                "expected output uses this convention."
            ),
            key_terms=[
                ('Intermediate variable', 'A named value created during a multi-step calculation, used downstream.'),
            ],
            think_about=[
                'Why compute galveston_total as a separate variable instead of jamming everything into one line?',
                "If you rolled a 20 and miles_rolled is 200, what's austin_remaining? Is that good or bad for the player?",
            ],
            source_url='https://docs.python.org/3/reference/expressions.html#arithmetic-operations',
        ),
    )

    # =========================================================================
    # SLIDE 10: CP3 Demo - calculation block
    # =========================================================================
    cp3_code = """    miles_rolled = roll * 10

    corpus_remaining = SAT_TO_CORPUS - miles_rolled
    houston_remaining = SAT_TO_HOUSTON - miles_rolled
    austin_remaining = SAT_TO_AUSTIN - miles_rolled

    galveston_total = SAT_TO_HOUSTON + HOU_TO_GALVESTON
    galveston_remaining = galveston_total - miles_rolled
"""

    deck.add_demo_slide(
        title='Demo: The CP3 Calculation Block',
        code=cp3_code,
        png='slide10_cp3.png',
        notes=format_demo_notes(
            code=cp3_code,
            instructor_notes=(
                "Eight lines, all indented inside main. Walk top to "
                "bottom. miles_rolled first because everything depends "
                "on it. Then the three direct destinations as a group. "
                "Notice they're visually grouped by being together with "
                "no blank lines between them. Then a blank line, then "
                "the Galveston pair. The blank line signals to the "
                "reader these are conceptually separate from the direct "
                "destinations. Each line is a single assignment. No "
                "math is happening inside any print statement. That's "
                "the rule. Compute first, print later. Tell students: "
                "if you write any one of these on multiple lines or try "
                "to combine the Galveston steps, your code won't be "
                "wrong but it'll be harder for you to debug when "
                "something goes off."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: CP3 Output - debug verification at two roll values
    # =========================================================================
    cp3_output = """\
Test 1 (roll = 10):
DEBUG: miles_rolled = 100
DEBUG: corpus_remaining = 50
DEBUG: galveston_total = 250

Test 2 (roll = 20):
DEBUG: miles_rolled = 200
DEBUG: corpus_remaining = -50
DEBUG: galveston_total = 250"""

    deck.add_output_slide(
        title='Output: Debug-Check Your Math',
        output_text=cp3_output,
        png='slide11_cp3_output.png',
        notes=format_output_notes(
            output_text=cp3_output,
            instructor_notes=(
                "The lab asks you to add temporary DEBUG prints after "
                "the calculations and run with two test rolls, ten and "
                "twenty. Verify these numbers match. Test 1 with roll "
                "ten: miles_rolled is 100 (10 times 10), "
                "corpus_remaining is 50 (150 minus 100), "
                "galveston_total is 250 (200 plus 50). Test 2 with roll "
                "twenty: miles_rolled is 200, corpus_remaining is "
                "negative 50 because the player overshot Corpus by 50 "
                "miles, galveston_total is still 250 because it doesn't "
                "depend on the roll. Critical reminder: the DEBUG lines "
                "are TEMPORARY. Delete them all before moving to CP4. "
                "Forgetting to delete them is a common style violation "
                "that causes CodeGrade output mismatches."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 12: CP4 Concept - Travel Report
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 4: Travel Report',
        bullets=[
            "Print a Travel Report header with its own banner: a divider line, the title, another divider.",
            "Show the player's name, the roll, and miles_rolled using f-strings.",
            "Print a destinations section listing all four with their total distance and remaining miles.",
            "Each destination follows the SAME two-line pattern. Copy, change the variable names.",
            "Close with the legend explaining what negative and positive remaining mean.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 4 is the user-facing output. Everything you "
                "built so far is invisible to the player until this "
                "checkpoint shows up. The Travel Report has four pieces. "
                "First, the header. Same banner trick as the welcome "
                "banner, with TRAVEL REPORT as the title. Second, the "
                "roll summary. Three lines showing Driver, Roll, and "
                "Miles you can travel, all f-strings pulling in your "
                "variables. Then another divider to close the summary. "
                "Third, the destinations block. Four destinations, each "
                "with the same two-line shape. A header line with the "
                "destination name and its total distance, a second line "
                "with how many miles remain after the roll. Indented "
                "with leading spaces inside the string so the report "
                "looks like a list. Fourth, the closing legend: "
                "negative means made it, positive means more to go. "
                "Sprinkle blank prints between sections for breathing "
                "room. Read the expected output in the lab sheet and "
                "match it exactly. Whitespace matters. Punctuation "
                "matters. The exclamation point after BEACH matters. "
                "Compare line by line."
            ),
            key_terms=[
                ('f-string', 'A string prefixed with f that lets you embed variables in curly braces. Used everywhere here.'),
            ],
            think_about=[
                "Why does it matter that each destination follows the SAME two-line shape? What would happen if you made one different?",
                'When the lab says "match the expected output exactly," what kinds of differences could cost you points?',
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals',
        ),
    )

    # =========================================================================
    # SLIDE 13: CP4 Demo - report header + first destination pattern
    # =========================================================================
    cp4_code = """    print()
    print('=' * 50)
    print('TRAVEL REPORT')
    print('=' * 50)
    print(f'Driver: {player_name}')
    print(f'You rolled: {roll}')
    print(f'Miles you can travel: {miles_rolled}')
    print('=' * 50)
    print()
    print('DISTANCES FROM SAN ANTONIO:')
    print()
    print(f'  Corpus Christi: {SAT_TO_CORPUS} miles (BEACH!)')
    print(f'    After your roll: {corpus_remaining} miles remaining')
"""

    deck.add_demo_slide(
        title='Demo: Report Header + First Destination',
        code=cp4_code,
        png='slide13_cp4.png',
        notes=format_demo_notes(
            code=cp4_code,
            instructor_notes=(
                "Thirteen lines shown, but the full CP4 block is closer "
                "to twenty-five lines. What's on screen is the header "
                "and the first destination. The pattern continues "
                "identically for Houston, Austin, and Galveston: a "
                "header line with name and distance, an indented "
                "remaining line. Then a closing legend and blank "
                "print. Walk top to bottom. Blank print, banner, "
                "TRAVEL REPORT, banner. Three f-strings showing the "
                "roll summary. Closing banner. Blank print. The "
                "DISTANCES line. Blank print. Then the Corpus pair: "
                "two spaces of leading indent inside the string for "
                "the destination name, four spaces for the remaining "
                "line. Those leading spaces are inside the quotes, "
                "they're part of the string. Stop here and ask the "
                "class: how many more pairs do you need to write? "
                "Answer: three. Houston, Austin, Galveston. Same "
                "shape, change the words and the variables."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: CP4 Output - full final output with Maria/15
    # =========================================================================
    cp4_output = """\
==================================================
TRAVEL REPORT
==================================================
Driver: Maria
You rolled: 15
Miles you can travel: 150
==================================================

DISTANCES FROM SAN ANTONIO:

  Corpus Christi: 150 miles (BEACH!)
    After your roll: 0 miles remaining
  Houston: 200 miles
    After your roll: 50 miles remaining
  Austin: 80 miles
    After your roll: -70 miles remaining"""

    deck.add_output_slide(
        title='Output: The Travel Report (Maria, roll 15)',
        output_text=cp4_output,
        png='slide14_cp4_output.png',
        notes=format_output_notes(
            output_text=cp4_output,
            instructor_notes=(
                "Maria rolled fifteen, so miles_rolled is 150. The "
                "report shows that, then walks the four destinations. "
                "What's on screen here is everything through Austin, "
                "trimmed to fit. The full expected output in the lab "
                "sheet continues with Galveston (250 miles, 100 "
                "remaining) and the closing legend (Negative equals "
                "made it, Positive equals more to go). Trace the "
                "numbers with the class. Corpus is 150 miles, Maria "
                "rolled 150 miles, so remaining is zero. She just "
                "barely made it. Houston is 200, she rolled 150, 50 "
                "miles short. Austin is 80, she rolled 150, so "
                "remaining is negative 70, which means she overshot "
                "Austin by 70 miles. If your output doesn't match line "
                "by line, the issue is almost always a missing print "
                "for spacing, a missing f prefix on an f-string, or a "
                "typo in one of the literal strings. Compare carefully."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 15: Common Stumbles - top pitfalls across all CPs
    # =========================================================================
    deck.add_concept_slide(
        title='Common Stumbles',
        bullets=[
            "NameError on a constant -> typo in the name or constant defined inside main() instead of at module level.",
            "TypeError on the math -> forgot int() around the roll input. Python tried to multiply a string by 10.",
            "Output shows literal {player_name} -> missing the f prefix on an f-string.",
            "Output 'almost' matches expected -> count blank lines and leading spaces. Whitespace is part of the test.",
            "DEBUG lines still in your submitted file -> delete every DEBUG print from CP2 and CP3 before submitting.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Five things go wrong most often. Memorize this list. "
                "First, NameError on a constant. The error message says "
                "name SAT_TO_HOUSTON is not defined or something "
                "similar. Two causes. Either you have a typo in the "
                "constant name, or you defined it inside main instead "
                "of at the module level. Constants live OUTSIDE main, "
                "at the top of the file. Second, TypeError on the "
                "math. Specifically, can't multiply sequence by "
                "non-int of type str. You forgot to wrap input in "
                "int. Python kept the roll as a string and tried to "
                "multiply a string by ten. Add int parentheses around "
                "the input call. Third, the output shows literal "
                "curly braces around variable names, like Welcome, "
                "open brace player_name close brace exclamation. You "
                "forgot the f prefix on the f-string. Every string "
                "with placeholders needs the lowercase f right before "
                "the opening quote. Fourth, your output ALMOST "
                "matches expected but something's off. Count blank "
                "lines. Count leading spaces inside strings. "
                "Whitespace is part of CodeGrade's test. Two spaces "
                "vs four spaces on a destination indent will fail "
                "the test. Fifth, you forgot to delete the DEBUG "
                "prints from CP2 or CP3 before submitting. They were "
                "TEMPORARY. Remove every line that starts with print "
                "f DEBUG before you submit."
            ),
            key_terms=[
                ('NameError', "Python tried to use a name that isn't defined in the current scope."),
                ('TypeError', "An operation was attempted on a value of the wrong type, like multiplying a string by an int when you meant int times int."),
            ],
            think_about=[
                "Which of these five stumbles do you think you're most likely to make? Why?",
                'When you get an error, what\'s the first thing you should look at: the error message, the line number, or the variable in the error?',
            ],
            source_url='https://docs.python.org/3/tutorial/errors.html',
        ),
    )

    # =========================================================================
    # SLIDE 16: Final Check & Submit / What's Next
    # =========================================================================
    deck.add_overview_slide(
        title='Final Check, Submit, What\'s Next',
        section1_label='BEFORE YOU SUBMIT',
        section1_body=(
            "Run the whole program with name Maria and roll 15. Compare "
            "your output to the expected output in the lab sheet, line "
            "by line, word by word. Then run it again with a different "
            "roll, like 5 or 20, to confirm the math holds. Delete any "
            "DEBUG lines. Verify the file is named lab-1-1.py exactly. "
            "Confirm the docstring at the top has your name, abc123, "
            "section, and description."
        ),
        section2_body=(
            "Submit to CodeGrade as many times as you need. Unlimited "
            "submissions. If a test fails, read the failure message, "
            "fix the issue, resubmit. Don't try to submit a perfect "
            "first attempt. Iterate. The graders watch your final "
            "submission, not the count of attempts."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "Lab 1.1 is the foundation for Lab 1.2. You'll copy this "
            "code and add the power of DECISIONS, which is what M1-U2 "
            "is all about. The player will pick a destination from a "
            "menu, and your program will respond differently based on "
            "their choice. The Chapter 3 toolkit is next."
        ),
        notes=format_concept_notes(
            video_script=(
                "Before you submit, do the dry run. Run the whole "
                "program with Maria and 15. Open the expected output "
                "from the lab sheet. Compare line by line, word by "
                "word, character by character. Most submission "
                "failures come down to a single missing print or a "
                "single missing f prefix. Once it looks right, run it "
                "again with a different roll to make sure the math "
                "isn't accidentally hardcoded. Then delete any DEBUG "
                "lines, double-check the filename is lab dash 1 dash "
                "1 dot py exactly, and confirm your docstring has all "
                "four required pieces: name, abc123, section, and "
                "description. Then submit to CodeGrade. Submit early, "
                "submit often. Unlimited tries. There's no penalty "
                "for trying and failing. Read whatever error CodeGrade "
                "shows you, fix the specific issue, resubmit. Save "
                "your finished lab-1-1.py file when you're done. Lab "
                "1.2 next week starts by you copying this file. The "
                "course promise is that you carry your code forward "
                "all semester. That starts right here. Next week in "
                "M1-U2 we add the Chapter 3 toolkit, decisions. The "
                "player picks a destination from a menu, and the "
                "program responds differently based on the choice. "
                "You're going to feel the difference between a "
                "program that runs the same code every time and a "
                "program that branches. See you in U2."
            ),
            think_about=[
                "When you've finished Lab 1.1, what's one thing you'd want to add to make the game more interesting? Is that already on the roadmap, or is it something we'd add later?",
                "Out of everything in this lab, what felt easy and what felt foreign? That answer tells you what to review before U2.",
            ],
        ),
    )

    # =========================================================================
    # Save
    # =========================================================================
    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
