# demo_06_strip.py
# .strip(), .lstrip(), .rstrip()
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    raw   = '   San Antonio   '
    clean = raw.strip()
    print(f'Before: "{raw}"')
    print(f'After:  "{clean}"')

    # lstrip / rstrip — one side only
    left_only  = raw.lstrip()   # 'San Antonio   '
    right_only = raw.rstrip()   # '   San Antonio'

    # Always strip user input before comparing
    city = input('Enter city: ').strip()
    if city == 'Austin':
        print('Heading to the capital!')


if __name__ == '__main__':
    main()
