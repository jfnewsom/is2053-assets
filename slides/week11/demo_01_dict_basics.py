# demo_01_dict_basics.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Dictionary creation, access, adding entries, membership check

def main():
    # Creating a dictionary
    city_taglines = {
        'San Antonio': 'Home of the Alamo',
        'Austin':      'Keep Austin Weird',
        'Houston':     'Space City',
        'El Paso':     'Sun City'
    }

    # Accessing a value by key
    print('Accessing by key:')
    print(city_taglines['Austin'])
    print(city_taglines['Houston'])

    # Adding a new entry
    city_taglines['Corpus Christi'] = 'Sparkling City by the Sea'
    print()
    print('After adding Corpus Christi:')
    print(f'Dictionary has {len(city_taglines)} cities.')

    # Checking if a key exists
    print()
    if 'Dallas' in city_taglines:
        print('Dallas is in the dictionary.')
    else:
        print('Dallas is not here yet.')

    if 'Austin' in city_taglines:
        print('Austin is in the dictionary.')


if __name__ == '__main__':
    main()
