"""
Bring Chapters 8, 9, and 10 BookEx checkpoints in line with Chapters 2 through 7.

These three chapters were authored in a separate pass and never matched the
pattern the other seven use. Two defects, both present since the original
2026-03-25 commit:

  1. The build steps sat under the `what_youre_building` heading, so the
     section meant to DESCRIBE the program instead listed how to write it.
     There was no `step_by_step` heading at all.
  2. The step lists never told the student to open the textbook and type the
     program, which is what the assignment actually is.

This moves the per-program description into `what_youre_building` prose and
replaces the step list with the standard five-step transcription block under a
`step_by_step` heading. Every other content item (intro text, why_this_matters,
tips_and_pitfalls, pro_tip, tables) is left untouched.

Run once from the repo root, then re-render chapters 8, 9, and 10.
"""
import json
import sys

# filename -> (program label for step 1, What You're Building prose, optional
# override for the "type it" step where the book spreads one program across
# several listings)
SPEC = {
    # ---------------- Chapter 8 ----------------
    "count_Ts.py": (
        "Program 8-1",
        "A program that counts how many times the letter T appears in a string the user "
        "types. It sets a counter to zero before the loop, reads a string with "
        "<code>input()</code>, then uses a <code>for</code> loop to walk the string one "
        "character at a time. Each character that matches <code>'T'</code> or "
        "<code>'t'</code> increments the counter, and an f-string prints the total after "
        "the loop ends.",
        None,
    ),
    "concatenate.py": (
        "Program 8-2",
        "A short program that assigns <code>'Carmen'</code> to a variable, prints it, then "
        "joins <code>' Brown'</code> onto it with <code>+</code> and assigns the result "
        "back to the same variable. Printing it a second time shows the updated value.",
        None,
    ),
    "string_test.py": (
        "Program 8-5",
        "A program that reads a string from the user and runs six testing methods against "
        "it: <code>.isalnum()</code>, <code>.isdigit()</code>, <code>.isalpha()</code>, "
        "<code>.isspace()</code>, <code>.islower()</code>, and <code>.isupper()</code>. "
        "Each one that returns <code>True</code> prints a message. Run it several times "
        "with different inputs, including a number, a word, all caps, all spaces, and a "
        "mix, so you can see which tests fire for each.",
        None,
    ),
    "string_split.py": (
        "Program 8-9",
        "A short program that calls <code>.split()</code> with no arguments on the string "
        "<code>'One two three four'</code>, which breaks it on whitespace and returns a "
        "list of words. Printing the result shows the list.",
        None,
    ),
    "split_date.py": (
        "Program 8-10",
        "A program that parses a date string in MM/DD/YYYY format. Calling "
        "<code>.split('/')</code> breaks <code>'11/26/2019'</code> into a three-element "
        "list, and indexing that list at 0, 1, and 2 pulls out the month, day, and year "
        "for labeled printing.",
        None,
    ),
    # ---------------- Chapter 9 ----------------
    "card_dealer.py": (
        "Program 9-1",
        "A program that uses a dictionary as a deck of cards, with each card name as a key "
        "and its point value as the value. Three functions work together: "
        "<code>create_deck()</code> builds and returns the 52-card dictionary, "
        "<code>deal_cards()</code> selects cards at random with "
        "<code>random.choice(list(deck))</code> and accumulates their values, and "
        "<code>main()</code> coordinates the two. Face cards are worth 10, aces 1, and "
        "number cards match their number.",
        "The book prints this program across several listings, one per function. Type all "
        "of them into the single file, in the order they appear.",
    ),
    "sets.py": (
        "Program 9-3",
        "A program that builds two sets of student athletes with the <code>set()</code> "
        "constructor, then demonstrates all four set operations against them: "
        "<code>.intersection()</code>, <code>.union()</code>, <code>.difference()</code> "
        "in both directions, and <code>.symmetric_difference()</code>. Each result prints "
        "through a <code>for</code> loop. The output order will not be alphabetical, "
        "because sets are unordered.",
        None,
    ),
    # ---------------- Chapter 10 ----------------
    "bankaccount2.py": (
        "Program 10-9",
        "A <code>BankAccount</code> class that manages a balance held in a private "
        "attribute, <code>self.__balance</code>. It defines <code>__init__</code>, "
        "<code>deposit</code>, <code>withdraw</code> (which refuses an overdraft), "
        "<code>get_balance</code>, and <code>__str__</code>, which returns the balance "
        "formatted with the <code>:,.2f</code> format spec. This file holds the class "
        "definition only, with no <code>main()</code> and no <code>input()</code> calls.",
        None,
    ),
    "account_test2.py": (
        "Program 10-10",
        "A program that imports <code>bankaccount2</code> and exercises the class. It "
        "reads a starting balance from the user, creates a <code>BankAccount</code> "
        "object, makes a deposit and a withdrawal, and prints the object directly both "
        "times so that <code>__str__</code> handles the formatting.",
        None,
    ),
    "cellphone.py": (
        "Program 10-12",
        "A <code>CellPhone</code> class with three private attributes for manufacturer, "
        "model, and retail price, plus a full set of getters and setters for each. This "
        "file holds the class definition only.",
        None,
    ),
    "cell_phone_test.py": (
        "Program 10-13",
        "A program that imports <code>cellphone</code>, reads manufacturer, model, and "
        "retail price from the user, creates a <code>CellPhone</code> object, and reads "
        "the values back through the getter methods. The book also has you try "
        "<code>phone.__retail_price</code> directly so you can watch the "
        "<code>AttributeError</code>, which is encapsulation doing its job.",
        None,
    ),
}


def build_steps(program, filename, type_override):
    type_step = type_override or "Type the program exactly as shown in the book."
    return [
        f"Open your textbook to {program}.",
        f"Create a new file named {filename}.",
        type_step,
        "Run the file and confirm your output matches the book.",
        "Fix any typos until it runs cleanly.",
    ]


def patch(path):
    with open(path) as fh:
        data = json.load(fh)

    changed = 0
    for cp in data.get("checkpoints", []):
        title = cp.get("title", "")
        filename = next((f for f in SPEC if f in title), None)
        if not filename:
            print(f"  SKIP CP{cp.get('number')}: no spec entry for {title!r}")
            continue

        program, prose, type_override = SPEC[filename]
        content = cp.get("content", [])

        # Locate the what_youre_building heading and the instructions block
        # that currently (wrongly) sits under it.
        try:
            h3_i = next(i for i, it in enumerate(content)
                        if it.get("type") == "h3"
                        and it.get("label") == "what_youre_building")
            ins_i = next(i for i, it in enumerate(content)
                         if it.get("type") == "instructions")
        except StopIteration:
            print(f"  SKIP CP{cp.get('number')}: expected shape not found")
            continue

        if ins_i != h3_i + 1:
            print(f"  SKIP CP{cp.get('number')}: instructions not directly "
                  f"under what_youre_building")
            continue

        replacement = [
            {"type": "h3", "label": "what_youre_building"},
            {"type": "text", "body": prose},
            {"type": "h3", "label": "step_by_step"},
            {"type": "instructions",
             "items": build_steps(program, filename, type_override)},
        ]
        cp["content"] = content[:h3_i] + replacement + content[ins_i + 1:]
        changed += 1
        print(f"  CP{cp.get('number')}: {filename} -> {program}")

    if changed:
        with open(path, "w") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    return changed


if __name__ == "__main__":
    total = 0
    for p in sys.argv[1:]:
        print(f"== {p}")
        total += patch(p)
    print(f"\nTotal checkpoints rewritten: {total}")
