'''
Elves write their Calorie inventory as 1 count / line, and seperate themselves with blanks.
Find the number of Calories the elf with the highest number has.
'''

first = 0
second = -1
third = -2
cal = 0

with open("day1in.txt") as inventory:
    for entry in inventory:
        if entry[:-1].isdigit():
            cal += int(entry)
        elif entry == "\n":
            if cal > first:
                third = second
                second = first
                first = cal
            elif cal > second:
                third = second
                second = cal
            elif cal > third:
                third = cal
            cal = 0

print(first + second + third)
