"""
function_library.py
A collection of reusable functions for the road trip game.

Student Name: SOLUTION
UTSA ID: SOLUTION
Section: SOLUTION

This module grows throughout the semester!
"""

import random


# ============================================================
# CONSTANTS
# ============================================================
D20_MIN = 1
D20_MAX = 20
SAVE_FILE = 'savegame.txt'


# ============================================================
# RANDOM FUNCTIONS (Added in Lab 2-2)
# ============================================================

def flip_coin():
    """
    Flip a coin and return the result.

    Returns:
        str: 'HEADS' or 'TAILS'
    """
    result = random.randint(1, 2)
    if result == 1:
        return 'HEADS'
    else:
        return 'TAILS'


def roll_d20():
    """
    Roll a 20-sided die.

    Returns:
        int: Random number from 1 to 20
    """
    return random.randint(D20_MIN, D20_MAX)


def check_percentage(percent):
    """
    Return True a certain percentage of the time.

    Args:
        percent (int): The percentage chance (0-100)

    Returns:
        bool: True if the roll is within the percentage
    """
    roll = random.randint(1, 100)
    return roll <= percent


# ============================================================
# STRING UTILITIES (Added in Lab 4-3)
# ============================================================

def clean_input(prompt):
    """
    Ask a question and return the answer without spaces, in capitals.

    Args:
        prompt (str): The prompt to show

    Returns:
        str: What the player typed, stripped and uppercased
    """
    return input(prompt).strip().upper()


# ============================================================
# VALIDATION FUNCTIONS (Added in Lab 2-3)
# ============================================================

def get_valid_int(prompt, min_val, max_val):
    """
    Ask until the player types a whole number in a range.

    Args:
        prompt (str): The prompt to show
        min_val (int): The lowest number allowed
        max_val (int): The highest number allowed

    Returns:
        int: A whole number from min_val to max_val
    """
    value = 0
    valid = False
    while not valid:
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            print('ERROR: Please enter a valid whole number.')
        else:
            value = int(user_input)
            if value < min_val or value > max_val:
                print(f'ERROR: Enter a number between '
                      f'{min_val} and {max_val}.')
            else:
                valid = True
    return value


def get_yes_no(prompt):
    """
    Ask until the player answers y or n.

    Args:
        prompt (str): The prompt to show

    Returns:
        bool: True for yes, False for no
    """
    answer = input(prompt).strip().upper()
    while answer != 'Y' and answer != 'N':
        print("ERROR: Please enter 'y' or 'n'.")
        answer = input(prompt).strip().upper()
    return answer == 'Y'


# ============================================================
# SAVE AND LOAD (Moved here in Lab 3-2)
# ============================================================

def save_game(player_name, current_city, total_miles, total_turns,
              total_hazards, total_escaped, games_played,
              session_miles, session_hazards, visited_cities,
              hazards_list):
    """
    Save the game to SAVE_FILE: nine values, one on each line, then
    the route, a marker line, and the hazards.

    Args:
        player_name (str): The player's name
        current_city (str): Where the player is now
        total_miles (int): Miles so far this game
        total_turns (int): Turns so far this game
        total_hazards (int): Hazards faced so far this game
        total_escaped (int): Hazards escaped so far this game
        games_played (int): Games finished this session
        session_miles (int): Miles in the finished games
        session_hazards (int): Hazards in the finished games
        visited_cities (list): Every city this game, in order
        hazards_list (list): Every hazard this game, in order
    """
    outfile = open(SAVE_FILE, 'w')
    outfile.write(player_name + '\n')
    outfile.write(current_city + '\n')
    outfile.write(str(total_miles) + '\n')
    outfile.write(str(total_turns) + '\n')
    outfile.write(str(total_hazards) + '\n')
    outfile.write(str(total_escaped) + '\n')
    outfile.write(str(games_played) + '\n')
    outfile.write(str(session_miles) + '\n')
    outfile.write(str(session_hazards) + '\n')
    for city in visited_cities:
        outfile.write(city + '\n')
    outfile.write('---LISTS_END---\n')
    for hazard in hazards_list:
        outfile.write(hazard + '\n')
    outfile.close()
    print('Game saved!')


def load_game():
    """
    Load the game from SAVE_FILE.

    Returns:
        tuple: The nine saved values, then the route and the hazards,
        in the order save_game() writes them, or None if there is no
        save file or it can't be read
    """
    try:
        infile = open(SAVE_FILE, 'r')
        player_name = infile.readline().rstrip('\n')
        current_city = infile.readline().rstrip('\n')
        total_miles = int(infile.readline().rstrip('\n'))
        total_turns = int(infile.readline().rstrip('\n'))
        total_hazards = int(infile.readline().rstrip('\n'))
        total_escaped = int(infile.readline().rstrip('\n'))
        games_played = int(infile.readline().rstrip('\n'))
        session_miles = int(infile.readline().rstrip('\n'))
        session_hazards = int(infile.readline().rstrip('\n'))

        # The route, up to the marker line
        visited_cities = []
        line = infile.readline().rstrip('\n')
        while line != '---LISTS_END---' and line != '':
            visited_cities.append(line)
            line = infile.readline().rstrip('\n')

        # The hazards, up to the end of the file
        hazards_list = []
        line = infile.readline().rstrip('\n')
        while line != '':
            hazards_list.append(line)
            line = infile.readline().rstrip('\n')

        infile.close()
        return (player_name, current_city, total_miles, total_turns,
                total_hazards, total_escaped, games_played,
                session_miles, session_hazards, visited_cities,
                hazards_list)
    except (FileNotFoundError, ValueError):
        return None


# ============================================================
# DISPLAY HELPERS (Added in Lab 3-2)
# ============================================================

def display_numbered_list(items, title):
    """
    Show a title, an underline, and the items numbered from 1.

    Args:
        items (list): The items to show
        title (str): The title above them
    """
    print(title)
    print('-' * len(title))
    for i in range(len(items)):
        print(f'  {i + 1}. {items[i]}')
    print()


# ============================================================
# CITY DATA LOADERS (Added in Lab 4-1)
# ============================================================

def load_city_distances(filename):
    """
    Read the city routes from a file into a nested dictionary.

    Args:
        filename (str): The file to read, one city1,city2,miles per line

    Returns:
        dict: distances[city1][city2] is the miles from city1 to city2
    """
    distances = {}
    infile = open(filename, 'r')
    for line in infile:
        parts = line.strip().split(',')
        city1 = parts[0]
        city2 = parts[1]
        miles = int(parts[2])
        if city1 not in distances:
            distances[city1] = {}
        distances[city1][city2] = miles
    infile.close()
    return distances


def load_city_info(filename):
    """
    Read each city's type and tagline from a file into a dictionary.

    Args:
        filename (str): The file to read, one city,type,tagline per line

    Returns:
        dict: info[city] is {'type': ..., 'tagline': ...}
    """
    info = {}
    infile = open(filename, 'r')
    for line in infile:
        parts = line.strip().split(',')
        city = parts[0]
        city_type = parts[1]
        tagline = parts[2]
        info[city] = {'type': city_type, 'tagline': tagline}
    infile.close()
    return info


# ============================================================
# HAZARD FUNCTIONS (Added in Lab 4-2)
# ============================================================

def load_hazards(filename):
    """
    Read the hazards from a file into a list of dictionaries.

    Args:
        filename (str): The file to read, one name,heads,tails per line

    Returns:
        list: One dictionary per hazard, with 'name', 'heads', and 'tails'
    """
    hazards = []
    infile = open(filename, 'r')
    for line in infile:
        parts = line.strip().split(',')
        hazard = {'name': parts[0], 'heads': parts[1], 'tails': parts[2]}
        hazards.append(hazard)
    infile.close()
    return hazards


def handle_hazard(hazards):
    """
    Pick a random hazard, show it, and flip to see if the player escapes.

    Args:
        hazards (list): The list of dictionaries from load_hazards()

    Returns:
        tuple: The hazard's name, and True if the player escaped
    """
    hazard = random.choice(hazards)
    print('*** HAZARD! ***')
    print(hazard['name'])
    flip = flip_coin()
    print(f'{flip}!')
    if flip == 'HEADS':
        print(hazard['heads'])
        return hazard['name'], True
    else:
        print(hazard['tails'])
        return hazard['name'], False


# ============================================================
# TRIVIA FUNCTIONS (Added in Lab 4-3)
# ============================================================

def load_trivia(filename):
    """
    Read the trivia from a file into a dictionary of lists.

    Args:
        filename (str): The file to read, one city,question,answer per line

    Returns:
        dict: trivia[city] is a list of {'question': ..., 'answer': ...}
    """
    trivia = {}
    infile = open(filename, 'r')
    for line in infile:
        parts = line.strip().split(',')
        city = parts[0]
        question = parts[1]
        answer = parts[2]
        if city not in trivia:
            trivia[city] = []
        trivia[city].append({'question': question, 'answer': answer})
    infile.close()
    return trivia


def main():
    """Quick self-test for the library."""
    print('Testing function_library.py...')
    print(f'  flip_coin() => {flip_coin()}')
    print(f'  roll_d20() => {roll_d20()}')
    print(f'  check_percentage(50) => {check_percentage(50)}')
    print('  Library loaded successfully.')


if __name__ == '__main__':
    main()
