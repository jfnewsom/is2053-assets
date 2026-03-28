# demo_14_split.py
# .split() and .split(delimiter)
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    # .split() — no argument splits on whitespace
    sentence = 'Deep in the Heart of Texas'
    words    = sentence.split()
    print(words)
    print(f'Word count: {len(words)}')

    # .split(delimiter) — split on a specific character
    route  = 'San Antonio,Houston,Galveston'
    cities = route.split(',')
    print(cities)
    print(f'First city: {cities[0]}')
    print(f'Last city:  {cities[2]}')


if __name__ == '__main__':
    main()
