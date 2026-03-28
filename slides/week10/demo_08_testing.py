# demo_08_testing.py
# String testing methods: isalpha(), isdigit(), isalnum(), isspace()
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    samples = ['Austin', '42', '3.14', 'abc123', '   ']

    for s in samples:
        print(f'"{s}"')
        print(f'  isalpha():  {s.isalpha()}')
        print(f'  isdigit():  {s.isdigit()}')
        print(f'  isalnum():  {s.isalnum()}')
        print(f'  isspace():  {s.isspace()}')
        print()


if __name__ == '__main__':
    main()
