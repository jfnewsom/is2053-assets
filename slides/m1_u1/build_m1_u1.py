"""
build_m1_u1.py - M1-U1 ("The Chapter 2 Toolkit") slide deck.

Module 1, Unit 1 | Chapter 2: Variables, Input, Output, Arithmetic, F-Strings
Pairs with: Lab 1.1, Welcome to San Antonio

USAGE
-----
    python3 slides/m1_u1/build_m1_u1.py

The deck is written to /home/claude/M1-U1.pptx by default. PNGs land in
/home/claude/m1_u1_pngs/.

PATTERN
-------
This file is the canonical example of a per-deck build script. To create a
new deck:

    1. Copy this directory:    cp -r slides/m1_u1 slides/<new_deck>
    2. Rename the script:      mv build_m1_u1.py build_<new_deck>.py
    3. Replace the OUTPUT_*, PNG_OUT, deck_id, and slide content below.
    4. Run it.

The shared library at slides/build_lib.py handles the rest.
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-24_M1-U1_Deck.pptx'
PNG_OUT = '/home/claude/m1_u1_pngs'
WORK_DIR = '/tmp/build_m1_u1'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='The Chapter 2 Toolkit',
        subtitle='IS2053 Programming I  \u2022  Module 1  \u2022  Unit 1',
        notes=format_title_notes(
            deck_id='M1-U1',
            deck_title='The Chapter 2 Toolkit',
            opening_line=(
                '"Welcome to your first week of IS2053. This is Module 1, Unit 1. '
                "We're going to spend the next hour or so walking through the Chapter 2 "
                'toolkit, the seven small ideas that turn a script into an actual working '
                'program. Let\'s get started."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro (The Chapter 2 Toolkit)
    # =========================================================================
    deck.add_narrative_slide(
        title='The Chapter 2 Toolkit',
        section_label='THE BIG IDEA',
        bold_oneliner='From a closed box to a working program.',
        body=(
            "A program with no inputs and no outputs is a closed box talking to itself. "
            "Chapter 2 is the chapter that opens the box: how to ask, how to answer, and "
            "how to do work in between. Seven small ideas live here. Variables, print, "
            "input, type conversion, arithmetic, string concatenation, and f-strings. "
            "None of them are individually hard. The first time you see all seven together "
            "can feel like a lot, so we'll work top-down on each: what problem are we "
            "trying to solve, then how Python solves it."
        ),
        notes=format_concept_notes(
            video_script=(
                "Welcome to your first week. I want to start with a weird question. What "
                "is a program actually FOR? Most of the code you'll write in this course "
                "exists because something on the other end of the screen wants information "
                "from the program, or wants to give information to the program. The program "
                "is the part in the middle. Chapter 2 is the chapter that gives the program "
                "a way to listen and a way to speak. It's also where you learn how to store "
                "the things people tell you so you can use them later, and how to do basic "
                "math on whatever's in storage. By the end of this video you should "
                "understand seven small ideas: variables, print, input, type conversion, "
                "arithmetic, string concatenation, and f-strings. None of them are "
                "individually hard. The first time you see all seven together can feel like "
                "a lot, so my plan is to walk through them in the order you'd actually meet "
                "them when writing a real program. We're going top-down on every concept: "
                "what problem are we trying to solve, then how Python solves it, then a "
                "quick example. Think about this. Have you ever used a vending machine "
                "where the screen tells you the total and waits for your money? That's a "
                "program with inputs, outputs, and work happening in between. Hold that "
                "picture for the rest of the video."
            ),
            think_about=[
                "Vending machine, ATM, self-checkout. What were the inputs, what were the outputs, what was happening in the middle?",
                "What do you imagine is the hardest part about writing a program that has to TALK to a person?",
            ],
            source_url='https://docs.python.org/3/tutorial/introduction.html',
        ),
    )

    # =========================================================================
    # SLIDE 3: Concept - The Shape of a Python Lab File
    # =========================================================================
    deck.add_concept_slide(
        title='The Shape of a Python Lab File',
        bullets=[
            'Every lab file in this course has the same shape: docstring, constants, def main(), if __name__.',
            'The docstring names you, your section, and what the program does.',
            'The constants block holds fixed values you reference repeatedly: distances, limits, magic numbers.',
            'def main(): is a container for all your program logic. For now, write everything inside it.',
            "if __name__ == '__main__': at the bottom is what runs main() when you press play. Always there. Don't touch it.",
        ],
        notes=format_concept_notes(
            video_script=(
                "The lab template you'll open in VS Code already has this skeleton in "
                "place. Your job is to fill in the body of main(). The structural pieces "
                "around it (docstring, def main, if __name__) are given to you. The "
                "reason this shape exists is twofold. One, it's how real Python programs "
                "are organized. By the end of the course you'll understand WHY def main "
                "exists and what if __name__ means; today you accept it as the wrapper "
                "and move on. Two, it gives every lab in the course the same shape, so "
                "once you've seen Lab 1.1's structure, you've seen Lab 2.1's structure "
                "too. The labs grow inside the same scaffolding. Don't try to remove the "
                "def main line. Don't write code outside it. Stay inside the function "
                "body and your life will be easier. The demos in the rest of this video "
                "are kept simple and don't show the wrapper, but rest assured: when you "
                "open the Lab 1.1 file, the wrapper is there and your code goes inside "
                "it. Think about this. Have you ever opened a Word document template "
                "that already has the formatting set up so you just fill in the body? "
                "Same idea here."
            ),
            key_terms=[
                ('Docstring', 'A triple-quoted string at the top of a file or function that documents what it does.'),
                ('Function', 'A named chunk of code you can call by name. def is the keyword that defines one.'),
            ],
            think_about=[
                'Why might a Python course put all program logic inside def main() instead of just typing it at the top of the file?',
                "The if __name__ == '__main__' line looks cryptic. We're not going to fully explain it today. What other things in life have you accepted on faith and circled back to understand later?",
            ],
            source_url='https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts',
        ),
    )

    # =========================================================================
    # SLIDE 4: Concept - Why We Need Variables
    # =========================================================================
    deck.add_concept_slide(
        title='Why We Need Variables',
        bullets=[
            'Programs deal with information they need to remember and reuse.',
            'A variable is a labeled container you put a value into.',
            "Once you've named it, you refer to the value by the label, not by retyping it.",
            'The label is for you and your fellow developers, not for the computer.',
            "Python's = does NOT mean 'equals' the way it did in algebra class. It's an instruction.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Picture your kitchen pantry. Now picture it without any labels. Every shelf "
                "is a mystery, every container looks the same. If you want flour, you open "
                "seven containers until you find it. You finally find it, pour what you need, "
                "and then six weeks later when you need flour again, you have to do the whole "
                "hunt again. That is what programming would be without variables. A variable "
                "is a label on a container. When you write player_name = \"Maria\", you're "
                "writing the word player_name on a sticker, slapping it on a container, and "
                "dropping the string Maria inside. From that point on, whenever your code "
                "refers to player_name, Python opens that container and pulls Maria out. The "
                "container lives in memory somewhere; you don't need to know where. The "
                "label is what matters. Now here's the part that trips people up. The equals "
                "sign in a Python assignment is NOT the equals sign from algebra. In algebra, "
                "x equals three is a statement of fact, an unchanging truth. In Python, that "
                "same line is an instruction: take the value on the right, store it in the "
                "container on the left. Direction matters. You can write roll = 12, then a "
                "few lines later write roll = 18, and the 12 is just gone. The container now "
                "has 18. Think about this. What's the difference between \"this thing equals "
                "five\" and \"put five in this thing\"?"
            ),
            key_terms=[
                ('Variable', 'A labeled container in memory that holds a value.'),
                ('Assignment', 'Using = to put a value into a variable.'),
            ],
            think_about=[
                'What\'s the difference between "this thing equals five" in math class and "put five in this thing" in Python?',
                'If your kitchen labeled everything with eight-character alphanumeric codes like LB39H4XQ for flour, would that be better or worse than today\'s setup? Why?',
            ],
            source_url='https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator',
        ),
    )

    # =========================================================================
    # SLIDE 4: Concept - How Variables Work in Python
    # =========================================================================
    deck.add_concept_slide(
        title='How Variables Work in Python',
        bullets=[
            '= takes the value on the right and stores it in the name on the left.',
            "Names use letters, digits, and underscores. They can't start with a digit.",
            'Names are case-sensitive: Name and name are different containers.',
            "You don't declare a type. Python figures out the type from the value.",
            'Reassigning a variable overwrites the previous value. The old value is gone.',
        ],
        notes=format_concept_notes(
            video_script=(
                "Now that you know what a variable IS, let me walk you through the rules "
                "Python plays by. First, the name. Letters, digits, and underscores. You "
                "can't start with a digit, because something like 1roll would confuse "
                "Python's parser. Conventionally we use lowercase with underscores between "
                "words: player_name, miles_traveled. That's not a Python rule, that's a "
                "community convention called snake_case, and the auto-grader is going to "
                "check for it. Second, names are case-sensitive. name and Name are two "
                "different containers. This bites everyone the first week, so just remember "
                "it now. Third, Python doesn't make you declare what type the variable "
                "holds. Other languages do. In Python you just write roll = 14 and Python "
                "figures it out. Same variable can hold a string later: roll = \"fourteen\" "
                "is legal. Python doesn't complain. Fourth, assignment is destructive. If "
                "roll holds 12 and you write roll = 18, the 12 is gone. Not archived, not "
                "in some history, just gone. If you needed the 12 for later, you should "
                "have stored it in a different variable. That's it. Five small rules that "
                "govern every assignment you'll ever write. Think about this. If you "
                "assigned roll = 14 and then accidentally wrote Roll = 20, what would "
                "Python think you did?"
            ),
            key_terms=[
                ('snake_case', 'A naming convention using lowercase letters with underscores between words, like player_name.'),
                ('Identifier', 'The technical term for any name you give to a variable, function, or class.'),
            ],
            think_about=[
                'If you assigned roll = 14 and then accidentally wrote Roll = 20, what does Python think happened?',
                "Python doesn't make you declare types up front. Other languages do. Which side of that tradeoff feels more comforting to you, and why?",
            ],
            source_url='https://docs.python.org/3/reference/simple_stmts.html#assignment-statements',
        ),
    )

    # =========================================================================
    # SLIDE 6: Concept - Named Constants for Fixed Values
    # =========================================================================
    deck.add_concept_slide(
        title='Named Constants for Fixed Values',
        bullets=[
            "Some values in your program don't change while it runs: a distance to a city, the number of sides on a die.",
            'Store those values in variables named in UPPER_SNAKE_CASE: SAT_TO_CORPUS = 150.',
            'The ALL CAPS is a signal to other programmers (and your future self): treat this as a constant.',
            "Python doesn't ENFORCE it. You CAN reassign all-caps names. The convention is for humans, not the interpreter.",
            'Declare constants at the top of the file, above def main(), so the program\'s fixed values are visible up front.',
        ],
        notes=format_concept_notes(
            video_script=(
                "When you read your own lab solution six weeks from now, will you "
                "remember why the number 150 keeps appearing in the math? Probably "
                "not. But if every place that used to say 150 now says SAT_TO_CORPUS, "
                "you'll instantly understand: that's the distance from San Antonio to "
                "Corpus Christi. That's the entire purpose of a named constant. It's "
                "a label on a number, exactly like a variable has a label, but with "
                "one social convention. The label is in ALL CAPS. UPPER_SNAKE_CASE. "
                "The constants from your Lab 1.1 are SAT_TO_CORPUS, SAT_TO_HOUSTON, "
                "SAT_TO_AUSTIN, and HOU_TO_GALVESTON. Three letters of city code from, "
                "T-O, three letters of city code to. Read them out loud: san antonio "
                "to corpus. That's it. There's a piece of weird programming culture "
                "to understand here. Python doesn't actually FORCE these to be "
                "constant. You can write SAT_TO_CORPUS = 9999 anywhere in your "
                "program and Python will let you. The all caps is a signal to humans, "
                "not to Python: treat this as if it were constant. Don't change it. "
                "Future-you reads your past-you's code, sees ALL CAPS, and knows not "
                "to mess with it. The other small rule is location. Declare these at "
                "the top of your file, before def main(). The reason is that anyone "
                "reading the file can see, in the first ten lines, what fixed values "
                "your program uses. Think about this. Why is the convention ALL CAPS "
                "rather than something else?"
            ),
            key_terms=[
                ('Constant', "A value that doesn't change during program execution."),
                ('UPPER_SNAKE_CASE', 'All capital letters with underscores between words. Python convention for constants.'),
            ],
            think_about=[
                'Why is the convention ALL CAPS rather than something like underscores around the name?',
                "If Python doesn't actually prevent you from reassigning a constant, why bother with the convention?",
            ],
            source_url='https://peps.python.org/pep-0008/#constants',
        ),
    )

    # =========================================================================
    # SLIDE 7: Concept - print() and the Banner Trick
    # =========================================================================
    deck.add_concept_slide(
        title='print() and the Banner Trick',
        bullets=[
            'print() is how a program sends text to the screen.',
            'Every call to print() adds a new line at the end automatically.',
            'Pass it a string in quotes, a variable, or a mix.',
            "'=' * 60 repeats a string. Sixty equals signs become a banner.",
            'Banners frame important blocks: the open, the report, the goodbye.',
        ],
        notes=format_concept_notes(
            video_script=(
                "A program is invisible until it prints something. You can run it, you can "
                "do calculations, you can move data around, but if you never call print(), "
                "the person watching has no idea anything happened. So print() is the "
                "program's voice. The basic form is the function name, an open paren, the "
                "thing you want to say in quotes, and a close paren. print('Hello') and "
                "Python sends Hello to the terminal. Here's a small feature that becomes "
                "useful immediately. Every call to print() adds a newline at the end "
                "automatically. So three prints make three lines on the screen, with no "
                "extra work from you. There's another small trick I want you to know about "
                "early. If you write '=' * 60, Python takes one equals sign and gives you "
                "back sixty of them in a row. That's string multiplication. Same trick "
                "works with any character: dashes, stars, spaces. Combine print() with "
                "string multiplication and you get banners. A row of equals signs, a title, "
                "another row of equals signs. That's how every program in this course is "
                "going to open. It's not decoration. It's signal to the user that the "
                "program is up, this is the right program, and here is where it begins. "
                "Think about this. If you write print() with nothing inside the parens at "
                "all, what shows up on the screen?"
            ),
            key_terms=[
                ('Function', 'A reusable named operation in Python. You call it by writing its name followed by parentheses, like print().'),
                ('Argument', 'A value you pass to a function, written inside the parentheses.'),
            ],
            think_about=[
                'If you write print() with nothing inside the parens, what shows up on the screen?',
                'Why might a program want three separate prints in a row instead of one big print containing all the text?',
            ],
            source_url='https://docs.python.org/3/library/functions.html#print',
        ),
    )

    # =========================================================================
    # SLIDE 6: Concept - Why Programs Need to Ask Questions
    # =========================================================================
    deck.add_concept_slide(
        title='Why Programs Need to Ask Questions',
        bullets=[
            'A program that only prints is a monologue. Same output every time.',
            'For the program to behave differently for different people, it has to ASK them something.',
            'Asking in code means three things: print the question, pause, capture what they typed.',
            'Python wraps all three into a single function called input().',
            'Once the program has the answer, it can use it for everything that follows.',
        ],
        notes=format_concept_notes(
            video_script=(
                "So now your program can talk. But there's a problem. A program that only "
                "talks is a monologue. You run it, it prints whatever was hardcoded into "
                "it, it stops. Run it a thousand times, get the exact same output a thousand "
                "times. That's fine for a calculator that always adds two and two, but it's "
                "useless for a game where the player has a name, or a quiz that asks "
                "questions, or an order form that needs to know what you want to buy. For "
                "the program to behave differently for different people, the program has to "
                "ASK them something. It has to pause, listen, and respond based on what it "
                "heard. That is the entire purpose of input. Now think about what \"asking "
                "a question\" really means in code. The program has to print the question. "
                "Then it has to stop. It has to wait for a human to type something. It has "
                "to wait for the human to hit Enter. Then it has to grab what they typed "
                "and store it somewhere usable. That's actually quite a lot of work, and "
                "Python wraps all of it into one small function called input(). We'll see "
                "exactly how on the next slide. For now, just sit with the shift in mental "
                "model. Your program is no longer a one-way speech. It's a conversation. "
                "Think about this. What's the difference between a webpage that just "
                "displays information and a webpage with a form?"
            ),
            think_about=[
                'What\'s the difference between a webpage that just displays information and a webpage with a form?',
                'If the user runs your program and then just sits there and never types anything, what do you imagine your program is doing in that moment?',
            ],
            source_url='https://docs.python.org/3/library/functions.html#input',
        ),
    )

    # =========================================================================
    # SLIDE 7: Concept - How input() Works
    # =========================================================================
    deck.add_concept_slide(
        title='How input() Works',
        bullets=[
            "Pattern: variable_name = input('Prompt: ')",
            'The string inside the parens is the prompt, shown to the user.',
            'The user types something and hits Enter. Python collects what they typed.',
            'Whatever they typed comes back as a STRING. Always. Even if they typed digits.',
            "If you don't assign the return value to a variable, the answer is lost.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here's the syntax. Write the name of a variable, then equals, then the "
                "word input, then the prompt inside parens. Three parts: the bucket on the "
                "left, the assignment in the middle, the question on the right. When "
                "Python hits this line, it prints the prompt, pauses the program, waits "
                "for the user to type, waits for Enter, then drops whatever they typed "
                "into the variable you named. There's a crucial detail buried in that. "
                "Whatever they typed comes back as a STRING. A piece of text. Even if the "
                "user typed the digits one and four, what your variable holds is the "
                "string \"14\", not the number 14. That's two text characters sitting next "
                "to each other, not a number. If you want a number, you'll have to convert "
                "it, which is the very next slide. One more thing while we're here. If you "
                "call input() without assigning the result to a variable, the typed text "
                "just evaporates. Python collected it, but you didn't put it anywhere. So "
                "always assign. Always give the typed answer a home. The pattern is so "
                "common you'll write it dozens of times this semester. Think about this. "
                "If you wrote input('Your name: ') with no variable on the left, would "
                "the program still pause and wait for typing, or would it skip past?"
            ),
            key_terms=[
                ('Return value', 'The value a function hands back when it finishes running.'),
                ('Prompt', 'The text shown to the user before they type their input.'),
            ],
            think_about=[
                "If you wrote input('Your name: ') with no variable assignment, would the program still pause for typing?",
                "Why might Python's designers have made input() always return a string instead of trying to guess the type?",
            ],
            source_url='https://docs.python.org/3/library/functions.html#input',
        ),
    )

    # =========================================================================
    # SLIDE 8: Demo - Getting Information from the User
    # =========================================================================
    input_demo_code = """\
# Get the user's name, age, and income.
name = input('What is your name? ')
age = int(input('What is your age? '))
income = float(input('What is your income? '))

# Display the data.
print('Here is the data you entered:')
print('Name:', name)
print('Age:', age)
print('Income:', income)"""

    deck.add_demo_slide(
        title='Demo: Getting Information from the User',
        code=input_demo_code,
        png='slide06a_input_demo.png',
        notes=format_demo_notes(
            code=input_demo_code,
            instructor_notes=(
                "This is the BookEx input.py exercise students just typed. Mention that "
                "by name on screen so they connect this demo to their own work. Walk "
                "through line by line. The name line is plain string input. The age line "
                "wraps int() around input() to convert text digits into a usable "
                "integer. The income line wraps float() instead because income usually "
                "has cents (a decimal point). Then four prints at the bottom display "
                "what came in. Run the program. Use Maria for the name, 19 for the age, "
                "12500.00 for the income. Then point at the output: notice that 12500.00 "
                "comes back as 12500.0. Python's float type drops trailing zeros after "
                "the decimal. That's a real-world detail that surprises every student "
                "the first time. It's a quirk to notice and accept; the labs in this "
                "course don't apply formatting to clean it up."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 9: Output - What the User Sees
    # =========================================================================
    input_output_text = """\
What is your name? Maria
What is your age? 19
What is your income? 12500.00
Here is the data you entered:
Name: Maria
Age: 19
Income: 12500.0"""

    deck.add_output_slide(
        title='Output: What the User Sees',
        output_text=input_output_text,
        png='slide06b_input_demo_output.png',
        notes=format_output_notes(
            output_text=input_output_text,
            instructor_notes=(
                "Walk through what the user did and what the program produced. The "
                "first three lines are the input prompts; the user typed Maria, 19, "
                "and 12500.00. Then the program echoes back what it captured. Point at "
                "the last line, Income: 12500.0. The user typed 12500.00 but the "
                "program shows 12500.0. Python's float displayed it without the "
                "trailing zero. That's not wrong, it's how floats work. Just note the "
                "behavior and move on; the labs accept this display as-is."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: Concept - int(), a Translator Between Text and Numbers
    # =========================================================================
    deck.add_concept_slide(
        title='int(), a Translator Between Text and Numbers',
        bullets=[
            'input() always returns a string. Always.',
            "You can't do math on the string '14'. You CAN do math on the integer 14.",
            'int() converts a string of digits into an integer.',
            'Common pattern: wrap int() around an input() call so the result is a number.',
            "int('14') works. int('fourteen') crashes. We'll handle bad input in Module 2.",
        ],
        notes=format_concept_notes(
            video_script=(
                "A check from your boss has the amount written on it: a hundred dollars, "
                "in ink. You can look at the check. You can read the numbers. But you "
                "can't spend it. Until you take it to a bank and cash it, that hundred is "
                "just decoration. int() is the function that cashes the check. The bank "
                "takes a piece of paper that LOOKS like a number, and gives you back an "
                "actual usable number, the kind you can do math with. When input() hands "
                "you the string \"14\", that's the check. The digits are there, you can "
                "see them, but you can't multiply by them or subtract from them. You wrap "
                "int() around the input call, and what you get back is the real integer "
                "fourteen, ready for the rest of your program to use. The syntax looks "
                "like nesting. You write int(input('Roll the die: ')). Read that from the "
                "inside out. input() runs first, gets the string from the user, hands the "
                "string to int(), int() converts it, the integer lands in the variable on "
                "the left. One line, two functions, one variable holding the final number. "
                "There's a catch. If the user types fourteen as a word instead of as "
                "digits, int() can't make sense of it and the program crashes. We'll learn "
                "how to defend against that in Module 2. For now, expect the user to type "
                "digits. Think about this. Why didn't Python's designers just have input() "
                "return numbers when the user types numbers?"
            ),
            key_terms=[
                ('Type conversion', 'Changing a value from one type to another, like int("14") becoming 14.'),
                ('Integer', 'A whole number, positive, negative, or zero. No decimal part.'),
            ],
            think_about=[
                "Why didn't Python's designers have input() return a number when the user types digits?",
                'If the player types "twelve" instead of "12" and your code calls int() on it, what do you expect to happen?',
            ],
            source_url='https://docs.python.org/3/library/functions.html#int',
        ),
    )

    # =========================================================================
    # SLIDE 11: Concept - Why Programs Do Math
    # =========================================================================
    deck.add_concept_slide(
        title='Why Programs Do Math',
        bullets=[
            'The user gives you raw inputs. They want processed outputs.',
            'A weather app converts Celsius to Fahrenheit; a tip calculator turns a bill into a total.',
            'Arithmetic is how a program TRANSFORMS what came in into something more useful.',
            'Python uses the standard math operators you already know.',
            'Plus a few extras that do not show up in algebra, like integer division.',
        ],
        notes=format_concept_notes(
            video_script=(
                "Think about every useful program you've ever interacted with. A weather "
                "app takes a temperature reading from a sensor and converts it to whatever "
                "unit you prefer. A tip calculator takes a bill total and a percentage and "
                "gives you the tip and the new total. A grading program takes your scores "
                "and gives you the average. In every case, the user gave the program some "
                "raw inputs, and the program did some math, and then the program handed "
                "back something more useful than what came in. That's the whole pattern. "
                "Take inputs, transform them, produce outputs. The transformation step is "
                "where arithmetic lives. Python uses the same arithmetic operators you've "
                "seen in math class, mostly. Plus and minus, the star for multiply, the "
                "slash for divide. Those four will carry most of your work. There are a "
                "couple of Python-specific extras that don't show up in algebra. Double-"
                "slash for integer division, which divides and throws away the remainder. "
                "We'll see why that matters on the next slide. The big idea here isn't the "
                "operators themselves. The big idea is the shape of every useful program: "
                "in, transform, out. Almost everything you'll build this semester fits "
                "that shape. Think about this. What programs do you use every day that "
                "take simple inputs and give you back transformed outputs?"
            ),
            think_about=[
                'What programs do you use every day that take simple inputs and turn them into transformed outputs?',
                'If a program just printed its inputs back without changing them, why would you bother running it?',
            ],
            source_url='https://docs.python.org/3/tutorial/introduction.html#numbers',
        ),
    )

    # =========================================================================
    # SLIDE 12: Concept - How Arithmetic Works in Python
    # =========================================================================
    deck.add_concept_slide(
        title='How Arithmetic Works in Python',
        bullets=[
            '+ - * work the way you expect. / always returns a float, even when the result could be an integer.',
            '// is integer division. 20 // 3 is 6; the remainder is dropped.',
            'Python follows standard math precedence: * and / before + and -.',
            'Parentheses force order: (2 + 3) * 4 is 20, not 14.',
            'Store the result in a variable so you can use it later: miles = roll * 10.',
        ],
        notes=format_concept_notes(
            video_script=(
                "Five operators do most of the work in Chapter 2. Plus, minus, star for "
                "multiply, slash for divide, double-slash for integer division. The first "
                "three behave the way you expect from math class. Five plus three is "
                "eight. Five minus three is two. Five times three is fifteen. The "
                "divisions are where Python adds a small twist. The single slash, the "
                "regular divide, ALWAYS gives you back a number with a decimal point. So "
                "twenty divided by four is 5.0, not 5. That trailing zero matters when the "
                "program prints results to the user. Double slash is integer division, "
                "which drops the decimal entirely. Twenty floor-divide four is 5. Twenty "
                "floor-divide three is 6. The remainder gets thrown away. Use the regular "
                "slash when you want a precise answer. Use the double slash when you want "
                "a whole number of whatever you're counting. The other thing to watch for "
                "is order of operations. Python follows the same precedence you learned "
                "in school. Multiplication and division before addition and subtraction. "
                "So 2 + 3 * 4 is 14, not 20. If you want the addition to happen first, "
                "wrap it in parens: (2 + 3) * 4 is 20. When in doubt, put parens around "
                "the part you want first. Think about this. If a tip calculator computes "
                "the total bill with the line total + total * 0.20, did the developer get "
                "it right, or did they forget about precedence?"
            ),
            key_terms=[
                ('Operator', 'A symbol that does something to one or more values, like + or *.'),
                ('Float', 'A number with a decimal point, like 5.0 or 3.14.'),
                ('Operator precedence', 'The order Python uses when evaluating an expression with multiple operators.'),
            ],
            think_about=[
                'If a tip calculator uses total + total * 0.20, does it correctly compute the bill with tip? Or did the developer forget about precedence?',
                'When would you actually want // instead of / in real code? Can you think of an example?',
            ],
            source_url='https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations',
        ),
    )

    # =========================================================================
    # SLIDE 13: Demo - Simple Math with Variables
    # =========================================================================
    arithmetic_demo_code = """\
# Assign a value to the salary variable.
salary = 2500.0

# Assign a value to the bonus variable.
bonus = 1200.0

# Calculate the total pay by adding salary
# and bonus. Assign the result to pay.
pay = salary + bonus

# Display the pay.
print('Your pay is', pay)"""

    deck.add_demo_slide(
        title='Demo: Simple Math with Variables',
        code=arithmetic_demo_code,
        png='slide09a_arithmetic_demo.png',
        notes=format_demo_notes(
            code=arithmetic_demo_code,
            instructor_notes=(
                "This is the BookEx simple_math.py exercise. Walk through the four "
                "moving parts: store salary, store bonus, compute pay by adding them, "
                "print the result. Notice that all three variables are floats (2500.0, "
                "1200.0). Why floats and not just 2500? Because real money has cents. "
                "The decimal point is there to remind us this is a quantity that COULD "
                "have a fractional part, even when it doesn't. Now point at the line "
                "pay = salary + bonus. The right side gets evaluated first: Python "
                "computes 2500.0 + 1200.0 to get 3700.0, then assigns that result to "
                "pay. Two arrows: arithmetic produces a number, assignment stores the "
                "number. Run the program. Output is 'Your pay is 3700.0.' Worth "
                "highlighting that the final number has a trailing .0 because Python "
                "is showing the float as-is, the same situation we saw earlier with "
                "Income: 12500.0. Same quirk, same acceptance: notice, move on."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: Output - What the Math Produced
    # =========================================================================
    arithmetic_output_text = "Your pay is 3700.0"

    deck.add_output_slide(
        title='Output: What the Math Produced',
        output_text=arithmetic_output_text,
        png='slide09b_arithmetic_demo_output.png',
        notes=format_output_notes(
            output_text=arithmetic_output_text,
            instructor_notes=(
                "Short output, big lesson. Trace the math live: 2500.0 + 1200.0 = "
                "3700.0. The result is a float because both operands are floats. "
                "Python preserves the type. Then notice the .0 at the end. The program "
                "is correct, but the output reads weirdly: nobody talks about salary as "
                "3700 point zero dollars. That's just how Python shows floats by "
                "default. Acknowledge it, don't fix it; the labs accept this format."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 15: Concept - String Concatenation with +
    # =========================================================================
    deck.add_concept_slide(
        title='String Concatenation with +',
        bullets=[
            'The + operator works on strings, not just numbers.',
            "'Hello, ' + name glues the two strings together end-to-end.",
            'It does NOT add a space between them. You put the space in yourself.',
            "You can't + a string and a number. Python crashes with a TypeError.",
            'F-strings (next slide) handle this more cleanly. Concatenation is the older way.',
        ],
        notes=format_concept_notes(
            video_script=(
                "The plus sign in Python isn't just for numbers. It also works on strings, "
                "where it means \"stick these two strings together end to end.\" If you "
                "write 'Hello, ' + 'Maria', what you get back is the single string 'Hello, "
                "Maria'. The two pieces are now one piece. Watch the spaces. Concatenation "
                "does NOT automatically add a space between the strings. You have to put "
                "the space inside one of the strings yourself. Notice the trailing space "
                "inside the quotes after Hello, in that example. Without it you'd get "
                "'Hello,Maria', smashed together with no breathing room. Now here's the "
                "bear trap. Concatenation only works between strings and strings. If you "
                "write 'You rolled ' + 14, Python refuses. You'll get an error that says "
                "you can't concatenate a string and an integer. To make it work, you'd "
                "have to wrap the number in str() first to convert it to text. That's "
                "clunky. It's the main reason most modern Python code uses f-strings "
                "instead, which we'll meet on the next slide. So why am I teaching you "
                "concatenation at all? Because you'll see it in older code, in textbook "
                "examples, and in BookEx 2.8. It still works, it's still legal Python, "
                "but f-strings are usually cleaner. Think about this. Why might Python's "
                "designers have NOT made + automatically convert numbers to strings when "
                "you mix them?"
            ),
            key_terms=[
                ('Concatenation', 'Joining two strings together with + to make a longer string.'),
                ('TypeError', "Python's complaint when you try to use a value the wrong way for its type."),
            ],
            think_about=[
                "Why might Python's designers have NOT made + automatically convert numbers to strings when mixed?",
                "If you wrote 'Roll: ' + 14, what error would you guess Python gives you? Phrase it in your own words.",
            ],
            source_url='https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str',
        ),
    )

    # =========================================================================
    # SLIDE 16: Two-Column - Why F-Strings Exist
    # =========================================================================
    deck.add_two_column_slide(
        title='Why F-Strings Exist',
        left_label='F-STRINGS',
        left_bullets=[
            'Write a sentence with blanks; drop values into the blanks',
            'Handle type conversion automatically; no str() needed',
            'Read like English when said out loud',
            'Used in almost all modern Python code',
        ],
        right_label='CONCATENATION (THE OLD WAY)',
        right_bullets=[
            'Glue strings together with + and lots of quote marks',
            'Crashes if you try to + a string and a number',
            'Requires str() calls to mix in numbers, which gets clunky fast',
            'Reads like furniture assembly instructions, not a sentence',
        ],
        notes=format_concept_notes(
            video_script=(
                "Picture the Mad Libs game from elementary school. You have a sentence "
                "with blanks in it: \"The blank ran into the blank and yelled blank.\" "
                "You fill in noun, place, exclamation, and the sentence comes to life. "
                "F-strings are Python's Mad Libs. You write a normal-looking sentence in "
                "quotes, but in the spots where you want a value to appear, you put curly "
                "braces with a variable name inside. Python fills in the blanks at "
                "runtime, using whatever's currently in those variables. So instead of "
                "writing 'Hello, ' + player_name + '. You rolled ' + str(roll) + '.', "
                "with all those plus signs and quote marks and a stray str() thrown in to "
                "convert the number, you write f'Hello, {player_name}. You rolled "
                "{roll}.'. One string, two blanks, all the values dropped in. The "
                "reading-out-loud test is what sells me on f-strings. Read the f-string "
                "version aloud. It sounds like a sentence. Read the concatenation version "
                "aloud. It sounds like instructions for assembling furniture. Both produce "
                "the same output, but one of them takes thirty seconds to read and the "
                "other takes three. There's another upside. F-strings handle the type "
                "conversion problem from the last slide automatically. You can drop a "
                "number, a string, or even an expression inside the braces, and Python "
                "figures it out. No str() calls. Think about this. If you had to debug "
                "someone else's code, which version would you rather see?"
            ),
            think_about=[
                "If you had to debug someone else's code and find a problem, would you rather see the f-string or the concatenation version?",
                'Where else in software, websites, or apps have you seen "fill in the blanks" templates?',
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals',
        ),
    )

    # =========================================================================
    # SLIDE 17: Concept - How F-Strings Work
    # =========================================================================
    deck.add_concept_slide(
        title='How F-Strings Work',
        bullets=[
            "Put a lowercase f directly before the opening quote: f'Hello, {name}'.",
            'Inside the string, wrap any variable name in curly braces and Python substitutes it.',
            'You can put expressions inside the braces too: {roll * 10} is legal.',
            'F-strings produce a regular string. Pass them to print(), store them, anywhere strings are valid.',
            "Forgetting the f is the most common bug. Python won't crash; the braces just print literally.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Three pieces. The f, the quotes, the braces. The lowercase letter f sits "
                "directly before the opening quote, with no space between them. That's "
                "what tells Python \"this string has values to substitute.\" Inside the "
                "quotes, you write whatever you want the sentence to say. Anywhere you "
                "want a value to appear, you wrap a variable name in curly braces. Python "
                "evaluates whatever's in the braces and drops the result in. That's it. "
                "There's a nice little surprise. The thing in the braces doesn't have to "
                "be just a variable name. You can put an expression in there too. f'You "
                "rolled {roll}, which is {roll * 10} miles.'. Python computes the "
                "multiplication on the spot and inserts the answer. You can also call "
                "functions inside the braces, do arithmetic, do anything that produces a "
                "value. Most of the time you'll just use bare variable names, but the "
                "flexibility is there if you need it. The most common bug with f-strings "
                "is forgetting the f. If you write 'Hello, {name}' without the f, Python "
                "doesn't crash. It just prints the string literally, braces and all, and "
                "the user sees the curly braces on screen. The fix is to add the f. I've "
                "debugged that one many times. Think about this. If roll is 14, what does "
                "f'You rolled {roll * 10}' print to the screen?"
            ),
            key_terms=[
                ('F-string', 'A string literal prefixed with the letter f that lets you embed expressions in curly braces.'),
                ('Expression', 'Any piece of code that produces a value, like roll, roll * 10, or 2 + 2.'),
            ],
            think_about=[
                "If roll is 14, what does f'You rolled {roll * 10}' print to the screen?",
                "What happens if you forget the f and write just 'Hello, {name}'? What does the user see?",
            ],
            source_url='https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals',
        ),
    )

    # =========================================================================
    # SLIDE 18: Demo - An F-String with No Formatting
    # =========================================================================
    fstring_demo_code = """\
# This program demonstrates how a floating-point
# number is displayed with no formatting.
amount_due = 5000.0
monthly_payment = amount_due / 12.0
print(f'The monthly payment is {monthly_payment}.')"""

    deck.add_demo_slide(
        title='Demo: An F-String with No Formatting',
        code=fstring_demo_code,
        png='slide12a_fstring_demo.png',
        notes=format_demo_notes(
            code=fstring_demo_code,
            instructor_notes=(
                "This is the BookEx f_string_no_formatting.py exercise. Walk through "
                "the four lines. Comment for context. Set amount_due to 5000. Compute "
                "monthly_payment by dividing by 12. Display with an f-string. The "
                "{monthly_payment} inside the curly braces is the substitution slot: "
                "Python evaluates the expression and inserts the result into the "
                "string. Run the program. Pause when the output appears. Let viewers "
                "see how many decimal places come out. That's a real Python quirk "
                "students will run into anywhere they do division on floats. Don't "
                "promise a fix here; just let them sit with it."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 19: Output - The Monthly Payment, Unformatted
    # =========================================================================
    fstring_output_text = "The monthly payment is 416.6666666666667."

    deck.add_output_slide(
        title='Output: The Monthly Payment, Unformatted',
        output_text=fstring_output_text,
        png='slide12b_fstring_demo_output.png',
        notes=format_output_notes(
            output_text=fstring_output_text,
            instructor_notes=(
                "Stop and let the output sit on screen. Five thousand divided by twelve "
                "is mathematically 416.66666... with a six that repeats forever. Python "
                "doesn't repeat forever, but it does show thirteen digits of decimal. "
                "That's just how Python displays floats by default. In a real-world "
                "program you'd usually round it for display, and your textbook covers "
                "that technique in BookEx (f_string_rounding.py). We don't apply it in "
                "the labs this semester, so just notice the quirk, hold it in your "
                "mental model, and keep moving."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 22: Overview - What You Can Build Now
    # =========================================================================
    deck.add_overview_slide(
        title='What You Can Build Now',
        section1_label='WHAT YOU CAN DO NOW',
        section1_body=(
            "You can write a program that opens with a banner, asks the user for their "
            "name, asks for a number, converts that number from text to an integer, "
            "multiplies it by something useful, subtracts to find what's left, and "
            "displays a clean, formatted report at the end. That is a complete, working "
            "program. Not a toy."
        ),
        section2_body=(
            "The shape you just learned (in, transform, out, with banners and a clean "
            "report) is the shape of most useful software. Bigger programs do more steps, "
            "take more inputs, produce more outputs. The shape is the same. If you're "
            "wondering whether you really know how to program yet, the answer is yes. "
            "You're not done learning, but you've cleared the entire first chapter of "
            "the toolkit."
        ),
        section3_label="WHAT'S NEXT",
        section3_body=(
            "BookEx Chapter 2 gives you ten small programs that use these exact "
            "techniques, one or two at a time. Lab 1.1 then puts several of them "
            "together into a single working program. Next week in U2 we add the ability "
            "for the program to make DECISIONS, which is where things really start to "
            "get interesting."
        ),
        notes=format_concept_notes(
            video_script=(
                "Stop and notice what you can do now that you couldn't do an hour ago. "
                "You can write a program that opens with a banner. Asks the user for "
                "their name. Asks them for a number. Converts that number from text to "
                "an integer. Multiplies it by something useful. Subtracts to find what's "
                "left. Displays a clean, formatted report at the end. That's a complete, "
                "working program. It's not a toy. The same shape, in, transform, out, "
                "with banners and a clean report, is the shape of most useful software. "
                "Bigger programs do more steps. They have more inputs. They produce more "
                "outputs. The shape is the same. So if you're sitting there wondering "
                "whether you \"really\" know how to program yet, here's the answer. Yes. "
                "You're not done learning, but you've cleared the entire first chapter "
                "of the toolkit, and what you have already qualifies as programming. "
                "BookEx Chapter 2 is going to ask you to write ten small programs using "
                "these exact techniques. Each one is short. Each one is a low-stakes "
                "excuse to type the techniques out yourself, because typing them is what "
                "makes them stick. Lab 1.1 will then ask you to put several of these "
                "techniques together into a single working program. You'll come out the "
                "other end knowing how the toolkit feels in your hands. Next week, in "
                "U2, we add the ability for the program to make DECISIONS, which is "
                "where things get really interesting. Think about this. Out of "
                "everything you saw today, what felt the easiest, and what felt the "
                "most foreign?"
            ),
            think_about=[
                'Out of everything in this chapter, what felt the easiest, and what felt the most foreign?',
                'What kind of program, real or invented, would you actually WANT to build with what you know now?',
            ],
        ),
    )

    # =========================================================================
    # Save
    # =========================================================================
    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
