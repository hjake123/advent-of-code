from io import StringIO

sensor_list = []
beacon_list = []

def read_next_number(line: StringIO):
    '''
    Read the next number and return it. Modifies line to be cut to the end of that number.
    '''
    c = line.read(1)
    negative = False
    while not c.isdigit():
        if c == '-':
            negative = True
        c = line.read(1)
        if c == '':
            return None
    buf = []
    while c.isdigit():
        buf.append(c)
        c = line.read(1)
    i = int("".join([str(p) for p in buf]))
    if negative:
        i *= -1
    return i

minx = -2147483648
maxx = 2147483647

def read_lists(filename):
    global minx
    global maxx
    with open(filename) as file:
        index = -1
        for line in file:
            index += 1
            ioline = StringIO(line[12:])
            sx = read_next_number(ioline)
            sy = read_next_number(ioline)
            sensor_list.append((sx, sy))
            bx = read_next_number(ioline)
            by = read_next_number(ioline)
            beacon_list.append((bx, by))

def check_cell(x: int, y: int) -> bool:
    '''
    Determine whether a specific cell of the space is within the exclusion range of any sensor.
    Runs with O(len(sensor_list)) time.
    '''
    
    for i in range(len(sensor_list)):
        dist = abs(sensor_list[i][0] - beacon_list[i][0]) + abs(sensor_list[i][1] - beacon_list[i][1])
        
        if abs(sensor_list[i][0] - x) + abs(sensor_list[i][1] - y) <= dist:
            return True
    return False

def check_is_beacon(x: int, y: int) -> bool:
    '''
    Check if a particular cell is in the beacon list.
    '''
    for beacon in beacon_list:
        if beacon[0] == x and beacon[1] == y:
            return True
    return False
        
read_lists("day15/in.txt")
print('min:', minx, 'max:', maxx, '-=- scanning', (maxx - minx), "cells with", len(sensor_list), "sensors")
y_level = 2000000
count = 0
for i in range(minx, maxx+1):
    if i % (int(maxx/100)+1) == 0:
        print(i)
    blocked = check_cell(i, y_level)
    if blocked:
        if not check_is_beacon(i, y_level):
            count += 1
print('ans:', count)