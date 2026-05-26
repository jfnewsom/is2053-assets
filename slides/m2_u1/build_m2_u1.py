"""
build_m2_u1.py - M2-U1 ("Programs That Repeat") slide deck.

Module 2, Unit 1 | Chapter 4: while loops and the accumulator pattern
Pairs with: Lab 2.1, Keep On Driving

Scope (from lab-2-1.json keyConceptsText):
  Chapter 4 Sections: 4.2 (The while Loop), 4.4 (Calculating a Running Total)

Pedagogy notes:
  - while is the lab's tool; teach it as the primary loop concept.
  - Accumulator is taught as a pattern (loop-agnostic); BookEx 4-17
    demonstrates it with a for loop, which is fine - the pattern is
    the point, not the loop type.
  - Sentinel loops (4.5) and input validation (4.6) are deferred to
    Lab 2.3 / M2-L3.

USAGE
-----
    python3 slides/m2_u1/build_m2_u1.py
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-25_M2-U1_Deck.pptx'
PNG_OUT = '/home/claude/m2_u1_pngs'
WORK_DIR = '/tmp/build_m2_u1'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Programs That Repeat',
        subtitle='IS2053 Programming I  \u2022  Module 2  \u2022  Unit 1',
        notes=format_title_notes(
            deck_id='M2-U1',
            deck_title='Programs That Repeat',
            opening_line=(
                '"Welcome back. This is Module 2, Unit 1. Module 1 gave you '
                "everything you need to write a program that runs once. This week, "
                "we teach the program to do something over and over without you "
                'copying and pasting code. That tool is called a loop. Let\'s go."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='Programs That Repeat',
        section_label='THE BIG IDEA',
        bold_oneliner='Every program you have written so far runs once. This week, you teach it to do something over and over.',
        body=(
            "Up to now, every line of your code has run exactly once, top to bottom, then stopped. "
            "That is fine for a program that asks one question and prints one answer. But the real world "
            "asks the same question many times. A road trip is not one turn, it is many turns until you "
            "arrive. A grocery total is not one item, it is many items added up. Chapter 4 introduces the "
            "while loop, which lets a chunk of code run again and again as long as some condition is True, "
            "and the accumulator pattern, which lets you carry a running total across all those repetitions. "
            "Two ideas. That is the whole chapter slice for this lab. By the end of this unit, you will be "
            "ready to write Lab 2.1, where you keep on driving turn after turn until you reach your destination."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome back. Take a second and think about Lab 1.3. You picked a destination, the dice "
                "rolled, you either made it or you did not, and the program ended. One shot. That works fine "
                "for a single roll, but a road trip is not one roll. A road trip is many turns, you keep "
                "driving, you check how far you have left, you keep going until you arrive. That is what "
                "Chapter 4 is about. It hands you the tool that makes a program repeat. The tool is called "
                "a loop, and the specific kind we are starting with is called a while loop. Right after that, "
                "we are going to teach you the accumulator pattern. That is just a fancy name for a variable "
                "that keeps track of a running total while the loop runs. Two ideas this week. That is the "
                "whole chapter slice for Lab 2.1. By the end of this video, you will be ready to take your "
                "Lab 1.3 code, simplify it down to three destinations, and wrap the travel in a loop that "
                "keeps you on the road until you arrive."
            ),
            think_about=[
                "Think of three things in your daily life that happen 'over and over until some condition is met.' How would you describe the stopping condition for each one?",
                "If you had to add up a grocery list of 50 items without a loop, how would your code look? What would happen if the list grew to 500 items?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#while-statements',
        ),
    )

    # =========================================================================
    # SLIDE 3: Concept - Why Programs Need to Repeat
    # =========================================================================
    deck.add_concept_slide(
        title='Why Programs Need to Repeat',
        bullets=[
            "Without loops, you would have to copy and paste the same code for every repetition.",
            "Loops let one chunk of code do its work many times, without you typing it twice.",
            "Two ways a loop can know when to stop: count to a number, or watch for a condition.",
            "When you do not know how many repetitions you will need, you use a while loop.",
            "Examples: drive until you arrive, ask until they answer correctly, read until the file ends.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here is the why before the how. Without loops, every time a program needed to do something "
                "again, you would have to physically write that code again. Want to add up five numbers? "
                "Write the add line five times. Want to add up five hundred numbers? You see the problem. "
                "Loops solve this. You write the work once, and the loop runs it as many times as you need. "
                "There are two flavors of loops you will meet this semester. The first is when you know in "
                "advance how many times to repeat, like 'do this five times.' That is what a for loop is "
                "best at. The second is when you do not know in advance, you just know when to stop. Like "
                "'drive until you get there,' or 'keep asking until they give a valid answer,' or 'read the "
                "file until it ends.' That is what a while loop is best at. Lab 2.1 is going to use a while "
                "loop, because when you start the trip you do not know how many turns it will take. You just "
                "know you want to keep driving until your miles remaining hits zero. So that is the loop we "
                "are going to focus on first."
            ),
            key_terms=[
                ('Loop', 'A control structure that makes a block of code run more than once.'),
                ('Iteration', 'One pass through the body of a loop. A loop that runs five times has five iterations.'),
            ],
            think_about=[
                "If you had to teach a friend the difference between 'repeat this five times' and 'repeat this until I tell you to stop,' how would you explain it without using code?",
                "Why might Python give you two different kinds of loops instead of just one that does everything?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html',
        ),
    )

    # =========================================================================
    # SLIDE 4: Concept - The while Loop
    # =========================================================================
    deck.add_concept_slide(
        title='The while Loop',
        bullets=[
            "Shape: while CONDITION: then an indented block of code that repeats.",
            "Before each pass, Python checks the condition. True means run the body, False means stop.",
            "The body must eventually make the condition False, or the loop runs forever.",
            "Use while when the stopping point is a condition, not a count.",
            "Reads in English as: 'while this is still true, keep doing the indented stuff.'",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here is the anatomy of the while loop. You write the keyword while, then a condition, then "
                "a colon, then an indented block of code underneath. That indented block is called the body "
                "of the loop. Python's behavior is simple. Before every single pass through the loop, Python "
                "checks the condition. If the condition is True, Python runs the body once. Then it goes "
                "back up and checks the condition again. If True again, run the body again. If at any point "
                "the condition is False, Python skips the body and moves on to whatever code is after the "
                "loop. That is the entire mechanic. The critical thing, and I am going to put a whole slide "
                "on this in a moment, is that something inside the body has to eventually make the condition "
                "False. Otherwise the loop runs forever. Notice this is the same indentation pattern you "
                "already know from if statements. Anything you indent under the while line is what gets "
                "repeated. Anything at the same level as while runs once after the loop ends. Read the loop "
                "out loud in plain English. While my temperature is too high, keep adjusting the thermostat. "
                "While I still have miles to go, keep driving. While the user has not given me a valid "
                "answer, keep asking. The English reading and the Python reading line up exactly."
            ),
            key_terms=[
                ('Condition', 'A Boolean expression that evaluates to either True or False, like miles_remaining > 0.'),
                ('Body', 'The indented block of code under the while line. This is what repeats.'),
            ],
            think_about=[
                "If the condition is False the very first time Python checks it, how many times does the body run?",
                "Why is the loop body indented? What would happen if you forgot to indent one of the lines inside it?",
            ],
            source_url='https://docs.python.org/3/reference/compound_stmts.html#the-while-statement',
        ),
    )

    # =========================================================================
    # SLIDE 5: Demo - temperature.py (BookEx 4-2)
    # =========================================================================
    temperature_code = '''# Check a substance's temperature, prompt to adjust
# until it is at or below MAX_TEMP.
MAX_TEMP = 102.5

temperature = float(input("Enter the Celsius temperature: "))

while temperature > MAX_TEMP:
    print('The temperature is too high.')
    print('Turn the thermostat down and wait 5 minutes.')
    print('Then take the temperature again and enter it.')
    temperature = float(input("Enter the Celsius temperature: "))

print('The temperature is acceptable.')
'''
    deck.add_demo_slide(
        title='Demo: temperature.py',
        code=temperature_code,
        png='slide05_temperature_demo.png',
        notes=format_demo_notes(
            code=temperature_code,
            instructor_notes=(
                "Source: BookEx Chapter 4, program 4-2 (temperature.py). Comments are trimmed for screen "
                "space; the logic is unchanged from the textbook. Walk through it line by line. First, set "
                "the constant MAX_TEMP. Then get an initial reading from the user. Now point at the while "
                "line and read it out loud: while temperature is greater than MAX_TEMP, do the indented "
                "stuff. Emphasize the indented stuff includes asking for a new reading at the bottom. THAT "
                "is what eventually makes the condition False. If the new reading is at or below 102.5, the "
                "next time Python checks the condition it is False, the loop exits, and we print the "
                "acceptable message. Show the running of this in a moment so they see the loop in action."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 6: Output - temperature.py
    # =========================================================================
    temperature_output = '''Enter the Celsius temperature: 104.5
The temperature is too high.
Turn the thermostat down and wait 5 minutes.
Then take the temperature again and enter it.
Enter the Celsius temperature: 103.0
The temperature is too high.
Turn the thermostat down and wait 5 minutes.
Then take the temperature again and enter it.
Enter the Celsius temperature: 101.8
The temperature is acceptable.
'''
    deck.add_output_slide(
        title='Output: temperature.py',
        output_text=temperature_output,
        png='slide06_temperature_output.png',
        notes=format_output_notes(
            output_text=temperature_output,
            instructor_notes=(
                "Notice the pattern in the output. The block of three messages appears twice, because the "
                "user entered two readings that were still too high. The third reading (101.8) was at or "
                "below MAX_TEMP, so Python checked the condition, got False, and skipped the body entirely. "
                "Then it ran the line after the loop. Point out: the user controls when the loop ends, "
                "because each iteration the program asks for a new reading. If they kept entering values "
                "above 102.5 forever, the loop would keep going forever. The exit is in the user's hands. "
                "Connect this to Lab 2.1 verbally: in the lab, the user does not control the exit, the "
                "MILES_PER_TURN constant does, by ticking miles_remaining down 50 each turn."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 7: Concept - The Infinite Loop Trap
    # =========================================================================
    deck.add_concept_slide(
        title='The Infinite Loop Trap',
        bullets=[
            "Every while loop needs SOMETHING inside the body that can flip the condition to False.",
            "Forget that, and Python happily runs the loop forever. Your terminal will spin.",
            "Stop a runaway loop with Ctrl + C (Windows / Linux) or Cmd + . (Mac).",
            "When in doubt, add print('DEBUG: condition =', condition) above the body to watch it.",
            "Test with small numbers first. A loop that never ends with MAX=5 is easier than with MAX=5000.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Now we have to talk about the most common bug in your life this week. The infinite loop. "
                "It happens when you write a while loop and forget to put anything in the body that changes "
                "the condition. Python is not going to save you. Python is going to check the condition, "
                "see True, run the body, check again, see True, run the body, forever. Your terminal will "
                "print or do whatever the body does, over and over, until you intervene. Two things to "
                "remember. One, the way you intervene is Ctrl + C on Windows or Linux, Cmd + period on a "
                "Mac. Memorize that key combo. You will use it this week. Two, the way to AVOID infinite "
                "loops is to ask yourself every time you write a while: what inside this body is going to "
                "eventually make the condition False? If you cannot point at a specific line that updates "
                "the thing being checked, you have a problem. In the temperature program, the update is "
                "the line that asks for a new reading. In Lab 2.1, the update is the line that subtracts "
                "MILES_PER_TURN from miles_remaining. Find the update line. Every loop has to have one."
            ),
            key_terms=[
                ('Infinite loop', 'A loop whose condition never becomes False, so it runs without stopping.'),
                ('Loop-control variable', 'The variable being checked in the condition. Something in the body must change it.'),
            ],
            think_about=[
                "If you write `while True:` with no break inside, what does that program do?",
                "If your loop seems to be running forever, what is the FIRST thing you would print to figure out why?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements',
        ),
    )

    # =========================================================================
    # SLIDE 8: Concept - The Accumulator Pattern
    # =========================================================================
    deck.add_concept_slide(
        title='The Accumulator Pattern',
        bullets=[
            "An accumulator is a variable whose job is to keep a running total across loop iterations.",
            "Step 1: Initialize it BEFORE the loop (usually to 0 for numbers, '' for strings, [] for lists).",
            "Step 2: Inside the loop, add to it: total = total + something.",
            "Step 3: AFTER the loop ends, use the final value.",
            "Works with any loop type. The textbook shows it with for; the lab will use it with while.",
        ],
        notes=format_concept_notes(
            video_script=(
                "The accumulator pattern is so common it has a name. An accumulator is just a variable that "
                "you use to keep a running total inside a loop. Three steps. Step one, before the loop, you "
                "create the variable and set it to zero. This is critical. If you forget to initialize it, "
                "Python does not know what total is when the loop body first tries to update it, and you "
                "get a NameError. Step two, inside the body of the loop, you add to it. Total equals total "
                "plus the new value. That line is doing two things at once. It is taking the old value of "
                "total, adding something to it, and storing the new value back in total. Step three, after "
                "the loop is done, you use that final accumulated value. Print it, save it, whatever you "
                "need. Now here is the thing about the pattern. It does not care what kind of loop you wrap "
                "around it. Whether it is a for loop or a while loop, the pattern is the same. Initialize "
                "before, update inside, use after. The textbook is going to show you the pattern with a "
                "for loop, because that is the easier loop to demo. Then we are going to flip it and show "
                "you the same pattern with a while loop, because that is what Lab 2.1 is going to use."
            ),
            key_terms=[
                ('Accumulator', 'A variable that collects a running total as a loop runs.'),
                ('Initialize', 'To give a variable its starting value before any other code touches it.'),
            ],
            think_about=[
                "What happens if you initialize total = 0 INSIDE the loop body instead of before it?",
                "If you wanted to keep a running COUNT instead of a running total, how would the pattern change?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#for-statements',
        ),
    )

    # =========================================================================
    # SLIDE 9: Demo - sum_numbers.py (BookEx 4-17)
    # =========================================================================
    sum_numbers_code = '''# Calculate the sum of MAX numbers entered by the user.
MAX = 5

# Initialize the accumulator BEFORE the loop.
total = 0.0

print(f'This program sums {MAX} numbers.')

# Add each number to the running total.
for counter in range(MAX):
    number = int(input('Enter a number: '))
    total = total + number

# Display the final accumulated total.
print(f'The total is {total}.')
'''
    deck.add_demo_slide(
        title='Demo: sum_numbers.py',
        code=sum_numbers_code,
        png='slide09_sum_numbers_demo.png',
        notes=format_demo_notes(
            code=sum_numbers_code,
            instructor_notes=(
                "Source: BookEx Chapter 4, program 4-17 (sum_numbers.py). Comments are slightly trimmed for "
                "screen space; the logic is the textbook's. This is the canonical accumulator demo. Three "
                "things to highlight as you walk it. ONE: total = 0.0 sits BEFORE the loop. That is the "
                "initialization. Without that line you get a NameError when the loop body tries to update "
                "total. TWO: total = total + number is the update. Read it right to left in your head. "
                "Take old total, add number, store back in total. THREE: the final print is AFTER the loop, "
                "outside the indentation, so it runs once at the end. This deck pairs a for loop with the "
                "accumulator on purpose. The pattern is loop-agnostic. The very next slide shows you the "
                "same pattern with a while loop, set up for the Lab 2.1 travel use case."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: Output - sum_numbers.py
    # =========================================================================
    sum_numbers_output = '''This program sums 5 numbers.
Enter a number: 10
Enter a number: 20
Enter a number: 30
Enter a number: 40
Enter a number: 50
The total is 150.0.
'''
    deck.add_output_slide(
        title='Output: sum_numbers.py',
        output_text=sum_numbers_output,
        png='slide10_sum_numbers_output.png',
        notes=format_output_notes(
            output_text=sum_numbers_output,
            instructor_notes=(
                "Five prompts, one total. Trace what total holds after each iteration: 10, then 30, then 60, "
                "then 100, then 150. The total grows as the loop runs. Then the loop ends and the print "
                "line runs once with the final value. If you want to bring this to life, mentally run it "
                "with all the same number (say 5 fives = 25.0) or with mixed numbers including a negative "
                "(like 10, -5, 10, -5, 10 = 20.0). The pattern handles whatever you throw at it."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: Demo - Accumulator with while (Lab 2.1 preview)
    # =========================================================================
    while_accum_code = '''# Travel turn by turn until we arrive.
# (This is the pattern Lab 2.1 will use.)
MILES_PER_TURN = 50
miles_remaining = 150
total_miles = 0

while miles_remaining > 0:
    print(f'Miles remaining: {miles_remaining}')
    miles_remaining = miles_remaining - MILES_PER_TURN
    total_miles = total_miles + MILES_PER_TURN

print(f'Arrived! Total miles traveled: {total_miles}')
'''
    deck.add_demo_slide(
        title='Demo: The Same Pattern with while',
        code=while_accum_code,
        png='slide11_while_accum_demo.png',
        notes=format_demo_notes(
            code=while_accum_code,
            instructor_notes=(
                "This demo is not from BookEx. It is the pattern you just saw, ported to a while loop, with "
                "the Lab 2.1 variables in place: MILES_PER_TURN, miles_remaining, total_miles. Walk through "
                "it side by side with the previous demo. Initialize BEFORE the loop: miles_remaining = 150 "
                "and total_miles = 0. INSIDE the loop body, two updates happen. The travel update: "
                "miles_remaining = miles_remaining - MILES_PER_TURN (this is what eventually makes the "
                "condition False and ends the loop). The accumulator update: total_miles = total_miles + "
                "MILES_PER_TURN. AFTER the loop, print the final total. Two variables, two roles. One is "
                "tracking how much is left. One is tracking how much you have done. Both follow the "
                "initialize-update-use rhythm. This is almost line-for-line what Lab 2.1 wants from you."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 12: Output - Accumulator with while
    # =========================================================================
    while_accum_output = '''Miles remaining: 150
Miles remaining: 100
Miles remaining: 50
Arrived! Total miles traveled: 150
'''
    deck.add_output_slide(
        title='Output: The Same Pattern with while',
        output_text=while_accum_output,
        png='slide12_while_accum_output.png',
        notes=format_output_notes(
            output_text=while_accum_output,
            instructor_notes=(
                "Three iterations, then exit. Walk through what is happening on each line. Pass 1: "
                "condition checks 150 > 0, True. Body runs, prints 'Miles remaining: 150', subtracts 50 "
                "(now 100), adds 50 to total (now 50). Pass 2: 100 > 0, True. Print 100, subtract 50 "
                "(now 50), add 50 to total (now 100). Pass 3: 50 > 0, True. Print 50, subtract 50 (now 0), "
                "add 50 to total (now 150). Loop checks: 0 > 0 is False. Exits. Final print runs. Notice "
                "the message 'Arrived!' is outside the loop, so it appears once. In Lab 2.1 you will have "
                "more going on inside the body (turn counter, arrival check), but this is the skeleton."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13: Forward link - What You Can Build Now
    # =========================================================================
    deck.add_concept_slide(
        title='What You Can Build Now: Lab 2.1',
        bullets=[
            "Start from your Lab 1.3 code. Remove Galveston, the dice roll, and the win/short branches.",
            "Trim the destination menu down to 3: Corpus Christi, Houston, Austin.",
            "Add a new constant: MILES_PER_TURN = 50.",
            "Wrap the travel in a while loop, ticking miles_remaining down each turn.",
            "Use the accumulator pattern to track total_miles for the trip summary at the end.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here is what Lab 2.1 asks you to do, in plain English. You are taking your Lab 1.3 code "
                "as the starting point. You are stripping it down: no more dice roll, no more Galveston, "
                "no more win-or-short logic. Just three clean destinations from San Antonio. Then you are "
                "adding the new constant MILES_PER_TURN equal to 50. And then you are wrapping the travel "
                "in a while loop. The loop condition is miles_remaining greater than zero. Each pass: print "
                "where you are, subtract MILES_PER_TURN from miles_remaining, add MILES_PER_TURN to "
                "total_miles, advance the turn counter. When miles_remaining hits zero or below, the loop "
                "exits and you print a trip summary. Two new things compared to Module 1: the loop, and "
                "the accumulator. Everything else is stuff you already know. Get the while loop working "
                "first with just one destination, then plug it into the menu logic you already wrote. "
                "Build a little, test a little, then build the next piece. Have fun out there."
            ),
            key_terms=[
                ('MILES_PER_TURN', 'A new named constant introduced in Lab 2.1. Sets how many miles you cover each loop iteration.'),
                ('Trip summary', 'The block of output that prints AFTER the loop ends, using the accumulated total_miles.'),
            ],
            think_about=[
                "Before you write any code, sketch out: what is your loop condition? What gets initialized before? What gets updated inside? What gets used after?",
                "Why does it help to get the loop working with a single hard-coded destination before you wire up the menu?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#while-statements',
        ),
    )

    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
