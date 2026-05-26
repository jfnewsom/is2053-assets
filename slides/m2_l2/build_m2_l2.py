"""
build_m2_l2.py - M2-L2 ("Lab 2.2: Texas Has Other Plans") walkthrough deck.

Module 2, Lab 2 (ENHANCE) | walks all 6 checkpoints.

Source-of-truth chain (do not invert):
  1. Modules/mod2/lab-2-2.py          - bedrock main game code
  2. Modules/mod2/function_library.py - bedrock library code
  3. pages/labs/json/lab-2-2.json     - student-facing assignment
                                        (now aligned to bedrock as of
                                        the May 25 hazard-count fix)
  4. This deck (downstream)

Pedagogy notes:
  - Pairs with M2-U2 which introduced functions, parameters, return
    values, the random module, and the function_library.py pattern.
  - Lab 2.2 builds the library STUDENTS will carry forward all
    semester. flip_coin, roll_d20, check_percentage land here.
  - Three hazards (1-3) is the locked plan per the World Bible -
    Tyler's CP6 Patch Note flags the scaling problem; later modules
    move hazards to a text file. Do not show 8 hazards.
  - flip_coin maps 1 -> HEADS and 0 -> TAILS. The CodeGrade
    deterministic fixture returns 1 for randint(0, 1) - reversed
    mapping is the #1 source of "everything times out" tickets.
    Surface this in CP1 speaker notes.

USAGE
-----
    python3 slides/m2_l2/build_m2_l2.py
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-25_M2-L2_Deck.pptx'
PNG_OUT = '/home/claude/m2_l2_pngs'
WORK_DIR = '/tmp/build_m2_l2'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 2.2: Texas Has Other Plans',
        subtitle='IS2053 Programming I  \u2022  Module 2  \u2022  Lab Walkthrough',
        notes=format_title_notes(
            deck_id='M2-L2',
            deck_title='Lab 2.2: Texas Has Other Plans',
            opening_line=(
                '"Welcome to the Lab 2.2 walkthrough. You just finished M2-U2 - '
                "functions, the random module, the function_library.py pattern. "
                "This is where we build that library for real and start adding "
                'randomness to the road trip. Six checkpoints. Let us go."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='From Fixed to Random',
        section_label='THE STORY',
        bold_oneliner='Lab 2.1 was predictable. Lab 2.2 is anything but.',
        body=(
            "Two files this week, not one. First, you build function_library.py and put three small "
            "functions in it: flip_coin, roll_d20, check_percentage. That file is the toolbox you carry "
            "forward to every remaining lab this semester. Second, you take your Lab 2.1 main game and "
            "rewire it. The fixed 50-mile travel becomes a D20 roll (1 to 20 times 10). The destination "
            "menu still asks where you want to go, but a coin flip decides whether Texas lets you. And "
            "every turn rolls for a hazard: a Buc-ee's, an armadillo crossing, a speed trap. The bones "
            "of the while loop from Lab 2.1 stay. What is INSIDE the loop gets much more interesting. "
            "Six checkpoints. CP1 and CP2 build the library. CP3 prepares the main game. CP4 adds the "
            "Destination Gate. CP5 replaces fixed travel with the D20. CP6 adds hazards."
        ),
        notes=format_concept_notes(
            video_script=(
                "Reset your mental model. You are not editing one file this week; you are working in two. "
                "function_library.py is brand new. It is going to live in the same folder as your main "
                "lab file from this week forward. Every lab from here on imports it. We are starting "
                "small: three functions. flip_coin returns HEADS or TAILS. roll_d20 returns 1 through 20. "
                "check_percentage takes a chance value and returns True or False at that rate. Tiny functions. "
                "Big consequences for the game. Once the library is in place, you take lab-2-1.py, save "
                "it as lab-2-2.py, and start wiring it to call your new functions. The Destination Gate "
                "is the first big surprise. The player picks Houston, then a coin flip decides whether "
                "they actually GET Houston, or whether Texas reroutes them to Corpus or Austin instead. "
                "Then D20 travel replaces your fixed 50 miles per turn. Now you do not know how many "
                "turns the trip takes. Then hazards: thirty percent chance per turn, three flavors, each "
                "resolved with another coin flip. Six checkpoints. Two files. A LOT of new texture in the "
                "game. The while loop you built last week barely changes. It just gets richer guests."
            ),
            think_about=[
                "Before CP1: why do three functions in a separate file feel like a bigger leap than three functions inside lab-2-2.py? What changes structurally?",
                "When you imported random in CP1 of Lab 2.1 (you didn't - that was Lab 2.2), what happened in the program? When you `import function_library` this week, what's the same and what's different?",
            ],
            source_url='https://docs.python.org/3/tutorial/modules.html',
        ),
    )

    # =========================================================================
    # SLIDE 3: CP1 Concept - Create Your Function Library
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 1: Create Your Function Library',
        bullets=[
            "Create a NEW file in the same folder as your lab: function_library.py. Exact spelling.",
            "Add a module docstring, then import random. This is the only import the library needs.",
            "Define flip_coin() with NO parameters and a docstring that says what it returns.",
            "Body: result = random.randint(0, 1). Map 1 -> 'HEADS', 0 -> 'TAILS'. The order matters.",
            "Test it with a 10-flip loop. Confirm you see a mix of HEADS and TAILS, then DELETE the test.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 1 is your first file from scratch in this course. New file, same folder as "
                "your lab-2-2.py is going to live, named exactly function_library.py with the underscore. "
                "Module docstring at the top with your name and a description. Then import random. Then "
                "your first function: def flip_coin paren paren colon. No parameters. The docstring "
                "right under the def says what it returns. Inside the body, you call random.randint(0, 1) "
                "and store the result. Then an if-else that returns the string HEADS when the result is "
                "1, and the string TAILS otherwise. CRITICAL: the mapping is 1 -> HEADS, 0 -> TAILS. If "
                "you flip it - 0 -> HEADS instead - your code still RUNS, but it breaks every CodeGrade "
                "test that uses flip_coin because the autograder's deterministic random fixture always "
                "returns 1 for randint(0, 1). Reversed mapping means every test thinks you got TAILS "
                "when the test expects HEADS. This is the number-one ticket I get on Lab 2.2 and labs "
                "downstream. Get the mapping right NOW. Bottom of the file, add a temporary test: a for "
                "loop that calls flip_coin ten times and prints the results. Run it. See a mix. THEN "
                "delete the test before moving on. CodeGrade does not want stray print statements at "
                "module scope."
            ),
            key_terms=[
                ('Module', 'A Python file you can import. function_library.py becomes a module the moment you save it.'),
                ('HEADS/TAILS mapping', 'In flip_coin: if random.randint(0,1) returns 1, return HEADS. If 0, return TAILS. Reversed mapping fails every grader.'),
            ],
            think_about=[
                "Why does the function need a docstring? What changes about the function if you forget it?",
                "If you wrote your test loop INSIDE the def (so it ran every time flip_coin was called), what would happen when lab-2-2.py imports the library?",
            ],
            source_url='https://docs.python.org/3/library/random.html#random.randint',
        ),
    )

    # =========================================================================
    # SLIDE 4: CP1 Demo - flip_coin
    # =========================================================================
    cp1_code = '''"""function_library.py - Bat City Collective toolkit."""

import random


def flip_coin():
    """Return 'HEADS' or 'TAILS' randomly."""
    result = random.randint(0, 1)
    if result == 1:
        return 'HEADS'
    else:
        return 'TAILS'
'''
    deck.add_demo_slide(
        title='Demo: flip_coin()',
        code=cp1_code,
        png='slide04_cp1.png',
        notes=format_demo_notes(
            code=cp1_code,
            instructor_notes=(
                "Read it top to bottom with the class. Module docstring first - one line is fine. Blank "
                "line, then import random. Two blank lines (PEP 8 prefers two between top-level items), "
                "then the function. def flip_coin parens. One-line docstring. result = random.randint(0, "
                "1). The if maps 1 to HEADS, the else handles everything else (which is just 0, since "
                "randint(0,1) returns only 0 or 1). Both branches return. Function ends cleanly. Triple "
                "underscore the mapping order out loud: ONE is HEADS, ZERO is TAILS. CodeGrade's "
                "deterministic random always returns 1 for randint(0, 1), so a reversed mapping fails "
                "every test. Get this right today and you do not pay for it for the rest of the semester."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 5: CP1 Output - 10 test flips
    # =========================================================================
    cp1_output = '''Testing flip_coin():
  Flip 1: HEADS
  Flip 2: TAILS
  Flip 3: HEADS
  Flip 4: HEADS
  Flip 5: TAILS
  Flip 6: TAILS
  Flip 7: HEADS
  Flip 8: TAILS
  Flip 9: HEADS
  Flip 10: TAILS
'''
    deck.add_output_slide(
        title='Output: Ten Test Flips',
        output_text=cp1_output,
        png='slide05_cp1_output.png',
        notes=format_output_notes(
            output_text=cp1_output,
            instructor_notes=(
                "This is what your temporary test loop produces. The exact mix of HEADS and TAILS will "
                "differ for each student because the random seed is different. THE POINT: you should see "
                "both values appear in some mix. If you see only HEADS or only TAILS, something is wrong. "
                "Either your random call is bad or your if-else is. If you see literal 'None' values, "
                "you forgot to return inside one of the branches. After verifying, DELETE the test loop "
                "from the bottom of the file. Library files should never have stray code at module "
                "scope - just function definitions and constants."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 6: CP2 Concept - Complete the Library
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 2: Complete the Library',
        bullets=[
            "Add constants D20_MIN = 1 and D20_MAX = 20 near the top (under imports).",
            "Define roll_d20() with no parameters. Return random.randint(D20_MIN, D20_MAX).",
            "Define check_percentage(chance) with ONE parameter. Returns True or False.",
            "Inside check_percentage: roll = random.randint(1, 100), then return roll <= chance.",
            "Test all three with another temporary block. Delete the test code before moving on.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 2 adds the other two functions your game needs. roll_d20 first. Two named "
                "constants at the top of the file, just under your imports: D20_MIN equals 1 and D20_MAX "
                "equals 20. Then the function. def roll_d20 parens, docstring, return random.randint of "
                "D20_MIN and D20_MAX. One line of body. Done. Next, check_percentage. This one is the "
                "first function in your library that takes a PARAMETER. def check_percentage paren "
                "chance paren. Docstring. Body: roll equals random.randint of 1 and 100. Return roll "
                "less-than-or-equal-to chance. The return statement is a comparison; Python evaluates "
                "it to True or False and returns whichever it is. Test all three. Roll a D20 five times "
                "and see a mix of 1-through-20 values. Call check_percentage(30) twenty times in a loop "
                "and count how many come back True. You should see a number close to 6 (30 percent of "
                "20), give or take a few because randomness is bursty in small samples. Delete the test "
                "code when you are satisfied."
            ),
            key_terms=[
                ('D20_MIN, D20_MAX', 'Named constants for the die range. UPPER_SNAKE_CASE because they never change.'),
                ('Comparison return', 'return roll <= chance evaluates the comparison to True or False, then returns it. Same pattern as if conditions, but you skip the if and just return the boolean.'),
            ],
            think_about=[
                "Why use named constants D20_MIN and D20_MAX instead of just writing random.randint(1, 20) directly?",
                "What's the difference between `return roll <= chance` and `if roll <= chance: return True; else: return False`? Which is cleaner?",
            ],
            source_url='https://docs.python.org/3/reference/expressions.html#comparisons',
        ),
    )

    # =========================================================================
    # SLIDE 7: CP2 Demo - roll_d20 + check_percentage
    # =========================================================================
    cp2_code = '''# At the top of function_library.py (under imports):
D20_MIN = 1
D20_MAX = 20


def roll_d20():
    """Return a random int from 1 to 20."""
    return random.randint(D20_MIN, D20_MAX)


def check_percentage(chance):
    """Return True 'chance' percent of the time."""
    roll = random.randint(1, 100)
    return roll <= chance
'''
    deck.add_demo_slide(
        title='Demo: roll_d20 and check_percentage',
        code=cp2_code,
        png='slide07_cp2.png',
        notes=format_demo_notes(
            code=cp2_code,
            instructor_notes=(
                "Two functions on one slide because they are small and related. Constants D20_MIN, "
                "D20_MAX go above both functions, at module scope, same place as the random import. "
                "roll_d20 is one line of body - a return statement using the constants. check_percentage "
                "is two lines - a roll, then a comparison return. The comparison `roll <= chance` "
                "evaluates to True or False, and the return hands that boolean back. No need to write "
                "the if-else explicitly. Walk through what check_percentage(30) does: roll a number 1 "
                "through 100. If roll is 1 through 30 (30 possible values), return True. If roll is 31 "
                "through 100 (70 possible values), return False. 30 out of 100 chances. That is 30 "
                "percent."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: CP3 Concept - Prepare the Main Game
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 3: Prepare the Main Game',
        bullets=[
            "Copy lab-2-1.py and save as lab-2-2.py. Update the docstring (title, description).",
            "Add `import random` at the top (you need it for the destination gate redirect and hazards).",
            "Add `import function_library` right under that - this loads YOUR library.",
            "Add two new constants: MILES_MULTIPLIER = 10 and HAZARD_CHANCE = 30.",
            "Run it once. With no other changes, it should still work exactly like Lab 2.1.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 3 is the bridge between your library and your main game. File-save-as your "
                "lab-2-1 to lab-2-2. Update the docstring: new title, new description. Chapter 5 "
                "concepts now, not just Chapter 4. Then two import lines at the top. Import random. "
                "Import function_library. Random comes first by convention (standard library imports go "
                "before your own). The library import has no .py extension, no quotes, just the bare "
                "module name. You wrote a module, you import it. Then two new named constants. "
                "MILES_MULTIPLIER equals 10. This is what we multiply the D20 roll by to get miles. A "
                "roll of 15 becomes 150 miles. HAZARD_CHANCE equals 30. This is the percent chance of a "
                "hazard each turn. You will pass it directly into check_percentage in CP6. After all "
                "these changes, your file should still RUN. You have not actually wired any of the new "
                "functions into the game yet. The point of this CP is to make sure imports work and "
                "constants are in place. Run it and play a quick Corpus trip. Should look identical to "
                "Lab 2.1."
            ),
            key_terms=[
                ('MILES_MULTIPLIER', 'New constant in Lab 2.2 (= 10). D20 roll times multiplier equals miles for that turn.'),
                ('HAZARD_CHANCE', 'New constant in Lab 2.2 (= 30). The percent chance, passed to check_percentage in CP6.'),
            ],
            think_about=[
                "Why does Python convention put standard library imports (random) before your own modules (function_library)? What's the practical benefit?",
                "What happens if you accidentally name your import `import function_library.py`? Try it. What does the error look like?",
            ],
            source_url='https://docs.python.org/3/reference/import.html',
        ),
    )

    # =========================================================================
    # SLIDE 9: CP3 Demo - imports + new constants
    # =========================================================================
    cp3_code = '''"""Lab 2.2: Texas Has Other Plans
Student Name / abc123 / Section
"""

import random
import function_library

# Distances from San Antonio (carried from Lab 2.1):
SAT_TO_CORPUS = 150
SAT_TO_HOUSTON = 200
SAT_TO_AUSTIN = 80

# NEW in Lab 2.2:
MILES_MULTIPLIER = 10
HAZARD_CHANCE = 30
'''
    deck.add_demo_slide(
        title='Demo: Imports and New Constants',
        code=cp3_code,
        png='slide09_cp3.png',
        notes=format_demo_notes(
            code=cp3_code,
            instructor_notes=(
                "Top of your lab-2-2.py file after CP3. Updated docstring. Two imports: random first, "
                "then function_library. Old distance constants stay (you still need them). The MILES_PER_TURN "
                "from Lab 2.1 is GONE - we replace it with MILES_MULTIPLIER which multiplies a D20 roll "
                "instead. HAZARD_CHANCE is brand new. Both new constants are integers in UPPER_SNAKE. "
                "If a student forgets to delete MILES_PER_TURN, it is harmless - it just becomes dead "
                "code. But if they forget to ADD MILES_MULTIPLIER and try to use it in CP5, NameError. "
                "Tell them: do this CP's adds before CP5's edits."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: CP4 Concept - The Destination Gate
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 4: The Destination Gate',
        bullets=[
            "After the if-elif-else sets destination and distance from menu choice, add the gate.",
            "Flip a coin: gate_result = function_library.flip_coin(). Print 'Result: {gate_result}!'",
            "HEADS: print a 'Texas says come on through' message. Keep destination/distance as-is.",
            "TAILS: print 'Texas has other plans...' Then pick from the OTHER 2 destinations.",
            "Use random.randint(1, 2) inside an if-elif on choice to pick the redirect destination.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 4 is the first place your library actually does work in the game. After the "
                "player picks a destination from the menu, you set destination and distance like before. "
                "Then, right there, you call function_library.flip_coin. Store the result. Print it so "
                "the player sees the suspense build. If HEADS, Texas cooperates. Print a friendly "
                "message and leave destination/distance alone. If TAILS, things get interesting. Print "
                "'Texas has other plans for you...' and then you have to PICK A NEW destination from the "
                "two the player did not choose. The bedrock pattern is: an if-elif-else by their "
                "original choice number, and inside each branch a random.randint(1, 2) plus a small "
                "if-else picks one of the OTHER two destinations. So if the player wanted Corpus, the "
                "redirect picks Houston or Austin. If they wanted Houston, redirect picks Corpus or "
                "Austin. And so on. Three branches in the outer if-elif, two-way randint inside each. "
                "Then keep the rest of the game running with the (possibly redirected) destination and "
                "distance. From the player's perspective: their choice got hijacked. From your code's "
                "perspective: destination and distance got reassigned."
            ),
            key_terms=[
                ('Destination Gate', 'A coin flip that decides whether the player gets their chosen destination or gets redirected to a different one.'),
                ('Redirect', 'When TAILS lands, the code picks one of the OTHER two destinations using random.randint(1, 2).'),
            ],
            think_about=[
                "Why does the redirect use random.randint(1, 2) instead of (0, 1) or (1, 3)? What does the range have to be?",
                "If a player picks 4 (invalid) and the else branch defaulted them to Corpus, what should the gate do on TAILS? Trace it.",
            ],
            source_url='https://docs.python.org/3/library/random.html#random.randint',
        ),
    )

    # =========================================================================
    # SLIDE 11: CP4 Demo - the gate logic (compressed, one redirect branch)
    # =========================================================================
    cp4_code = '''print('Flipping to see if Texas cooperates...')
gate_result = function_library.flip_coin()
print(f'Result: {gate_result}!')

if gate_result == 'HEADS':
    print('Texas says: "Y\\'all come on through!"')
else:
    print('Texas has other plans for you...')
    if choice == 1:  # wanted Corpus -> Houston or Austin
        redirect = random.randint(1, 2)
        if redirect == 1:
            destination = 'Houston'
            distance = SAT_TO_HOUSTON
    # (elif choice 2, else 3: see assignment sheet)
'''
    deck.add_demo_slide(
        title='Demo: The Destination Gate',
        code=cp4_code,
        png='slide11_cp4.png',
        notes=format_demo_notes(
            code=cp4_code,
            instructor_notes=(
                "Compressed for slide-fit: shows the gate flip and ONE redirect branch (when the player "
                "wanted Corpus). The full bedrock has parallel elif blocks for choice == 2 (wanted "
                "Houston) and choice == 3 (wanted Austin), each picking from the OTHER two destinations. "
                "Same pattern, different city names. Point at the gate flip first: store the result, "
                "print it for drama. Then the HEADS branch is trivial - destination already set, just "
                "print a message. The TAILS branch is the interesting one. Outer if by original choice, "
                "inner randint(1, 2) plus if-else by the random result. Speaker reminder: this demo "
                "only shows ONE of the three TAILS branches; students fill in the other two from the "
                "assignment sheet."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 12: CP4 Output - HEADS path
    # =========================================================================
    cp4_output = '''[After the menu and choice = 2]

Flipping to see if Texas cooperates...
Result: HEADS!

Texas says: "Y'all come on through!"
You're headed to Houston!
Distance: 200 miles
'''
    deck.add_output_slide(
        title='Output: Destination Gate (HEADS)',
        output_text=cp4_output,
        png='slide12_cp4_output.png',
        notes=format_output_notes(
            output_text=cp4_output,
            instructor_notes=(
                "Heads path - the player asked for Houston and Texas said yes. Five sections: menu, "
                "choice entry, flip announcement, flip result, the friendly Texas message. Note the "
                "ordering: 'Result: HEADS!' on its own line, blank line, then the Texas message. Then "
                "the standard 'You're headed to X' confirmation lines. For TAILS the only change is the "
                "block after 'Result: TAILS!': 'Texas has other plans for you...' instead of the friendly "
                "message, then a different destination shown. Not showing the TAILS path on a separate "
                "slide for budget; speaker note covers the variant."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13: CP5 Concept - D20 Travel System
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 5: D20 Travel System',
        bullets=[
            "Inside the while loop, REPLACE the fixed MILES_PER_TURN travel with a D20 roll.",
            "Call function_library.roll_d20() and store as roll. Print 'You rolled a {roll}!'",
            "Calculate miles_this_turn = roll * MILES_MULTIPLIER. A roll of 15 becomes 150 miles.",
            "Print 'You travel {miles_this_turn} miles...' so the player sees the impact.",
            "Update miles_remaining (subtract) and total_miles (add) using miles_this_turn, NOT MILES_PER_TURN.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 5 is the change you have been waiting for. Inside your while loop from Lab "
                "2.1, find the lines that printed 'You travel 50 miles' and updated miles_remaining "
                "with MILES_PER_TURN. Those lines change. Now: call function_library.roll_d20 and store "
                "the result as roll. Print the roll so the player sees it - 'You rolled a 15!' or "
                "whatever number came back. Multiply by MILES_MULTIPLIER and store as miles_this_turn. "
                "Print 'You travel 150 miles' using the new variable. THEN update miles_remaining and "
                "total_miles using miles_this_turn instead of MILES_PER_TURN. The accumulator pattern "
                "is the same - initialize before the loop, update inside, use after - but the amount "
                "varies each turn. Houston is 200 miles. Could be one turn (roll 20 -> 200 miles, "
                "arrive). Could be many turns (string of low rolls -> creeping toward Houston). The "
                "while-greater-than-zero condition does not change. It still exits when miles_remaining "
                "hits zero or goes negative. The trip length is now unpredictable."
            ),
            key_terms=[
                ('roll', 'The 1-20 value returned by function_library.roll_d20(). Stored per iteration.'),
                ('miles_this_turn', 'The variable that replaced MILES_PER_TURN inside the loop. Equals roll * MILES_MULTIPLIER. Different value each iteration.'),
            ],
            think_about=[
                "Why introduce a NEW variable miles_this_turn instead of just writing `roll * MILES_MULTIPLIER` everywhere? Trace what happens if you don't.",
                "What's the smallest possible Houston trip (rolls = 20 every turn)? What's the largest (worst-case rolls)? Predict before you test.",
            ],
            source_url='https://docs.python.org/3/library/random.html#random.randint',
        ),
    )

    # =========================================================================
    # SLIDE 14: CP5 Demo - D20 travel loop body
    # =========================================================================
    cp5_code = '''while miles_remaining > 0:
    print(f'--- Turn {turn} ---')
    print(f'Miles remaining: {miles_remaining}')

    # NEW: Roll D20 instead of using fixed MILES_PER_TURN
    roll = function_library.roll_d20()
    miles_this_turn = roll * MILES_MULTIPLIER
    print(f'You rolled a {roll}!')
    print(f'You travel {miles_this_turn} miles...')

    # Update tracking variables using miles_this_turn:
    miles_remaining = miles_remaining - miles_this_turn
    total_miles = total_miles + miles_this_turn

    turn = turn + 1
'''
    deck.add_demo_slide(
        title='Demo: D20 Travel Loop',
        code=cp5_code,
        png='slide14_cp5.png',
        notes=format_demo_notes(
            code=cp5_code,
            instructor_notes=(
                "The loop body from Lab 2.1, with the travel section swapped out. Walk it. While "
                "miles_remaining > 0 is the same condition. Turn header same. The line that printed "
                "'You travel 50 miles' is replaced by FOUR lines: the roll, the calculation, the roll "
                "announcement, and the travel message. Then the accumulator updates use miles_this_turn "
                "instead of MILES_PER_TURN. Comment is on the line where the call happens, so students "
                "know exactly what changed. The arrival announcement (if miles_remaining <= 0 - print "
                "'You made it!') is omitted here for slide space; that block carries over from Lab 2.1 "
                "unchanged. CP6 adds the hazard check inside the else branch of that arrival check."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 15: CP5 Output - Houston run with two big rolls
    # =========================================================================
    cp5_output = '''--- Turn 1 ---
Miles remaining: 200
You rolled a 15!
You travel 150 miles...
Miles remaining: 50

--- Turn 2 ---
Miles remaining: 50
You rolled a 15!
You travel 150 miles...

You made it to Houston!
'''
    deck.add_output_slide(
        title='Output: Houston in Two Rolls',
        output_text=cp5_output,
        png='slide15_cp5_output.png',
        notes=format_output_notes(
            output_text=cp5_output,
            instructor_notes=(
                "Houston with two rolls of 15 each. Turn 1: 200 miles to start, roll 15 -> 150 miles, "
                "now 50 left. Turn 2: 50 miles left, roll 15 -> 150 miles, overshoot by 100. The "
                "while condition checks 50 > 0 (True, enter the body). After the update, miles_remaining "
                "is -100, less than or equal to zero, so the inner if fires the arrival message. Loop "
                "exits next iteration. Notice we ROLLED 150 miles but only NEEDED 50 - the extra is "
                "thrown away. The trip summary will show Total Miles 300, not 200. The total tracks "
                "actual miles rolled, not distance to destination. That is a real-world quirk that "
                "matches the road trip vibe: you do not stop driving at the city limits sign."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 16: CP6 Concept - Hazard Encounters
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 6: Hazard Encounters',
        bullets=[
            "Before the while loop, add: hazards_faced = 0 and hazards_escaped = 0.",
            "Inside the loop, AFTER the miles update, call function_library.check_percentage(HAZARD_CHANCE).",
            "If True: hazards_faced += 1, then pick a hazard with random.randint(1, 3) and an if-elif-else.",
            "Print the hazard, flip a coin. HEADS: print escape, hazards_escaped += 1. TAILS: print consequence.",
            "Add Hazards Faced and Hazards Escaped to your Trip Summary block.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 6 is the most complex one. Three new variables: hazards_faced and "
                "hazards_escaped, both starting at zero before the while loop (same place you init "
                "miles_remaining, total_miles, and turn). Inside the loop, AFTER the miles update, you "
                "call check_percentage with HAZARD_CHANCE - that returns True 30 percent of the time. "
                "When it returns True, a hazard happens. Bump hazards_faced. Print 'star star star "
                "HAZARD star star star'. Then pick which hazard with random.randint(1, 3). Three "
                "hazards: Buc-ee's, Armadillo, Speed trap. Each hazard has a name, a HEADS message (you "
                "escaped) and a TAILS message (you got got). After picking, print the hazard name. Then "
                "flip a coin to determine the outcome. If HEADS, print the escape message and bump "
                "hazards_escaped. If TAILS, print the consequence message - no increment to "
                "hazards_escaped. Lastly, add two lines to your existing Trip Summary block: Hazards "
                "Faced and Hazards Escaped. The reference table in the assignment sheet has the exact "
                "name and message text for all three hazards. Use the text verbatim - the autograder "
                "compares output line-by-line."
            ),
            key_terms=[
                ('hazards_faced', 'Counts every hazard that fires. Increments each time check_percentage returns True.'),
                ('hazards_escaped', 'Counts only the HEADS outcomes. Increments only inside the if flip == HEADS branch.'),
            ],
            think_about=[
                "Why does hazards_faced increment BEFORE the coin flip but hazards_escaped only on HEADS? Trace what happens if you flip those.",
                "The hazard check is INSIDE the loop, AFTER the miles update. What would happen if you put it BEFORE the miles update instead?",
            ],
            source_url='https://docs.python.org/3/library/random.html#random.randint',
        ),
    )

    # =========================================================================
    # SLIDE 17: CP6 Demo A - Pick the hazard
    # =========================================================================
    cp6a_code = '''# Inside the while loop, AFTER the miles update each turn:

if function_library.check_percentage(HAZARD_CHANCE):
    hazards_faced = hazards_faced + 1
    print()
    print('*** HAZARD! ***')

    hazard_type = random.randint(1, 3)
    if hazard_type == 1:
        hazard = "Buc-ee's appears!"
        heads_msg = "You resist the beaver's call."
        tails_msg = "Lost 2 hours on beef jerky."
    # elif 2 (Armadillo), else (Speed trap) - see table
'''
    deck.add_demo_slide(
        title='Demo: Hazard Pick (CP6 part 1)',
        code=cp6a_code,
        png='slide17_cp6a.png',
        notes=format_demo_notes(
            code=cp6a_code,
            instructor_notes=(
                "First half of CP6. Inside the loop, AFTER the miles math, we ask 'did a hazard "
                "happen?' That is the check_percentage call. 30 percent True. When True, three things: "
                "bump hazards_faced, print a blank line for breathing room, print the HAZARD banner. "
                "Then pick. random.randint(1, 3) returns 1, 2, or 3. The if-elif-else assigns three "
                "variables: hazard (the name), heads_msg (escape text), tails_msg (consequence text). "
                "Showing only branch 1 fully expanded here for slide space. Students fill in branches "
                "2 and 3 from the reference table in the assignment sheet. NEXT SLIDE: what happens "
                "AFTER the hazard is picked - we flip another coin for the outcome."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 18: CP6 Demo B - The escape coin flip
    # =========================================================================
    cp6b_code = '''# Continuing inside the same `if check_percentage` block:

    print(hazard)
    flip = function_library.flip_coin()
    print(f'{flip}!')

    if flip == 'HEADS':
        print(heads_msg)
        hazards_escaped = hazards_escaped + 1
    else:
        print(tails_msg)
'''
    deck.add_demo_slide(
        title='Demo: Escape Coin Flip (CP6 part 2)',
        code=cp6b_code,
        png='slide18_cp6b.png',
        notes=format_demo_notes(
            code=cp6b_code,
            instructor_notes=(
                "Second half of CP6. Hazard is now picked - hazard, heads_msg, tails_msg are all "
                "assigned from CP6 part 1. Print the hazard name. Flip a coin. Announce the result. "
                "Then a simple if-else: HEADS prints the escape and bumps hazards_escaped; TAILS prints "
                "the consequence and does NOT bump (player got got). Critical: hazards_escaped lives "
                "INSIDE the if-flip-HEADS branch. If you put it outside, every hazard counts as an "
                "escape and the trip summary lies. After this block, the loop continues with the next "
                "iteration - hazards do not affect miles_remaining. They are pure side events."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 19: CP6 Output - Hazard fire excerpt
    # =========================================================================
    cp6_output = '''--- Turn 1 ---
Miles remaining: 200
You rolled a 15!
You travel 150 miles...
Miles remaining: 50

*** HAZARD! ***
Buc-ee's appears!
HEADS!
You resist the beaver's call.
'''
    deck.add_output_slide(
        title='Output: A Hazard Fires',
        output_text=cp6_output,
        png='slide19_cp6_output.png',
        notes=format_output_notes(
            output_text=cp6_output,
            instructor_notes=(
                "Turn 1 of a Houston trip with a hazard. Standard turn header. The travel happens "
                "first - roll, miles, update. Miles_remaining shown after the update (50 miles left). "
                "Then a blank line and the HAZARD banner. Buc-ee's appears (this is hazard 1, the most "
                "common with the deterministic fixture). Coin came up HEADS. Escape message. Then the "
                "loop would continue normally. The Trip Summary at the end of the run will show "
                "Hazards Faced equal to whatever total hazards fired, Hazards Escaped equal to "
                "HEADS-only outcomes. NOT shown here: the trip summary block. That gains two lines "
                "(Hazards Faced and Hazards Escaped) below the existing Total Miles line."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 20: Common Stumbles (sourced from lab JSON finalCheck.ifSomethingBreaks)
    # =========================================================================
    deck.add_concept_slide(
        title='Common Stumbles',
        bullets=[
            "Gate always TAILS in tests -> CP1. Reversed flip_coin mapping. Must be: result == 1 -> HEADS.",
            "ModuleNotFoundError: 'function_library' -> CP3. Files in different folders, or typo in import.",
            "AttributeError: no attribute 'flip_coin' -> CP1/CP2. Missing or misspelled function in library.",
            "NameError: 'hazards_faced' in trip summary -> CP6. Initialize BEFORE the loop, not inside.",
            "Hazards Faced shows 0 after a long trip -> CP6. Increment is OUTSIDE the if check_percentage block.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Five things that bite hardest on this lab. Memorize the order. ONE: Gate result is "
                "always TAILS in CodeGrade. That means you reversed the HEADS/TAILS mapping inside "
                "flip_coin. The autograder's random fixture always returns 1 for randint(0, 1). Your "
                "if-else MUST map 1 to HEADS. Open CP1, check the mapping. TWO: ModuleNotFoundError "
                "with the name function_library in it. Your library file is somewhere Python cannot see "
                "it. Both files have to live in the same folder. Or you mistyped the import. "
                "function_library, not function-library, not functionLibrary. THREE: AttributeError "
                "complaining the module has no attribute flip_coin (or roll_d20, or check_percentage). "
                "The function is missing from your library file, or its name is spelled differently "
                "there than in your main file. Open function_library.py and verify. FOUR: NameError on "
                "hazards_faced. You initialized it inside the while loop body instead of before. Move "
                "it up alongside total_miles and turn. FIVE: Hazards Faced shows 0 even after a long "
                "trip. The increment is outside the if check_percentage block, so the line never runs "
                "when a hazard fires. The increment must be INDENTED inside the if block. Indentation "
                "is membership. Get the indentation right and the counts will follow."
            ),
            key_terms=[
                ('Reversed mapping', 'When flip_coin returns TAILS for randint=1 and HEADS for randint=0. Every CodeGrade test fails because the deterministic fixture always returns 1.'),
                ('Indentation membership', 'A line is inside a block if and only if it is indented under that block. Misplaced increments are the #2 cause of wrong trip summary counts.'),
            ],
            think_about=[
                "Which of these five is most likely to bite YOU? Why? Pre-mitigate.",
                "When CodeGrade says 'AttributeError: module function_library has no attribute X', what's the first place to look? The lab file or the library file?",
            ],
            source_url='https://docs.python.org/3/tutorial/errors.html',
        ),
    )

    # =========================================================================
    # SLIDE 21: Final Check & Submit / What's Next
    # =========================================================================
    deck.add_overview_slide(
        title='Final Check, Submit, What\'s Next',
        section1_label='BEFORE YOU SUBMIT',
        section1_body=(
            "Run the program with each destination at least once. Try invalid choice 4 to test the "
            "default. Verify the gate flips both ways across runs. Verify D20 rolls show variable "
            "miles per turn. Verify hazards show all three types (run enough trips). Delete any DEBUG "
            "prints from both files. Confirm filenames: lab-2-2.py AND function_library.py exactly. "
            "Both submitted to CodeGrade together."
        ),
        section2_body=(
            "Submit BOTH files to CodeGrade together. Unlimited submissions: if a test fails, read the "
            "failure message, use the redirect map to find the right CP, fix, resubmit. The number-one "
            "failure on this lab is the reversed HEADS/TAILS mapping. If most of your tests fail at "
            "once, that is the FIRST place to look."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "Lab 2.3 is the MASTER. The function_library grows two more functions (get_valid_int, "
            "get_yes_no). The game gains input validation loops and a play-again sentinel loop, so one "
            "session can be multiple trips. Trip stats accumulate across games. The Chapter 4 toolkit "
            "completes (sentinel loops, input validation loops). The library you wrote this week is "
            "the foundation for every lab from here on."
        ),
        notes=format_concept_notes(
            video_script=(
                "Before submitting, do the run-throughs. Each destination at least once. Choice 4 to "
                "test the default. Watch the gate flip both ways across attempts. Watch D20 rolls vary "
                "the miles. Try to see all three hazards over enough trips. Delete EVERY DEBUG line "
                "from BOTH files - the test loops you added in CP1 and CP2 to verify the library are "
                "the most common forgotten DEBUGs. Confirm filenames precisely. lab-2-2.py and "
                "function_library.py, no caps, no spaces. Both files get submitted to CodeGrade in the "
                "same submission. If you forget the library, the autograder cannot run anything. If a "
                "lot of tests fail at the same time, the first thing to check is the HEADS/TAILS "
                "mapping in flip_coin. Number-one ticket I get. Lab 2.3 is MASTER week. Library grows "
                "by two more functions. Input validation and sentinel loops complete the Chapter 4 "
                "toolkit. The play-again loop means a single run can be many trips - session stats "
                "across games. We will walk it next week. See you in 2.3."
            ),
            think_about=[
                "When you finished Lab 2.2, what new thing felt EASIEST and what felt HARDEST? Tell me before 2.3.",
                "If you had to add ONE more function to function_library.py right now, what would it do? Save the idea.",
            ],
        ),
    )

    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
