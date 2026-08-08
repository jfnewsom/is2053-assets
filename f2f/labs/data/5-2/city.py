"""
city.py
City class for the road trip game.

Provided by Bat City Collective as a reference implementation.

This is a working City class that satisfies every method call made by
lab-5-2.py and every test in test.py. If your own city.py from Lab 5.1
is working, keep using it - you will get full Lab 5.1 credit when you
submit player.py.

Use this file only as a backup if your own city.py is broken or missing,
so you can still complete and test Lab 5.2.

Chapter 10 Concepts:
- Class definition with class keyword
- __init__ constructor
- Private attributes with __ prefix
- Getter methods
- __str__ method
"""


class City:
    """
    Represents a city in the Texas road trip game.

    Attributes (private):
        __name (str): City name
        __city_type (str): Type of city
        __tagline (str): City motto
        __connections (dict): Connected cities and distances
    """

    def __init__(self, name, city_type, tagline):
        """
        Initialize a City object.

        Args:
            name (str): City name
            city_type (str): Type ('START', 'HUB', 'WIN', 'DEAD_END')
            tagline (str): City's motto
        """
        self.__name = name
        self.__city_type = city_type
        self.__tagline = tagline
        self.__connections = {}

    # --- Getter Methods ---

    def get_name(self):
        """Return the city's name."""
        return self.__name

    def get_type(self):
        """Return the city's type."""
        return self.__city_type

    def get_tagline(self):
        """Return the city's tagline."""
        return self.__tagline

    # --- Connection Methods ---

    def add_connection(self, city_name, distance):
        """Add a connection to another city."""
        self.__connections[city_name] = distance

    def get_distance_to(self, city_name):
        """Get distance to a connected city. Returns -1 if not connected."""
        return self.__connections.get(city_name, -1)

    def get_destination_names(self):
        """Return list of connected city names."""
        return list(self.__connections.keys())

    # --- Status Methods ---

    def is_win_city(self):
        """Return True if this is a winning destination (beach)."""
        return self.__city_type == 'WIN'

    def is_dead_end(self):
        """Return True if this is a dead end or wrong-way city."""
        return self.__city_type in ['DEAD_END', 'WRONG_WAY']

    # --- Display Methods ---

    def display_destinations(self):
        """Display available destinations from this city."""
        prompt = 'you can travel to:'
        print(f'From {self.__name}, {prompt}')
        option_num = 1
        for dest_name, distance in self.__connections.items():
            print(f'  {option_num}. {dest_name} - {distance} miles')
            option_num = option_num + 1

    def get_arrival_message(self):
        """Return arrival message for this city."""
        if self.__city_type == 'WIN':
            return f'YOU MADE IT TO {self.__name.upper()}! THE BEACH AWAITS!'
        elif self.__city_type == 'DEAD_END':
            return f'{self.__name} is a dead end. No beach here!'
        elif self.__city_type == 'WRONG_WAY':
            return f'{self.__name}? That\'s the wrong way entirely!'
        else:
            return f'Welcome to {self.__name}!'

    def __str__(self):
        """Return string representation of the city."""
        return f'{self.__name} ({self.__city_type})'
