# demo_02_nested_dict.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Nested dictionary for city distances + safe .get() lookup

def main():
    CITY_DISTANCES = {
        'San Antonio': {
            'Houston':        200,
            'Austin':          80,
            'Corpus Christi': 150,
            'Laredo':         160,
            'El Paso':        550
        },
        'Houston': {
            'Galveston':    50,
            'Dallas':      240,
            'San Antonio': 200
        },
        'Austin': {
            'Dallas':      200,
            'Fort Worth':  190,
            'San Antonio':  80
        }
    }

    # Access nested values
    print('Accessing nested values:')
    dist1 = CITY_DISTANCES['San Antonio']['Houston']
    print(f'San Antonio to Houston:  {dist1} miles')

    dist2 = CITY_DISTANCES['Houston']['Dallas']
    print(f'Houston to Dallas:       {dist2} miles')

    dist3 = CITY_DISTANCES['Austin']['Dallas']
    print(f'Austin to Dallas:        {dist3} miles')

    # Safe .get() lookup
    print()
    print('Safe .get() lookups:')
    known = CITY_DISTANCES['San Antonio'].get('Austin', -1)
    missing = CITY_DISTANCES['San Antonio'].get('Waco', -1)
    print(f'SA to Austin: {known} miles')
    print(f'SA to Waco:   {missing}  (not found)')

    # Loop through routes from one city
    print()
    print('Routes from San Antonio:')
    for dest in CITY_DISTANCES['San Antonio']:
        print(f'  -> {dest}')


if __name__ == '__main__':
    main()
