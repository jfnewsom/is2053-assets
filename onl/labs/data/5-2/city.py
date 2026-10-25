"""
city.py
Reference City class for Lab 5.2: Deep in the Heart

Provided by Bat City Collective as a backup. It is the Lab 5.1 City
class. If your own city.py from Lab 5.1 works, keep using it. Use
this file only if yours is broken, so you can still run lab-5-2.py
and test your player.py. You don't submit city.py in Lab 5.2.

Chapter 10 Concepts: class, __init__, self, private attributes,
                     accessor and mutator methods, __str__
"""

import random


class City:
    """
    One city in the road trip game.

    Private attributes:
        __name (str): The city's name, like 'San Antonio'
        __city_type (str): 'START', 'WIN', 'DEAD_END', 'WRONG_WAY', etc.
        __tagline (str): The city's motto
        __connections (dict): destination name -> miles
    """

    def __init__(self, name, city_type, tagline):
        """
        Create a City with no road connections yet.

        Args:
            name (str): The city's name
            city_type (str): The city's type from city_info.txt
            tagline (str): The city's motto from city_info.txt
        """
        self.__name = name
        self.__city_type = city_type
        self.__tagline = tagline
        self.__connections = {}

    # ========================================================
    # ACCESSORS AND MUTATOR
    # ========================================================

    def get_name(self):
        """Return the city's name."""
        return self.__name

    def get_type(self):
        """Return the city's type."""
        return self.__city_type

    def get_tagline(self):
        """Return the city's tagline."""
        return self.__tagline

    def add_connection(self, dest, miles):
        """
        Add a road from this city to another one.

        Args:
            dest (str): The destination city's name
            miles (int): Distance to that city
        """
        self.__connections[dest] = miles

    # ========================================================
    # DESTINATION METHODS
    # ========================================================

    def display_destinations(self):
        """
        Display a numbered menu of this city's destinations.

        Returns:
            int: The number of destinations shown
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
        Return the destination and distance for a menu choice.

        Args:
            choice (int): 1-based menu choice

        Returns:
            tuple: (destination_name, distance_in_miles)
        """
        dests = list(self.__connections.keys())
        index = choice - 1
        dest = dests[index]
        return dest, self.__connections[dest]

    def get_distance_to(self, dest):
        """
        Return the miles from this city to a connected city.

        Args:
            dest (str): A destination this city connects to

        Returns:
            int: Distance in miles
        """
        return self.__connections[dest]

    def get_redirect(self, avoid):
        """
        Pick a random destination other than 'avoid'.

        If 'avoid' is the only destination, return it anyway.

        Args:
            avoid (str): The destination to leave out

        Returns:
            tuple: (destination_name, distance_in_miles)
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

    # ========================================================
    # TYPE CHECKS AND DISPLAY
    # ========================================================

    def is_win_city(self):
        """Return True if this city is a beach (type 'WIN')."""
        return self.__city_type == 'WIN'

    def is_dead_end(self):
        """Return True if this city is a 'DEAD_END' or 'WRONG_WAY'."""
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
    print(f'  is_win_city() => {beach.is_win_city()}')
    print('  City class loaded successfully.')


if __name__ == '__main__':
    main()
