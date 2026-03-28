# demo_18_chaining.py
# Method chaining and the clean_input() pattern
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def clean_input(prompt):
    return input(prompt).strip().upper()


def main():
    answer  = clean_input('Keep playing? (y/n): ')
    choice  = clean_input('A) Dallas  B) Houston: ')
    confirm = clean_input('Are you sure? (yes/no): ')

    if answer == 'Y':
        print('Continuing the trip!')
    if choice == 'A':
        print('Heading to Dallas!')
    if confirm == 'YES':
        print('All confirmed. Buckle up.')


if __name__ == '__main__':
    main()
