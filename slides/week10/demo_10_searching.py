# demo_10_searching.py
# in, .find(), .startswith(), .endswith(), .count()
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    city = 'San Antonio, Texas'

    # in — True/False substring check
    print('Antonio' in city)        # True
    print('Houston' in city)        # False

    # .find() — returns index, or -1 if not found
    print(city.find('Texas'))       # 13
    print(city.find('Dallas'))      # -1

    # .startswith() / .endswith()
    print(city.startswith('San'))   # True
    print(city.endswith('Texas'))   # True

    # .count() — how many times does it appear?
    print(city.count('a'))          # 3


if __name__ == '__main__':
    main()
