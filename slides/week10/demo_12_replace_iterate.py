# demo_12_replace_iterate.py
# .replace() and character-by-character iteration
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    # .replace(old, new) — returns a NEW string every time
    route    = 'SAT -> HOU -> GAL'
    expanded = route.replace('SAT', 'San Antonio')
    expanded = expanded.replace('HOU', 'Houston')
    expanded = expanded.replace('GAL', 'Galveston')
    print(expanded)

    # Iterate character by character — count vowels in a city name
    city        = 'Galveston'
    vowel_count = 0
    for ch in city:
        if ch.lower() in 'aeiou':
            vowel_count += 1
    print(f'{city} has {vowel_count} vowels')


if __name__ == '__main__':
    main()
