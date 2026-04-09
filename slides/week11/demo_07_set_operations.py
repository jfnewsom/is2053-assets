# demo_07_set_operations.py
# IS2053 Week 11 — Chapter 9: Dictionaries and Sets
# Demo: Set operations -- union, intersection, difference, symmetric difference

def main():
    baseball   = set(['Jodi', 'Carmen', 'Aida', 'Alicia'])
    basketball = set(['Eva', 'Carmen', 'Alicia', 'Sarah'])

    print('Baseball team:  ', sorted(baseball))
    print('Basketball team:', sorted(basketball))

    # Union -- plays at least one sport
    print()
    print('Union (plays at least one sport):')
    print(sorted(baseball.union(basketball)))

    # Intersection -- plays both sports
    print()
    print('Intersection (plays both sports):')
    print(sorted(baseball.intersection(basketball)))

    # Difference -- baseball players NOT on basketball
    print()
    print('Difference (baseball only):')
    print(sorted(baseball.difference(basketball)))

    # Symmetric difference -- plays exactly one sport
    print()
    print('Symmetric difference (exactly one sport):')
    print(sorted(baseball.symmetric_difference(basketball)))


if __name__ == '__main__':
    main()
