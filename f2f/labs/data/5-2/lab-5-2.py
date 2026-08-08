"""
lab-5-2.py
Assignment 5.2: Deep in the Heart

Provided by Bat City Collective.
Do not modify this file.

------------------------------------------------------------
YOUR JOB
------------------------------------------------------------
Build player.py so this program runs.

Read through this file carefully before you start. Every call
to player.travel_to(), player.record_hazard(), player.get_name(),
and so on tells you exactly what methods your Player class needs
and what each one must do.

------------------------------------------------------------
WHAT CHANGED FROM lab-5-1.py
------------------------------------------------------------
One thing changed: the ten scattered state variables in main()
were replaced with a single Player object.

BEFORE (lab-5-1.py):
    current_city = 'San Antonio'
    total_miles = 0
    total_hazards = 0
    total_escaped = 0
    trivia_asked = 0
    trivia_correct = 0
    visited = [current_city]
    unique_cities = set()
    unique_cities.add(current_city)
    unique_hazards = set()

AFTER (lab-5-2.py):
    player = Player(name, 'San Antonio')

Every place those variables were updated is now a method call
on the player object. Search for the comments marked
    # WAS: ...
throughout this file to see every substitution.

------------------------------------------------------------
WHAT DID NOT CHANGE
------------------------------------------------------------
Everything else is identical to lab-5-1.py:
- All four load functions
- build_cities()
- trivia_gate()
- execute_travel() / handle_hazard()
- The game loop logic
- The text files
- function_library

OOP did not replace any of that. It just gave the game state
a better home.

------------------------------------------------------------
FILES REQUIRED
------------------------------------------------------------
city.py           -- your City class from Lab 5.1
player.py         -- your Player class (what you are building now)
function_library.py
city_distances.txt
city_info.txt
hazards.txt
trivia.txt
"""

import random
import function_library

# We now import both City and Player.
# City is the same class you built in Lab 5.1.
# Player is the class you are building now.
from city import City
from player import Player


# ============================================================
# LOAD FUNCTIONS
# ============================================================
# These four functions are identical to lab-5-1.py.
# They read the text files and build Python data structures.
# Nothing changed here -- the files and the parsing logic
# are exactly the same as they were in Module 4.


def load_city_distances(filename):
    """
    Load city distances from file into a nested dictionary.

    Returns:
        dict: {city1: {city2: distance, ...}, ...}
    """
    distances = {}
    file = open(filename, 'r')

    for line in file:
        parts = line.strip().split(',')
        city1 = parts[0]
        city2 = parts[1]
        distance = int(parts[2])

        if city1 not in distances:
            distances[city1] = {}
        distances[city1][city2] = distance

    file.close()
    return distances


def load_city_info(filename):
    """
    Load city info from file into a dictionary.

    Returns:
        dict: {city_name: {'type': str, 'tagline': str}, ...}
    """
    info = {}
    file = open(filename, 'r')

    for line in file:
        parts = line.strip().split(',')
        city = parts[0]
        city_type = parts[1]
        tagline = parts[2]
        info[city] = {'type': city_type, 'tagline': tagline}

    file.close()
    return info


def load_hazards(filename):
    """
    Load hazards from file into a list of dictionaries.

    Returns:
        list: [{'name': str, 'heads': str, 'tails': str}, ...]
    """
    hazards = []
    file = open(filename, 'r')

    for line in file:
        parts = line.strip().split(',')
        hazard = {
            'name': parts[0],
            'heads': parts[1],
            'tails': parts[2]
        }
        hazards.append(hazard)

    file.close()
    return hazards


def load_trivia(filename):
    """
    Load trivia from file into a dictionary keyed by city.

    File format: city,question,answer

    Returns:
        dict: {city: [{'question': str, 'answer': str}, ...], ...}
    """
    trivia = {}
    file = open(filename, 'r')

    for line in file:
        parts = line.strip().split(',')
        city = parts[0]
        question = parts[1]
        answer = parts[2]

        if city not in trivia:
            trivia[city] = []

        trivia[city].append({'question': question, 'answer': answer})

    file.close()
    return trivia


# ============================================================
# BUILD_CITIES
# ============================================================
# This function is identical to lab-5-1.py.
# It converts the two raw dictionaries (distances and city_info)
# into a dictionary of City objects.
#
# This is the bridge between the file-loading world (Module 4)
# and the object-oriented world (Module 5). The load functions
# give us raw dictionaries; build_cities() wraps them in objects.


def build_cities(distances, city_info):
    """
    Build City objects from the loaded data dictionaries.

    Creates one City object per city in city_info, then adds
    all connections from distances.

    Args:
        distances (dict): Nested dict of city-to-city distances
        city_info (dict): Dict of city types and taglines

    Returns:
        dict: {city_name (str): City object}
    """
    cities = {}

    # Create a City object for each city in city_info
    for city_name in city_info:
        info = city_info[city_name]
        city = City(city_name, info['type'], info['tagline'])
        cities[city_name] = city

    # Add connections from the distances dictionary
    for city_name in distances:
        for dest, dist in distances[city_name].items():
            if city_name in cities:
                cities[city_name].add_connection(dest, dist)

    return cities


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def get_destination_by_number(city_obj, choice):
    """
    Get a destination city name by menu number.

    In lab-5-1.py this took (city, distances, choice) and
    did list(distances[city].keys())[choice - 1].

    Now it takes the City object directly and calls
    get_destination_names() -- the same data, cleaner access.

    Args:
        city_obj (City): The current City object
        choice (int): The player's menu selection (1-based)

    Returns:
        str: The destination city name
    """
    destinations = city_obj.get_destination_names()
    return destinations[choice - 1]


# ============================================================
# TRIVIA GATE
# ============================================================
# This function is nearly identical to lab-5-1.py.
# The only change is the signature and one distance lookup.
#
# BEFORE (lab-5-1.py):
#   trivia_gate(dest, trivia, all_dests, distances, current)
#   used: distances[current][dest]  and  distances[current][redirect]
#
# AFTER (lab-5-2.py):
#   trivia_gate(dest, trivia, all_dests, cities, current_name)
#   uses: cities[current_name].get_distance_to(dest)
#
# The trivia_gate returns a tuple -- the Player object is NOT
# passed in here. The main game loop calls player.record_trivia()
# after trivia_gate() returns. That keeps this function focused
# on ONE job: asking the question and returning the result.


def trivia_gate(dest, trivia, all_dests, cities, current_name):
    """
    Ask a trivia question to earn the chosen destination.

    If answered correctly: player gets their chosen destination.
    If answered incorrectly: player is redirected randomly.

    Args:
        dest (str): The destination the player chose
        trivia (dict): All trivia questions by city
        all_dests (list): All available destinations from here
        cities (dict): All City objects
        current_name (str): Name of the current city

    Returns:
        tuple: (final_destination (str), distance (int), correct (bool))
    """
    print()
    print('--- TRIVIA TIME! ---')
    print(f'To reach {dest}, answer this question:')
    print()

    # Get a trivia question for this destination.
    # If the destination has no trivia, pick from a random city.
    if dest in trivia and len(trivia[dest]) > 0:
        q = random.choice(trivia[dest])
    else:
        cities_with_trivia = []
        for c in trivia:
            if len(trivia[c]) > 0:
                cities_with_trivia.append(c)
        random_city = random.choice(cities_with_trivia)
        q = random.choice(trivia[random_city])

    print(f'  {q["question"]}')
    print()

    answer = input('TRUE or FALSE? ').strip().upper()

    # Accept T / TRUE / F / FALSE
    if answer == 'T' or answer == 'TRUE':
        player_answer = 'TRUE'
    elif answer == 'F' or answer == 'FALSE':
        player_answer = 'FALSE'
    else:
        print('Invalid answer! Counting as FALSE.')
        player_answer = 'FALSE'

    if player_answer == q['answer']:
        print('CORRECT!')
        # WAS: return (dest, distances[current][dest], True)
        # NOW: use the City object to look up the distance
        return (dest, cities[current_name].get_distance_to(dest), True)
    else:
        print(f'WRONG! The answer was {q["answer"]}.')

        # Random redirect to another destination
        other = []
        for d in all_dests:
            if d != dest:
                other.append(d)

        if len(other) > 0:
            redirect = random.choice(other)
            print(f'Detour! Going to {redirect} instead.')
            # WAS: return (redirect, distances[current][redirect], False)
            return (redirect,
                    cities[current_name].get_distance_to(redirect),
                    False)

        # No other options -- go to original destination anyway
        return (dest, cities[current_name].get_distance_to(dest), False)


# ============================================================
# HAZARD HANDLER
# ============================================================
# This function changed in one important way:
#
# BEFORE (lab-5-1.py):
#   handle_hazard(hazards, unique_hazards)
#   -- took the unique_hazards SET as a parameter
#   -- called unique_hazards.add(hazard['name']) directly
#   -- returned True/False for the caller to handle
#
# AFTER (lab-5-2.py):
#   handle_hazard(hazards, player)
#   -- takes the Player OBJECT instead of the set
#   -- calls player.record_hazard() which handles everything:
#      incrementing faced, incrementing escaped (if lucky),
#      and adding the hazard name to the unique set
#   -- no return value needed (player handles its own state)


def handle_hazard(hazards, player):
    """
    Handle a random hazard encounter.

    Picks a random hazard, flips a coin, prints the outcome,
    and records everything in the Player object.

    Args:
        hazards (list): All hazard dictionaries
        player (Player): The player object -- records the encounter
    """
    hazard = random.choice(hazards)

    print()
    print(f'*** HAZARD: {hazard["name"]} ***')
    function_library.enter_to_continue(
        'Flipping the coin... Press Enter to see your fate...')

    result = function_library.flip_coin()
    print(f'  {result}!')

    if result == 'HEADS':
        print(f'  {hazard["heads"]}')
        escaped = True
    else:
        print(f'  {hazard["tails"]}')
        escaped = False

    function_library.enter_to_continue(
        'Press Enter to get back on the road...')

    # WAS: unique_hazards.add(hazard['name'])
    # WAS: total_hazards += 1
    # WAS: if escaped: total_escaped += 1
    # NOW: one method call handles all three updates
    player.record_hazard(hazard['name'], escaped)


# ============================================================
# TRAVEL EXECUTOR
# ============================================================
# This function was called travel_to() in lab-5-1.py.
# We renamed it execute_travel() here to avoid confusion with
# player.travel_to() -- they do different things:
#
#   execute_travel() -- runs the D20 loop, handles hazards,
#                       then calls player.travel_to() at the end
#
#   player.travel_to() -- updates the player's location, miles,
#                         visited list, and unique city set
#
# BEFORE (lab-5-1.py):
#   travel_to(destination, distance, hazards, unique_hazards)
#   -- returned (miles_traveled, hazards_faced, hazards_escaped)
#   -- the caller updated all the variables from the return value
#
# AFTER (lab-5-2.py):
#   execute_travel(destination, distance, hazards, player)
#   -- no return value
#   -- player.record_hazard() handles hazard tracking inside
#   -- player.travel_to() handles location/miles/visited at the end


def execute_travel(destination, distance, hazards, player):
    """
    Run the D20 travel loop to a destination.

    Rolls the die, checks for hazards along the way, then
    updates the player object when the destination is reached.

    Args:
        destination (str): Name of the destination city
        distance (int): Miles to the destination
        hazards (list): All hazard dictionaries
        player (Player): The player object
    """
    print()
    print(f'--- Traveling to {destination} ---')

    remaining = distance
    miles_traveled = 0

    while remaining > 0:
        function_library.enter_to_continue(
            'Hit the gas! Press Enter to roll the D20...')
        roll = function_library.roll_d20()
        miles = roll * 10

        # Don't overshoot the destination
        if miles > remaining:
            miles = remaining

        miles_traveled = miles_traveled + miles
        remaining = remaining - miles

        print(f'  Rolled {roll}! That\'s {roll * 10} miles...')
        if miles < roll * 10:
            print(f'  (Only {miles} miles left -- you\'re almost there!)')
        print(f'  {remaining} miles remaining to {destination}.')

        function_library.enter_to_continue(
            'Press Enter to continue down the road...')

        # 30% chance of a hazard on each turn, but not the last one
        if remaining > 0 and function_library.check_percentage(30):
            handle_hazard(hazards, player)

    print(f'Arrived at {destination}!')

    # WAS: current_city = final_dest
    # WAS: total_miles = total_miles + miles_traveled
    # WAS: visited.append(final_dest)
    # WAS: unique_cities.add(final_dest)
    # NOW: one method call handles all four updates
    player.travel_to(destination, miles_traveled)


# ============================================================
# MAIN
# ============================================================
# This is where you will see the biggest difference between
# lab-5-1.py and lab-5-2.py.
#
# In lab-5-1.py, main() opened with ten state variables:
#
#   current_city = 'San Antonio'
#   total_miles = 0
#   total_hazards = 0
#   total_escaped = 0
#   trivia_asked = 0
#   trivia_correct = 0
#   visited = [current_city]
#   unique_cities = set()
#   unique_cities.add(current_city)
#   unique_hazards = set()
#
# In lab-5-2.py, all ten become one line:
#
#   player = Player(name, 'San Antonio')
#
# Every variable that was updated in the game loop is now
# updated through a player method call instead. Look for
# the WAS/NOW comments throughout main() to see each one.


def main():
    """Main game function."""
    print()
    print('=' * 55)
    print('DEEP IN THE HEART: A LONE STAR JOURNEY')
    print('Lab 5.2: Now with a Player Class!')
    print('=' * 55)
    print()

    # ----------------------------------------------------------
    # LOAD DATA
    # Identical to lab-5-1.py. The text files did not change.
    # ----------------------------------------------------------
    print('Loading game data...')
    distances = load_city_distances('city_distances.txt')
    city_info = load_city_info('city_info.txt')
    hazards = load_hazards('hazards.txt')
    trivia = load_trivia('trivia.txt')

    trivia_count = sum(len(trivia[c]) for c in trivia)
    print(f'Loaded {len(city_info)} cities, {len(hazards)} hazards,',
          f'{trivia_count} trivia questions!')
    print()

    # ----------------------------------------------------------
    # BUILD CITY OBJECTS
    # Identical to lab-5-1.py.
    # ----------------------------------------------------------
    cities = build_cities(distances, city_info)

    # ----------------------------------------------------------
    # GET PLAYER NAME
    # ----------------------------------------------------------
    name = input('Enter your name: ').strip()
    if name == '':
        name = 'Driver'

    print()

    # ----------------------------------------------------------
    # CREATE PLAYER OBJECT
    #
    # WAS (lab-5-1.py) -- ten separate variables:
    #   current_city = 'San Antonio'
    #   total_miles = 0
    #   total_hazards = 0
    #   total_escaped = 0
    #   trivia_asked = 0
    #   trivia_correct = 0
    #   visited = [current_city]
    #   unique_cities = set()
    #   unique_cities.add(current_city)
    #   unique_hazards = set()
    #
    # NOW -- one object that holds all of them:
    # ----------------------------------------------------------
    player = Player(name, 'San Antonio')

    print(f'Welcome, {player.get_name()}!')
    print('Goal: Reach Corpus Christi or Galveston!')
    print()

    # ----------------------------------------------------------
    # GAME LOOP
    # ----------------------------------------------------------
    playing = True

    while playing:

        # Get the current city NAME from the player object,
        # then look up the City OBJECT from the cities dictionary.
        #
        # WAS: info = city_info[current_city]
        # NOW: current_city is the City object itself
        current_city_name = player.get_current_city()
        current_city = cities[current_city_name]

        print()
        print('=' * 40)

        # WAS: print(f'You are in: {current_city}')
        # WAS: print(f'"{info["tagline"]}"')
        # NOW: call methods on the City object
        print(f'You are in: {current_city.get_name()}')
        print(f'"{current_city.get_tagline()}"')
        print('=' * 40)

        # ----------------------------------------------------------
        # WIN CHECK
        # WAS: if is_win_city(current_city, city_info):
        # NOW: City object knows its own type
        # ----------------------------------------------------------
        if current_city.is_win_city():
            print()
            print('YOU REACHED THE BEACH!')
            playing = False
            continue

        # ----------------------------------------------------------
        # DEAD END CHECK
        # WAS: if is_dead_end(current_city, city_info):
        # NOW: City object knows its own type
        # ----------------------------------------------------------
        if current_city.is_dead_end():
            print()
            print('This is a dead end!')
            choice = input('Return to San Antonio? (y/n): ').strip().upper()
            if choice == 'Y':
                # WAS: current_city = 'San Antonio'
                # WAS: visited.append(current_city)
                # WAS: unique_cities.add(current_city)
                # NOW: one method call, distance 0 (no miles for turning back)
                player.travel_to('San Antonio', 0)
            else:
                playing = False
            continue

        # ----------------------------------------------------------
        # SHOW DESTINATIONS
        # WAS: display_destinations(current_city, distances)
        # NOW: City object displays its own destinations
        # ----------------------------------------------------------
        current_city.display_destinations()

        # ----------------------------------------------------------
        # GET PLAYER CHOICE
        # ----------------------------------------------------------
        num_choices = len(current_city.get_destination_names())
        choice = function_library.get_valid_int(
            f'Choose (1-{num_choices}): ', 1, num_choices)

        dest = get_destination_by_number(current_city, choice)
        all_dests = current_city.get_destination_names()

        # ----------------------------------------------------------
        # TRIVIA GATE
        # Returns (final_destination, distance, correct)
        # ----------------------------------------------------------
        final_dest, dist, correct = trivia_gate(
            dest, trivia, all_dests, cities, current_city_name)

        # WAS: trivia_asked = trivia_asked + 1
        # WAS: if correct: trivia_correct = trivia_correct + 1
        # NOW: one method call handles both counters
        player.record_trivia(correct)

        # ----------------------------------------------------------
        # TRAVEL
        # execute_travel() runs the D20 loop, handles hazards,
        # and calls player.travel_to() and player.record_hazard()
        # internally. No return value needed -- the player object
        # tracks everything.
        #
        # WAS: miles, faced, escaped = travel_to(...)
        # WAS: current_city = final_dest
        # WAS: total_miles = total_miles + miles
        # WAS: total_hazards = total_hazards + faced
        # WAS: total_escaped = total_escaped + escaped
        # WAS: visited.append(final_dest)
        # WAS: unique_cities.add(final_dest)
        # NOW: all of that happens inside execute_travel()
        # ----------------------------------------------------------
        execute_travel(final_dest, dist, hazards, player)

    # ----------------------------------------------------------
    # FINAL REPORT
    # WAS: used local variables directly
    # NOW: all data comes from player getter methods
    # ----------------------------------------------------------
    print()
    print('=' * 55)
    print('FINAL TRIP REPORT')
    print('=' * 55)

    # WAS: print(f'Driver: {name}')
    print(f'Driver: {player.get_name()}')

    # WAS: print(f'Final City: {current_city}')
    print(f'Final City: {player.get_current_city()}')
    print()

    # WAS: print('  ' + ' -> '.join(visited))
    print('ROUTE:')
    print(f'  {player.get_route_string()}')
    print()

    # WAS: print(f'UNIQUE CITIES ({len(unique_cities)}):')
    # WAS: for city in sorted(unique_cities): ...
    print(f'UNIQUE CITIES ({player.get_unique_city_count()}):')
    for city in sorted(player.get_unique_cities()):
        print(f'  - {city}')
    print()

    print('TRIVIA:')
    # WAS: print(f'  Asked: {trivia_asked}')
    # WAS: print(f'  Correct: {trivia_correct}')
    # WAS: pct = (trivia_correct / trivia_asked) * 100 ...
    print(f'  Asked: {player.get_trivia_asked()}')
    print(f'  Correct: {player.get_trivia_correct()}')
    print(f'  Accuracy: {player.get_trivia_accuracy()}')
    print()

    print('HAZARDS:')
    # WAS: print(f'  Faced: {total_hazards}')
    # WAS: print(f'  Escaped: {total_escaped}')
    # WAS: print(f'  Unique types: {len(unique_hazards)}')
    print(f'  Faced: {player.get_hazards_faced()}')
    print(f'  Escaped: {player.get_hazards_escaped()}')
    print(f'  Unique types: {player.get_unique_hazard_count()}')
    print()

    print('STATS:')
    # WAS: print(f'  Total Miles: {total_miles}')
    print(f'  Total Miles: {player.get_total_miles()}')
    print()


# ============================================================
# ENTRY POINT GUARD
# ============================================================
# The same pattern you have used all semester.
# When Python runs this file directly, __name__ is '__main__'
# and main() is called. If this file were imported by another
# file, main() would not run automatically.

if __name__ == '__main__':
    main()
