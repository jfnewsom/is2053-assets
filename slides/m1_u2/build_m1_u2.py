"""
build_m1_u2.py - M1-U2 ("The Chapter 3 Toolkit") slide deck.

Module 1, Unit 2 | Chapter 3: Decision Structures (sections 3.1, 3.2, 3.4)
Pairs with: Lab 1.2, Choose Your Destination (ENHANCE)

SCOPE (verified against lab-1-2.json and the M1 handoff, 2026-05-24)
- 3.1 the if statement
- 3.2 the if-else statement
- 3.4 the if-elif-else statement (multi-way branch)
- The else clause as catch-all for invalid input ("garbage collector")
- Multi-variable conditional assignment pattern (Lab 1.2 #1 NameError trap)
- abs() for converting negative miles_remaining into positive miles_short
- Boolean values and comparison operators: ==, !=, >, <, >=, <=

OUT OF SCOPE (these go to M1-L3 / Lab 1.3, do not introduce here)
- 3.3 Nested if statements
- 3.5 Logical operators and / or / not
- 3.6 Boolean variables / flag pattern (not used in M1 at all)
- 3.7 String testing methods (not in scope anywhere)

USAGE
-----
    python3 slides/m1_u2/build_m1_u2.py

The deck is written to /home/claude/IS2053_2026-05-24_M1-U2_Deck.pptx.
PNGs land in /home/claude/m1_u2_pngs/.
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-24_M1-U2_Deck.pptx'
PNG_OUT = '/home/claude/m1_u2_pngs'
WORK_DIR = '/tmp/build_m1_u2'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='The Chapter 3 Toolkit',
        subtitle='IS2053 Programming I  \u2022  Module 1  \u2022  Unit 2',
        notes=format_title_notes(
            deck_id='M1-U2',
            deck_title='The Chapter 3 Toolkit',
            opening_line=(
                '"Welcome back. This is Module 1, Unit 2. Last week we built '
                'programs that ran the same code every time, no matter what the '
                'user typed. This week we teach the program to make choices. '
                "Let's get into it."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='The Chapter 3 Toolkit',
        section_label='THE BIG IDEA',
        bold_oneliner='Same program, different outcome.',
        body=(
            "In U1 you built programs that ran top to bottom, the same way every "
            "time. Same questions, same math, same report. Chapter 3 is where that "
            "ends. We give the program the power to look at a value and ask, is "
            "this true? If yes, do one thing. If no, do something else. Three "
            "small structures will carry you through this entire unit. The if "
            "statement, the if-else statement, and the if-elif-else chain. Add a "
            "couple of comparison operators and one helper function called abs, "
            "and you have everything you need to write Lab 1.2."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome back to IS2053. Last week's programs all had one thing in "
                "common. They ran the same code every time you ran them. Get a "
                "name, get a number, do the math, print the report. The user "
                "could change the inputs, but the program's behavior never "
                "changed. This week we fix that. By the end of this video your "
                "programs will be able to look at what the user typed, ask a "
                "question about it, and then take different actions depending on "
                "the answer. That single capability, the ability to BRANCH, is "
                "what separates a calculator from software. Three structures do "
                "all the heavy lifting in this chapter. The if statement on its "
                "own, which does something when a condition is true. The "
                "if-else pair, which does one thing when true and something else "
                "when false. And the if-elif-else chain, which handles multiple "
                "possibilities, like a menu. That's it. Three patterns. You'll "
                "see them in every program you ever write."
            ),
            think_about=[
                'Think of a program you use that behaves differently depending on what you click or type. What was the choice the program was responding to?',
                "What's a real-world rule in your own life that looks like 'if this, then that, otherwise something else'?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 3: Concept - Why Programs Need to Make Choices
    # =========================================================================
    deck.add_concept_slide(
        title='Why Programs Need to Make Choices',
        bullets=[
            'Real software responds to its input. Same code, different outcome.',
            "Without branching, every run of your program looks identical to the last.",
            'A branch is a fork in the road. Python checks a condition and picks a path.',
            'The condition is always a yes/no question Python can answer with True or False.',
            "Branching is what makes a login screen, a menu, a quiz, or a game possible.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Let me show you why this matters with two versions of the same "
                "program. Version one. A login screen that prints WELCOME no "
                "matter what password you type. Wrong password, still welcome. "
                "Empty input, still welcome. That program has no decisions in "
                "it, and as a result it is also completely useless as a login "
                "screen. Version two. A login screen that checks whether the "
                "password matches and prints WELCOME if it does, ACCESS DENIED "
                "if it doesn't. That second version is doing something the "
                "first one literally cannot do, no matter how many lines of "
                "code you add to it. It's branching. It's making a choice based "
                "on the input. Every piece of software you've ever used does "
                "this constantly. The menu that knows you tapped option 2. The "
                "form that won't submit because you forgot the email. The game "
                "that says you levelled up. All of them. Branching."
            ),
            key_terms=[
                ('Branching', 'Choosing between two or more paths through your code based on a condition.'),
                ('Condition', 'A yes/no question your code asks. Python evaluates it to True or False.'),
            ],
            think_about=[
                "What's a moment in a program you've used recently where you said something on the screen and the program responded differently because of it?",
                'Could a program that never branches still be useful? Can you name one?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 4: Concept - Boolean Values and Comparison Operators
    # =========================================================================
    deck.add_concept_slide(
        title='Boolean Values and Comparison Operators',
        bullets=[
            'A Boolean is a value with exactly two possibilities: True or False.',
            'Comparison operators compare two values and produce a Boolean.',
            "== checks equality. = is for assigning. They are NOT the same.",
            '>= and <= include the boundary. > and < do not.',
            "!= means 'not equal'. Use it when 'anything except this' is the rule.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Before you can branch, you need a way to ask a question. The "
                "question always has the same shape. Take two values, ask "
                "Python to compare them, and Python gives you back True or "
                "False. That True or False is a Boolean. Named after George "
                "Boole, a mathematician from the 1800s. Booleans are the only "
                "thing an if statement actually cares about. The question "
                "itself is built out of comparison operators. There are six. "
                "Equals equals checks if two things are the same value. "
                "Exclamation mark equals checks if they're different. Greater "
                "than, less than, those are the same as math class. Then "
                "greater than or equal to, less than or equal to. The keyboard "
                "shortcut for those is the angle bracket followed by an equals "
                "sign. No space. The single biggest trap in your first month "
                "of programming is mixing up the one equals sign with the two "
                "equals signs. One equals is an instruction. It puts a value "
                "into a variable. Two equals is a question. It asks if two "
                "things are the same. If your program is doing weird things, "
                "this is the first thing to check. Lab 1.2 uses greater than "
                "or equal to to test whether the player made it. Did they "
                "roll enough miles, or did they fall short by exactly nothing? "
                "Both count as making it, so we use greater than or equal to, "
                "not just greater than."
            ),
            key_terms=[
                ('Boolean', 'A value that is either True or False. Named after George Boole.'),
                ('Comparison operator', 'A symbol that compares two values and returns a Boolean.'),
            ],
            think_about=[
                "If you wrote x == 5 but meant x = 5, what kind of bug would that cause? Would Python even tell you?",
                'Is age >= 18 the same rule as age > 17? When do they behave differently?',
            ],
            source_url='https://docs.python.org/3/reference/expressions.html#comparisons',
        ),
    )

    # =========================================================================
    # SLIDE 5: Concept - The if Statement
    # =========================================================================
    deck.add_concept_slide(
        title='The if Statement',
        bullets=[
            'An if statement runs a block of code ONLY when a condition is True.',
            'The line ends in a colon. The body is indented underneath it.',
            "Indentation is how Python knows what's inside the if and what isn't.",
            'If the condition is False, Python skips the body and moves on.',
            "An if with no else has no fallback. If False, nothing happens.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here's the simplest branch in Python. The if statement on its "
                "own. You write the word if, then a condition, then a colon. "
                "On the next line, you indent four spaces, and you write the "
                "code you want to run when that condition is True. That's it. "
                "If the condition is True, Python runs the indented code. If "
                "the condition is False, Python skips the indented code and "
                "keeps going with whatever comes after. Notice what's NOT here. "
                "There's no else. There's no alternative path. If the condition "
                "is False, the program just keeps moving and the indented code "
                "never runs. That's the right tool when you want something "
                "extra to happen in a specific case, but you don't need a "
                "fallback. Like congratulating someone for a high score. If "
                "their score is high, print the congrats message. If it's not, "
                "say nothing extra, the average already got printed. The "
                "indentation is doing real work here, by the way. In Python, "
                "indentation isn't a style choice, it's syntax. The indented "
                "lines are INSIDE the if. The unindented lines are OUTSIDE. "
                "Get the indentation wrong and the program behaves wrong, even "
                "if every word is spelled correctly."
            ),
            key_terms=[
                ('if statement', 'A structure that runs a block of code only when a condition evaluates to True.'),
                ('Block', 'One or more lines of indented code that belong to a control structure.'),
                ('Indentation', "In Python, leading whitespace that defines which lines are inside a block. Usually four spaces."),
            ],
            think_about=[
                'When would you reach for an if WITHOUT an else? Think of a case where "do something extra" makes sense but "do something different" does not.',
                'If you forgot to indent the line under an if, what do you think Python would do? Why is indentation a syntax rule and not just a style rule?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 6: Demo - A Simple if Test (test_average.py from BookEx 3.1)
    # =========================================================================
    test_average_code = """# BookEx Ch 3 - test_average.py
HIGH_SCORE = 95

test1 = int(input('Enter the score for test 1: '))
test2 = int(input('Enter the score for test 2: '))
test3 = int(input('Enter the score for test 3: '))

average = (test1 + test2 + test3) / 3
print(f'The average score is {average}.')

if average >= HIGH_SCORE:
    print('Congratulations!')
    print('That is a great average!')
"""

    deck.add_demo_slide(
        title='Demo: A Simple if Test',
        code=test_average_code,
        png='slide06a_test_average.png',
        notes=format_demo_notes(
            code=test_average_code,
            instructor_notes=(
                "This is BookEx Chapter 3 program test_average.py from section "
                "3.1, the same file students typed for BookEx. Walk it top to "
                "bottom. Start at the HIGH_SCORE constant and call back to "
                "U1's named constants pattern verbally. Don't reteach it. Then "
                "the three input lines, all wrapped in int. Then the average "
                "calculation. Then the print of the average. Stop and trace "
                "through one example by hand. If the scores are 95, 95, 95, "
                "what's the average? 95. Is 95 greater than or equal to 95? "
                "Yes. So the congrats prints. Now try 95, 95, 94. Average is "
                "94 point 67. Is that greater than or equal to 95? No. So "
                "nothing extra prints, the program just ends after the "
                "average line. The point to land here is that the indented "
                "print lines are part of the if. The unindented lines are "
                "not. Drag your finger down the indentation column on screen "
                "to make this visual."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 7: Output - test_average Run
    # =========================================================================
    test_average_output = """\
Enter the score for test 1: 95
Enter the score for test 2: 95
Enter the score for test 3: 95
The average score is 95.0.
Congratulations!
That is a great average!"""

    deck.add_output_slide(
        title='Output: One Run, Two Possible Endings',
        output_text=test_average_output,
        png='slide06b_test_average_output.png',
        notes=format_output_notes(
            output_text=test_average_output,
            instructor_notes=(
                "Read the output line by line. The three prompt lines are "
                "from the three input calls. The average line is the print "
                "right after the calculation. Then the two Congratulations "
                "lines are the body of the if, which only fired because the "
                "average hit the threshold. Then say: now imagine the same "
                "program but with the inputs 80, 80, 80. Walk through what "
                "the screen would look like. Same first four lines, but no "
                "Congratulations lines. The program just stops. That's an if "
                "with no else. Sometimes nothing happens. That's a feature, "
                "not a bug."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: Concept - The if-else Statement
    # =========================================================================
    deck.add_concept_slide(
        title='The if-else Statement',
        bullets=[
            'if-else gives you two paths. One runs when True, the other when False.',
            'Exactly one of the two blocks always runs. Never both. Never neither.',
            'The else keyword has no condition of its own. It catches everything else.',
            "Indent the else body the same way you indent the if body.",
            "Use if-else when 'do nothing in the other case' would leave a hole.",
        ],
        notes=format_concept_notes(
            video_script=(
                "The if statement on its own is good when you want something "
                "extra to happen sometimes. But often you want one thing OR "
                "the other. A password check is the classic example. If the "
                "password is right, let them in. If it's wrong, tell them no. "
                "There is no third option. You can't just stay silent when "
                "the password is wrong, because then the user has no idea "
                "what happened. That's what if-else is for. You write if, "
                "condition, colon, indented body. Then unindent back to the "
                "if's level and write else, colon, indented body. Exactly one "
                "of those two bodies always runs. The else has no condition "
                "of its own, by the way. It's the catch-all. It runs when the "
                "if's condition was False. Whatever False means in that "
                "context. Notice how this changes the shape of your code. "
                "With a plain if, your code could just keep flowing past it. "
                "With an if-else, you've forced the program to pick a side."
            ),
            key_terms=[
                ('if-else statement', 'A two-way branch: one block runs when the condition is True, the other when False.'),
                ('else clause', "The fallback path. Runs when the if's condition is False. Has no condition of its own."),
            ],
            think_about=[
                'How is if-else different from writing two separate if statements with opposite conditions? Would they always behave the same way?',
                'Pick a real-world rule like "if it\'s raining, take an umbrella, otherwise wear sunglasses." What\'s the condition? What are the two paths?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 9: Demo - One Path or the Other (password.py from BookEx 3.2)
    # =========================================================================
    password_code = """# This program compares two strings.
# Get a password from the user.
password = input('Enter the password: ')

# Determine whether the correct password
# was entered.
if password == 'prospero':
    print('Password accepted.')
else:
    print('Sorry, that is the wrong password.')
"""

    deck.add_demo_slide(
        title='Demo: One Path or the Other',
        code=password_code,
        png='slide09a_password.png',
        notes=format_demo_notes(
            code=password_code,
            instructor_notes=(
                "This is BookEx Chapter 3 program password.py from section "
                "3.2, the file students typed for BookEx. Open by reading the "
                "comment at the top out loud. Then the input. Then the if. "
                "Pause on the double equals. Say it explicitly. 'This is "
                "double equals. Single equals would assign prospero into "
                "password, which would always make the if True, which would "
                "never lock anyone out. Double equals is a question. Are "
                "these two values the same?' This is the kind of slip that "
                "costs students hours, so name the trap explicitly. Then the "
                "else clause. Notice it has no condition. It's the fallback. "
                "Run the program twice live: once with the right password, "
                "once with a wrong one. Both runs use the SAME code, but "
                "produce DIFFERENT output. That's branching."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: Output - Two Runs, Two Outcomes
    # =========================================================================
    password_output = """\
Run 1:
Enter the password: prospero
Password accepted.

Run 2:
Enter the password: hunter2
Sorry, that is the wrong password."""

    deck.add_output_slide(
        title='Output: Two Runs, Two Outcomes',
        output_text=password_output,
        png='slide09b_password_output.png',
        notes=format_output_notes(
            output_text=password_output,
            instructor_notes=(
                "Show two runs side by side on this slide so students see "
                "both paths firing. In Run 1 the user typed prospero, the "
                "condition was True, the if block ran. In Run 2 the user "
                "typed hunter2, the condition was False, the else block ran. "
                "Same code. Different inputs. Different outcomes. That is "
                "everything you came here to do. Optionally, mention that "
                "prospero comes from Shakespeare's The Tempest. The textbook "
                "author is having a little fun. The point lands either way."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: Concept - The if-elif-else Chain
    # =========================================================================
    deck.add_concept_slide(
        title='The if-elif-else Chain',
        bullets=[
            'if-elif-else handles three or more possible cases in one structure.',
            "elif means 'else if'. It's an extra condition to check when the previous ones were False.",
            "You can have as many elif branches as you need. Add or remove as the problem requires.",
            'Python checks each condition top to bottom and runs the FIRST one that is True.',
            "Once one branch fires, the rest are skipped. Order matters.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Most real decisions in a program aren't two-way. A menu has "
                "five items. A letter grade has six possibilities. A "
                "destination has three choices plus the option of an invalid "
                "selection. That's where if-elif-else comes in. elif is "
                "short for else if. You stack as many elif lines as you need "
                "between your if and your else, and Python checks them in "
                "order from top to bottom. The first one that comes back "
                "True is the one that runs, and Python skips the rest. That "
                "last point is doing a lot of work, so let me say it again. "
                "Python checks the conditions in the order you wrote them, "
                "and the FIRST True one wins. The rest are skipped, even if "
                "they would also have been True. That means the order you "
                "list your conditions actually matters. In Lab 1.2 this "
                "week, the menu has three valid choices and then an invalid "
                "case. Three elif branches, plus the else. Each branch sets "
                "up a different destination. Same program, four possible "
                "outcomes."
            ),
            key_terms=[
                ('elif', "Short for else if. An additional condition checked when the previous if and any earlier elifs were False."),
                ('if-elif-else chain', 'A multi-way branch that checks several conditions in order and runs the first one whose condition is True.'),
            ],
            think_about=[
                'If two of your elif conditions could BOTH be True, which one runs? Why does that matter?',
                'Could you replace an if-elif-else chain with a stack of plain if statements? Would the program behave the same way?',
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 12: Concept - The else Clause as Garbage Collector
    # =========================================================================
    deck.add_concept_slide(
        title='The else Clause as Garbage Collector',
        bullets=[
            "if and elif handle the cases you planned for. else handles everything else.",
            "Users will type things you did not expect. else is your safety net.",
            "Without an else, an invalid input falls through and breaks your program later.",
            "The else block is where you say 'this is what to do when none of my plans match.'",
            "In a menu, the else is what catches the user who types 99 when you asked for 1, 2, or 3.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here's the frame I want you to carry with you for the rest "
                "of this course. The if and the elif branches handle the "
                "specific cases you've planned for. The else clause is the "
                "garbage collector. It catches everything you didn't plan "
                "for. The invalid inputs. The edge cases. The user typing "
                "the word potato when you asked for a number. The user "
                "hitting 99 in a 1-to-3 menu. Without an else, those cases "
                "fall through your code and cause problems downstream. "
                "Variables that should have been set don't get set. Math "
                "happens on values that don't exist. The program either "
                "crashes or, worse, prints nonsense. With an else, you stay "
                "in control. You acknowledge the unexpected input "
                "explicitly. You set safe default values. You print an "
                "error message that tells the user what went wrong. Lab "
                "1.2 has exactly this pattern. Three valid choices, plus "
                "the else for the invalid case. If you forget to include "
                "the else, your tests will pass when you choose 1, 2, or "
                "3, and crash the moment someone picks 99. The else is "
                "your safety net. Always include it."
            ),
            key_terms=[
                ('Catch-all', "A branch that handles any case not covered by the earlier conditions."),
                ('Edge case', "An input or situation outside the typical range your code was designed for."),
            ],
            think_about=[
                "What's the worst thing a user could type into your menu? Does your else handle it gracefully?",
                "Can you think of a real form or app that handled an unexpected input badly? What would the 'else' have done differently?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#if-statements',
        ),
    )

    # =========================================================================
    # SLIDE 13a: Demo - The Nested Version (matches what students typed in BookEx)
    # =========================================================================
    grader_nested_code = """A_score = 90
B_score = 80
C_score = 70
score = int(input('Enter your test score: '))
if score >= A_score:
    print('Your grade is A.')
else:
    if score >= B_score:
        print('Your grade is B.')
    else:
        if score >= C_score:
            print('Your grade is C.')
        else:
            print('Your grade is F.')
"""

    deck.add_demo_slide(
        title='Demo: What You Typed in BookEx',
        code=grader_nested_code,
        png='slide13a_grader_nested.png',
        notes=format_demo_notes(
            code=grader_nested_code,
            instructor_notes=(
                "This is BookEx Chapter 3 program grader.py, trimmed from the "
                "full A-B-C-D-F version to A-B-C-F so it fits on screen. "
                "Acknowledge that explicitly: this is the file students "
                "already typed for the textbook practice. It works. It "
                "produces the correct letter grade every time. Walk through "
                "score 75. Is 75 greater than or equal to 90? No, fall into "
                "the else. Is 75 greater than or equal to 80? No, fall into "
                "the next else. Is 75 greater than or equal to 70? Yes. "
                "Print C. Done. The logic is fine. The PROBLEM is what your "
                "eye has to do to follow it. Drag a finger down the "
                "indentation column. Four indent levels deep, and that's "
                "only three branches. The textbook's full version goes five "
                "levels deep. Notice how much horizontal space the actual "
                "logic occupies, and how easy it would be to lose track of "
                "which else belongs to which if. Now ask the class: imagine "
                "you had ten conditions to check instead of four. How wide "
                "is that code? How readable? That's the setup for the next "
                "slide."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13b: Demo - The if-elif-else Rewrite (same logic, flat structure)
    # =========================================================================
    grader_elif_code = """A_score = 90
B_score = 80
C_score = 70
score = int(input('Enter your test score: '))
if score >= A_score:
    print('Your grade is A.')
elif score >= B_score:
    print('Your grade is B.')
elif score >= C_score:
    print('Your grade is C.')
else:
    print('Your grade is F.')
"""

    deck.add_demo_slide(
        title='Demo: The Cleaner Rewrite',
        code=grader_elif_code,
        png='slide13b_grader_elif.png',
        notes=format_demo_notes(
            code=grader_elif_code,
            instructor_notes=(
                "Same problem. Same inputs. Same outputs. Different shape. "
                "Every nested else-if-else in the previous slide collapses "
                "into a single elif on this slide. The indentation stops "
                "growing. The branches line up vertically and your eye can "
                "scan them top-to-bottom in one pass. Walk through score 75 "
                "again. Is 75 greater than or equal to 90? No. Move to the "
                "next elif. Is 75 greater than or equal to 80? No. Next "
                "elif. Is 75 greater than or equal to 70? Yes. Print C. "
                "Done. Exact same path, same result. Python doesn't keep "
                "checking after a True; once an elif fires, the rest are "
                "skipped. The key point to land for Lab 1.2: this is the "
                "structure you want. Three valid menu choices and an else, "
                "not nested if-else trees. The textbook shows you both "
                "patterns in Section 3.4 because both exist in the wild. "
                "Now you know why we reach for if-elif-else when we have "
                "more than two outcomes."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13c: Output - Same Result, Both Versions
    # =========================================================================
    grader_output = """\
Run 1:
Enter your test score: 87
Your grade is B.

Run 2:
Enter your test score: 50
Your grade is F."""

    deck.add_output_slide(
        title='Output: Same Result, Both Versions',
        output_text=grader_output,
        png='slide13c_grader_output.png',
        notes=format_output_notes(
            output_text=grader_output,
            instructor_notes=(
                "This is the output for BOTH versions. Run the nested "
                "version with score 87, you get B. Run the if-elif-else "
                "version with score 87, you get B. Same input, same output, "
                "every time. Run 1 hits the second branch in either "
                "version. Run 2 falls through every condition and lands in "
                "the else. The user can't tell which version they're "
                "running. The difference is entirely about how readable the "
                "code is for the human writing and maintaining it. That's "
                "the lesson. When two pieces of code do exactly the same "
                "thing, prefer the one that's easier to read. In Lab 1.2 "
                "you'll write the destination menu using if-elif-else for "
                "the same reason: three valid choices plus an else, all in "
                "a flat chain. No nesting needed."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 15: Concept - The Multi-Variable Conditional Assignment Pattern
    # =========================================================================
    deck.add_concept_slide(
        title='Setting Multiple Variables Across Branches',
        bullets=[
            "A common pattern: each branch sets up the SAME set of variables with DIFFERENT values.",
            "Every branch, including else, must set EVERY variable. No exceptions.",
            "Skip one variable in one branch, and your program crashes downstream with a NameError.",
            "The crash happens AFTER the if-elif-else, not inside it. The error message points the wrong way.",
            "Sanity check: walk through every branch and confirm the same variable names appear in each one.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here's the single most common bug students hit in Lab 1.2, "
                "and I want to head it off before you write the lab. The lab "
                "wants you to set up four variables inside your "
                "if-elif-else chain. The destination, the distance, the "
                "status, and the message. Different values in each branch, "
                "but the SAME four variables in each branch. Every branch, "
                "including the else. If you forget to set one variable in "
                "one branch, here's what happens. The user picks that "
                "branch. Python runs that branch's code, which is missing a "
                "variable. Then Python keeps running, gets to the part of "
                "your program where you try to USE that variable, and "
                "crashes with a NameError saying the name is not defined. "
                "The trap is that the crash doesn't happen INSIDE the if. "
                "It happens LATER, when the variable is supposed to be "
                "used. So your error message points to the wrong place. "
                "The fix is to slow down and check every single branch "
                "before you run the program. Same variables. Every branch. "
                "Including the else."
            ),
            key_terms=[
                ('NameError', 'A Python error that happens when you try to use a variable name that was never assigned a value in the current path.'),
            ],
            think_about=[
                'If your code crashes on line 50 with a NameError, but the variable was supposed to be set inside an if-elif-else on line 25, what does that tell you about which branch ran?',
                "Why does the else branch have to set the same variables as the if branches? What does the program need from it later?",
            ],
            source_url='https://docs.python.org/3/library/exceptions.html#NameError',
        ),
    )

    # =========================================================================
    # SLIDE 16: Concept - abs() for Cleaning Up Negative Numbers
    # =========================================================================
    deck.add_concept_slide(
        title='abs() for Cleaning Up Negative Numbers',
        bullets=[
            'abs() is a built-in function that returns the absolute value of a number.',
            'abs(-12) is 12. abs(12) is 12. abs(0) is 0. Always non-negative.',
            'Useful when a negative result has a positive interpretation in plain English.',
            'In Lab 1.2: miles_remaining of -50 means the player was 50 miles SHORT.',
            "abs() lets you print 'you were 50 miles short' instead of 'you were negative 50 miles short.'",
        ],
        notes=format_concept_notes(
            video_script=(
                "One more small tool before we close out. The built-in "
                "function abs. Short for absolute value. You feed it a "
                "number, it gives you back that number with any negative "
                "sign stripped off. abs of negative 12 is 12. abs of 12 is "
                "also 12. abs of zero is zero. Never negative, ever. Why "
                "do we care? Because in Lab 1.2 you'll calculate "
                "miles_remaining by taking the miles the player rolled and "
                "subtracting the distance to the destination. If they "
                "rolled enough, miles_remaining is positive or zero, which "
                "means they made it. If they didn't roll enough, "
                "miles_remaining is negative. A negative number makes "
                "sense to the program, but it doesn't make sense to a "
                "human. Nobody says 'I was negative 50 miles short.' They "
                "say 'I was 50 miles short.' That's where abs comes in. "
                "You write abs of miles_remaining and you get the "
                "magnitude back as a positive number, ready to print. "
                "Quick footnote. abs isn't in the Gaddis textbook. Your "
                "professor is introducing it here because it's a built-in "
                "function that the lab uses. It's fair game."
            ),
            key_terms=[
                ('Absolute value', "The distance of a number from zero. Always non-negative."),
                ('Built-in function', "A function that comes with Python, ready to use without importing anything."),
            ],
            think_about=[
                "If miles_remaining is positive, do you need abs() before you print it? Why or why not?",
                'What other situations in everyday life take a positive AND a negative version of the same idea? (Hint: temperature, bank balance, finishing a race.)',
            ],
            source_url='https://docs.python.org/3/library/functions.html#abs',
        ),
    )

    # =========================================================================
    # SLIDE 17: Overview - What You Can Build Now
    # =========================================================================
    deck.add_overview_slide(
        title='What You Can Build Now',
        section1_label='WHAT YOU CAN DO NOW',
        section1_body=(
            "You can write a program that presents a menu, reads the user's "
            "choice, branches into different code depending on what they "
            "picked, sets up different variables for each path, checks "
            "whether a numeric goal was hit using a comparison, and prints "
            "different reports depending on the outcome. That is "
            "decision-making software. That's an entire category of program "
            "you couldn't write a week ago."
        ),
        section2_body=(
            "Three structures do all the work. The if statement, when you "
            "want something extra to happen sometimes. The if-else "
            "statement, when you want one path OR the other. The "
            "if-elif-else chain, when you have three or more options. The "
            "else clause is your safety net for everything else. The "
            "comparison operators are the questions you ask. abs() cleans "
            "up negative numbers when you want to print them as magnitudes."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "Lab 1.2, Choose Your Destination, is where you put this all "
            "together. You'll copy your Lab 1.1 code, add a destination "
            "menu, write the if-elif-else chain, and use abs() to report "
            "miles short. Next week in M1-L3 we extend this with NESTED "
            "decisions (an if inside an if) and the logical operators and "
            "and or, so that Houston can branch again into a Galveston "
            "side trip. The Chapter 3 toolkit is almost complete."
        ),
        notes=format_concept_notes(
            video_script=(
                "Stop and notice what you can do now that you couldn't do "
                "yesterday. You can write a program that presents a menu, "
                "reads the user's choice, branches into different code "
                "depending on what they picked, sets up different "
                "variables for each path, checks whether a numeric goal "
                "was hit, and prints different reports depending on the "
                "outcome. That's an entire category of program that was "
                "out of reach a week ago. Three structures got us here. "
                "The plain if. The if-else. The if-elif-else chain. Add "
                "the comparison operators and the abs function, and you "
                "have everything Lab 1.2 needs. Lab 1.2 is going to ask "
                "you to take your Lab 1.1 program from last week, copy "
                "it, drop in a destination menu, write the if-elif-else "
                "chain to handle the three valid choices plus the "
                "invalid case, and use abs to report how many miles the "
                "player fell short by. The lab walkthrough video in "
                "M1-L1 last week showed you exactly this shape, so go "
                "back and skim that if you need a refresher on the "
                "starting code. Next week we extend the toolkit. We add "
                "nested decisions, an if inside an if, and the logical "
                "operators and and or, so that one branch can branch "
                "again. That's what makes the Houston-to-Galveston side "
                "trip work in Lab 1.3. Get this week's lab in your "
                "fingers first. The rest builds on it."
            ),
            think_about=[
                'Of the three structures (if, if-else, if-elif-else), which one feels the most natural to you, and which one feels the most foreign?',
                "What's a small program you've used (a quiz app, a menu, a calculator with modes) that you can now imagine writing yourself?",
            ],
        ),
    )

    # =========================================================================
    # Save
    # =========================================================================
    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
