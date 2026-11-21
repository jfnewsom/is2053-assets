"""
city.py
Lab 5.1: Meet the Cities
Deep in the Heart: A Lone Star Journey

Student Name: SOLUTION
UTSA ID: SOLUTION
Section: SOLUTION

Description: The City class. Each City object holds one city's name,
type, tagline, and roads, and answers questions about that city.

Chapter 10 Concepts: a class, __init__, self, private attributes,
getters and setters, __str__
"""

import random


class City:
    """
    One city in the road trip game.

    Private attributes:
        __name (str): The city's name, like 'San Antonio'
        __city_type (str): Its type from city_info.txt, like 'WIN'
        __tagline (str): Its tagline from city_info.txt
        __connections (dict): Each road: destination name -> miles
    """

    def __init__(self, name, city_type, tagline):
        """
        Make a City with no roads yet.

        Args:
            name (str): The city's name
            city_type (str): The city's type
            tagline (str): The city's tagline
        """
        self.__name = name
        self.__city_type = city_type
        self.__tagline = tagline
        self.__connections = {}

    def get_name(self):
        """Return the city's name."""
        return self.__name

    def set_name(self, name):
        """Change the city's name."""
        self.__name = name

    def get_type(self):
        """Return the city's type."""
        return self.__city_type

    def set_type(self, city_type):
        """Change the city's type."""
        self.__city_type = city_type

    def get_tagline(self):
        """Return the city's tagline."""
        return self.__tagline

    def set_tagline(self, tagline):
        """Change the city's tagline."""
        self.__tagline = tagline

    def add_connection(self, dest, miles):
        """
        Add a road from this city to another one.

        Args:
            dest (str): The destination's name
            miles (int): The miles to it
        """
        self.__connections[dest] = miles

    def display_destinations(self):
        """
        Show the numbered menu of this city's destinations.

        Returns:
            int: How many destinations the menu shows
        """
        print(f'From {self.__name}, you can travel to:')
        option_num = 1
        for dest in self.__connections:
            miles = self.__connections[dest]
            print(f'  {option_num}. {dest} - {miles} miles')
            option_num = option_num + 1
        return len(self.__connections)

    def get_destination(self, choice):
        """
        Look up the destination for a menu choice.

        Args:
            choice (int): The menu number the player chose, from 1

        Returns:
            tuple: The destination and its distance
        """
        dests = list(self.__connections.keys())
        dest = dests[choice - 1]
        return dest, self.__connections[dest]

    def get_distance_to(self, dest):
        """
        Return the miles from this city to one it connects to.

        Args:
            dest (str): The destination's name

        Returns:
            int: The miles to it
        """
        return self.__connections[dest]

    def get_redirect(self, avoid):
        """
        Pick a random destination other than the one the player wanted.

        Args:
            avoid (str): The destination the player wanted

        Returns:
            tuple: Another destination and its distance, or the only one
            there is when the city has a single road
        """
        options = list(self.__connections.keys())
        if avoid in options:
            options.remove(avoid)
        if len(options) > 0:
            index = random.randint(0, len(options) - 1)
            dest = options[index]
            return dest, self.__connections[dest]
        else:
            only_option = list(self.__connections.keys())[0]
            return only_option, self.__connections[only_option]

    def is_win_city(self):
        """Return True if this city is a beach that wins the game."""
        return self.__city_type == 'WIN'

    def is_dead_end(self):
        """Return True if this city is a dead end: nowhere to go but home."""
        city_type = self.__city_type
        return city_type == 'DEAD_END' or city_type == 'WRONG_WAY'

    def __str__(self):
        """Return the city as text, like 'San Antonio (START)'."""
        return f'{self.__name} ({self.__city_type})'


# ============================================================
# Quick self-test when running this file directly.
# ============================================================
def main():
    """Quick checks of the City class."""
    print('Testing city.py...')
    home = City('San Antonio', 'START', 'Home of the Alamo')
    beach = City('Corpus Christi', 'WIN', 'Sparkling City by the Sea')
    print(f'  {home}')
    print(f'  {beach}')
    print(f'  get_name() => {beach.get_name()}')
    print(f'  get_type() => {beach.get_type()}')
    print(f'  get_tagline() => {beach.get_tagline()}')
    print(f'  is_win_city() => {beach.is_win_city()}')
    spot = City('Nowhere', 'HUB', 'Nothing to see')
    spot.set_name('Test Town')
    spot.set_type('DEAD_END')
    spot.set_tagline('Population: one tester')
    print(f'  set_name() => {spot.get_name()}')
    print(f'  set_type() => {spot.get_type()}')
    print(f'  set_tagline() => {spot.get_tagline()}')
    print('  City class loaded successfully.')


if __name__ == '__main__':
    main()
