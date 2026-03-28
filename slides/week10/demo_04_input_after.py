# demo_04_input_after.py
# AFTER: .upper() normalizes the input — one check each
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    answer = input('Keep playing? (y/n): ').upper()
    if answer == 'Y':
        keep_playing = True

    choice = input('A) Dallas  B) Houston: ').upper()
    if choice == 'A':
        destination = 'Dallas'
    elif choice == 'B':
        destination = 'Houston'

    confirm = input('Are you sure? (yes/no): ').upper()
    if confirm == 'YES':
        print('Confirmed!')


if __name__ == '__main__':
    main()
