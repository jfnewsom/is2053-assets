# demo_04_dynamic_menu.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Dynamic travel menu generated from CITY_DISTANCES + CITY_INFO

def main():
    CITY_DISTANCES = {
        'San Antonio': {
            'Houston':        200,
            'Austin':          80,
            'Corpus Christi': 150,
            'Laredo':         160,
        }
    }

    CITY_INFO = {
        'San Antonio':    {'type': 'START',    'tagline': 'Home of the Alamo'},
        'Houston':        {'type': 'GATEWAY',  'tagline': 'Space City'},
        'Austin':         {'type': 'GATEWAY',  'tagline': 'Keep Austin Weird'},
        'Corpus Christi': {'type': 'WIN',      'tagline': 'Sparkling City by the Sea'},
        'Laredo':         {'type': 'DEAD_END', 'tagline': 'Gateway to Mexico'},
    }

    current_city = 'San Antonio'

    print(f'You are in {current_city}')
    print(f'  "{CITY_INFO[current_city]["tagline"]}"')
    print()
    print(f'From {current_city}, you can travel to:')
    print()

    option = 1
    for destination, miles in CITY_DISTANCES[current_city].items():
        city_type = CITY_INFO[destination]['type']
        marker = ''
        if city_type == 'WIN':
            marker = '  [BEACH!]'
        elif city_type == 'DEAD_END':
            marker = '  [Dead End]'
        elif city_type == 'WRONG':
            marker = '  [Wrong Way]'
        print(f'  {option}. {destination} - {miles} miles{marker}')
        option += 1


if __name__ == '__main__':
    main()
