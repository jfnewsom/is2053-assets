"""
Lab 5.2: Deep in the Heart
Deep in the Heart: A Lone Star Journey

Provided by Bat City Collective. You don't submit this file:
CodeGrade runs its own copy with your player.py. The only changes
to make here are the test pins the lab sheet tells you to make.

What changed from Lab 5.1: one thing. The variables that tracked a
trip (current_city, total_miles, total_turns, total_hazards,
total_escaped, visited_cities, hazards_list, unique_cities,
unique_hazards, trivia_asked, and trivia_correct) now live inside
one Player object, built from player.py. Every place the game used
to change one of them now calls a Player method instead. Look for
the WAS / NOW comments: each one shows a Lab 5.1 line and the
Player call that replaced it.

Everything else is your Lab 5.1 game: the same loaders, cities,
trivia gate, travel loop, save and load, and trip report. Every
line it prints is the same.

Files it needs in the same folder:
- player.py (yours, this lab)
- city.py (yours, from Lab 5.1)
- function_library.py (yours, from Lab 5.1)
- city_distances.txt, city_info.txt, hazards.txt, trivia.txt
"""

import random
import function_library
from city import City
from player import Player

# ============================================================
# CONSTANTS
# ============================================================
DISTANCES_FILE = 'city_distances.txt'
INFO_FILE = 'city_info.txt'
HAZARDS_FILE = 'hazards.txt'
TRIVIA_FILE = 'trivia.txt'
REPORT_FILE = 'trip_report.txt'

MILES_MULTIPLIER = 10
HAZARD_CHANCE = 30


def build_cities(distances, city_info):
    """
    Build one City object for every city in the data files.

    Args:
        distances (dict): distances[city1][city2] = miles
        city_info (dict): city_info[city] = {'type': ..., 'tagline': ...}

    Returns:
        dict: cities[city_name] = City object
    """
    cities = {}
    for name in city_info:
        info = city_info[name]
        cities[name] = City(name, info['type'], info['tagline'])

    for name in distances:
        for dest in distances[name]:
            cities[name].add_connection(dest, distances[name][dest])

    return cities


def trivia_gate(dest, trivia, city):
    """
    Ask a TRUE/FALSE trivia question about the destination.

    A right answer earns the trip. A wrong or invalid answer detours
    the player through the City's get_redirect.

    Args:
        dest (str): The destination the player chose
        trivia (dict): trivia[city] -> list of {'question','answer'}
        city (City): The City object for the current city

    Returns:
        tuple: (final_dest, distance, correct_bool)
    """
    print()
    print('--- TRIVIA TIME! ---')
    print(f'To reach {dest}, answer this question:')
    print()

    q = random.choice(trivia[dest])

    print(f'  {q["question"]}')
    print()

    answer = function_library.clean_input('TRUE or FALSE? ')

    if answer == 'T' or answer == 'TRUE':
        player_answer = 'TRUE'
    elif answer == 'F' or answer == 'FALSE':
        player_answer = 'FALSE'
    else:
        print('Invalid answer! Counting as wrong.')
        player_answer = 'INVALID'

    if player_answer == q['answer']:
        print('CORRECT! You earned your destination.')
        return dest, city.get_distance_to(dest), True
    else:
        print(f'WRONG. The answer was {q["answer"]}.')
        redirect, redirect_miles = city.get_redirect(dest)
        print(f'Detour! You ended up going to {redirect} instead.')
        return redirect, redirect_miles, False


def save_trip_report(filename, player, status):
    """
    Write a formatted trip report to disk.

    WAS: save_trip_report took thirteen arguments, one per variable.
    NOW: it takes the Player and asks it for each value.

    Args:
        filename (str): Where to write the report
        player (Player): The player whose trip this is
        status (str): One of 'BEACH WINNER!', 'Dead End',
                      'Quit without saving', 'Trip Incomplete'
    """
    outfile = open(filename, 'w')

    outfile.write('DEEP IN THE HEART - TRIP REPORT\n')
    outfile.write('=' * 40 + '\n')
    outfile.write(f'Driver: {player.get_name()}\n')
    outfile.write(f'Final City: {player.get_current_city()}\n')
    outfile.write(f'Status: {status}\n')
    outfile.write('\n')

    outfile.write('ROUTE:\n')
    route_str = ' -> '.join(player.get_visited_cities())
    outfile.write(f'  {route_str}\n')
    unique_count = len(player.get_unique_cities())
    outfile.write(f'  Unique cities visited: {unique_count}\n')
    outfile.write('\n')

    total_hazards = player.get_total_hazards()
    total_escaped = player.get_total_escaped()
    outfile.write('STATISTICS:\n')
    outfile.write(f'  Total Miles: {player.get_total_miles()}\n')
    outfile.write(f'  Total Turns: {player.get_total_turns()}\n')
    outfile.write(f'  Hazards Faced: {total_hazards}\n')
    outfile.write(f'  Hazards Escaped: {total_escaped}\n')
    if total_hazards > 0:
        rate = (total_escaped / total_hazards) * 100
        rate_str = f'{rate:.1f}'
        outfile.write(f'  Escape Rate: {rate_str}%\n')
    outfile.write('\n')

    trivia_asked = player.get_trivia_asked()
    trivia_correct = player.get_trivia_correct()
    outfile.write('TRIVIA:\n')
    outfile.write(f'  Questions Asked: {trivia_asked}\n')
    outfile.write(f'  Answered Correct: {trivia_correct}\n')
    if trivia_asked > 0:
        accuracy = (trivia_correct / trivia_asked) * 100
        accuracy_str = f'{accuracy:.1f}'
        outfile.write(f'  Accuracy: {accuracy_str}%\n')
    outfile.write('\n')

    outfile.write('HAZARDS (A-Z):\n')
    sorted_hazards = sorted(player.get_unique_hazards())
    if len(sorted_hazards) > 0:
        for hazard in sorted_hazards:
            outfile.write('  - ' + hazard + '\n')
    else:
        outfile.write('  None - Lucky traveler!\n')
    outfile.write('\n')

    outfile.write('=' * 40 + '\n')
    outfile.close()


def main():
    """Main game function."""
    print()
    print('=' * 50)
    print('DEEP IN THE HEART: A LONE STAR JOURNEY')
    print('=' * 50)
    print()

    print('Loading city data...')
    distances = function_library.load_city_distances(DISTANCES_FILE)
    city_info = function_library.load_city_info(INFO_FILE)
    hazards = function_library.load_hazards(HAZARDS_FILE)
    trivia = function_library.load_trivia(TRIVIA_FILE)
    print(f'Loaded {len(distances)} cities with travel routes.')
    print(f'Loaded {len(city_info)} city info records.')
    print(f'Loaded {len(hazards)} possible hazards.')
    total_questions = 0
    for city in trivia:
        total_questions = total_questions + len(trivia[city])
    print(f'Loaded {total_questions} trivia questions across '
          f'{len(trivia)} cities.')
    print()

    cities = build_cities(distances, city_info)

    # ============================================================
    # MAIN MENU LOOP - outermost
    # ============================================================
    in_program = True
    while in_program:

        print('MAIN MENU')
        print('-' * 20)
        print('1. New Game')
        print('2. Load Saved Game')
        print('3. Quit')
        print()

        main_choice = function_library.get_valid_int(
            'Choice (1-3): ', 1, 3)
        print()

        if main_choice == 3:
            print('Thanks for playing!')
            in_program = False
            continue

        resumed_game = False

        if main_choice == 2:
            saved = function_library.load_game()
            if saved is None:
                print('No usable save file found. Starting new game.')
                print()
                main_choice = 1
            else:
                (player_name, current_city, total_miles, total_turns,
                 total_hazards, total_escaped, games_played,
                 session_miles, session_hazards,
                 visited_cities, hazards_list) = saved
                print(f'Welcome back, {player_name}!')
                print(f'Resuming from {current_city}.')
                print(f'Miles so far this game: {total_miles}')
                print(f'Games completed this session: {games_played}')
                print()
                resumed_game = True

        if main_choice == 1:
            player_name = input('What is your name, traveler? ')
            print()
            print(f'Welcome, {player_name}!')
            print('You are in San Antonio. Your goal: reach the beach!')
            print('Beach cities: Corpus Christi and Galveston.')
            print()

            games_played = 0
            session_miles = 0
            session_hazards = 0

        # ============================================================
        # PLAY-AGAIN LOOP - middle
        # ============================================================
        play_again = True
        while play_again:

            # WAS: eleven variables reset here at the start of every
            #      game (current_city = 'San Antonio', total_miles = 0,
            #      ... trivia_correct = 0, unique_cities = set(...)).
            # NOW: one new Player starts every game in San Antonio.
            player = Player(player_name)
            if resumed_game:
                # WAS: the eleven variables came straight from the save.
                # NOW: the new Player picks up the saved trip.
                player.resume(current_city, total_miles, total_turns,
                              total_hazards, total_escaped,
                              visited_cities, hazards_list)

            reached_beach = False
            saved_and_quit = False
            quit_without_saving = False
            hit_dead_end = False

            start = cities[player.get_current_city()]
            if resumed_game and start.is_win_city():
                reached_beach = True
                playing = False
            else:
                playing = True

            resumed_game = False

            # ============================================================
            # IN-GAME LOOP - innermost
            # ============================================================
            while playing:

                # WAS: current_city
                # NOW: player.get_current_city()
                here = cities[player.get_current_city()]
                print(f'You are in: {player.get_current_city()}')
                print(f'  "{here.get_tagline()}"')
                print()

                num_choices = here.display_destinations()
                print()
                choice = function_library.get_valid_int(
                    f'Choice (1-{num_choices}): ', 1, num_choices)
                print()

                wanted, _ = here.get_destination(choice)
                destination, distance, correct = trivia_gate(
                    wanted, trivia, here)
                # WAS: trivia_asked = trivia_asked + 1
                #      if correct: trivia_correct = trivia_correct + 1
                # NOW: one call does both.
                player.record_trivia(correct)

                print(f'You\'re headed to {destination}!')
                print(f'Distance: {distance} miles')
                print()

                print('=' * 50)
                print(f'TRAVELING TO {destination.upper()}!')
                print('=' * 50)
                print()

                miles_remaining = distance
                leg_turns = 0
                leg_miles = 0

                while miles_remaining > 0:
                    leg_turns = leg_turns + 1
                    print(f'--- Turn {leg_turns} ---')
                    print(f'Miles remaining: {miles_remaining}')

                    roll = function_library.roll_d20()
                    miles_this_turn = roll * MILES_MULTIPLIER
                    print(f'You rolled a {roll}!')
                    print(f'You travel {miles_this_turn} miles...')

                    miles_remaining = miles_remaining - miles_this_turn
                    leg_miles = leg_miles + miles_this_turn

                    if miles_remaining <= 0:
                        print()
                        print(f'You made it to {destination}!')
                    else:
                        print(f'Miles remaining: {miles_remaining}')

                        if function_library.check_percentage(
                                HAZARD_CHANCE):
                            print()
                            name, escaped = (
                                function_library.handle_hazard(hazards))
                            # WAS: hazards_faced, hazards_escaped,
                            #      hazards_list.append(name), and
                            #      unique_hazards.add(name)
                            # NOW: one call records the hazard.
                            player.record_hazard(name, escaped)

                    print()

                # WAS: total_miles, total_turns, current_city,
                #      visited_cities.append, and unique_cities.add
                # NOW: one call records the arrival.
                player.travel_to(destination, leg_miles, leg_turns)
                here = cities[player.get_current_city()]

                if here.is_win_city():
                    print('=' * 50)
                    print('CONGRATULATIONS! YOU REACHED THE BEACH!')
                    print('=' * 50)
                    print()
                    reached_beach = True
                    playing = False

                elif here.is_dead_end():
                    print(f'{player.get_current_city()} is a dead end!')
                    print(f'  "{here.get_tagline()}"')
                    print()
                    if function_library.get_yes_no(
                            'Return to San Antonio? (y/n): '):
                        # WAS: current_city = 'San Antonio', plus the
                        #      append and the add
                        # NOW: an arrival with no miles and no turns
                        player.travel_to('San Antonio', 0, 0)
                        print()
                    else:
                        hit_dead_end = True
                        playing = False

                else:
                    print('OPTIONS:')
                    print('  1. Continue journey')
                    print('  2. Save and quit')
                    print('  3. Quit without saving')
                    print()
                    opt = function_library.get_valid_int(
                        'Choice (1-3): ', 1, 3)
                    print()

                    if opt == 2:
                        function_library.save_game(
                            player_name, player.get_current_city(),
                            player.get_total_miles(),
                            player.get_total_turns(),
                            player.get_total_hazards(),
                            player.get_total_escaped(),
                            games_played, session_miles,
                            session_hazards,
                            player.get_visited_cities(),
                            player.get_hazards_list())
                        saved_and_quit = True
                        playing = False
                    elif opt == 3:
                        quit_without_saving = True
                        playing = False

            # ============================================================
            # AFTER IN-GAME LOOP - FINAL TRIP REPORT
            # ============================================================
            if saved_and_quit:
                play_again = False
                continue

            if reached_beach:
                status = 'BEACH WINNER!'
            elif hit_dead_end:
                status = 'Dead End'
            elif quit_without_saving:
                status = 'Quit without saving'
            else:
                status = 'Trip Incomplete'

            sorted_unique_hazards = sorted(player.get_unique_hazards())

            print()
            print('=' * 50)
            print('FINAL TRIP REPORT')
            print('=' * 50)
            print(f'Driver: {player.get_name()}')
            print(f'Final City: {player.get_current_city()}')
            print(f'Status: {status}')
            print()

            function_library.display_numbered_list(
                player.get_visited_cities(), 'YOUR ROUTE')
            unique_count = len(player.get_unique_cities())
            print(f'Unique cities visited: {unique_count}')
            print()

            if len(sorted_unique_hazards) > 0:
                function_library.display_numbered_list(
                    sorted_unique_hazards,
                    'HAZARDS ENCOUNTERED (Unique, A-Z)')
            else:
                print('HAZARDS ENCOUNTERED (Unique, A-Z)')
                print('-' * len('HAZARDS ENCOUNTERED (Unique, A-Z)'))
                print('  None - Lucky traveler!')
                print()

            total_hazards = player.get_total_hazards()
            total_escaped = player.get_total_escaped()
            print('STATISTICS')
            print('-' * len('STATISTICS'))
            print(f'  Total Miles: {player.get_total_miles()}')
            print(f'  Total Turns: {player.get_total_turns()}')
            print(f'  Hazards Faced: {total_hazards}')
            print(f'  Hazards Escaped: {total_escaped}')
            if total_hazards > 0:
                escape_rate = (total_escaped / total_hazards) * 100
                escape_rate_str = f'{escape_rate:.1f}'
                print(f'  Escape Rate: {escape_rate_str}%')
            print()

            trivia_asked = player.get_trivia_asked()
            trivia_correct = player.get_trivia_correct()
            print('TRIVIA')
            print('-' * len('TRIVIA'))
            print(f'  Questions Asked: {trivia_asked}')
            print(f'  Answered Correct: {trivia_correct}')
            if trivia_asked > 0:
                accuracy = (trivia_correct / trivia_asked) * 100
                accuracy_str = f'{accuracy:.1f}'
                print(f'  Accuracy: {accuracy_str}%')
            print()
            print('=' * 50)
            print()

            # WAS: thirteen arguments
            # NOW: the Player carries them
            save_trip_report(REPORT_FILE, player, status)
            print(f'Trip report saved to {REPORT_FILE}.')
            print()

            games_played = games_played + 1
            session_miles = session_miles + player.get_total_miles()
            session_hazards = session_hazards + player.get_total_hazards()

            play_again = function_library.get_yes_no(
                'Play again? (y/n): ')
            print()

        # ============================================================
        # AFTER PLAY-AGAIN LOOP
        # ============================================================
        if not saved_and_quit:
            print('=' * 50)
            print('SESSION STATISTICS')
            print('=' * 50)
            print(f'Games Played: {games_played}')
            print(f'Total Miles: {session_miles}')
            print(f'Total Hazards: {session_hazards}')
            print('=' * 50)
            print()
            print(f'Thanks for playing, {player_name}!')
            print('An All My Eggses Live in Texas Production')
            print()


if __name__ == '__main__':
    main()
