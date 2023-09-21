def priority(c):
    n = ord(c)
    if n >= ord('a') and n <= ord('z'):
        return n - ord('a') + 1
    if n >= ord('A') and n <= ord('Z'):
        return n - ord('A') + 27

trios = []
with open('day3/day3in.txt') as rucksacks:
    trio = []
    for rucksack in rucksacks:
        trio.append(rucksack.strip())
        if len(trio) == 3:
            trios.append(trio)
            trio = []

sum = 0
for trio in trios:
    candidates = list(set(trio[0]))
    candidates = list(set([c for c in candidates if c in trio[1]]))
    candidates = list(set([c for c in candidates if c in trio[2]]))
    badge = candidates[0]
    sum += priority(badge)

print(sum)