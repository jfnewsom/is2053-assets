# demo_03_dict_methods.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: .keys(), .values(), .items() with for loops

def main():
    CITY_DISTANCES = {
        'San Antonio': {'Houston': 200, 'Austin': 80},
        'Houston':     {'Galveston': 50, 'Dallas': 240},
        'Austin':      {'Dallas': 200, 'Fort Worth': 190}
    }

    # .keys() -- loop through starting city names
    print('Starting cities (.keys()):')
    for city in CITY_DISTANCES.keys():
        print(f'  {city}')

    # .values() -- loop through inner dictionaries
    print()
    print('Destination counts (.values()):')
    for routes in CITY_DISTANCES.values():
        print(f'  {len(routes)} destinations')

    # .items() -- key AND value together (most common pattern)
    print()
    print('All routes (.items()):')
    for city, routes in CITY_DISTANCES.items():
        for dest, miles in routes.items():
            print(f'  {city} -> {dest}: {miles} miles')


if __name__ == '__main__':
    main()
