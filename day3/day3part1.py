def priority(c):
    n = ord(c)
    if n >= ord('a') and n <= ord('z'):
        return n - ord('a') + 1
    if n >= ord('A') and n <= ord('Z'):
        return n - ord('A') + 27

with open('day3/day3in.txt') as rucksacks:
    sum = 0
    for rucksack in rucksacks:
        mid = int(len(rucksack)/2)
        dup = [c for c in rucksack[mid:] if c in rucksack[0:mid]][0]
        sum += priority(dup)
    print(sum)
        