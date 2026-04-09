# demo_06_set_basics.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Set basics -- adding, duplicate rejection, membership, sorted display

def main():
    # Building a set from scratch
    visited = set()             # Empty set -- NOT {}
    visited.add('San Antonio')
    visited.add('Houston')
    visited.add('Houston')      # Duplicate -- silently ignored
    visited.add('Austin')
    visited.add('Corpus Christi')

    print('Cities visited (as set):')
    print(visited)
    print(f'Unique city count: {len(visited)}')

    # Membership check
    print()
    if 'Austin' in visited:
        print('You have been to Austin.')
    if 'Dallas' not in visited:
        print('You have not been to Dallas.')

    # Convert to sorted list for display
    print()
    print('Cities visited (sorted):')
    for city in sorted(visited):
        print(f'  - {city}')

    # Convert a list with duplicates to a set instantly
    print()
    visit_log = ['San Antonio', 'Houston', 'Austin',
                 'Houston', 'Corpus Christi', 'Austin']
    unique = set(visit_log)
    print(f'Trips logged:   {len(visit_log)}')
    print(f'Unique cities:  {len(unique)}')


if __name__ == '__main__':
    main()
