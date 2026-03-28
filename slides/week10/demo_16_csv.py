# demo_16_csv.py
# CSV parsing pattern: strip, split, convert
# Week 10, Module 4 Week 1 — Chapter 8: More About Strings

def main():
    trip_data = [
        'Maria,San Antonio,Galveston,356,5',
        'Carlos,San Antonio,Corpus Christi,150,3',
        'Priya,San Antonio,Dallas,280,4',
    ]

    for line in trip_data:
        fields      = line.strip().split(',')
        name        = fields[0]
        start       = fields[1]
        destination = fields[2]
        miles       = int(fields[3])
        turns       = int(fields[4])
        print(f'{name}: {start} to {destination} — {miles} miles in {turns} turns')


if __name__ == '__main__':
    main()
