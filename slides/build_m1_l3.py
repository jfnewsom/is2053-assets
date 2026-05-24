"""
build_m1_l3.py - M1-L3 ("Lab 1.3: Hit the Road") slide deck.

Module 1, Lab 3 (MASTER) | Chapter 3 application + completion
Pairs with: Lab 1.3 assignment sheet (lab-1-3.json)

PIPELINE FRAMING (locked May 24, 2026)
--------------------------------------
M1-L3 is the MASTER deck for Module 1. It does double duty:
  1. Walks the four checkpoints of Lab 1.3
  2. Introduces the two Chapter 3 pieces that were deferred from M1-U2:
     - Section 3.3: Nested if statements
     - Section 3.5: The `or` logical operator
There is no separate M1-U3 in the pipeline; those new concepts get short
concept slides early in this deck, then get applied in CP2's nested logic.

SCOPE (verified against lab-1-3.py and lab-1-3.json)
- CP1: setup, HOU_TO_GALVESTON constant returns, tracking-var defaults
  (miles_remaining = miles_rolled; distance = 0)
- CP2: nested if in the Houston branch -- check made-it, prompt for Galveston,
  nested if with the `or` operator for y/Y
- CP3: Corpus, Austin, Invalid branches set distance and status consistently
- CP4: Trip Summary update + status-driven final message dispatch

NEW CONCEPTS THIS DECK INTRODUCES (deferred from M1-U2)
- Nested if (Gaddis Section 3.3)
- The `or` logical operator (Gaddis Section 3.5)
- The default-initialization pattern (set defaults before if-elif-else,
  overwrite in branches)
- String comparison with == (used for y/Y check)

OUT OF SCOPE
- Anything Chapter 4+ (loops, functions students define, lists, dicts)
- Format specs

USAGE
-----
    python3 slides/m1_l3/build_m1_l3.py

The deck is written to /home/claude/IS2053_2026-05-24_M1-L3_Deck.pptx.
PNGs land in /home/claude/m1_l3_pngs/.
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-24_M1-L3_Deck.pptx'
PNG_OUT = '/home/claude/m1_l3_pngs'
WORK_DIR = '/tmp/build_m1_l3'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Lab 1.3: Hit the Road',
        subtitle='IS2053 Programming I  \u2022  Module 1  \u2022  Lab Walkthrough (MASTER)',
        notes=format_title_notes(
            deck_id='M1-L3',
            deck_title='Lab 1.3: Hit the Road',
            opening_line=(
                '"Welcome to the MASTER lab. This one closes Module 1 and brings '
                'two new pieces of the Chapter 3 toolkit online: nested if statements, '
                "and the or logical operator. We'll introduce them up front, then "
                'walk Lab 1.3 checkpoint by checkpoint."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='MASTER: Close Out Module 1',
        section_label='THE STORY',
        bold_oneliner='Houston was a stop. Now it can be a decision.',
        body=(
            "In Lab 1.2, picking Houston meant you stopped in Houston. Done. "
            "In Lab 1.3, picking Houston means a SECOND choice opens up. The "
            "beach (Galveston) is fifty miles past Houston. Do you push for "
            "it? Or do you stay put? That second question is a decision "
            "INSIDE a decision: a nested if. We'll learn the pattern in the "
            "next two slides, then apply it in the lab. By the end, your "
            "program will have up to four levels of nesting in one branch, "
            "and a status variable that drives a custom ending message."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome back. This is M1-L3, the MASTER lab for Module 1. "
                "Two things happen in this deck. First, we introduce two "
                "new pieces of the Chapter 3 toolkit. Nested if statements, "
                "and the or logical operator. We held these off in U2 "
                "specifically so we could land them here, in context, as "
                "soon as the lab actually needs them. Second, we walk Lab "
                "1.3, the destination game with a Galveston side trip. "
                "The Houston choice now branches a second time. Did you "
                "make Houston? If yes, do you want to keep going to "
                "Galveston? That second question is a decision sitting "
                "inside the first decision. That's the new pattern. "
                "We'll see it formally in the next slide, then apply it "
                "in CP2. By the end of this video you'll have walked all "
                "four checkpoints, seen up to four levels of nested "
                "logic, and learned how to use a status variable to drive "
                "different endings to your program."
            ),
            think_about=[
                'When you imagine "a decision inside another decision" in real life, what example comes to mind? (Hint: any time the next question depends on the previous answer.)',
                "What's the difference between asking two SEPARATE questions and asking one question THEN another based on the answer to the first?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 3: NEW concept - Nested If
    # =========================================================================
    deck.add_concept_slide(
        title='New Concept: Nested If',
        bullets=[
            "A nested if is an if statement INSIDE the body of another if statement.",
            "The inner if only runs when the outer if's condition is True.",
            "Each level of nesting adds 4 more spaces of indentation. The shape steps to the right.",
            "Use nested if when the NEXT question depends on the PREVIOUS answer being yes.",
            "Lab 1.3's Houston branch nests up to FOUR levels deep: choice, made-Houston, y/Y, made-Galveston.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here's the new pattern. A nested if is an if statement "
                "inside another if statement. Outer if, condition, colon. "
                "Indent four spaces. Inside that body, another if "
                "statement. Condition, colon. Indent four MORE spaces. "
                "That inner if's body lives at eight spaces of indent. "
                "The inner if only runs when the outer if was True, "
                "because if the outer was False, Python skipped the "
                "entire body, including the inner if. Use this whenever "
                "the next question only makes sense given a previous "
                "answer. The real-world example. Did you reach Houston? "
                "If yes, do you want to keep going to Galveston? If "
                "you didn't reach Houston, the second question is "
                "irrelevant. There's no point asking it. The nested if "
                "encodes that conditional relationship. In Lab 1.3, "
                "the Houston branch goes up to four levels deep. "
                "Choice equals 2 is level one. Made Houston is level "
                "two. Said yes to Galveston is level three. Made "
                "Galveston is level four. Each level adds four spaces "
                "of indent. By the deepest level you're sixteen spaces "
                "in from the left margin. The indentation tells you "
                "exactly how many things had to be true for that line "
                "to run."
            ),
            key_terms=[
                ('Nested if', 'An if statement placed inside the body of another if statement.'),
                ('Level of nesting', 'How many ifs deep your current code is. Each level adds 4 spaces of indentation.'),
            ],
            think_about=[
                "If you have a nested if four levels deep, how many spaces of indentation does the innermost line have? Count it.",
                'Could you achieve the same logic with separate, non-nested if statements? Would the code be easier or harder to read?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 4: NEW concept - the `or` operator
    # =========================================================================
    deck.add_concept_slide(
        title='New Concept: The or Operator',
        bullets=[
            "`or` joins two conditions. If EITHER condition is True, the whole expression is True.",
            "Syntax: condition1 or condition2. Both sides are full comparisons, not just values.",
            "Example: continue_choice == 'y' or continue_choice == 'Y' accepts both lowercase and uppercase.",
            "Python checks left to right and short-circuits: if the left is True, the right is never evaluated.",
            "Sibling operator `and` needs BOTH sides True. Lab 1.3 uses `or` only; `and` is part of Module 3+.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Second new piece. The or operator. or joins two "
                "conditions into one. If EITHER one is true, the whole "
                "expression is true. The syntax is condition1, the "
                "keyword or, condition2. Both sides have to be full "
                "comparisons. You can't write continue_choice equals "
                "equals quote y quote or quote Y quote, even though "
                "that reads like English. Python doesn't carry the "
                "left side's variable into the right side. You have to "
                "spell it out: continue_choice equals equals quote y "
                "quote, or, continue_choice equals equals quote Y "
                "quote. Two complete comparisons, joined by or. That's "
                "exactly how Lab 1.3 handles the y/Y choice for "
                "continuing to Galveston. About short-circuiting. "
                "Python evaluates left to right. The moment it finds a "
                "true value, it stops and returns true. The right side "
                "never runs. This matters for performance in big "
                "programs and matters for correctness when the right "
                "side has a side effect. Worth knowing, not worth "
                "worrying about for Lab 1.3. About and. The sibling "
                "operator. and needs BOTH sides true. The lab only "
                "uses or, so we'll stay focused there. and shows up "
                "again in Module 3 when we start filtering data."
            ),
            key_terms=[
                ('or operator', 'A logical operator. Result is True if at least one of the two conditions is True.'),
                ('Short-circuit evaluation', 'Python stops evaluating an or expression as soon as it finds a True. The rest is skipped.'),
            ],
            think_about=[
                "Why do we have to write `c == 'y' or c == 'Y'` instead of `c == 'y' or 'Y'`? What does Python do with the second version?",
                "If `or` is True when either side is True, when is `or` False? Hint: count the cases.",
            ],
            source_url='https://docs.python.org/3/reference/expressions.html#boolean-operations',
        ),
    )

    # =========================================================================
    # SLIDE 5: CP1 Concept - Setup & Tracking Variables
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 1: Setup & Tracking Variables',
        bullets=[
            "Save Lab 1.2 as lab-1-3.py. Edit the copy, never the original.",
            "Add HOU_TO_GALVESTON = 50 back to your constants. (It was dropped in 1.2; it comes back here.)",
            "Initialize miles_remaining = miles_rolled BEFORE the if-elif-else block.",
            "Initialize distance = 0 BEFORE the if-elif-else block.",
            "The default-initialization pattern: set safe values up front, overwrite in branches. Bulletproof against missed branches.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 1 is the setup. Save Lab 1.2 as lab dash "
                "1 dash 3 dot py. Always work on the copy. Update the "
                "docstring with the new lab number and description. "
                "Then add HOU_TO_GALVESTON equals fifty back to your "
                "constants. Galveston was dropped in Lab 1.2 because "
                "we didn't need it. It comes back in 1.3 because the "
                "Houston branch is going to use it. Then the new "
                "pattern. BEFORE your if-elif-else block, you "
                "initialize two tracking variables. miles_remaining "
                "equals miles_rolled, which means by default the "
                "player hasn't traveled yet. distance equals zero, "
                "which means by default no destination has been "
                "chosen. Why do this BEFORE the if-elif-else? "
                "Because the Houston branch is going to update "
                "miles_remaining as the player makes nested "
                "decisions, and we need it to exist before any "
                "branch touches it. Same for distance. The pattern "
                "is: set safe defaults up front, then let each "
                "branch overwrite what it needs. If a branch forgets "
                "to set distance, the default zero still gets used "
                "downstream. The program doesn't crash. It just "
                "shows the default. That's a much friendlier failure "
                "mode than a NameError. We saw the NameError trap "
                "in Lab 1.2. This is how you defend against it "
                "structurally."
            ),
            key_terms=[
                ('Default-initialization pattern', "Set every variable to a safe default BEFORE any conditional logic runs. Branches overwrite what they need."),
                ('Tracking variable', 'A variable whose value changes over the course of the program to track running state. miles_remaining is a tracking variable in Lab 1.3.'),
            ],
            think_about=[
                "Why initialize miles_remaining = miles_rolled instead of miles_remaining = 0? What does the default represent?",
                'If you forgot to initialize distance before the if-elif-else, what would happen when the Houston "didn\'t make it" branch tried to use it?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html',
        ),
    )

    # =========================================================================
    # SLIDE 6: CP1 Demo - constants + default initialization
    # =========================================================================
    cp1_code = """# Constants - distances from San Antonio (in miles)
SAT_TO_CORPUS = 150
SAT_TO_HOUSTON = 200
SAT_TO_AUSTIN = 80

# Distance from Houston to Galveston
HOU_TO_GALVESTON = 50


def main():
    # ... banner, name, roll, miles_rolled, menu, choice ...

    # Initialize tracking variables BEFORE the if-elif-else
    miles_remaining = miles_rolled
    distance = 0
"""

    deck.add_demo_slide(
        title='Demo: New Constant + Default Initialization',
        code=cp1_code,
        png='slide06_cp1.png',
        notes=format_demo_notes(
            code=cp1_code,
            instructor_notes=(
                "Two changes from Lab 1.2 to highlight. First, "
                "HOU_TO_GALVESTON equals fifty is back in the "
                "constants. Same value as Lab 1.1. Second, the "
                "two new initialization lines right before the "
                "if-elif-else block. The placeholder comment "
                "shows where they go in the larger program. "
                "Walk through the logic. miles_remaining starts "
                "as miles_rolled, meaning before any travel the "
                "player still has all their miles. distance "
                "starts at zero because no destination has been "
                "chosen yet. Then the if-elif-else runs and "
                "each branch updates these. The Houston branch "
                "in CP2 will update miles_remaining multiple "
                "times as the player nests through choices. "
                "These initializations make all of that "
                "downstream code safe to write."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 7: CP2 Concept - Nested Houston Logic
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 2: Nested Houston Logic',
        bullets=[
            "Inside the choice == 2 branch, write a NESTED if to check whether the player reached Houston.",
            "If they made it: print the arrival, ask 'Continue to Galveston? (y/n)', then ANOTHER nested if on the answer.",
            "Use the `or` operator to accept both 'y' and 'Y': continue_choice == 'y' or continue_choice == 'Y'.",
            "Inside the y/Y branch, ANOTHER nested if checks whether the player made it to Galveston.",
            "Four Houston outcomes in total: WINNER (Galveston), SHORT (Galveston), STOPPED (n), SHORT (Houston).",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 2 is the heart of this lab and the "
                "biggest nested structure you've written. Inside "
                "the Houston branch, you stack four layers of "
                "decisions. Layer one is already there from Lab "
                "1.2: elif choice equals two. Layer two is new: "
                "an if that checks whether miles_remaining is "
                "enough to reach Houston. If yes, you're inside "
                "the made-Houston region. Layer three is the "
                "y/n prompt. You print the arrival, ask Continue "
                "to Galveston, and get the answer. Then an if "
                "with the or operator checks if the answer is "
                "y or Y. If yes, you're inside the trying-for-"
                "Galveston region. Layer four is the deepest "
                "nest: did they make Galveston with the miles "
                "they had left? Set status WINNER or SHORT. The "
                "lab tells you to test all four Houston "
                "outcomes. Roll five, choice two: didn't make "
                "Houston, status SHORT. Roll twenty, choice "
                "two, then n: made Houston, stayed, status "
                "STOPPED. Roll twenty, choice two, then y: "
                "made Houston, reached Galveston, status "
                "WINNER. Roll fifteen, choice two, then y: "
                "made Houston, short of Galveston, status "
                "SHORT. All four paths must produce sensible "
                "output."
            ),
            key_terms=[
                ('Decision tree', 'A branching structure where each node is a decision and each branch is an outcome. Nested ifs are decision trees in code.'),
            ],
            think_about=[
                "When you sketch out the four Houston outcomes as a tree, where does each branch end? Hint: there should be a clear status at every endpoint.",
                "Why does the or operator help here? What would the code look like if Python required strict case match (no `or`)?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html',
        ),
    )

    # =========================================================================
    # SLIDE 8: CP2 Demo A - Houston outer nested structure
    # =========================================================================
    cp2a_code = """    elif choice == 2:
        miles_remaining = miles_rolled - SAT_TO_HOUSTON
        if miles_remaining >= 0:                # Made it to Houston
            print('You made it to Houston! Space City!')
            print(f'Miles remaining: {miles_remaining}')
            continue_choice = input('Continue to Galveston? (y/n): ')
            if continue_choice == 'y' or continue_choice == 'Y':
                ...   # Galveston sub-block (see next slide)
            else:
                ...   # Stay in Houston: status = 'STOPPED'
        else:                                   # Didn't make Houston
            distance = SAT_TO_HOUSTON
            status = 'SHORT'
            message = 'Highway traffic got you!'
"""

    deck.add_demo_slide(
        title='Demo: Houston Outer Structure (Three Levels Deep)',
        code=cp2a_code,
        png='slide08_cp2a.png',
        notes=format_demo_notes(
            code=cp2a_code,
            instructor_notes=(
                "Walk top to bottom and count the indents as you "
                "go. elif choice equals two is the outer level "
                "(4 spaces). The miles_remaining update sits at "
                "that same level. Then the new nested if at 4 "
                "spaces deeper (8 total). That if checks whether "
                "miles_remaining is greater than or equal to "
                "zero, meaning the player reached Houston. "
                "Inside that if (12 spaces deep) we print the "
                "arrival, ask the y/n question, then nest "
                "AGAIN. The continue_choice equals quote y "
                "quote or continue_choice equals quote Y quote "
                "check is yet another if. Its body sits at 16 "
                "spaces. That's where the Galveston code goes, "
                "which we'll look at on the next slide. The "
                "else clause for that y/Y check is the STOPPED "
                "branch: player chose to stay in Houston. "
                "Finally, way back out at 8 spaces of indent, "
                "the else for the outer 'did they make "
                "Houston' check: SHORT. Three new ifs in this "
                "block, all nested. The deepest line of code "
                "sits at 16 spaces. Tell students the lab "
                "JSON walks them through this step by step. "
                "Don't try to type the whole thing at once. "
                "Build outside-in, one nested layer at a time."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 9: CP2 Demo B - Galveston sub-block (the `or` in action)
    # =========================================================================
    cp2b_code = """            if continue_choice == 'y' or continue_choice == 'Y':
                # Try for Galveston
                destination = 'Galveston'
                distance = SAT_TO_HOUSTON + HOU_TO_GALVESTON
                miles_remaining = miles_remaining - HOU_TO_GALVESTON

                if miles_remaining >= 0:
                    status = 'WINNER'
                    message = 'Sun, sand, and the Gulf of Mexico!'
                else:
                    status = 'SHORT'
                    message = 'So close to Galveston!'
            # else: Stay in Houston -- destination='Houston', status='STOPPED'
"""

    deck.add_demo_slide(
        title='Demo: The Galveston Sub-Block (or operator + deepest nest)',
        code=cp2b_code,
        png='slide09_cp2b.png',
        notes=format_demo_notes(
            code=cp2b_code,
            instructor_notes=(
                "This is the deepest part of the program. "
                "The if at the top uses the or operator. "
                "Read it out loud: 'if continue_choice "
                "equals quote y quote OR continue_choice "
                "equals quote Y quote.' Both comparisons "
                "are full expressions joined by the keyword "
                "or. If the player typed lowercase y, the "
                "left side is true and Python stops "
                "checking. If they typed uppercase Y, the "
                "left side is false, Python checks the "
                "right side, which is true. Either way the "
                "body fires. Inside that body, we set "
                "destination to Galveston, compute the "
                "total distance from San Antonio (Houston "
                "plus Galveston), and subtract "
                "HOU_TO_GALVESTON from miles_remaining to "
                "see what's left. Then ANOTHER nested if: "
                "did they actually make Galveston? If yes, "
                "WINNER. If no, SHORT. The deepest lines "
                "of code (status and message inside the "
                "made-Galveston check) sit at sixteen "
                "spaces from the left margin -- four "
                "levels deep. The else for this if (not "
                "shown for space) is the Stay-in-Houston "
                "branch. It sets destination to 'Houston', "
                "distance to SAT_TO_HOUSTON, status to "
                "'STOPPED', message to 'Check out the "
                "Space Center!' -- the same 4-variable "
                "pattern we used throughout Lab 1.2."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: CP2 Output - winner path through Galveston
    # =========================================================================
    cp2_output = """\
What did you roll? (1-20): 20

You rolled 20! That gives you 200 miles.

Where would you like to go?
  1. Corpus Christi - 150 miles (BEACH!)
  2. Houston - 200 miles
  3. Austin - 80 miles

Enter your choice (1-3): 2

You made it to Houston! Space City!
Miles remaining: 0

Continue to Galveston? (y/n): y"""

    deck.add_output_slide(
        title='Output: The Galveston Path (rolled 20, chose Houston, said y)',
        output_text=cp2_output,
        png='slide10_cp2_output.png',
        notes=format_output_notes(
            output_text=cp2_output,
            instructor_notes=(
                "Walk through the trace. Player rolls 20, "
                "which gives 200 miles. They pick Houston "
                "(choice 2). The outer Houston branch "
                "subtracts SAT_TO_HOUSTON (200) from "
                "miles_remaining, leaving zero. Zero is "
                "greater than or equal to zero, so the "
                "made-Houston branch fires. We print the "
                "arrival, show miles remaining, ask about "
                "Galveston. Player types y. The or check "
                "passes on the left side ('y' equals 'y'). "
                "The Galveston attempt runs: distance "
                "becomes 250, miles_remaining becomes "
                "negative 50 (zero minus fifty). Negative "
                "is NOT greater than or equal to zero, so "
                "the inner SHORT branch fires. The "
                "arrival output (not shown on this slide) "
                "will say 'You didn't make it to "
                "Galveston, you were 50 miles short.' "
                "Status is SHORT. Then the Trip Summary "
                "and the final message. Mention to "
                "students: the lab requires testing all "
                "FOUR Houston outcomes. This is one of "
                "them. Run the others and confirm each "
                "produces the expected status."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: CP3 Concept - Update Other Branches
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 3: Update Other Branches',
        bullets=[
            "Corpus and Austin branches need the same shape as Houston (minus the Galveston nesting).",
            "Each branch: set destination, set distance, compute miles_remaining, then nested if for made-it check.",
            "Every branch must set distance AND status. Without them, the Trip Summary breaks for that path.",
            "Add a DEBUG print at the end of the if-elif-else to verify distance and status for every choice.",
            "CP3 is mechanical: apply the same nested if-else shape to two more branches, plus the safety-net else.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 3 is mechanical. You take the "
                "pattern you used inside the Houston branch and "
                "apply it to Corpus and Austin. Same shape: "
                "set destination, set distance, compute "
                "miles_remaining for that destination, then "
                "nested if to check if they made it. If yes, "
                "status WINNER or DETOUR. If no, status "
                "SHORT. The else branch for invalid input is "
                "still there, still essential. It sets the "
                "error defaults so the rest of the program "
                "doesn't crash when someone types 99. The "
                "lab tells you to add a temporary DEBUG line "
                "at the end of the entire if-elif-else block. "
                "It prints distance and status. Run the "
                "program with several different choices and "
                "rolls and verify the DEBUG output matches "
                "what you expect. Choice 1, roll big: WINNER. "
                "Choice 1, roll small: SHORT. Choice 3, roll "
                "big: DETOUR. Choice 99: ERROR. If all four "
                "show correct values, your branches are "
                "consistent. Delete the DEBUG line before "
                "moving on. The discipline here is making "
                "sure every branch sets the same set of "
                "tracking variables. Same rule as Lab 1.2. "
                "Distance and status, no exceptions."
            ),
            think_about=[
                "Why doesn't Austin need the deeper nesting that Houston has? What makes the Houston branch the special case?",
                'The else branch sets distance to 0 and status to ERROR. What happens downstream that justifies those specific values?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html',
        ),
    )

    # =========================================================================
    # SLIDE 12: CP3 Demo - Corpus full + placeholders for Austin/else
    # =========================================================================
    cp3_code = """    if choice == 1:                              # Corpus: direct route
        destination = 'Corpus Christi'
        distance = SAT_TO_CORPUS
        miles_remaining = miles_rolled - SAT_TO_CORPUS
        if miles_remaining >= 0:
            status = 'WINNER'
            message = 'The Sparkling City by the Sea!'
        else:
            status = 'SHORT'
            message = 'So close to the beach!'
    # elif choice == 2: Houston -- see CP2 (nested logic)
    # elif choice == 3: Austin -- same nested if-else shape as Corpus
    else:                                        # Invalid: safety net
        status = 'ERROR'
        message = 'Invalid choice!'
"""

    deck.add_demo_slide(
        title='Demo: Corpus Branch Pattern (Austin Follows the Same Shape)',
        code=cp3_code,
        png='slide12_cp3.png',
        notes=format_demo_notes(
            code=cp3_code,
            instructor_notes=(
                "What's shown is the Corpus branch in full "
                "plus the Houston/Austin/else handled in "
                "comments and shortened form. The Corpus "
                "branch is the template. Set destination, "
                "set distance, compute miles_remaining for "
                "Corpus specifically, then a nested if to "
                "check if they made it. If miles_remaining "
                "is greater than or equal to zero, WINNER "
                "with the Sparkling City message. Else, "
                "SHORT with 'So close to the beach.' "
                "Austin follows the same shape with "
                "different destination, distance, "
                "messages. Austin's WINNER status is "
                "actually DETOUR because Austin isn't the "
                "beach goal. Austin's SHORT message "
                "blames I-35 traffic. The else branch at "
                "the bottom is the safety net for invalid "
                "input. It only needs to set status and "
                "message; destination and distance "
                "already have their defaults from CP1's "
                "initialization. That's why we set those "
                "defaults BEFORE the if-elif-else. The "
                "else branch can be short and clean."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13: CP3 Output - debug verification across branches
    # =========================================================================
    cp3_output = """\
Test 1 (choice 1, roll 15):
DEBUG: distance = 150, status = WINNER

Test 2 (choice 1, roll 5):
DEBUG: distance = 150, status = SHORT

Test 3 (choice 3, roll 20):
DEBUG: distance = 80, status = DETOUR

Test 4 (choice 99, any roll):
DEBUG: distance = 0, status = ERROR"""

    deck.add_output_slide(
        title='Output: Debug Verification of Every Branch',
        output_text=cp3_output,
        png='slide13_cp3_output.png',
        notes=format_output_notes(
            output_text=cp3_output,
            instructor_notes=(
                "Four runs, four different combinations, "
                "four different status values. Test 1 hits "
                "the Corpus WINNER branch (rolled enough). "
                "Test 2 hits the Corpus SHORT branch "
                "(didn't roll enough). Test 3 hits the "
                "Austin DETOUR branch (made it but Austin "
                "isn't the goal). Test 4 hits the else "
                "branch for invalid input. Notice the "
                "ERROR test shows distance equals zero. "
                "That zero came from CP1's default "
                "initialization, never overwritten by any "
                "branch because the else for invalid only "
                "sets status and message. That's the "
                "default-initialization pattern paying "
                "off. Reminder: DEBUG lines are "
                "TEMPORARY. Delete every DEBUG print "
                "before submitting."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: CP4 Concept - Trip Summary & Final Message
    # =========================================================================
    deck.add_concept_slide(
        title='Checkpoint 4: Trip Summary & Final Message',
        bullets=[
            "The Trip Summary is mostly carried over from Lab 1.2. Same fields, same f-strings.",
            "NEW: a final message dispatched on the status variable using if-elif-else.",
            "Five status values, five different closing messages: WINNER, SHORT, DETOUR, STOPPED, ERROR.",
            "This is the SAME if-elif-else shape from U2, just using status instead of choice as the discriminator.",
            "A status variable + dispatch is a common real-world pattern. You'll see it again in M3 with functions.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Checkpoint 4 has two pieces. The Trip "
                "Summary block is mostly carried over from "
                "Lab 1.2. Same banners, same six labeled "
                "lines: Driver, Destination, Distance, Miles "
                "Rolled, Miles Remaining, Status. Don't "
                "reinvent it. The new piece is the final "
                "message. After the Trip Summary closes, you "
                "add ONE more if-elif-else block. This one "
                "checks the status variable and prints a "
                "different closing line for each possible "
                "status. WINNER gets congratulations. SHORT "
                "gets better luck next time. DETOUR gets a "
                "suggestion to try Corpus or Houston. "
                "STOPPED gets a 'the beach will be waiting' "
                "message. else (ERROR) gets a generic "
                "'Thanks for playing.' Notice the shape. "
                "This is an if-elif-else chain dispatching "
                "on a status variable instead of a menu "
                "choice. Same structure you learned in U2. "
                "Different discriminator. That dispatch "
                "pattern, where you use a variable's value "
                "to choose what to print or what to do, "
                "shows up everywhere in real code. Game "
                "state, HTTP response codes, order "
                "fulfillment statuses. You're going to see "
                "this pattern again."
            ),
            key_terms=[
                ('Status-based dispatch', 'Using a status variable to drive an if-elif-else that chooses different behavior or output.'),
            ],
            think_about=[
                "If you have five possible statuses but only handle four explicitly with elif, what does the else catch?",
                "Why is using a status variable cleaner than re-checking the same conditions (miles_remaining, choice, etc.) all over again at the end?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 15: CP4 Demo - status-based final message dispatch
    # =========================================================================
    cp4_code = """    # ... Trip Summary banner block prints first ...

    # Final message dispatched on status
    if status == 'WINNER':
        print('CONGRATULATIONS! You made it to the beach!')
    elif status == 'SHORT':
        print('Better luck next time! Roll higher!')
    elif status == 'DETOUR':
        print('Try Corpus Christi or Houston next time!')
    elif status == 'STOPPED':
        print('The beach will be waiting for your next adventure!')
    else:
        print('Thanks for playing!')
"""

    deck.add_demo_slide(
        title='Demo: Status-Based Final Message Dispatch',
        code=cp4_code,
        png='slide15_cp4.png',
        notes=format_demo_notes(
            code=cp4_code,
            instructor_notes=(
                "Eleven lines, all indented inside main, "
                "right after the Trip Summary banner "
                "block. Walk top to bottom. if status "
                "equals equals quote WINNER quote (notice "
                "string comparison with double equals "
                "just like number comparison): print "
                "CONGRATULATIONS. elif SHORT: better luck. "
                "elif DETOUR: try Corpus or Houston. elif "
                "STOPPED: the beach will be waiting. else: "
                "Thanks for playing. The else catches any "
                "status value we didn't explicitly check, "
                "including ERROR (invalid choice). "
                "Important pedagogical moment: this is "
                "the SAME if-elif-else shape from U2, "
                "just discriminating on a string variable "
                "instead of an integer choice. The "
                "underlying mechanic is identical. "
                "Python checks each condition in order, "
                "runs the first body whose condition is "
                "true, skips the rest. Order doesn't "
                "matter as much here because the status "
                "values are mutually exclusive: only one "
                "status can be set per run."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 16: CP4 Output - full happy path output
    # =========================================================================
    cp4_output = """\
You made it to Corpus Christi!
The Sparkling City by the Sea!
YOU REACHED THE BEACH!
Miles to spare: 0

==================================================
TRIP SUMMARY
==================================================
Driver: Maria
Destination: Corpus Christi
Distance: 150 miles
Miles Rolled: 150
Miles Remaining: 0
Status: WINNER
==================================================

CONGRATULATIONS! You made it to the beach!"""

    deck.add_output_slide(
        title='Output: Happy Path (Maria, rolled 15, chose Corpus)',
        output_text=cp4_output,
        png='slide16_cp4_output.png',
        notes=format_output_notes(
            output_text=cp4_output,
            instructor_notes=(
                "Maria rolls 15 (150 miles) and picks "
                "Corpus (150 miles). Exact arrival. "
                "miles_remaining equals zero, which "
                "passes the >= 0 check, so status is "
                "WINNER. The arrival output prints "
                "the made-it message, the sparkling "
                "city flavor line, the YOU REACHED THE "
                "BEACH banner line, and miles to spare. "
                "Then the Trip Summary block. Then the "
                "final message dispatched on status: "
                "since status is WINNER, the "
                "CONGRATULATIONS line prints. Walk "
                "through it with the class. Mention "
                "that other status values would change "
                "BOTH the arrival output AND the final "
                "message. The lab's expected outputs "
                "cover all five status paths. Compare "
                "your output line by line to the "
                "expected output. Whitespace and "
                "punctuation matter."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 17: Common Stumbles
    # =========================================================================
    deck.add_concept_slide(
        title='Common Stumbles',
        bullets=[
            "Indentation drift in nested ifs -> each level adds EXACTLY 4 spaces. Count carefully, or VS Code will count for you.",
            "`or` written as 'c == y or Y' -> doesn't work. Each side needs a full comparison: 'c == 'y' or c == 'Y''.",
            "Missing the y/Y check -> only accepts lowercase y. Uppercase Y falls through and the player ends up in the STOPPED branch.",
            "Forgot to initialize distance or miles_remaining -> NameError in the invalid-choice path where CP1's defaults should have kicked in.",
            "Status set in only some branches -> Trip Summary or final message uses the wrong value (or crashes). Every branch must set status.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Five new stumbles to add to your "
                "mental list. First, indentation drift "
                "in nested ifs. Each level is four "
                "spaces. By the time you're four levels "
                "deep in the Houston-Galveston path, "
                "you're at sixteen spaces of indent. "
                "Counting that by hand is hard. Let VS "
                "Code do it. Tab when you start a new "
                "level, the editor handles the spaces. "
                "Second, the or operator syntax. Don't "
                "write c equals equals y or Y. Python "
                "doesn't carry the comparison across. "
                "Write c equals equals quote y quote "
                "or c equals equals quote Y quote. Two "
                "full comparisons joined by or. Third, "
                "missing the case check. If you only "
                "test for lowercase y, uppercase Y "
                "falls through and the player gets the "
                "STOPPED branch when they wanted "
                "Galveston. Use the or with both "
                "cases. Fourth, NameError on distance "
                "or miles_remaining. This means you "
                "forgot to initialize them before the "
                "if-elif-else, or you have a typo. CP1 "
                "sets the defaults specifically to "
                "prevent this. Fifth, status not set "
                "in every branch. The final message "
                "dispatch in CP4 will either use a "
                "stale value or crash. Make sure every "
                "single nested branch sets status to "
                "one of WINNER, SHORT, DETOUR, STOPPED, "
                "or ERROR before it exits."
            ),
            think_about=[
                "Which of these five do you think is the easiest mistake to make without noticing? Why?",
                'If a NameError happens in your final message dispatch, but the variable was supposed to be set in CP2, what does that tell you about which Houston branch fired?',
            ],
            source_url='https://docs.python.org/3/tutorial/errors.html',
        ),
    )

    # =========================================================================
    # SLIDE 18: Final Check, Submit, Module 1 Close
    # =========================================================================
    deck.add_overview_slide(
        title='Final Check, Submit, Module 1 Close',
        section1_label='BEFORE YOU SUBMIT',
        section1_body=(
            "Test every status outcome. WINNER: roll big, "
            "choice 1. SHORT: roll small, any choice. "
            "DETOUR: roll big, choice 3. STOPPED: roll "
            "big, choice 2, type n. ERROR: choice 99. "
            "That's five different runs. Each one should "
            "produce a coherent Trip Summary AND a "
            "status-appropriate final message. Compare "
            "your output line by line to the expected "
            "output in the lab sheet. Delete all DEBUG "
            "lines. Confirm filename is lab-1-3.py."
        ),
        section2_body=(
            "Submit to CodeGrade. Unlimited submissions. "
            "If a test fails, the test name will tell "
            "you which scenario broke. Walk that "
            "scenario through your code on paper. Save "
            "lab-1-3.py. Lab 1.3 is the foundation for "
            "Module 2 -- you'll copy it again at the "
            "start of Lab 2.1."
        ),
        section3_label='MODULE 1 IS DONE',
        section3_body=(
            "Three labs, three weeks. You started with a "
            "calculator. You ended with a game that "
            "branches up to four levels deep, dispatches "
            "on status, and produces a different "
            "experience for every player. Chapter 2 and "
            "Chapter 3 are complete. Next: Module 2 "
            "introduces LOOPS, which finally lets your "
            "program do the SAME thing more than once "
            "per run. The Texas road trip becomes a "
            "multi-day journey."
        ),
        notes=format_concept_notes(
            video_script=(
                "Before you submit, test every status. "
                "Five status values means five different "
                "runs minimum. WINNER, SHORT, DETOUR, "
                "STOPPED, ERROR. Each one should produce "
                "a sensible Trip Summary and a "
                "status-matched closing line. The lab "
                "sheet has expected outputs for each. "
                "Compare line by line. Delete every "
                "DEBUG print. Confirm the filename. "
                "Then submit. Unlimited submissions. "
                "If a test fails, look at which test "
                "failed and walk that specific scenario "
                "through your code. Save your finished "
                "lab-1-3.py. You'll copy it again at the "
                "start of Lab 2.1 next week. That's "
                "Module 1. Three labs. Calculator to "
                "game. Variables to nested decisions. "
                "Every program you've written so far "
                "runs through its code exactly once. "
                "That ends in Module 2. Loops let your "
                "program do the same thing many times "
                "per run. The road trip becomes a "
                "multi-day journey. The dice get "
                "rolled multiple times. Inventory "
                "accumulates. See you in M2-U1."
            ),
            think_about=[
                "Three weeks ago you couldn't write a program that took input. Now you can write a program with four levels of nested decisions and five outcome paths. What's changed in how you THINK about a problem?",
                "Looking at all of Module 1, which concept clicked fastest? Which one is still fuzzy? That answer is what to review before M2 starts.",
            ],
        ),
    )

    # =========================================================================
    # Save
    # =========================================================================
    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
