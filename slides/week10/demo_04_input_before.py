# demo_04_input_before.py
# BEFORE: checking both cases manually, every single time
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    answer = input('Keep playing? (y/n): ')
    if answer == 'y' or answer == 'Y':
        keep_playing = True

    choice = input('A) Dallas  B) Houston: ')
    if choice == 'A' or choice == 'a':
        destination = 'Dallas'
    elif choice == 'B' or choice == 'b':
        destination = 'Houston'

    confirm = input('Are you sure? (yes/no): ')
    if confirm == 'yes' or confirm == 'Yes' or confirm == 'YES':
        print('Confirmed!')


if __name__ == '__main__':
    main()
