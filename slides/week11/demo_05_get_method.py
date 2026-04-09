# demo_05_get_method.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Safe dictionary lookups with .get() vs bracket notation

def main():
    CITY_DISTANCES = {
        'San Antonio': {
            'Houston':        200,
            'Austin':          80,
            'Corpus Christi': 150
        }
    }

    # Bracket access -- works when key exists
    print('Bracket access (key exists):')
    dist = CITY_DISTANCES['San Antonio']['Houston']
    print(f'  San Antonio to Houston: {dist} miles')

    # .get() -- returns default instead of crashing
    print()
    print('Safe .get() access:')
    dist_known = CITY_DISTANCES['San Antonio'].get('Austin', -1)
    dist_missing = CITY_DISTANCES['San Antonio'].get('Waco', -1)
    print(f'  San Antonio to Austin: {dist_known} miles')
    print(f'  San Antonio to Waco:   {dist_missing} (not found)')

    # Practical use: check before using
    print()
    destination = 'Waco'
    distance = CITY_DISTANCES['San Antonio'].get(destination, -1)
    if distance == -1:
        print(f'  No direct route to {destination} from San Antonio.')
    else:
        print(f'  Distance to {destination}: {distance} miles')


if __name__ == '__main__':
    main()
