"""
build_m2_u2.py - M2-U2 ("Functions and Randomness") slide deck.

Module 2, Unit 2 | Chapter 5: Functions, Parameters, Return Values, and Random
Pairs with: Lab 2.2, Texas Has Other Plans (ENHANCE)

Scope (from lab-2-2.json keyConceptsText):
  Chapter 5 Sections: 5.5 (Parameters), 5.8 (Return Values),
                      5.9 (Modules and Random)

  Foundational dependency: def (students have used def main() since
  Lab 1.1; this week they write more functions of their own).

Pedagogy notes:
  - Build-your-own-module (function_library.py) is the lab's big
    structural new thing. The BookEx demos cover def/parameters/return
    via verbatim textbook code; the function_library.py pattern needs
    a custom demo since BookEx does not teach "write your own importable
    module."
  - Sentinel loops are out of scope (deferred to Lab 2.3 / M2-L3) so
    dice.py is trimmed to remove its outer while-again loop.

USAGE
-----
    python3 slides/m2_u2/build_m2_u2.py
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
OUTPUT_PPTX = '/home/claude/IS2053_2026-05-25_M2-U2_Deck.pptx'
PNG_OUT = '/home/claude/m2_u2_pngs'
WORK_DIR = '/tmp/build_m2_u2'


def main():
    deck = DeckBuilder(png_out=PNG_OUT, work=WORK_DIR)

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    deck.add_title_slide(
        main_title='Functions and Randomness',
        subtitle='IS2053 Programming I  \u2022  Module 2  \u2022  Unit 2',
        notes=format_title_notes(
            deck_id='M2-U2',
            deck_title='Functions and Randomness',
            opening_line=(
                '"Welcome to Module 2, Unit 2. Last unit we taught your program '
                "how to repeat. This unit we're going to teach you how to package "
                "your code into named, reusable chunks called functions, and how to "
                'pull a little randomness into your programs. Let\'s get going."'
            ),
        ),
    )

    # =========================================================================
    # SLIDE 2: Narrative intro
    # =========================================================================
    deck.add_narrative_slide(
        title='Functions and Randomness',
        section_label='THE BIG IDEA',
        bold_oneliner='Stop copy-pasting. Start naming. Build a toolbox you carry with you for the rest of the semester.',
        body=(
            "Up to now, every line of code in every lab has lived inside one big def main(). That works for "
            "small programs. It stops working the moment you need the same idea in two places. Chapter 5 "
            "gives you the tool that fixes that: functions. A function is a named chunk of code you can "
            "define once and call from anywhere. Then Chapter 5 hands you something that real programs need "
            "constantly, randomness, in the form of the random module. The biggest thing this week, the "
            "thing that carries you through the rest of the course, is that you are going to build your own "
            "module called function_library.py. You will import it the same way you import random. From "
            "Module 2 forward, every lab uses it. It is the toolbox you are building for the rest of the "
            "semester."
        ),
        notes=format_concept_notes(
            video_script=(
                "Think about Lab 2.1 for a second. By the end of it, your code probably had a chunk of "
                "lines that asked the user a question, checked their answer, asked again if it was wrong. "
                "Now imagine you needed to do that three more times for three different questions. Are you "
                "going to copy-paste those lines four times? Of course not. You are going to give the chunk "
                "a name, like get_valid_int, and then just CALL it by name wherever you need it. That is "
                "what a function is. A named chunk of code you write once and call by name as often as you "
                "want. This week you start writing your own. Three of them in Lab 2.2, two more in Lab 2.3, "
                "and then a bunch more across the rest of the semester. All of them go in a single file "
                "called function_library.py that you will literally carry forward into every remaining lab. "
                "By the end of the course this file is a real toolbox. The other thing Chapter 5 brings is "
                "the random module. It is one of the standard tools that comes with Python. You import it "
                "and you immediately have a coin flip, a dice roll, a random integer between any two "
                "numbers you want. Lab 2.2 uses all three of those for the game mechanics."
            ),
            think_about=[
                "Think of three places in your Lab 2.1 code where the same idea appeared more than once. What would a good name be for each of those chunks?",
                "If you imported a coin_flip function someone else wrote, would your code work exactly the same as if you wrote it yourself? Why?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#defining-functions',
        ),
    )

    # =========================================================================
    # SLIDE 3: Concept - Why Functions
    # =========================================================================
    deck.add_concept_slide(
        title='Why Functions',
        bullets=[
            "Don't repeat yourself. If you have copied a chunk of code, that is a function trying to be born.",
            "A function gives a chunk of code a NAME. The name describes what it does in plain English.",
            "Once named, you call it from anywhere. The same idea is now reusable without copy-paste.",
            "Functions make code readable. read 'flip_coin()' once and you instantly know what is happening.",
            "Functions make code testable. You can poke at one function in isolation instead of the whole program.",
        ],
        notes=format_concept_notes(
            video_script=(
                "There is a software engineering principle called Don't Repeat Yourself, often shortened to "
                "DRY. The idea is simple. If you have the same chunk of code in two places, that is a problem "
                "waiting to happen. Suppose you fix a bug in one copy and forget to fix the other. Suppose "
                "you change the behavior in one place and the other place silently keeps doing the old thing. "
                "Functions are the fix. You write the chunk once, you give it a name, and from then on you "
                "just call it by name wherever you need it. Fix the function once, fixed everywhere. That is "
                "reason number one. Reason number two is that names communicate intent. If I show you a "
                "twelve-line block of code that loops and asks for input and validates and re-asks, your eyes "
                "have to read the whole block before you know what it does. But if I just write "
                "get_valid_int, you know what it does in zero seconds. Code with good function names reads "
                "almost like English. Reason number three, you can test a function on its own. Lab 2.2 asks "
                "you to write three small functions. You can write each one and run it by itself before you "
                "wire it into the main game. That isolation is gold when you are debugging."
            ),
            key_terms=[
                ('DRY (Don\'t Repeat Yourself)', 'A principle of software design: every piece of knowledge should live in one place in the code.'),
                ('Function', 'A named chunk of code that can be called by its name. The named-and-callable part is what makes it a function.'),
            ],
            think_about=[
                "Look at any program longer than 30 lines you have ever written. Pick three lines that could become a function. What would you name it?",
                "Why is 'get_valid_int' a better name than 'do_thing' or 'helper1'?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#defining-functions',
        ),
    )

    # =========================================================================
    # SLIDE 4: Concept - Defining a Function (def)
    # =========================================================================
    deck.add_concept_slide(
        title='Defining a Function',
        bullets=[
            "You have used def main(): in every lab. That IS function syntax. You already know the shape.",
            "Shape: def name(): then an indented block. The indented block is the body of the function.",
            "Function names follow the same rules as variables: lowercase with underscores (snake_case).",
            "Define functions ABOVE def main() in the file. Call them FROM inside main().",
            "A definition does not RUN the function. It just teaches Python what to do when you call it.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Good news. You already know the syntax for defining a function, because you have been "
                "writing def main() since Lab 1.1. The keyword def, the name, parentheses, a colon, then "
                "an indented block. That is it. That is the syntax. The only difference this week is that "
                "you are going to write more of them, with names you choose. The convention for function "
                "names is exactly the same as for variables. Lowercase letters and underscores, like "
                "flip_coin, roll_d20, calculate_total. The auto-grader will check for this. Now, two "
                "important structural rules. One, all your function definitions go ABOVE def main in the "
                "file. Python reads top to bottom, so it has to see the function definition before main "
                "tries to call it. Two, and this is the subtle one, defining a function does not run it. "
                "When Python hits a def line, it just memorizes that, hey, there is a function called X "
                "with this body. The body does not actually execute until someone CALLS the function with "
                "X parentheses. Definition is the recipe. Call is making the meal. Two separate things."
            ),
            key_terms=[
                ('def', 'The Python keyword that starts a function definition.'),
                ('Call', 'To execute a function. You call a function by writing its name followed by parentheses, like flip_coin().'),
            ],
            think_about=[
                "If you put def main() at the TOP of your file but called main() from the BOTTOM, would the program still work?",
                "If you write a function but never call it, what happens when you run the program?",
            ],
            source_url='https://docs.python.org/3/reference/compound_stmts.html#function-definitions',
        ),
    )

    # =========================================================================
    # SLIDE 5: Concept - Parameters: Passing Data In
    # =========================================================================
    deck.add_concept_slide(
        title='Parameters: Passing Data In',
        bullets=[
            "Parameters are names in the parentheses of the def line. They receive values when the function is called.",
            "Arguments are the actual values you pass when you call: my_func(5, 10) sends 5 and 10.",
            "Inside the function, parameters work like normal variables. They hold whatever was passed in.",
            "Order matters. The first argument goes into the first parameter, second into the second.",
            "A function can have zero, one, or many parameters. Pick what makes sense for the job.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Parameters are how you give a function the information it needs to do its job. Think of "
                "a function like a coffee machine. The coffee machine does a fixed thing, but YOU tell it "
                "what size cup and what strength. Those are parameters. When you define the function, you "
                "put parameter names in the parentheses after the function name. Inside the function body, "
                "you use those names like any other variable. When you CALL the function, you pass actual "
                "values in those same positions. Those values are called arguments. So def show_sum(num1, "
                "num2), that is parameters. show_sum(12, 45), that is arguments. 12 lands in num1, 45 "
                "lands in num2. Order matters. If you wrote show_sum(45, 12), num1 would be 45 and num2 "
                "would be 12. For most of the functions we write, order matters a lot. The check_percentage "
                "function you will write in Lab 2.2 takes one parameter, the percent chance. flip_coin "
                "takes zero parameters. roll_d20 takes zero parameters. Most early functions are like that. "
                "Pick the smallest number of parameters that gets the job done."
            ),
            key_terms=[
                ('Parameter', 'A name in the function definition that receives a value when the function is called.'),
                ('Argument', 'The actual value you pass into a function call.'),
            ],
            think_about=[
                "If you wrote a function called calculate_tip(bill, percent), what is the parameter and what is the argument when you call it with calculate_tip(50, 20)?",
                "When would a function need zero parameters? Can you think of one we will write in Lab 2.2 that needs none?",
            ],
            source_url='https://docs.python.org/3/tutorial/controlflow.html#defining-functions',
        ),
    )

    # =========================================================================
    # SLIDE 6: Demo - multiple_args.py (BookEx 5-8)
    # =========================================================================
    multiple_args_code = '''# A function with two parameters and a return value.

def main():
    print('The sum of 12 and 45 is')
    total = show_sum(12, 45)
    print(total)

# show_sum accepts two arguments and returns their sum.
def show_sum(num1, num2):
    result = num1 + num2
    return result

main()
'''
    deck.add_demo_slide(
        title='Demo: multiple_args.py',
        code=multiple_args_code,
        png='slide06_multiple_args_demo.png',
        notes=format_demo_notes(
            code=multiple_args_code,
            instructor_notes=(
                "Source: BookEx Chapter 5, program 5-8 (multiple_args.py). Comments trimmed for screen "
                "space; logic is unchanged. Walk through this in order. Python reads it top to bottom. "
                "It sees def main, memorizes it. Sees def show_sum, memorizes it. Then it hits the bare "
                "main() at the bottom, which is the actual call that starts everything. main runs, prints "
                "the heading line, then on line 6 calls show_sum(12, 45). At that moment, control jumps "
                "into show_sum. num1 becomes 12, num2 becomes 45. result becomes 57. The return statement "
                "sends 57 back to wherever the call happened, which means total now holds 57. Control "
                "returns to main, the next line prints total. Notice: the textbook has not yet introduced "
                "the if __name__ guard at this point; that comes in the next BookEx file. We'll start "
                "using __name__ in the lab walkthroughs."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 7: Output - multiple_args.py
    # =========================================================================
    multiple_args_output = '''The sum of 12 and 45 is
57
'''
    deck.add_output_slide(
        title='Output: multiple_args.py',
        output_text=multiple_args_output,
        png='slide07_multiple_args_output.png',
        notes=format_output_notes(
            output_text=multiple_args_output,
            instructor_notes=(
                "Two lines of output, one from each print in main. The first print fires before show_sum "
                "is called. Then show_sum runs invisibly (it does not print anything itself), returns 57, "
                "and the second print displays that returned value. This is the smallest possible demo of "
                "the round-trip pattern: data goes IN through parameters, data comes OUT through return. "
                "Trace the value 12: it starts in main's call as an argument, lands in num1 inside "
                "show_sum, gets added to num2, becomes part of result, gets returned, lands in total, "
                "gets printed. That is the entire lifecycle."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 8: Concept - Return Values: Passing Data Out
    # =========================================================================
    deck.add_concept_slide(
        title='Return Values: Passing Data Out',
        bullets=[
            "The return statement sends a value BACK to whoever called the function.",
            "When a function returns, it stops executing. Lines below the return do not run.",
            "Catch the return value with an assignment: result = my_function(args).",
            "A function without a return statement returns None. That is Python's 'no value' object.",
            "Use return when you need a value to use later. Use print when you just want to show text.",
        ],
        notes=format_concept_notes(
            video_script=(
                "Parameters get data IN. Return values get data OUT. The return statement is the way a "
                "function hands a value back to the code that called it. The pattern is simple. Inside the "
                "function body, you write return followed by whatever value you want to send back. The very "
                "instant Python hits a return, the function stops dead in its tracks and the value goes "
                "back to the caller. Any lines after the return in the function body do not run. That is "
                "important to internalize, because you will sometimes write a return inside an if branch "
                "and forget that it ends the function. On the caller's side, you usually catch the return "
                "value with an assignment. result equals my function paren args paren. Then result holds "
                "whatever was returned. Now, a key distinction. Return is not print. Return sends a value "
                "back to your code so your code can use it. Print sends text to the screen so a human can "
                "read it. When in doubt, ask yourself: does some OTHER piece of code need this value? If "
                "yes, return. Does some HUMAN need to see it on the screen? If yes, print. Sometimes both, "
                "and that's fine; just understand they do different jobs."
            ),
            key_terms=[
                ('return', 'A statement that ends a function and sends a value back to the caller.'),
                ('None', 'Python\'s special "no value" object. A function with no return statement returns None.'),
            ],
            think_about=[
                "If a function has the line `return 5` followed by the line `print('hi')`, does 'hi' ever get printed? Why or why not?",
                "When you call random.randint(1, 6), where does the random number GO? What lets you store it in a variable?",
            ],
            source_url='https://docs.python.org/3/reference/simple_stmts.html#the-return-statement',
        ),
    )

    # =========================================================================
    # SLIDE 9: Demo - rectangle2.py (BookEx 5-32)
    # =========================================================================
    rectangle_code = '''def area(width, length):
    return width * length

def perimeter(width, length):
    return 2 * (width + length)

def main():
    width = float(input("Enter the width: "))
    length = float(input("Enter the length: "))
    print('The area is', area(width, length))
    print('The perimeter is', perimeter(width, length))

if __name__ == '__main__':
    main()
'''
    deck.add_demo_slide(
        title='Demo: rectangle2.py',
        code=rectangle_code,
        png='slide09_rectangle_demo.png',
        notes=format_demo_notes(
            code=rectangle_code,
            instructor_notes=(
                "Source: BookEx Chapter 5, program 5-32 (rectangle2.py). Comments trimmed; logic is the "
                "textbook's. Two things to highlight. ONE: notice the return values are used INLINE inside "
                "the print statements. print('The area is', area(width, length)) calls area, gets its "
                "return value, hands that value straight to print. No intermediate variable needed. That "
                "is a real pattern you will use constantly. TWO: this is your first formal look at "
                "if __name__ == '__main__'. We have used it in lab templates already; this is the "
                "explanation. It means: only run main() if this file is the program being executed "
                "directly. If someone imports this file as a module, do not run main automatically. This "
                "is the guard that makes a file safely importable. function_library.py will NOT have a "
                "main(), but the lab files always will. Same idea."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 10: Output - rectangle2.py
    # =========================================================================
    rectangle_output = '''Enter the width: 4
Enter the length: 7
The area is 28.0
The perimeter is 22.0
'''
    deck.add_output_slide(
        title='Output: rectangle2.py',
        output_text=rectangle_output,
        png='slide10_rectangle_output.png',
        notes=format_output_notes(
            output_text=rectangle_output,
            instructor_notes=(
                "Trace through with these inputs. width is 4.0, length is 7.0. First print line: calls "
                "area(4.0, 7.0), which returns 28.0, and print displays it next to the label. Second "
                "print line: calls perimeter(4.0, 7.0), which returns 2 * 11.0 = 22.0, and print displays "
                "it. Two function calls, two return values, two display lines. The point of this demo is "
                "to make the round-trip pattern feel routine. Define, call, return, use. That is the loop "
                "your code will run a hundred times this semester."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 11: Concept - The random Module
    # =========================================================================
    deck.add_concept_slide(
        title='The random Module',
        bullets=[
            "random is a module that ships with Python. You get it for free by writing: import random",
            "After import, call functions with the dotted name: random.randint(a, b).",
            "random.randint(a, b) returns a random integer from a to b, BOTH ends included.",
            "random.randint(1, 6) is a die roll. random.randint(0, 1) is a coin flip. random.randint(1, 100) is a percent roll.",
            "Each call gives you a fresh value. Two calls in a row will usually give different results.",
        ],
        notes=format_concept_notes(
            video_script=(
                "The random module is one of the standard tools that comes pre-installed with Python. "
                "You do not have to install it, you just write import random at the top of your file and "
                "now you have access to all of its functions. The one you will use almost exclusively this "
                "semester is randint. Random dot randint, paren, low, high, paren. It gives you back a "
                "random integer somewhere in that range. The important thing to memorize: both endpoints "
                "are inclusive. randint(1, 6) can return 1, 2, 3, 4, 5, or 6. randint(0, 1) can return 0 "
                "or 1. randint(1, 100) can return anything from 1 to 100 including the 1 and the 100. "
                "This is different from range, which excludes the top end. Easy to confuse, so anchor it "
                "early. For Lab 2.2 you will use randint three different ways. randint(0, 1) for the "
                "coin flip in flip_coin. randint(1, 20) for the dice in roll_d20. randint(1, 100) for the "
                "percentage check in check_percentage. Same function, different ranges, different "
                "purposes."
            ),
            key_terms=[
                ('Module', 'A file of Python code you can import. The standard library has many; you can also write your own.'),
                ('random.randint(a, b)', 'Returns a random integer between a and b, inclusive of BOTH endpoints.'),
            ],
            think_about=[
                "How would you call random.randint to simulate flipping two coins, where each flip is 1 or 0?",
                "If random.randint(1, 100) gave you the same number every time, how would you debug it?",
            ],
            source_url='https://docs.python.org/3/library/random.html#random.randint',
        ),
    )

    # =========================================================================
    # SLIDE 12: Demo - dice.py (BookEx 5-21, trimmed)
    # =========================================================================
    dice_code = '''# Simulating dice rolls with random.randint.
import random

# Constants for the minimum and maximum values on a die.
MIN = 1
MAX = 6


def main():
    print('Rolling two dice...')
    print(random.randint(MIN, MAX))
    print(random.randint(MIN, MAX))


main()
'''
    deck.add_demo_slide(
        title='Demo: dice.py',
        code=dice_code,
        png='slide12_dice_demo.png',
        notes=format_demo_notes(
            code=dice_code,
            instructor_notes=(
                "Source: BookEx Chapter 5, program 5-21 (dice.py). The textbook version wraps this in a "
                "sentinel-controlled while loop ('Roll again? y for yes'), which is Chapter 4.5 territory "
                "that we have not covered yet. Trimmed to just the random.randint calls so the demo "
                "focuses on the module-import pattern without dragging in a loop concept. Walk it line by "
                "line: import random is at the top, the module is now available. Two constants for the "
                "die range, named so the magic numbers do not have to live inside the call. Inside main, "
                "two calls to random.randint, each returning an independent random number 1 through 6. "
                "Two calls, two different rolls. Each call is a fresh draw."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 13: Output - dice.py
    # =========================================================================
    dice_output = '''Rolling two dice...
4
2
'''
    deck.add_output_slide(
        title='Output: dice.py',
        output_text=dice_output,
        png='slide13_dice_output.png',
        notes=format_output_notes(
            output_text=dice_output,
            instructor_notes=(
                "Three lines of output. The heading, then two random rolls. The numbers shown here are "
                "just one possible run; the next run will give different numbers. That is the point. "
                "Mention that for the lab, CodeGrade uses a deterministic random fixture so the random "
                "values are predictable during automated testing. The student does not see the fixture; "
                "from their seat it looks like normal random. We are not going to dig into the testing "
                "harness here, but if a student is curious in office hours that is a fun thread to pull."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 14: Concept - Build Your Own Module
    # =========================================================================
    deck.add_concept_slide(
        title='Build Your Own Module: function_library.py',
        bullets=[
            "A module is just a Python file. random is a module. Your own .py files can be modules too.",
            "function_library.py is the module you create this week. You will carry it forward all semester.",
            "Put functions you want to reuse inside it. Same def syntax as anything else.",
            "Other files import it the same way as random: import function_library at the top.",
            "Call functions in it with dotted names: function_library.flip_coin(), function_library.roll_d20().",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here is the structural idea that makes the rest of the course click. A module is just a "
                "Python file. That is literally the whole definition. random is a module because someone "
                "wrote a file called random.py. The math module is a file called math.py. And you are "
                "about to make a module called function_library.py the same way. You create a file, you "
                "put def lines and function bodies in it, you save it next to your lab file. That's it. "
                "It is a module now. To use it in your lab file, you import it the same way as random. "
                "import function_library at the top, then call its functions with the dotted name. "
                "function_library.flip_coin parens. function_library.roll_d20 parens. Same shape as "
                "random.randint, because it's the same pattern. Why are we doing this instead of just "
                "putting all the helper functions directly in lab-2-2.py? Two reasons. One, you are going "
                "to want flip_coin in Lab 2.3 and Lab 4.2 and Lab 5.1. If it lives in function_library.py, "
                "you just import the library and you have it. If it lives inside lab-2-2.py, you would "
                "have to copy it forward every time. Two, this is how real software is organized. Library "
                "code in one file, application code in another."
            ),
            key_terms=[
                ('Module', 'A Python file. Both standard-library files (like random.py) and files you write can be modules.'),
                ('import', 'A statement that loads a module so you can use its functions. Goes at the top of the file.'),
            ],
            think_about=[
                "If you wrote a function in lab-2-2.py and a different function with the SAME name in function_library.py, which one would Python use?",
                "When you import a module, the module's code runs ONCE at the import. If function_library.py had a print at the top level, when would that print fire?",
            ],
            source_url='https://docs.python.org/3/tutorial/modules.html',
        ),
    )

    # =========================================================================
    # SLIDE 15: Demo - function_library.py
    # =========================================================================
    library_code = '''# function_library.py - YOUR reusable module.
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
        title='Demo: function_library.py',
        code=library_code,
        png='slide15_library_demo.png',
        notes=format_demo_notes(
            code=library_code,
            instructor_notes=(
                "This is what the contents of function_library.py looks like after you write flip_coin. "
                "Three things to point out. ONE: function_library.py imports random itself. Modules can "
                "import other modules. The library needs random to do its job, so it imports random at "
                "the top. TWO: the function uses what students already know - def, return, if-else, "
                "random.randint. There is nothing genuinely new here EXCEPT the file it lives in. THREE: "
                "no def main() and no if __name__ guard. This file is not meant to be run on its own. "
                "It exists to be imported. That is the difference between a library file and an "
                "application file. Lab 2.2 has two files: function_library.py (the library, no main) "
                "and lab-2-2.py (the application, has main, imports the library)."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 16: Demo - Using the Library
    # =========================================================================
    using_code = '''# lab-2-2.py - YOUR main game file.
import function_library


def main():
    # Call functions with the dotted name.
    coin = function_library.flip_coin()
    print(f'Coin came up: {coin}')

    # Each call is a fresh random result.
    coin2 = function_library.flip_coin()
    print(f'Second flip: {coin2}')


main()
'''
    deck.add_demo_slide(
        title='Demo: Importing and Using It',
        code=using_code,
        png='slide16_using_demo.png',
        notes=format_demo_notes(
            code=using_code,
            instructor_notes=(
                "This is what your lab file looks like once it can use the library. Note the import line: "
                "import function_library. No dot, no .py extension, just the bare module name. Then "
                "calls use the dotted name, just like random.randint. function_library.flip_coin parens. "
                "Two calls in a row. Each one is an independent random result, because each call invokes "
                "flip_coin fresh, which calls random.randint fresh, which gives a fresh value. By the end "
                "of Lab 2.2, your lab-2-2.py file will import BOTH function_library AND random directly, "
                "because the main game uses random.randint(1, n) to pick which hazard happens. Two "
                "imports at the top of the file is normal and expected."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 17: Output - Using the Library
    # =========================================================================
    using_output = '''Coin came up: HEADS
Second flip: TAILS
'''
    deck.add_output_slide(
        title='Output: Importing and Using It',
        output_text=using_output,
        png='slide17_using_output.png',
        notes=format_output_notes(
            output_text=using_output,
            instructor_notes=(
                "Two lines. The first flip returned HEADS, the second flip returned TAILS. The pattern: "
                "from outside the library, you call flip_coin and you get either of two strings back. "
                "You do not care HOW it picks. You do not have to remember that it uses random.randint(0, 1) "
                "internally. The function hides that detail. That is called abstraction. When you import "
                "random.randint, you do not know how it generates the random number either; you just call "
                "it and trust the return value. Your function_library is doing the same thing for the "
                "people who use it later, including you."
            ),
        ),
    )

    # =========================================================================
    # SLIDE 18: Forward link - Lab 2.2 preview
    # =========================================================================
    deck.add_concept_slide(
        title='What You Can Build Now: Lab 2.2',
        bullets=[
            "Create function_library.py with three functions: flip_coin(), roll_d20(), check_percentage(percent).",
            "All three use random.randint with different ranges. Each returns a value (string, int, or bool).",
            "Update lab-2-2.py to import function_library AND random. Bring forward your Lab 2.1 code.",
            "Replace fixed MILES_PER_TURN with D20 rolls: roll_d20() * MILES_MULTIPLIER (= 10).",
            "Add the Destination Gate (coin flip decides if you get your pick) and hazards (30% chance per turn).",
        ],
        notes=format_concept_notes(
            video_script=(
                "Here is what Lab 2.2 asks you to do. Step one, create function_library.py from scratch. "
                "Three functions go in it. flip_coin returns either the string HEADS or the string TAILS. "
                "Implementation: random.randint(0, 1), then map 1 to HEADS and 0 to TAILS. roll_d20 "
                "returns a random integer 1 through 20, with the constants D20_MIN and D20_MAX at the top "
                "of the file. check_percentage takes a parameter called percent and returns True or False "
                "based on whether a random 1-to-100 roll is less than or equal to that percent. Step two, "
                "carry your Lab 2.1 code forward into lab-2-2.py, then make some changes. Import "
                "function_library at the top. Import random too, because the main game uses random.randint "
                "directly to pick which hazard happens. Replace the fixed 50-mile-per-turn travel with a "
                "D20 roll times MILES_MULTIPLIER (which is 10). So a roll of 15 is 150 miles. Add the "
                "Destination Gate, which is a coin flip after the user picks. HEADS means they get what "
                "they picked; TAILS means Texas redirects them somewhere else. Add hazards, which is a "
                "30% chance per turn that something happens (Buc-ee's, armadillo, speed trap), and a coin "
                "flip determines whether the hazard escapes you. Get the library file working first, then "
                "wire it into the main game one piece at a time. Build, test, build, test. Have fun."
            ),
            key_terms=[
                ('MILES_MULTIPLIER', 'New constant in Lab 2.2 (= 10). D20 roll times multiplier equals miles traveled.'),
                ('HAZARD_CHANCE', 'New constant in Lab 2.2 (= 30). Passed to check_percentage to determine if a hazard happens.'),
            ],
            think_about=[
                "Before you write any code: sketch out what each of the three library functions takes as input and returns as output. The signatures matter more than the bodies.",
                "Why does the main lab file import BOTH function_library and random directly? Could it get random through the library somehow?",
            ],
            source_url='https://docs.python.org/3/library/random.html',
        ),
    )

    deck.save(OUTPUT_PPTX)


if __name__ == '__main__':
    main()
