"""
test.py
Local test suite for Module 5 -- City and Player classes.

Provided by Bat City Collective.
Do not submit this file to CodeGrade. It is for local use only.

------------------------------------------------------------
HOW TO USE THIS FILE
------------------------------------------------------------
1. Place test.py in the same folder as your city.py and player.py.
2. Open a terminal in that folder.
3. Run:  python test.py
4. Read the results. Fix anything marked [FAIL] or [ERROR].
5. Run it again. Repeat until you see all [PASS].
6. Then submit to CodeGrade.

Tests city.py if it exists, then player.py if it exists.
If neither file exists, it exits gracefully.

------------------------------------------------------------
WHAT THE OUTPUT MEANS
------------------------------------------------------------
[PASS]  - Your code returned exactly what was expected.
[FAIL]  - Your code ran but returned the wrong value. Check the
          expected and got lines to see what went wrong.
[ERROR] - Your code raised an exception. The error type and
          message are shown to help you find the problem.

------------------------------------------------------------
A NOTE ON TEST.PY VS CODEGRADE
------------------------------------------------------------
This file uses different test values than CodeGrade's hidden tests.
Passing test.py does not guarantee a perfect CodeGrade score, but
failing test.py means CodeGrade will also fail.

------------------------------------------------------------
SOMETHING INTERESTING TO NOTICE
------------------------------------------------------------
This file is itself a Python program. Everything you see here --
functions, loops, conditionals, f-strings, try/except blocks --
is built from the same techniques you have learned this semester.
The only thing that might look unfamiliar is the lambda keyword
used in the run() function. A lambda is a tiny one-line function.
You will learn it properly in your next Python course.
"""

# os gives us os.path.exists() to check if a file exists before
# we try to import it. Without this check, a missing file would
# crash the whole program with a confusing error.
import os

# sys gives us sys.stdout -- the object that controls where print()
# sends its output. We use this in silence() to temporarily redirect
# output so display methods do not clutter the test results.
import sys

# io gives us io.StringIO() -- a fake file that lives in memory.
# We redirect print() into it when we want to run a function silently.
import io


# ============================================================
# GLOBAL COUNTERS
# ============================================================
# These track how many tests passed and failed across the entire run.
# The global keyword inside each function tells Python to use these
# module-level variables rather than creating local copies.

passed = 0
failed = 0


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def check(label, actual, expected):
    """
    Compare actual to expected. Print PASS or FAIL.

    repr() shows values with type markers -- strings get quotes,
    None shows as None -- making it easy to spot type mismatches.

    Args:
        label (str): Description shown next to [PASS] or [FAIL].
        actual: The value your code returned.
        expected: The value your code should have returned.
    """
    global passed, failed
    if actual == expected:
        print(f'  [PASS] {label}')
        passed += 1
    else:
        print(f'  [FAIL] {label}')
        print(f'         expected : {repr(expected)}')
        print(f'         got      : {repr(actual)}')
        failed += 1


def check_true(label, value):
    """
    Check that value is truthy. Print PASS or FAIL.

    Use when you cannot check for an exact value but can check that
    something is true -- a string is non-empty, isinstance() passes, etc.

    In Python, False, None, 0, '', [], {}, and set() are all falsy.
    Everything else is truthy.

    Args:
        label (str): Description shown next to [PASS] or [FAIL].
        value: Any expression tested with if value:.
    """
    global passed, failed
    if value:
        print(f'  [PASS] {label}')
        passed += 1
    else:
        print(f'  [FAIL] {label}')
        print(f'         expected : a true value')
        print(f'         got      : {repr(value)}')
        failed += 1


def check_in(label, item, collection):
    """
    Check that item is in collection. Print PASS or FAIL.

    Uses Python's in operator, which works for lists, sets, strings,
    and dictionaries (checks keys).

    Args:
        label (str): Description shown next to [PASS] or [FAIL].
        item: The value to look for.
        collection: The list, set, string, etc. to look in.
    """
    global passed, failed
    if item in collection:
        print(f'  [PASS] {label}')
        passed += 1
    else:
        print(f'  [FAIL] {label}')
        print(f'         expected : {repr(item)} to be in the collection')
        print(f'         collection was : {repr(collection)}')
        failed += 1


def section(title):
    """
    Print a visual section header.

    Purely cosmetic -- groups related tests in the output.
    Does not affect pass/fail counts.
    """
    print()
    print(f'  --- {title} ---')


def run(label, func):
    """
    Run a single test function safely, catching any exceptions.

    Without this wrapper, one crash would stop the entire test run.
    run() catches the exception, marks it as an error, and moves on
    so you can see ALL your problems in one pass.

    The func parameter is a function passed using lambda -- a tiny
    one-line function written without a name. For example:

        run('my test', lambda: check('x', obj.get_x(), 5))

    The lambda is not called here -- it is packaged and handed to
    run(), which calls it inside the try block.

    Args:
        label (str): Description shown if an error occurs.
        func: A callable (function or lambda) to execute.
    """
    global passed, failed
    try:
        func()
    except Exception as e:
        # type(e).__name__ gives the exception class as a string --
        # 'AttributeError', 'TypeError', etc.
        print(f'  [ERROR] {label}')
        print(f'          {type(e).__name__}: {e}')
        failed += 1


def silence(func):
    """
    Run a function and swallow all printed output.

    Temporarily replaces sys.stdout with a StringIO fake file.
    The try/finally guarantees stdout is ALWAYS restored, even if
    func() raises an exception.

    Args:
        func: A callable to run silently.
    """
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        func()
    finally:
        sys.stdout = old_stdout


# ============================================================
# CITY CLASS TESTS
# ============================================================

def test_city():
    """
    Run all tests for the City class.

    Tests are organized to mirror the City class structure:
        1. Import
        2. Object creation
        3. Getter methods
        4. __str__
        5. Connection methods
        6. Status methods
        7. get_arrival_message
        8. display_destinations
    """
    print()
    print('=' * 55)
    print('  TESTING: city.py')
    print('=' * 55)

    # ----------------------------------------------------------
    # IMPORT
    # We catch SyntaxError separately to give a more specific
    # message. In both cases we return immediately -- there is
    # nothing to test without a working import.
    # ----------------------------------------------------------
    try:
        from city import City
    except SyntaxError as e:
        print(f'  [ERROR] Syntax error in city.py -- fix this first.')
        print(f'          Line {e.lineno}: {e.msg}')
        print()
        print('  Tip: Check for missing colons, bad indentation,')
        print('       or unclosed parentheses near the line above.')
        return
    except ImportError as e:
        print(f'  [ERROR] Could not import City from city.py.')
        print(f'          {e}')
        print()
        print('  Tip: Make sure your class is named exactly "City"')
        print('       (capital C, no extra characters).')
        return

    print('  [PASS] city.py imported successfully')

    # ----------------------------------------------------------
    # OBJECT CREATION
    # If the START city fails we cannot continue.
    # WIN and DEAD_END are set to None and their tests skip.
    # ----------------------------------------------------------
    section('Creating City objects')

    try:
        sa = City('San Antonio', 'START', 'Home of the Alamo')
        print('  [PASS] City(\'San Antonio\', \'START\', \'Home of the Alamo\') created')
    except Exception as e:
        print(f'  [ERROR] Could not create City object.')
        print(f'          {type(e).__name__}: {e}')
        print()
        print('  Tip: Check your __init__ signature:')
        print('       def __init__(self, name, city_type, tagline)')
        print('  Cannot continue City tests without a working object.')
        return

    try:
        corpus = City('Corpus Christi', 'WIN', 'Sparkling City by the Sea')
        print('  [PASS] City(\'Corpus Christi\', \'WIN\', ...) created')
    except Exception as e:
        print(f'  [ERROR] Could not create WIN city -- {type(e).__name__}: {e}')
        corpus = None

    try:
        laredo = City('Laredo', 'DEAD_END', 'Gateway to Mexico')
        print('  [PASS] City(\'Laredo\', \'DEAD_END\', ...) created')
    except Exception as e:
        print(f'  [ERROR] Could not create DEAD_END city -- {type(e).__name__}: {e}')
        laredo = None

    try:
        el_paso = City('El Paso', 'WRONG_WAY', 'Closer to California')
        print('  [PASS] City(\'El Paso\', \'WRONG_WAY\', ...) created')
    except Exception as e:
        print(f'  [ERROR] Could not create WRONG_WAY city -- {type(e).__name__}: {e}')
        el_paso = None

    # ----------------------------------------------------------
    # GETTER METHODS
    # ----------------------------------------------------------
    section('Getter methods')

    run('get_name()', lambda: check(
        'get_name() returns the city name',
        sa.get_name(), 'San Antonio'))

    run('get_type()', lambda: check(
        'get_type() returns the city type in uppercase',
        sa.get_type(), 'START'))

    run('get_tagline()', lambda: check(
        'get_tagline() returns the city tagline',
        sa.get_tagline(), 'Home of the Alamo'))

    # ----------------------------------------------------------
    # __STR__
    # Expected format: 'San Antonio (START)'
    # ----------------------------------------------------------
    section('__str__ method')

    run('__str__()', lambda: check(
        'str(city) returns name followed by type in parentheses',
        str(sa), 'San Antonio (START)'))

    # ----------------------------------------------------------
    # CONNECTION METHODS
    # We add connections here (not at creation time) because
    # __init__ should NOT accept connections as a parameter.
    # ----------------------------------------------------------
    section('Connection methods')

    run('add_connection()', lambda: (
        sa.add_connection('Houston', 200),
        sa.add_connection('Corpus Christi', 150),
        sa.add_connection('Laredo', 160),
        check(
            'add_connection() stores the distance correctly',
            sa.get_distance_to('Houston'), 200)
    ))

    run('get_distance_to() -- connected city', lambda: check(
        'get_distance_to() returns correct distance',
        sa.get_distance_to('Corpus Christi'), 150))

    # Important edge case: unconnected city returns -1, not 0 or None.
    # Returning 0 would imply a connected city with zero distance.
    # Returning None would crash any code that does math with the result.
    run('get_distance_to() -- unconnected city', lambda: check(
        'get_distance_to() returns -1 for unconnected city',
        sa.get_distance_to('Dallas'), -1))

    run('get_destination_names() contains expected city', lambda: check_in(
        'get_destination_names() contains Houston',
        'Houston', sa.get_destination_names()))

    run('get_destination_names() returns a list', lambda: check_true(
        'get_destination_names() returns a list',
        isinstance(sa.get_destination_names(), list)))

    # ----------------------------------------------------------
    # STATUS METHODS
    # We test both True and False cases to catch hardcoded returns.
    # ----------------------------------------------------------
    section('Status methods')

    run('is_win_city() -- START city', lambda: check(
        'is_win_city() returns False for START city',
        sa.is_win_city(), False))

    if corpus:
        run('is_win_city() -- WIN city', lambda: check(
            'is_win_city() returns True for WIN city',
            corpus.is_win_city(), True))

    run('is_dead_end() -- START city', lambda: check(
        'is_dead_end() returns False for START city',
        sa.is_dead_end(), False))

    if laredo:
        run('is_dead_end() -- DEAD_END city', lambda: check(
            'is_dead_end() returns True for DEAD_END city',
            laredo.is_dead_end(), True))

    # WRONG_WAY cities are also dead ends in gameplay terms.
    if el_paso:
        run('is_dead_end() -- WRONG_WAY city', lambda: check(
            'is_dead_end() returns True for WRONG_WAY city',
            el_paso.is_dead_end(), True))

    # ----------------------------------------------------------
    # ARRIVAL MESSAGE
    # We do not test exact text -- students have creative freedom.
    # We check that a non-empty string is returned and that WIN
    # city messages reference the city name or the beach.
    # ----------------------------------------------------------
    section('get_arrival_message()')

    run('get_arrival_message() -- regular city', lambda: check_true(
        'get_arrival_message() returns a non-empty string',
        isinstance(sa.get_arrival_message(), str)
        and len(sa.get_arrival_message()) > 0))

    if corpus:
        run('get_arrival_message() -- WIN city', lambda: check_true(
            'get_arrival_message() for WIN city mentions city name or beach',
            'CORPUS CHRISTI' in corpus.get_arrival_message().upper()
            or 'BEACH' in corpus.get_arrival_message().upper()))

    if laredo:
        run('get_arrival_message() -- DEAD_END city', lambda: check_true(
            'get_arrival_message() for DEAD_END city returns a string',
            isinstance(laredo.get_arrival_message(), str)
            and len(laredo.get_arrival_message()) > 0))

    # ----------------------------------------------------------
    # DISPLAY METHODS
    # display_destinations() prints to screen but returns nothing.
    # We silence the output and just check it does not crash.
    # ----------------------------------------------------------
    section('display_destinations()')

    run('display_destinations() runs without error', lambda: (
        silence(lambda: sa.display_destinations()),
        check_true(
            'display_destinations() completes without raising an exception',
            True)
    ))


# ============================================================
# PLAYER CLASS TESTS
# ============================================================

def test_player():
    """
    Run all tests for the Player class.

    The Player class tracks all game state that was previously
    scattered across main() in Module 4. Tests verify each piece
    of state is tracked correctly:
        1. Import
        2. Object creation
        3. Initial state (before travel)
        4. travel_to() and its effects
        5. record_hazard()
        6. record_trivia()
        7. Unique set behavior
        8. Display methods
        9. __str__
    """
    print()
    print('=' * 55)
    print('  TESTING: player.py')
    print('=' * 55)

    # ----------------------------------------------------------
    # IMPORT
    # ----------------------------------------------------------
    try:
        from player import Player
    except SyntaxError as e:
        print(f'  [ERROR] Syntax error in player.py -- fix this first.')
        print(f'          Line {e.lineno}: {e.msg}')
        print()
        print('  Tip: Check for missing colons, bad indentation,')
        print('       or unclosed parentheses near the line above.')
        return
    except ImportError as e:
        print(f'  [ERROR] Could not import Player from player.py.')
        print(f'          {e}')
        print()
        print('  Tip: Make sure your class is named exactly "Player"')
        print('       (capital P, no extra characters).')
        return

    print('  [PASS] player.py imported successfully')

    # ----------------------------------------------------------
    # OBJECT CREATION
    # ----------------------------------------------------------
    section('Creating Player object')

    try:
        player = Player('Maria', 'San Antonio')
        print('  [PASS] Player(\'Maria\', \'San Antonio\') created')
    except Exception as e:
        print(f'  [ERROR] Could not create Player object.')
        print(f'          {type(e).__name__}: {e}')
        print()
        print('  Tip: Check your __init__ signature:')
        print('       def __init__(self, name, starting_city)')
        print('  Cannot continue Player tests without a working object.')
        return

    # ----------------------------------------------------------
    # INITIAL STATE (before any travel or events)
    # Verify __init__ sets everything up correctly.
    # ----------------------------------------------------------
    section('Initial state (before any travel)')

    run('get_name()', lambda: check(
        'get_name() returns the player name',
        player.get_name(), 'Maria'))

    run('get_current_city()', lambda: check(
        'get_current_city() returns the starting city',
        player.get_current_city(), 'San Antonio'))

    run('get_total_miles() starts at 0', lambda: check(
        'get_total_miles() returns 0 before any travel',
        player.get_total_miles(), 0))

    # Starting city should already be in visited list and unique set
    run('get_visited_cities() contains starting city', lambda: check_in(
        'get_visited_cities() contains San Antonio at start',
        'San Antonio', player.get_visited_cities()))

    run('get_visited_cities() returns a list', lambda: check_true(
        'get_visited_cities() returns a list',
        isinstance(player.get_visited_cities(), list)))

    run('get_unique_city_count() starts at 1', lambda: check(
        'get_unique_city_count() returns 1 at start',
        player.get_unique_city_count(), 1))

    run('get_hazards_faced() starts at 0', lambda: check(
        'get_hazards_faced() returns 0 before any hazards',
        player.get_hazards_faced(), 0))

    run('get_hazards_escaped() starts at 0', lambda: check(
        'get_hazards_escaped() returns 0 before any hazards',
        player.get_hazards_escaped(), 0))

    run('get_unique_hazard_count() starts at 0', lambda: check(
        'get_unique_hazard_count() returns 0 before any hazards',
        player.get_unique_hazard_count(), 0))

    run('get_trivia_asked() starts at 0', lambda: check(
        'get_trivia_asked() returns 0 before any trivia',
        player.get_trivia_asked(), 0))

    run('get_trivia_correct() starts at 0', lambda: check(
        'get_trivia_correct() returns 0 before any trivia',
        player.get_trivia_correct(), 0))

    # ----------------------------------------------------------
    # TRAVEL_TO
    # Must update: current city, miles, visited list, unique set.
    # ----------------------------------------------------------
    section('travel_to() method')

    run('travel_to() does not crash', lambda: (
        player.travel_to('Houston', 200),
        check_true('travel_to() runs without error', True)
    ))

    run('get_current_city() after travel', lambda: check(
        'get_current_city() returns Houston after traveling there',
        player.get_current_city(), 'Houston'))

    run('get_total_miles() after travel', lambda: check(
        'get_total_miles() returns 200 after traveling 200 miles',
        player.get_total_miles(), 200))

    run('get_visited_cities() contains destination', lambda: check_in(
        'get_visited_cities() contains Houston after traveling there',
        'Houston', player.get_visited_cities()))

    run('get_unique_city_count() increases', lambda: check(
        'get_unique_city_count() returns 2 after visiting one new city',
        player.get_unique_city_count(), 2))

    # Second travel -- miles must accumulate
    run('miles accumulate correctly', lambda: (
        player.travel_to('Galveston', 50),
        check(
            'get_total_miles() returns 250 after SA->Houston->Galveston',
            player.get_total_miles(), 250)
    ))

    # ----------------------------------------------------------
    # RECORD_HAZARD
    # Must update: faced count, escaped count (if True), unique set.
    # ----------------------------------------------------------
    section('record_hazard() method')

    run('record_hazard() -- escaped (True)', lambda: (
        player.record_hazard("Buc-ee's appears!", True),
        check(
            'get_hazards_faced() returns 1 after one hazard',
            player.get_hazards_faced(), 1)
    ))

    run('get_hazards_escaped() after lucky hazard', lambda: check(
        'get_hazards_escaped() returns 1 after escaped hazard',
        player.get_hazards_escaped(), 1))

    run('get_unique_hazard_count() after hazard', lambda: check(
        'get_unique_hazard_count() returns 1 after one hazard',
        player.get_unique_hazard_count(), 1))

    run('record_hazard() -- not escaped (False)', lambda: (
        player.record_hazard('Speed trap!', False),
        check(
            'get_hazards_faced() returns 2 after second hazard',
            player.get_hazards_faced(), 2)
    ))

    run('get_hazards_escaped() after unlucky hazard', lambda: check(
        'get_hazards_escaped() still returns 1 after unlucky hazard',
        player.get_hazards_escaped(), 1))

    # ----------------------------------------------------------
    # RECORD_TRIVIA
    # Must update: asked count, correct count (if True).
    # ----------------------------------------------------------
    section('record_trivia() method')

    run('record_trivia() -- correct (True)', lambda: (
        player.record_trivia(True),
        check(
            'get_trivia_asked() returns 1 after one question',
            player.get_trivia_asked(), 1)
    ))

    run('get_trivia_correct() after correct answer', lambda: check(
        'get_trivia_correct() returns 1 after correct answer',
        player.get_trivia_correct(), 1))

    run('record_trivia() -- incorrect (False)', lambda: (
        player.record_trivia(False),
        check(
            'get_trivia_asked() returns 2 after second question',
            player.get_trivia_asked(), 2)
    ))

    run('get_trivia_correct() after incorrect answer', lambda: check(
        'get_trivia_correct() still returns 1 after wrong answer',
        player.get_trivia_correct(), 1))

    # ----------------------------------------------------------
    # UNIQUE SET BEHAVIOR
    # Revisiting a city should not increase unique count.
    # Revisiting a hazard should not increase unique hazard count.
    # ----------------------------------------------------------
    section('Unique set behavior')

    run('revisiting a city does not increase unique count', lambda: (
        player.travel_to('Houston', 50),
        check(
            'get_unique_city_count() stays at 3 after revisiting Houston',
            player.get_unique_city_count(), 3)
    ))

    run('revisited city still appears in visited list', lambda: check_true(
        'get_visited_cities() contains Houston at least twice',
        player.get_visited_cities().count('Houston') >= 2))

    run('same hazard does not increase unique hazard count', lambda: (
        player.record_hazard("Buc-ee's appears!", True),
        check(
            'get_unique_hazard_count() stays at 2 after repeat hazard',
            player.get_unique_hazard_count(), 2)
    ))

    # ----------------------------------------------------------
    # DISPLAY METHODS
    # ----------------------------------------------------------
    section('Display methods')

    run('get_route_string() returns a string', lambda: check_true(
        'get_route_string() returns a non-empty string',
        isinstance(player.get_route_string(), str)
        and len(player.get_route_string()) > 0))

    run('get_route_string() contains city names', lambda: check_true(
        'get_route_string() contains San Antonio and Houston',
        'San Antonio' in player.get_route_string()
        and 'Houston' in player.get_route_string()))

    run('get_route_string() uses arrow separator', lambda: check_true(
        'get_route_string() uses -> between cities',
        '->' in player.get_route_string()))

    run('get_trivia_accuracy() returns a string', lambda: check_true(
        'get_trivia_accuracy() returns a percentage string',
        isinstance(player.get_trivia_accuracy(), str)
        and '%' in player.get_trivia_accuracy()))

    run('get_unique_cities() returns a set', lambda: check_true(
        'get_unique_cities() returns a set',
        isinstance(player.get_unique_cities(), set)))

    # ----------------------------------------------------------
    # __STR__
    # ----------------------------------------------------------
    section('__str__ method')

    run('__str__() contains player name', lambda: check_true(
        'str(player) contains the player name',
        'Maria' in str(player)))


# ============================================================
# MAIN
# ============================================================

def main():
    """
    Check which files exist and run their tests.

    os.path.exists() returns True if the named file exists in the
    current directory. This is why test.py must be in the same
    folder as city.py and player.py.
    """
    global passed, failed

    city_exists = os.path.exists('city.py')
    player_exists = os.path.exists('player.py')

    if not city_exists and not player_exists:
        print()
        print('  No files found to test.')
        print('  Make sure test.py is in the same folder as your')
        print('  city.py and player.py files, then run it again.')
        print()
        return

    if city_exists:
        test_city()
    else:
        print()
        print('  city.py not found -- skipping City tests.')

    if player_exists:
        test_player()
    else:
        print()
        print('  player.py not found -- skipping Player tests.')

    # ----------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------
    print()
    print('=' * 55)
    total = passed + failed
    print(f'  Results: {passed} passed, {failed} failed out of {total} tests')
    if failed == 0:
        print('  All tests passed! Go submit to CodeGrade.')
    else:
        print('  Fix the failing tests above, then run test.py again.')
    print('=' * 55)
    print()


# ============================================================
# ENTRY POINT GUARD
# ============================================================
# __name__ is set to '__main__' when this file is run directly.
# If imported by another file, main() does not run automatically.

if __name__ == '__main__':
    main()
