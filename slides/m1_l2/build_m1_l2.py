"""
build_m1_l2.py - M1-L2 ("Lab 1.2: Choose Your Destination") slide deck.

Module 1, Lab 2 (ENHANCE) | Chapter 3 application
Pairs with: Lab 1.2 assignment sheet (lab-1-2.json)

PIPELINE FRAMING (locked May 24, 2026)
--------------------------------------
M1-L2 is a LAB WALKTHROUGH, not a concept introduction. M1-U2 already
taught the Chapter 3 toolkit (if, if-else, if-elif-else, the else as
garbage collector, the 4-variable conditional assignment pattern, abs(),
comparison operators including >=). This deck WALKS THE CHECKPOINTS of
Lab 1.2 with explicit callbacks to U2 concepts. We do NOT re-teach.

SCOPE (verified against lab-1-2.py and lab-1-2.json)
- CP1: copy Lab 1.1, drop HOU_TO_GALVESTON, add destination menu prints
- CP2: if-elif-else chain setting destination/distance/status/message in
       each branch including else (the 4-var pattern from U2)
- CP3: miles_remaining = miles_rolled - distance; if miles_remaining >= 0
       made it, else use abs() to report miles_short
- CP4: Trip Summary print block

KEY THING TO SURFACE: the miles_remaining math FLIPPED from Lab 1.1
- Lab 1.1: result = constant - miles_rolled (NEGATIVE means made it)
- Lab 1.2: result = miles_rolled - distance (POSITIVE/zero means made it)
This is intentional but easy to miss. CP3 concept slide calls it out.

OUT OF SCOPE
- Anything Chapter 4+ (loops, functions, lists, dicts, classes)
- Nested if (M1-L3 territory)
- Logical operators and/or/not (M1-L3 territory)
- Format specs

USAGE
-----
    python3 slides/m1_l2/build_m1_l2.py

The deck is written to /home/claude/IS2053_2026-05-24_M1-L2_Deck.pptx.
PNGs land in /home/claude/m1_l2_pngs/.
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-24_M1-L2_Deck.pptx'
PNG_OUT = '/home/claude/m1_l2_pngs'
WORK_DIR = '/tmp/build_m1_l2'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 1.2: Choose Your Destination',
        subtitle='IS2053 Programming I  \u2022  Module 1  \u2022  Lab Walkthrough (ENHANCE)',
        notes=format_title_notes(
            deck_id='M1-L2',
            deck_title='Lab 1.2: Choose Your Destination',
            opening_line=(
                '"You finished U2, the Chapter 3 toolkit. Today we take if-elif-else, '
                'the else as garbage collector, abs, and the 4-variable assignment '
                'pattern, and we put all of them to work in Lab 1.2. Four checkpoints, '
                "about an hour. Let's go."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='ENHANCE: Same Foundation, New Power',
        section_label='THE STORY',
        bold_oneliner='The travel calculator works. Time to make it interactive.',
        body=(
            "Lab 1.1 was a calculator. Same questions, same math, same report, "
            "every run. Lab 1.2 is a game. The player picks a destination from "
            "a menu, and the program responds differently to each choice. You "
            "copy your Lab 1.1 file as the starting point, drop one constant, "
            "add a menu, and stack two decision structures on top. By the end "
            "of this lab, no two runs of your program look the same."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome to the second lab walkthrough. This is an ENHANCE "
                "unit, which means you don't start from scratch. You open "
                "your finished Lab 1.1 file, save it as lab dash 1 dash 2 "
                "dot py, and then you grow it. The big idea of this lab is "
                "that you take a working program that runs the same code "
                "every time and turn it into a program that BRANCHES based "
                "on what the user picks. The destination menu is the new "
                "input. The if-elif-else chain is the new logic. The "
                "made-it-or-not check is the second decision. The trip "
                "summary is the new output. Four checkpoints. Each one "
                "applies something specific we covered in M1-U2. As we go "
                "through them, listen for the callbacks. When I say 'remember "
                "from U2,' that's a cue that the concept is already in your "
                "toolbox and we're just plugging it in. No new concepts get "
                "introduced in this video. Only applications. By the end, "
                "you'll have walked all four checkpoints and seen the code "
                "shape. Then you open your lab 1.1 file, save a copy, and "
                "type."
            ),
            think_about=[
                "Before we dig in, what's one thing about Lab 1.1 you'd want to change to make it feel more like a game?",
                "If you had to guess, which checkpoint is going to be the hardest? Why?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html',
        ),
    )

    # =========================================================================
    # SLIDE 3: CP1 Concept - Copy & Simplify
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 1: Copy & Simplify',
        bullets=[
            "Save your Lab 1.1 file as lab-1-2.py. You'll edit the copy, not the original.",
            "DROP the HOU_TO_GALVESTON constant. You're down to three: SAT_TO_CORPUS, SAT_TO_HOUSTON, SAT_TO_AUSTIN.",
            "DELETE the Travel Report block and all per-destination remaining calculations from Lab 1.1.",
            "ADD a destination menu printed to the screen, then int(input()) to get the player's choice.",
            "CP1 is mechanical: copy, delete, add the menu. No logic yet. That comes in CP2.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 1 is housekeeping. Save your Lab 1.1 file as "
                "lab dash 1 dash 2 dot py. Always work on the copy, never "
                "the original. If something goes wrong in Lab 1.2 you want "
                "Lab 1.1 still working as your fallback. Now you simplify. "
                "Galveston was in Lab 1.1 because we wanted to show a two "
                "step calculation. Lab 1.2 doesn't need it. You'll add "
                "Galveston back in Lab 1.3 next week, but for now, delete "
                "the HOU_TO_GALVESTON constant and the Galveston "
                "calculation. While you're at it, delete the whole Travel "
                "Report block at the bottom. It's going to be replaced by "
                "the Trip Summary at the end of CP4. You'll also delete "
                "the three remaining-miles calculations from CP3 of Lab "
                "1.1. We're going to replace them with ONE remaining "
                "calculation, after the player picks a destination. Now "
                "add the new piece. After the line where you set "
                "miles_rolled, you print a small destination menu and "
                "you get the player's choice. Three options, numbered 1, "
                "2, 3. The choice comes back from int input, exactly the "
                "same pattern as the roll. CP1 is mechanical. No "
                "decisions yet. The if-elif-else is CP2's job."
            ),
            key_terms=[
                ('ENHANCE lab', "A lab where you grow an existing program instead of starting from scratch. Module 1's middle lab is always ENHANCE."),
            ],
            think_about=[
                "Why save Lab 1.1 as a NEW file instead of editing it directly? What's the worst case if you skip that step?",
                'CP1 ends with the player having picked 1, 2, or 3. Where is that information stored? What gets done with it next?',
            ],
            source_url='https://docs.python.org/3/library/functions.html#input',
        ),
    )

    # =========================================================================
    # SLIDE 4: CP1 Demo - new menu block added to Lab 1.1
    # =========================================================================
    cp1_code = """    # ---- After roll and miles_rolled, ADD this block ----
    print(f'You rolled {roll}! That gives you {miles_rolled} miles.')
    print()

    print('Where would you like to go?')
    print(f'  1. Corpus Christi - {SAT_TO_CORPUS} miles (BEACH!)')
    print(f'  2. Houston - {SAT_TO_HOUSTON} miles')
    print(f'  3. Austin - {SAT_TO_AUSTIN} miles')
    print()

    choice = int(input('Enter your choice (1-3): '))
    print()
"""

    deck.add_demo_slide(
        title='Demo: The New Menu Block',
        code=cp1_code,
        png='slide04_cp1.png',
        notes=format_demo_notes(
            code=cp1_code,
            instructor_notes=(
                "This block goes AFTER you compute miles_rolled and "
                "BEFORE the if-elif-else chain you'll write in CP2. "
                "Walk top to bottom. The first f-string is a small "
                "callback that tells the player what they rolled and "
                "how many miles that gives them. Blank line. Then the "
                "menu: 'Where would you like to go,' question mark, "
                "then three indented options listing each destination "
                "with its distance. Notice the leading spaces inside "
                "the strings for visual indent. Then a blank, then the "
                "choice input wrapped in int. Same int input pattern "
                "as the roll input from CP2 of Lab 1.1. The choice is "
                "now an integer in memory. Tell students that as of "
                "this slide, nothing decides anything yet. The menu "
                "asks, the choice is captured, but the program "
                "doesn't yet DO anything different based on it. That's "
                "CP2. Mention the required prompt string: 'Enter your "
                "choice (1-3): '. CodeGrade checks the exact text "
                "including the trailing space."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 5: CP1 Output - banner + roll + menu, no logic yet
    # =========================================================================
    cp1_output = """\
DEEP IN THE HEART: A LONE STAR JOURNEY

What is your name, traveler? Maria

Welcome, Maria!
You are in San Antonio. Your goal: reach the beach!

What did you roll? (1-20): 15

You rolled 15! That gives you 150 miles.

Where would you like to go?
  1. Corpus Christi - 150 miles (BEACH!)
  2. Houston - 200 miles
  3. Austin - 80 miles

Enter your choice (1-3): 1"""

    deck.add_output_slide(
        title='Output: After CP1 (menu shown, choice captured)',
        output_text=cp1_output,
        png='slide05_cp1_output.png',
        notes=format_output_notes(
            output_text=cp1_output,
            instructor_notes=(
                "Maria rolls 15 and picks Corpus. Right now the "
                "program ends here. The choice variable holds the "
                "integer 1, but nothing has been done with it. If you "
                "added a 'print(choice)' debug line at the very end, "
                "it would print 1 and then the program would exit. "
                "That's correct for CP1. If your menu shows the wrong "
                "distances, you probably forgot to drop a constant or "
                "you have a typo. If your menu doesn't show at all, "
                "you're missing the print statements. If the choice "
                "input doesn't appear, you're missing the input line."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 6: CP2 Concept - The if-elif-else Chain (the centerpiece)
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 2: The if-elif-else Chain',
        bullets=[
            "Remember from U2: if-elif-else handles three or more choices in one structure. The else catches everything else.",
            "Set FOUR variables in EVERY branch: destination, distance, status, message.",
            "Include the else branch. Always. It catches the player who types 99 instead of 1, 2, or 3.",
            "Forgetting one variable in one branch is the #1 NameError trap in this lab.",
            "After this block runs, those four variables are guaranteed to exist no matter what the player typed.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 2 is where you apply the centerpiece of "
                "U2. The if-elif-else chain. Three valid choices, plus "
                "the else for invalid input. Each branch sets up the "
                "same four variables with different values. "
                "destination, distance, status, message. Why those "
                "four? Because everything downstream needs them. The "
                "miles_remaining math in CP3 needs distance. The made "
                "it message in CP3 needs destination and message. The "
                "Trip Summary in CP4 needs all four. So you set them "
                "up here, once, in the right branch. Now the trap. "
                "Remember the slide in U2 about setting multiple "
                "variables across branches? This is the lab that the "
                "slide was talking about. If you forget to set even "
                "one variable in even one branch, your program runs "
                "fine until the user happens to pick THAT branch. "
                "Then they get a NameError downstream when the trip "
                "summary tries to print a variable that was never "
                "assigned. The error message points to the print "
                "line, not to the if-elif-else block where the bug "
                "actually lives. So slow down and double-check: same "
                "four variable names, every branch, including the "
                "else. The else branch sets destination to Nowhere, "
                "distance to zero, status to ERROR, message to "
                "Invalid choice. That way, if the player typed 99, "
                "the program still has values for all four variables "
                "and the downstream code keeps working. The else is "
                "your safety net. Always."
            ),
            key_terms=[
                ('4-variable conditional assignment pattern', 'Each branch of an if-elif-else sets the SAME set of variables, with different values per branch. All branches must set all variables.'),
            ],
            think_about=[
                "If the user types 5 and you forgot the else branch, what happens to your four variables? When does the error appear?",
                "Why does it matter that the else sets distance to 0 specifically? What would break if you set it to something else, like -1?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 7: CP2 Demo - if-elif-else with first branch + placeholders + else
    # =========================================================================
    cp2_code = """    if choice == 1:
        destination = 'Corpus Christi'
        distance = SAT_TO_CORPUS
        status = 'BEACH'
        message = 'The Sparkling City by the Sea!'
    elif choice == 2:  # Houston: same shape, different values
        ...
    elif choice == 3:  # Austin: same shape, different values
        ...
    else:
        destination = 'Nowhere'
        distance = 0
        status = 'ERROR'
        message = 'Invalid choice!'
"""

    deck.add_demo_slide(
        title='Demo: The 4-Variable Pattern Across Branches',
        code=cp2_code,
        png='slide07_cp2.png',
        notes=format_demo_notes(
            code=cp2_code,
            instructor_notes=(
                "What's on screen is the structure: the first branch "
                "fully spelled out, the middle two branches "
                "represented as placeholders so the pattern stays "
                "visible, and the else fully spelled out so students "
                "see what the safety net looks like. In their actual "
                "code, every branch is fully spelled out. Walk top "
                "to bottom. Choice equals one, set destination to "
                "Corpus Christi, distance to SAT_TO_CORPUS, status "
                "to BEACH, message to The Sparkling City by the "
                "Sea. Done. That's one branch. Elif choice equals "
                "two follows the same four-line shape with Houston "
                "values. Elif choice equals three follows the same "
                "shape with Austin values. Then the else. "
                "destination Nowhere, distance zero, status ERROR, "
                "message Invalid choice exclamation. Four lines in "
                "every branch. Same four variable names. Look at "
                "the else branch with the class and ask: why "
                "destination equals Nowhere? Why distance equals "
                "zero? Why status equals ERROR? Because the "
                "downstream code is going to use these variables. "
                "The else branch can't leave them undefined. The "
                "Houston message references Galveston, which is a "
                "callback to Lab 1.1 and a forward reference to "
                "Lab 1.3 where Galveston comes back."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: CP2 Output - debug verification
    # =========================================================================
    cp2_output = """\
DEBUG (after the if-elif-else, for choice = 2):
  destination = 'Houston'
  distance = 200
  status = 'PROGRESS'
  message = 'Space City! Galveston is only 50 more miles...'

DEBUG (for choice = 99):
  destination = 'Nowhere'
  distance = 0
  status = 'ERROR'
  message = 'Invalid choice!'"""

    deck.add_output_slide(
        title='Output: Variables After the Chain',
        output_text=cp2_output,
        png='slide08_cp2_output.png',
        notes=format_output_notes(
            output_text=cp2_output,
            instructor_notes=(
                "If you add temporary DEBUG prints right after the "
                "if-elif-else block, this is what you should see. "
                "Top half: the player picked 2 (Houston), so the "
                "second elif fired and set the Houston values. "
                "Bottom half: the player typed 99, the else fired "
                "and set the safety-net values. The point to land: "
                "in BOTH cases, all four variables exist. The "
                "program will not crash downstream. That's what the "
                "else clause buys you. Remind students that any "
                "DEBUG print they add is TEMPORARY. Delete them all "
                "before submitting."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 9: CP3 Concept - Did You Make It? (the math flip + abs)
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 3: Did You Make It?',
        bullets=[
            "Calculate miles_remaining = miles_rolled - distance. Note the order: rolled MINUS distance.",
            "This flips Lab 1.1's convention. Now POSITIVE or zero means made it, NEGATIVE means short.",
            "Remember from U2: if-else gives you two paths. One runs when True, the other when False.",
            "Use miles_remaining >= 0 to check. The >= treats exact arrival (zero miles to spare) as 'made it.'",
            "If they fell short, use abs() to print a positive 'miles short' number instead of a negative one.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 3 is where you check whether the player "
                "actually made it to the destination they picked. "
                "Important. The math in this lab is FLIPPED from Lab "
                "1.1. In Lab 1.1 we wrote destination minus rolled, "
                "and a negative result meant the player made it with "
                "miles to spare. In Lab 1.2 we write rolled minus "
                "distance, which means positive or zero is good. The "
                "difference matters. The lab needs to use greater "
                "than or equal to zero to check made it, and that "
                "reads cleaner with the Lab 1.2 convention. Don't "
                "copy Lab 1.1's math direction. Use rolled minus "
                "distance. Once you have miles_remaining, plug it "
                "into an if-else. Remember from U2. If miles_remaining "
                "is greater than or equal to zero, they made it. "
                "Print made it. Print the message variable, which "
                "came from the if-elif-else in CP2. Print how many "
                "miles to spare. Else, they fell short. The remaining "
                "number is negative. Don't print a negative number "
                "to the player. Compute miles_short equals abs of "
                "miles_remaining. abs returns the positive version. "
                "Then print 'You ran out of miles, X miles from "
                "destination.' That's the made-it-or-not block. Two "
                "destinations, both feed off the variables CP2 set "
                "up. Notice how clean this is. The if-elif-else in "
                "CP2 did all the heavy lifting. CP3 just asks one "
                "question and prints one of two reports."
            ),
            key_terms=[
                ('Greater-than-or-equal (>=)', 'A comparison that treats the boundary as included. miles_remaining >= 0 counts exact arrival as made it.'),
                ('abs()', 'Built-in that returns the absolute value. abs(-50) is 50.'),
            ],
            think_about=[
                "Why use >= 0 instead of > 0? What happens if a player rolls EXACTLY the right distance?",
                "If you forgot the abs() and printed 'miles short: -50', would the program crash? Or would it just look wrong to the player?",
            ],
            source_url='https://docs.python.org/3/library/functions.html#abs',
        ),
    )

    # =========================================================================
    # SLIDE 10: CP3 Demo - if-else with abs
    # =========================================================================
    cp3_code = """    miles_remaining = miles_rolled - distance

    print(f'Heading to {destination}!')
    print(f'Distance: {distance} miles')
    print()

    if miles_remaining >= 0:
        print(f'You made it to {destination}!')
        print(message)
        print(f'Miles to spare: {miles_remaining}')
    else:
        miles_short = abs(miles_remaining)
        print(f'You ran out of miles {miles_short} miles from {destination}.')
        print('You will need to roll again next time!')
"""

    deck.add_demo_slide(
        title='Demo: The Made-It-Or-Not Block',
        code=cp3_code,
        png='slide10_cp3.png',
        notes=format_demo_notes(
            code=cp3_code,
            instructor_notes=(
                "Walk top to bottom. Line one, the math. Rolled "
                "MINUS distance, not the other way around. Stop and "
                "say that twice. Then a small lead-in: 'Heading to' "
                "destination, 'Distance' so many miles, blank line. "
                "Then the if-else. Inside the if, three prints "
                "telling them they made it and showing the slack. "
                "Inside the else, first compute miles_short using "
                "abs, then print the ran-out message and a "
                "consolation line. The variables destination, "
                "distance, and message all come from CP2's "
                "if-elif-else chain. They're guaranteed to exist "
                "because CP2 set them in every branch including "
                "the else. That's the payoff of CP2's discipline."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: CP3 Output - both branches firing
    # =========================================================================
    cp3_output = """\
Scenario A (rolled 15, chose Houston, distance 200):
Heading to Houston!
Distance: 200 miles

You ran out of miles 50 miles from Houston.
You will need to roll again next time!

Scenario B (rolled 20, chose Austin, distance 80):
Heading to Austin!
Distance: 80 miles

You made it to Austin!
Keep it weird! Nice city, but no beach here.
Miles to spare: 120"""

    deck.add_output_slide(
        title='Output: Two Scenarios Through the If-Else',
        output_text=cp3_output,
        png='slide11_cp3_output.png',
        notes=format_output_notes(
            output_text=cp3_output,
            instructor_notes=(
                "Two scenarios show both branches firing. Top: "
                "Maria rolled 15 (150 miles) and picked Houston "
                "(200 miles needed). miles_remaining is 150 minus "
                "200, which is negative 50. The if condition "
                "(greater than or equal to zero) is False. The "
                "else branch fires. miles_short is abs of negative "
                "50, which is 50. The ran-out message prints with "
                "50 as a positive number. Bottom: a different "
                "player rolled 20 (200 miles) and picked Austin "
                "(80 miles needed). miles_remaining is 200 minus "
                "80, which is positive 120. The if condition is "
                "True. The made-it branch fires with the Austin "
                "message and the slack number. Both runs use the "
                "same code. Different inputs produce different "
                "outputs. That's exactly what U2 was building "
                "toward."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 12: CP4 Concept - Trip Summary
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 4: Trip Summary',
        bullets=[
            "Print a Trip Summary block: banner, six labeled lines, closing banner.",
            "Each line is an f-string using one of the variables already in scope.",
            "Driver, Destination, Distance, Miles rolled, Miles remaining, Status. All six.",
            "Every variable here came from somewhere earlier. The summary is just final display.",
            "Same banner trick as Lab 1.1: print('=' * 50) for the dividing lines.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 4 is the closer. The Trip Summary is a "
                "tidy report showing every important value for the "
                "run. No new logic, no new variables. Just pulling "
                "together what's already in memory and presenting "
                "it. Six f-strings. Driver pulls from player_name "
                "(from CP2 of Lab 1.1). Destination pulls from the "
                "if-elif-else in CP2 of this lab. Distance pulls "
                "from the same place. Miles rolled pulls from "
                "Lab 1.1's roll calculation. Miles remaining "
                "pulls from CP3 of this lab. Status pulls from "
                "CP2 of this lab. Wrap it all in equal-sign "
                "banners like Lab 1.1. Add some blank prints for "
                "breathing room. That's it. If your variables "
                "are right, this block writes itself."
            ),
            key_terms=[
                ('Variable scope', "The region of code where a variable is accessible. All your locals are accessible anywhere inside main() after they're assigned."),
            ],
            think_about=[
                "Every variable used in the Trip Summary was created earlier in your code. Can you point at where each one was first assigned?",
                'If the player typed 99 and the else branch fired, what would the Trip Summary look like? Would it crash, or would it print something specific?',
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals',
        ),
    )

    # =========================================================================
    # SLIDE 13: CP4 Demo - Trip Summary print block
    # =========================================================================
    cp4_code = """    print()
    print('=' * 50)
    print('TRIP SUMMARY')
    print('=' * 50)
    print(f'Driver: {player_name}')
    print(f'Destination: {destination}')
    print(f'Distance: {distance} miles')
    print(f'Miles rolled: {miles_rolled}')
    print(f'Miles remaining: {miles_remaining}')
    print(f'Status: {status}')
    print('=' * 50)
    print()
"""

    deck.add_demo_slide(
        title='Demo: The Trip Summary Block',
        code=cp4_code,
        png='slide13_cp4.png',
        notes=format_demo_notes(
            code=cp4_code,
            instructor_notes=(
                "Twelve lines, all indented inside main. This is "
                "the very last thing the program does before "
                "ending. Walk top to bottom. Blank print, banner, "
                "TRIP SUMMARY title, banner. Then six f-strings, "
                "each pulling one variable. Driver, Destination, "
                "Distance, Miles rolled, Miles remaining, Status. "
                "Then a closing banner and a final blank for "
                "spacing. Every variable here exists because of "
                "work done in earlier checkpoints. Trace each one "
                "back as you walk through: player_name came from "
                "CP2 of Lab 1.1, destination/distance/status came "
                "from CP2 of this lab, miles_rolled came from "
                "Lab 1.1's roll math, miles_remaining came from "
                "CP3 of this lab. Notice that 'message' is NOT "
                "in the Trip Summary. It was printed back in CP3 "
                "as part of the made-it line. The summary is the "
                "structured recap; the message was the flavor "
                "line in the moment."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: CP4 Output - full final output
    # =========================================================================
    cp4_output = """\
Heading to Corpus Christi!
Distance: 150 miles

You made it to Corpus Christi!
The Sparkling City by the Sea!
Miles to spare: 0

==================================================
TRIP SUMMARY
==================================================
Driver: Maria
Destination: Corpus Christi
Distance: 150 miles
Miles rolled: 150
Miles remaining: 0
Status: BEACH
=================================================="""

    deck.add_output_slide(
        title='Output: Trip Summary (Maria, rolled 15, chose Corpus)',
        output_text=cp4_output,
        png='slide14_cp4_output.png',
        notes=format_output_notes(
            output_text=cp4_output,
            instructor_notes=(
                "Maria rolled 15 (150 miles) and picked Corpus "
                "(150 miles). miles_remaining is exactly zero. "
                "Because we used >= 0 in CP3, that counts as "
                "made it. Walk the output with the class. CP3's "
                "made-it block prints on top: Heading to Corpus "
                "Christi, Distance 150, blank, You made it, the "
                "message, Miles to spare zero. Then CP4's Trip "
                "Summary closes everything out. The Status field "
                "shows BEACH because that was set in CP2's first "
                "elif branch. If the player had picked an invalid "
                "choice, Status would show ERROR and Destination "
                "would show Nowhere. The summary tells the truth "
                "either way."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 15: Common Stumbles
    # =========================================================================
    deck.add_concept_slide(
        title='Common Stumbles',
        bullets=[
            "NameError on destination/distance/status/message -> a branch forgot to set that variable. Check every branch including else.",
            "Crash when typing 99 in the menu -> you forgot the else clause. else IS the safety net.",
            "miles_remaining sign feels off -> Lab 1.2 is rolled MINUS distance. Lab 1.1's direction was the opposite.",
            "Output shows 'miles short: -50' -> you forgot abs() in the else branch of CP3.",
            "Trip Summary shows the wrong status -> your if-elif-else order is off, or you used = instead of == in a condition.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Five stumbles to memorize. First, NameError on one "
                "of the four variables. Almost always means one "
                "branch of the if-elif-else didn't set that "
                "variable. The fix is to open the if-elif-else and "
                "make sure every branch has all four assignments. "
                "Second, the program crashes when the user types "
                "something other than 1, 2, 3. You forgot the else "
                "clause. The else is not optional. Always include "
                "it. Third, the math direction. Lab 1.1's "
                "miles_remaining was destination minus rolled. Lab "
                "1.2's is rolled minus destination. Copying Lab "
                "1.1's math literally will give you results with "
                "the wrong sign and the made-it check will fire "
                "backwards. Fourth, abs forgotten in CP3. The "
                "fall-short message ends up with a negative number "
                "like 'miles short: negative 50.' That's a sign "
                "you skipped the abs call. Add miles_short equals "
                "abs of miles_remaining inside the else branch. "
                "Fifth, the Trip Summary status looks wrong. Two "
                "common causes. Either the if-elif-else conditions "
                "are in the wrong order so a wrong branch fires, "
                "or you accidentally used single equals instead of "
                "double equals in a condition. Single equals is "
                "assignment. Double equals is a question. Use "
                "double equals in if statements, always."
            ),
            key_terms=[
                ('Boundary error', "A bug caused by getting the > vs >= or < vs <= wrong. Often subtle because the program works for most inputs."),
            ],
            think_about=[
                "Of these five stumbles, which one do you think a teammate would have the hardest time helping you debug? Why?",
                'When you see a NameError, the error message points at the line where the variable was USED, not where it was missed. Why?',
            ],
            source_url='https://docs.python.org/3/tutorial/errors.html',
        ),
    )

    # =========================================================================
    # SLIDE 16: Final Check, Submit, What's Next
    # =========================================================================
    deck.add_overview_slide(
        title='Final Check, Submit, What\'s Next',
        section1_label='BEFORE YOU SUBMIT',
        section1_body=(
            "Test all four paths. Pick 1 with a big roll. Pick 1 "
            "with a small roll. Pick 2. Pick 3. Pick 99 (or any "
            "invalid number) to confirm the else fires cleanly "
            "without crashing. For each run, compare your output "
            "to the expected output in the lab sheet, line by "
            "line. Delete any DEBUG lines. Confirm the filename "
            "is lab-1-2.py exactly."
        ),
        section2_body=(
            "Submit to CodeGrade. Unlimited submissions. If a "
            "test fails, read which test failed, look at the "
            "specific input it used, walk that input through your "
            "code on paper. Most failures point right at the "
            "checkpoint that owns the bug. Save your finished "
            "lab-1-2.py. Lab 1.3 starts with you copying this "
            "file."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "Lab 1.3 (MASTER) ties everything in Module 1 together. "
            "We add the Chapter 3 toolkit's last two pieces: NESTED "
            "if statements (an if inside an if) and the LOGICAL "
            "operators and / or / not. The Houston choice will "
            "branch again into a Galveston side trip. The Austin "
            "choice will use AND to check two conditions at once. "
            "Module 1 closes there. Then Module 2 introduces loops."
        ),
        notes=format_concept_notes(
            video_script=(
                "Before you submit, test all four paths. Pick "
                "one, two, three, and an invalid number. That's "
                "four runs minimum. Make sure the invalid run "
                "doesn't crash. Make sure each valid run shows "
                "the right destination, distance, status, and "
                "message. Compare your output line by line to the "
                "expected output in the lab sheet. Whitespace, "
                "punctuation, the exclamation point after BEACH, "
                "all of it matters. Then delete the DEBUG lines, "
                "confirm the filename, and submit. Submit early, "
                "submit often. Unlimited tries. There's no "
                "penalty. Save your finished lab-1-2.py file. "
                "Lab 1.3 next session is your MASTER lab for "
                "Module 1. We add nested if statements and the "
                "logical operators and, or, and not. The "
                "Houston choice gets to branch again into a "
                "Galveston side trip, which is why we drop "
                "Galveston in Lab 1.2 and add it back in Lab "
                "1.3. The Austin choice gets a two-condition "
                "check using and. That's the last of the "
                "Chapter 3 toolkit, and it closes Module 1. "
                "Module 2 introduces loops, which lets the "
                "player roll more than once per program. See "
                "you in L3."
            ),
            think_about=[
                "When you've finished Lab 1.2, what's one thing that would make the game more interesting that we HAVEN'T introduced yet?",
                "Looking back at all four checkpoints, which one applied the most U2 concepts? Which one applied the fewest?",
            ],
        ),
    )

    # =========================================================================
    # Save
    # =========================================================================
    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
