"""
build_m2_l1.py - M2-L1 ("Lab 2.1: Keep On Driving") walkthrough deck.

Module 2, Lab 1 | Lab 2.1 BUILD | walks all 6 checkpoints.

Source-of-truth chain (do not invert):
  1. Modules/mod2/lab-2-1.py     - bedrock solution code
  2. pages/labs/json/lab-2-1.json - student-facing assignment sheet
  3. This deck (downstream)

Pedagogy notes:
  - L decks WALK the lab; they call back to U-deck concepts verbally.
    Slide 8 (CP4 concept) says "remember from U1, every while loop
    needs a way to make the condition False" rather than re-teaching.
  - The lab pedagogy includes DEBUG + break safety nets at CP4 and CP5;
    demos reflect that so students see what the JSON tells them to type.
  - Common Stumbles slide is sourced from the lab's finalCheck.
    ifSomethingBreaks list, not invented.

USAGE
-----
    python3 slides/m2_l1/build_m2_l1.py
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-25_M2-L1_Deck.pptx'
PNG_OUT = '/home/claude/m2_l1_pngs'
WORK_DIR = '/tmp/build_m2_l1'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 2.1: Keep On Driving',
        subtitle='IS2053 Programming I  \u2022  Module 2  \u2022  Lab Walkthrough',
        notes=format_title_notes(
            deck_id='M2-L1',
            deck_title='Lab 2.1: Keep On Driving',
            opening_line=(
                '"Welcome to your Lab 2.1 walkthrough. You just finished M2-U1, '
                "where we covered the while loop and the accumulator pattern. "
                "This hour we put both of those to work in Lab 2.1 across six "
                'checkpoints. By the end you will know exactly what to type."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='From One Roll to a Real Road Trip',
        section_label='THE STORY',
        bold_oneliner='Lab 1.3 was one roll of the dice. Lab 2.1 is the journey.',
        body=(
            "Open your Lab 1.3 file. That code did exactly one thing: rolled a die, decided whether you "
            "made it to your destination, and ended. One shot. That is not how a road trip works. A road "
            "trip is many turns of driving until you actually arrive. Lab 2.1 takes your Lab 1.3 code "
            "as the starting point, trims it down to the bones, and wraps the travel in a while loop. "
            "Each turn the player travels a fixed 50 miles. The loop keeps going until miles_remaining "
            "drops to zero or below, at which point the trip summary prints. Six checkpoints get you "
            "from your Lab 1.3 code to the finished Lab 2.1. CP1 trims, CP2 adds a safety branch, CP3 "
            "sets up tracking variables, CP4 lays down the loop, CP5 fills in the loop body, CP6 prints "
            "the summary. Two new constants enter the game this week: MILES_PER_TURN (50) and the "
            "accumulator total_miles. Let us walk it."
        ),
        notes=format_concept_notes(
            video_script=(
                "Take a beat and look at your Lab 1.3 code. Notice that it runs top to bottom and ends. "
                "Player picks a destination, rolls once, and the program prints either you made it or you "
                "did not. That model is what we are throwing out this week. The new model is: many turns. "
                "Each turn you cover 50 miles. The loop keeps running until you have driven the full "
                "distance. The constant MILES_PER_TURN equals 50 is the entire game mechanic. We will use "
                "while-greater-than-zero as the loop condition and subtract MILES_PER_TURN from "
                "miles_remaining each turn. That is the U1 toolkit applied. Plus the accumulator pattern: "
                "total_miles starts at zero before the loop, gets added to inside the loop, gets displayed "
                "in the trip summary after. Six checkpoints. The first two are setup, the middle two are "
                "the loop, the last two are the loop body and the summary. We are going to walk every "
                "single one. Open your editor, open your Lab 1.3, and start with File Save As to make a "
                "copy called lab-2-1.py. That is checkpoint 1."
            ),
            think_about=[
                "Before we start CP1: how many turns would each destination take? Corpus Christi is 150 miles, MILES_PER_TURN is 50, so... how many turns? What about Houston (200 miles)? Austin (80 miles)?",
                "Why do we delete code from Lab 1.3 instead of just adding the loop on top of it? What problem does the deletion prevent?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#while-statements',
        ),
    )

    # =========================================================================
    # SLIDE 3: CP1 Concept - Cleanup
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 1: Cleanup',
        bullets=[
            "File - Save As lab-1-3.py -> lab-2-1.py. Update the docstring (lab title, description, Chapter 4).",
            "DELETE the dice roll block: the 'roll = int(input(...))' line and the miles_rolled calculation.",
            "DELETE the HOU_TO_GALVESTON constant and ALL Galveston / win-or-short / status logic.",
            "TRIM the three if/elif branches to just destination + distance (no other lines inside them).",
            "ADD the new constant MILES_PER_TURN = 50 below your three distance constants.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 1 is mechanical work. You are not writing new logic, you are stripping the old "
                "code down to a foundation we can build the loop on top of. Step one, copy the file. "
                "File menu, Save As, change lab-1-3 to lab-2-1. Then update the docstring at the top: new "
                "lab title, new description, change the Chapter 3 Concepts section to Chapter 4 (while "
                "loop, loop counter, accumulator pattern). Step two, find the dice roll block from Lab 1.3 "
                "and delete it. That is the print lines that asked you to roll, the roll equals int input "
                "line, the miles_rolled equals roll times ten calculation. Gone. We do not need them. "
                "Step three, delete the HOU_TO_GALVESTON constant at the top. Then find the nested "
                "Galveston logic inside the elif choice equals two branch and delete that whole nested "
                "block. While you are in the if-elif chain, trim each branch down to just two lines: "
                "destination equals the string and distance equals the constant. Everything else inside "
                "each branch was Lab 1.3 logic we are throwing out. Step four, the most important addition "
                "of the entire CP: add MILES_PER_TURN equals 50 underneath your three distance constants. "
                "Save the file and run it. It should not crash. The lab assignment sheet has the full "
                "deletion checklist with every specific line called out. Use that as your guide and check "
                "things off as you delete them."
            ),
            key_terms=[
                ('MILES_PER_TURN', 'The new constant introduced in Lab 2.1, equal to 50. Used to update miles_remaining inside the loop body in CP5.'),
                ('Trim', 'Removing lines without changing behavior of the remaining code. Cleanup is a series of trims to the Lab 1.3 file.'),
            ],
            think_about=[
                "Why does it make sense to trim before adding? What would go wrong if you added the while loop on top of the dice roll code without removing the dice roll first?",
                "If you accidentally delete one too many lines (like a constant), how does Python tell you? What's the error message you'd see?",
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html',
        ),
    )

    # =========================================================================
    # SLIDE 4: CP2 Concept - Setup & Simplify
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 2: Setup & Simplify',
        bullets=[
            "Run your CP1 file. Try choice 1, 2, 3 - each should set a different destination.",
            "Now try choice 4. The program may crash with NameError because no branch matched.",
            "Add an else: branch after the elif choice == 3 block.",
            "Inside the else: set destination = 'Corpus Christi' and distance = SAT_TO_CORPUS.",
            "Print a warning: 'Invalid choice. Defaulting to Corpus Christi.' so the user knows.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 2 patches a hole. After CP1, your if-elif chain handles choices 1, 2, and 3, "
                "but if a user types 4 or 5 or anything else, NO branch matches. Python skips the whole "
                "block, and then the next line tries to use the variable destination, which was never "
                "assigned, and the program crashes with NameError. The fix is the else clause at the end "
                "of the chain. Else covers every case the elifs did not catch. Inside the else, set "
                "destination and distance to the Corpus Christi values. Print a warning line so the user "
                "knows what happened. Why Corpus Christi as the default? Because the beach is the goal of "
                "the game, and defaulting to the beach is friendly behavior. Plus it gives us a "
                "predictable test case if a user fat-fingers their choice. Save the file, run it, and "
                "deliberately type 4 to verify the warning appears and the program continues without "
                "crashing. Then test 1, 2, 3 one more time to make sure you did not break anything. "
                "Recall from U1: an if-elif chain without an else has a hole. Every if-elif chain you "
                "write from here on should ask itself, what if none of these branches match?"
            ),
            key_terms=[
                ('else clause', 'The catch-all branch at the end of an if-elif chain. Runs when no earlier condition was True.'),
                ('NameError', 'Python error you get when you try to use a variable that has not been assigned. Adding an else clause prevents this when bad input slips through.'),
            ],
            think_about=[
                "What other 'sane defaults' could you set for the else clause besides Corpus Christi? What makes Corpus Christi a better choice than, say, Austin?",
                "Should the warning message say which choice was invalid (like 'You entered 4')? What are the tradeoffs?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 5: CP2 Demo - the default branch added
    # =========================================================================
    cp2_code = '''# Set destination and distance based on choice.
if choice == 1:
    destination = 'Corpus Christi'
    distance = SAT_TO_CORPUS
elif choice == 2:
    destination = 'Houston'
    distance = SAT_TO_HOUSTON
elif choice == 3:
    destination = 'Austin'
    distance = SAT_TO_AUSTIN
else:
    destination = 'Corpus Christi'
    distance = SAT_TO_CORPUS
    print('Invalid choice. Defaulting to Corpus Christi.')
'''
    deck.add_demo_slide(
        title='Demo: The Default Branch',
        code=cp2_code,
        png='slide05_cp2.png',
        notes=format_demo_notes(
            code=cp2_code,
            instructor_notes=(
                "Read this top to bottom with the class. The first three branches were already there from "
                "CP1; CP2 adds only the else block at the bottom. Three lines in the else: assign "
                "destination, assign distance, print the warning. Notice the warning print is INSIDE the "
                "else, not outside. If you put it outside, every choice would trigger the warning. "
                "Indentation matters here as always. Connect this to U2 of Module 1 if students need it: "
                "the if-elif-else chain is exactly the same structure they used in Lab 1.2 and 1.3, just "
                "with a more focused purpose this time around (two lines per branch, no nested logic)."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 6: CP3 Concept - Initialize Tracking Variables
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 3: Initialize Tracking Variables',
        bullets=[
            "Three new variables get created RIGHT BEFORE the while loop (which we add in CP4).",
            "miles_remaining = distance - starts equal to the full trip distance from the chosen branch.",
            "total_miles = 0 - this is the accumulator. It starts at zero and grows as the loop runs.",
            "turn = 1 - this is the turn counter. Used in the per-turn display and the trip summary.",
            "Initialize BEFORE the loop. Initialize INSIDE the loop and you reset every iteration - bug city.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 3 is small but critical. Three lines. Three variables. They go in your code "
                "right after the if-elif-else block finishes, BEFORE the while loop you will add in CP4. "
                "First, miles_remaining equals distance. Distance is the variable that the if-elif-else "
                "chain set to the destination distance. miles_remaining starts at that full value and the "
                "loop will whittle it down. Second, total_miles equals zero. That is your accumulator. "
                "Remember from U1: the accumulator pattern is three steps. Initialize before the loop, "
                "update inside the loop, use after the loop. This is step one of the pattern. Third, turn "
                "equals one. That is your turn counter. The very first time we display Turn 1, then we "
                "bump it to 2 for the next iteration, and so on. Why all three BEFORE the loop and not "
                "inside? Because if you put them inside the loop, they reset on every iteration. "
                "miles_remaining would reset to distance every turn and you would never make progress. "
                "total_miles would always be 0 because you keep zeroing it. turn would always print as 1. "
                "Initialize before. Update inside. Use after. The U1 rhythm."
            ),
            key_terms=[
                ('miles_remaining', 'The variable controlling the while loop condition. Starts at distance, decreases each turn.'),
                ('total_miles', 'The accumulator. Starts at 0. Each turn it grows by MILES_PER_TURN.'),
            ],
            think_about=[
                "What would happen if you set total_miles = distance instead of total_miles = 0? Trace through one turn and predict.",
                "Why does turn start at 1 instead of 0? When else in life do we start counting at 1 instead of 0?",
            ],
            source_url='https://docs.python.org/3/reference/simple_stmts.html#assignment-statements',
        ),
    )

    # =========================================================================
    # SLIDE 7: CP3 Demo - the init block
    # =========================================================================
    cp3_code = '''# After the if-elif-else, BEFORE the while loop:

# Initialize tracking variables.
miles_remaining = distance
total_miles = 0
turn = 1
'''
    deck.add_demo_slide(
        title='Demo: The Tracking Variables',
        code=cp3_code,
        png='slide07_cp3.png',
        notes=format_demo_notes(
            code=cp3_code,
            instructor_notes=(
                "Three lines. The placement matters: after the if-elif-else chain has finished setting "
                "distance, and BEFORE the while loop we add in CP4. Show students by pointing at the "
                "blank space between the if-elif-else and where the loop will go. miles_remaining starts "
                "at distance, which was set in the chosen branch. total_miles starts at zero, ready to "
                "accumulate. turn starts at one because Turn 1 is the first iteration we display. The "
                "lab assignment sheet shows a DEBUG block you can temporarily add to verify the three "
                "values are right before moving on. Strongly recommend students use it for a sanity check "
                "and then delete the DEBUG lines before CP4."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: CP4 Concept - Build the while Loop
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 4: Build the while Loop',
        bullets=[
            "Add a journey banner BEFORE the loop ('LET THE JOURNEY BEGIN!') so the trip has a clear start.",
            "Write the while line: while miles_remaining > 0: - the colon is not optional.",
            "Don't write the real body yet. The body comes in CP5.",
            "Use a TEMPORARY DEBUG print + break so you can test the loop without infinite-looping.",
            "Run it. Confirm 'Loop entered!' appears once, then the program exits. Delete DEBUG + break for CP5.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 4 lays down the loop frame. Two pieces. First, a journey banner BEFORE the "
                "while line, so the output has a visual break between setup and travel. Print fifty equal "
                "signs, then LET THE JOURNEY BEGIN, then fifty more equal signs, then a blank print. "
                "Second, the while line itself. While miles_remaining greater than zero colon. The colon "
                "is part of Python syntax. Forget it and you get a SyntaxError. Now here is the careful "
                "part. Do NOT write the real loop body yet. If you write the real body, you are doing "
                "CP5's work inside CP4. Worse, if you write a PARTIAL body that prints but does not "
                "update miles_remaining, you have an infinite loop. The lab tells you to add a TEMPORARY "
                "DEBUG block so you can verify the loop entered correctly. Print a line that says Loop "
                "entered, condition was True. Print the value of miles_remaining. Then break. The break "
                "statement forces the loop to exit after one iteration. With that safety net, you can "
                "run the program and confirm two things: the loop body executes, and the program does "
                "not run forever. CP5 you remove the DEBUG and the break and write the real body. From "
                "U1: every while loop needs a way to make the condition False. CP4's body does not have "
                "one yet. The break is your training wheels."
            ),
            key_terms=[
                ('break', 'A statement that immediately exits the loop, even if the condition is still True. Use it as a safety net while building.'),
                ('Loop frame', 'The structure of the loop without its real body: the while line, the journey banner, and (temporarily) safe placeholder code inside.'),
            ],
            think_about=[
                "Why does CP4 use break instead of just leaving the loop body empty? What would happen if you wrote a while loop with nothing inside it?",
                "Recall from U1: name the line in the temperature.py demo that eventually made the condition False. Which line in YOUR loop will do the same job in CP5?",
            ],
            source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
        ),
    )

    # =========================================================================
    # SLIDE 9: CP4 Demo - while with DEBUG + break
    # =========================================================================
    cp4_code = '''# CP4: Journey banner + loop frame (TEMPORARY DEBUG body).
print('=' * 50)
print('LET THE JOURNEY BEGIN!')
print('=' * 50)
print()

while miles_remaining > 0:
    # DEBUG - DELETE BEFORE CHECKPOINT 5
    print('DEBUG: Loop entered! Condition was True.')
    print(f'DEBUG: miles_remaining={miles_remaining}')
    break  # TEMPORARY - stops loop after 1 iteration
'''
    deck.add_demo_slide(
        title='Demo: CP4 Loop Frame',
        code=cp4_code,
        png='slide09_cp4.png',
        notes=format_demo_notes(
            code=cp4_code,
            instructor_notes=(
                "Two distinct parts to walk through. Top part: the journey banner. Four print lines that "
                "create a visual divider between setup and the trip. Mirrors the welcome banner pattern "
                "from M1-U1 (string multiplication, equal signs, blank lines for breathing room). Bottom "
                "part: the while line plus a SAFE placeholder body. The DEBUG prints confirm the loop "
                "entered, and break stops the loop after one iteration so the program actually exits. "
                "Note the comments call out that DEBUG and break are TEMPORARY: they must be deleted in "
                "CP5 when you add the real body. The lab assignment sheet has the exact DEBUG lines to "
                "use; this matches the lab JSON's CP4 code block verbatim."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: CP4 Output - DEBUG output (1 iteration)
    # =========================================================================
    cp4_output = '''==================================================
LET THE JOURNEY BEGIN!
==================================================

DEBUG: Loop entered! Condition was True.
DEBUG: miles_remaining=150
'''
    deck.add_output_slide(
        title='Output: CP4 DEBUG Check',
        output_text=cp4_output,
        png='slide10_cp4_output.png',
        notes=format_output_notes(
            output_text=cp4_output,
            instructor_notes=(
                "Six lines of output (counting the banner). Walk through them: banner with equal signs, "
                "title line, banner again, blank line, DEBUG entered confirmation, DEBUG miles_remaining "
                "value. The 150 in the last line is for the Corpus Christi run; for Houston it would be "
                "200, for Austin 80. If the DEBUG miles_remaining shows the WRONG number (or shows zero, "
                "or causes an error), the bug is upstream in CP3. The init line miles_remaining equals "
                "distance is what controls this value. CP4 working correctly means the loop entered "
                "exactly once and printed the correct starting miles. Now we delete DEBUG and break, and "
                "fill in the real body in CP5."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: CP5 Concept - Complete the Loop Body
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 5: Complete the Loop Body',
        bullets=[
            "Display the turn header ('--- Turn 1 ---', then Turn 2, Turn 3...).",
            "Display miles remaining BEFORE travel, then a travel message ('You travel 50 miles...').",
            "Update miles_remaining: SUBTRACT MILES_PER_TURN (this is what eventually exits the loop).",
            "Update total_miles: ADD MILES_PER_TURN (the accumulator pattern from U1).",
            "Increment turn: turn = turn + 1 (so the next iteration displays Turn 2, then Turn 3...).",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 5 is the meat of the lab. The empty placeholder body from CP4 becomes a real "
                "body with six distinct actions. Action one: print the turn header. Three dashes, the "
                "word Turn, the turn variable, three more dashes. f-string territory. Action two: print "
                "the current miles_remaining so the player sees where they are. Action three: print a "
                "travel message saying they covered MILES_PER_TURN miles. Action four, the critical one: "
                "miles_remaining equals miles_remaining minus MILES_PER_TURN. This is what makes the loop "
                "eventually exit. Action five, the accumulator: total_miles equals total_miles plus "
                "MILES_PER_TURN. This is the running total that the trip summary will display. Action "
                "six: turn equals turn plus one. This bumps the turn counter for the next iteration. "
                "Between CP4 and CP5 you MUST delete the DEBUG prints and the break statement. The "
                "subtract line is now what exits the loop, not break. The lab assignment sheet also "
                "shows an optional DEBUG END OF TURN print you can put at the very end of the body for "
                "verification, then delete before CP6. Recall from U1: this is the canonical "
                "initialize-before, update-inside, use-after rhythm. CP3 was initialize. CP5 is update. "
                "CP6 is use."
            ),
            key_terms=[
                ('Loop body', 'The block of code indented under the while line. Runs once per iteration.'),
                ('Increment', "Adding one to a variable. turn = turn + 1 is the classic 'add one' increment pattern."),
            ],
            think_about=[
                "What's the difference between 'miles_remaining = miles_remaining - MILES_PER_TURN' and 'miles_remaining - MILES_PER_TURN' by itself? Which one updates the variable?",
                "If you only wrote the subtract line and forgot the accumulator line, what would the trip summary show for Total Miles? Predict before you test.",
            ],
            source_url='https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements',
        ),
    )

    # =========================================================================
    # SLIDE 12: CP5 Demo - full loop body
    # =========================================================================
    cp5_code = '''while miles_remaining > 0:
    print(f'--- Turn {turn} ---')
    print(f'Miles remaining: {miles_remaining}')
    print(f'You travel {MILES_PER_TURN} miles...')

    # Update tracking variables (accumulator pattern!)
    miles_remaining = miles_remaining - MILES_PER_TURN
    total_miles = total_miles + MILES_PER_TURN

    if miles_remaining > 0:
        print(f'Miles remaining: {miles_remaining}')

    print()
    turn = turn + 1
'''
    deck.add_demo_slide(
        title='Demo: The Complete Loop Body',
        code=cp5_code,
        png='slide12_cp5.png',
        notes=format_demo_notes(
            code=cp5_code,
            instructor_notes=(
                "This is the complete CP5 body, matched to lab-2-1.py. Three display lines at top: turn "
                "header, current miles_remaining, travel message. Then a blank line for readability. "
                "Then the two update lines (subtract and accumulate). Then a small check: if "
                "miles_remaining is still greater than zero AFTER the subtract, display the new amount. "
                "This last bit is a polish touch from the solution code that prevents showing 'Miles "
                "remaining: 0' or '-50' on the final turn, since the arrival message comes from CP6 "
                "instead. Then a blank print for spacing, then the turn increment. DEBUG print is "
                "deliberately not shown here since CP5 ends with it deleted. If asked, point out the "
                "inner if statement is a nicety from the solution, not strictly required - lab autograder "
                "compares to the exact expected output, so this if statement is needed for the test to "
                "pass."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13: CP5 Output - Three turns of Corpus run
    # =========================================================================
    cp5_output = '''--- Turn 1 ---
Miles remaining: 150
You travel 50 miles...
Miles remaining: 100

--- Turn 2 ---
Miles remaining: 100
You travel 50 miles...
Miles remaining: 50

--- Turn 3 ---
Miles remaining: 50
You travel 50 miles...
'''
    deck.add_output_slide(
        title='Output: Three Turns (Corpus Christi)',
        output_text=cp5_output,
        png='slide13_cp5_output.png',
        notes=format_output_notes(
            output_text=cp5_output,
            instructor_notes=(
                "Corpus Christi is 150 miles, MILES_PER_TURN is 50, so the trip takes exactly three "
                "turns. Walk the trace with the class. Turn 1: condition checks 150 > 0, True. Body "
                "runs, prints header, prints 150, prints travel message. Updates: 150 - 50 = 100, "
                "0 + 50 = 50. Check if 100 > 0, yes, print new miles_remaining. Bump turn. Turn 2: "
                "100 > 0, True. Similar. Updates leave miles_remaining at 50, total_miles at 100. "
                "Turn 3: 50 > 0, True. Updates leave miles_remaining at 0, total_miles at 150. "
                "Inner if: 0 > 0 is False, so no extra 'Miles remaining' line at the bottom of turn 3 "
                "- the loop just exits and CP6's arrival message takes over. Notice three turns of the "
                "ramp: 150 -> 100 -> 50 -> 0. Predictable because MILES_PER_TURN is fixed. Lab 2.2 "
                "replaces that with a D20 roll and chaos ensues."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: CP6 Concept - Arrival & Trip Summary
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 6: Arrival & Trip Summary',
        bullets=[
            "After the while loop ends, print an arrival message: 'You made it to {destination}!'",
            "Print the TRIP SUMMARY banner (equal signs, header, equal signs).",
            "Display Driver, Destination, Distance, Total Turns, Total Miles - this uses the accumulator!",
            "Total Turns is turn - 1 because turn was incremented one extra time inside the loop.",
            "Print an outcome message that differs by destination (Corpus = beach, Houston = 'almost', Austin = 'no beach').",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 6 is the payoff. The loop has ended. Now we tell the player what happened. "
                "First, print an arrival message: You made it to and then the destination variable. One "
                "line. Then the trip summary block: a banner of fifty equal signs, the words TRIP "
                "SUMMARY, another banner, then five data lines, then a final banner. The data lines pull "
                "from variables you have been tracking: player_name, destination, distance (which is now "
                "the FULL trip distance, not what's remaining), total turns, and total miles. Note the "
                "subtlety: total turns is displayed as turn minus one. Why minus one? Because at the end "
                "of CP5's loop body, turn got incremented one final time even though that final "
                "iteration was the last. So if the trip took three turns, the variable turn ended at "
                "four. We display turn minus one to show three. Last piece: an outcome message that "
                "differs by destination. Corpus is the beach, congratulations. Houston is close but "
                "Galveston is fifty miles away. Austin is nice but no beach. Three branches in a small "
                "if-elif-else. This is the use phase of the accumulator pattern. total_miles has been "
                "growing all loop long; this is where it actually gets displayed."
            ),
            key_terms=[
                ('Arrival message', 'A single print line after the loop ends, before the summary banner.'),
                ('Outcome message', "A small if-elif-else after the trip summary, with one branch per destination."),
            ],
            think_about=[
                "Why is the total turn count `turn - 1` and not just `turn`? Trace what value turn holds at the moment the loop exits.",
                "What other useful stats could you add to the trip summary block? What variables do you already have available?",
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting',
        ),
    )

    # =========================================================================
    # SLIDE 15: CP6 Demo - trip summary block
    # =========================================================================
    cp6_code = '''# AFTER the while loop ends:

print(f'You made it to {destination}!')
print()
print('=' * 50)
print('TRIP SUMMARY')
print('=' * 50)
print(f'Driver: {player_name}')
print(f'Destination: {destination}')
print(f'Distance: {distance} miles')
print(f'Total Turns: {turn - 1}')
print(f'Total Miles: {total_miles}')
print('=' * 50)
'''
    deck.add_demo_slide(
        title='Demo: Trip Summary Block',
        code=cp6_code,
        png='slide15_cp6.png',
        notes=format_demo_notes(
            code=cp6_code,
            instructor_notes=(
                "Walk this in three sections. Top: the arrival message. One print, f-string with "
                "destination. The blank print after creates visual space before the summary. Middle: "
                "the summary banner. Three lines that form the equal-sign sandwich around the words "
                "TRIP SUMMARY. Same pattern as the welcome banner in CP1, just different label. Bottom: "
                "five data lines plus a closing banner. Each f-string pulls in a variable. Special "
                "callout on Total Turns: it's turn - 1, not just turn. The increment in CP5 ran one more "
                "time after the last useful iteration, so turn is one higher than the real count. The "
                "outcome message (Corpus / Houston / Austin if-elif-else) follows this block and is "
                "shown in lab-2-1.py - we covered it verbally on the previous concept slide; not "
                "repeating it on this demo to keep the slide focused."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 16: CP6 Output - Post-loop portion
    # =========================================================================
    cp6_output = '''You made it to Corpus Christi!

==================================================
TRIP SUMMARY
==================================================
Driver: Maria
Destination: Corpus Christi
Distance: 150 miles
Total Turns: 3
Total Miles: 150
==================================================

CONGRATULATIONS! You reached the beach!

Thanks for playing!
'''
    deck.add_output_slide(
        title='Output: Trip Summary',
        output_text=cp6_output,
        png='slide16_cp6_output.png',
        notes=format_output_notes(
            output_text=cp6_output,
            instructor_notes=(
                "Final stretch of the Corpus Christi run. Arrival message at top. Summary block. "
                "Outcome message at bottom (CONGRATULATIONS for the beach branch). Then Thanks for "
                "playing. The values are exactly what the trace from slide 13 predicted: Total Turns "
                "is 3 (since turn ended at 4 and we display turn - 1). Total Miles is 150 (the "
                "accumulator added 50 three times). For Houston you'd see Total Turns 4, Total Miles "
                "200, and a different outcome message about Galveston. Worth running both at home to "
                "confirm the math holds. The full end-to-end output (banner, name input, menu, choice, "
                "loop, summary) is in the lab assignment sheet's Final Check block; this slide just "
                "isolates the post-loop tail."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 17: Common Stumbles (sourced from lab JSON finalCheck.ifSomethingBreaks)
    # =========================================================================
    deck.add_concept_slide(
        title='Common Stumbles',
        bullets=[
            "Program runs forever -> CP4. Your loop body is missing the line 'miles_remaining = miles_remaining - MILES_PER_TURN'.",
            "Total Miles shows 0 or 50 -> CP3. You initialized total_miles INSIDE the loop instead of before it.",
            "Crash on choice 4 with NameError -> CP2. You forgot the else branch. Every if-elif chain needs one.",
            "NameError on miles_rolled or status -> CP1. You missed a reference to a Lab 1.3 variable when trimming.",
            "Total Turns is one too high (5 for Houston instead of 4) -> CP5. Use turn - 1 in the summary, not turn.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Five things that go wrong most often. Memorize this list, or at least keep it open in a "
                "tab. Number one, your program runs forever. Sometimes called an infinite loop. It means "
                "your loop condition never became False. The fix is in CP4. Your loop body is missing "
                "the line that subtracts from miles_remaining. Find it, add it, and the loop will exit. "
                "Number two, your Total Miles in the summary shows zero or fifty. That is the "
                "accumulator pattern broken. The fix is in CP3. You initialized total_miles inside the "
                "loop body, which resets it to zero every iteration. Move that line to BEFORE the while "
                "line. Number three, you choose 4 from the menu and the program crashes with NameError "
                "on destination. The fix is in CP2. You did not add the else clause. Every if-elif "
                "chain needs an else. Number four, you get NameError on miles_rolled or status when you "
                "run the program. The fix is in CP1. You missed a reference to a Lab 1.3 variable when "
                "trimming. Search your file for the broken name and delete the line that uses it. "
                "Number five, Total Turns shows one too many: 4 for Corpus when it should be 3, 5 for "
                "Houston when it should be 4. The fix is in CP5 or CP6. Use turn minus one in the trip "
                "summary, not turn. The increment ran one extra time inside the loop. These five cover "
                "almost every ticket I see. Source: the lab assignment sheet's Final Check section has "
                "the full redirect map."
            ),
            key_terms=[
                ('Redirect map', "The 'if something breaks' list at the bottom of the lab sheet. Symptom -> which CP to revisit."),
                ('Off-by-one error', "When a counter is exactly one higher or lower than expected. Total Turns is a classic example."),
            ],
            think_about=[
                "Which of these five do you think is most likely to bite YOU on this lab? Why? Plan ahead.",
                "What's the first thing you'd type to investigate an infinite loop? Hint: it's not Ctrl-C, it's something you write into the loop body.",
            ],
            source_url='https://docs.python.org/3/tutorial/errors.html',
        ),
    )

    # =========================================================================
    # SLIDE 18: Final Check & Submit / What's Next
    # =========================================================================
    deck.add_overview_slide(
        title='Final Check, Submit, What\'s Next',
        section1_label='BEFORE YOU SUBMIT',
        section1_body=(
            "Run the program three times - one for each destination (Corpus Christi, Houston, Austin). "
            "Verify the loop runs the right number of turns each time (3, 4, 2). Verify Total Miles "
            "equals the destination distance in each run. Try choice 4 once to confirm the else clause "
            "fires and defaults gracefully to Corpus. Delete any leftover DEBUG lines. Confirm the "
            "filename is lab-2-1.py exactly. Confirm the docstring has Name, abc123, Section, and "
            "Description."
        ),
        section2_body=(
            "Submit to CodeGrade. Unlimited submissions: if a test fails, read the failure message, "
            "use the redirect map to find the right CP, fix the issue, resubmit. Do not aim for a "
            "first-attempt perfect; iterate quickly. CodeGrade scores your final submission, not the "
            "count of attempts."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "Lab 2.1 is the foundation for Lab 2.2. Module 2 Unit 2 (M2-U2) introduces functions, the "
            "random module, and the function_library.py pattern. Then Lab 2.2 replaces the fixed "
            "MILES_PER_TURN with a D20 roll, adds the Destination Gate (coin flip decides if Texas "
            "lets you go where you want), and introduces hazards. The while loop you wrote today stays. "
            "What's INSIDE the loop body gets way more interesting."
        ),
        notes=format_concept_notes(
            video_script=(
                "Before you submit, do the dry runs. Three destinations, each one a complete run. Watch "
                "the turn counts: Corpus should be 3, Houston should be 4, Austin should be 2. Watch "
                "the Total Miles: it should equal the destination's distance in every case. Then test "
                "the else branch by typing 4 or 0 or 99 - any invalid number. Verify the warning prints "
                "and the program continues. Once those four runs look right, delete every DEBUG line "
                "from your file. Double check the filename, double check the docstring, then submit. "
                "Unlimited tries on CodeGrade. If a test fails, the failure message will tell you what "
                "the autograder saw that did not match. Open the redirect map in the lab sheet, find "
                "your symptom, go fix the indicated CP, resubmit. Iteration is the point. Lab 2.2 next "
                "week. We are going to cover Chapter 5 in M2-U2 - functions, the random module, and "
                "building your own function library. Then 2.2 applies all of that to the road trip "
                "game. D20 dice replace your fixed fifty miles. A coin flip decides whether Texas "
                "cooperates with your destination choice. Hazards roll in at thirty percent per turn. "
                "Everything you wrote today stays; the body of the loop just gets more interesting. "
                "See you in U2."
            ),
            think_about=[
                "When you finished Lab 2.1, what felt easy and what felt foreign? That answer tells you what to revisit before M2-U2.",
                "If you had to add ONE feature to Lab 2.1 to make it more fun, what would it be? Save the idea; we might be adding it in 2.2 or 2.3.",
            ],
        ),
    )

    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
