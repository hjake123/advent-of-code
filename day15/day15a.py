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

def check_sensor_er(sensor: tuple, beacon: tuple, y: int) -> bool:
    '''
    Return this sensor's exclusion range at height y to exclude_ranges.
    Each range is in a tuple of form (lowest, highest) inclusive
    '''
    dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    offset_from_y = abs(sensor[1] - y)
    bounds = max(0, dist - offset_from_y)
    return (sensor[0]-bounds, sensor[0]+bounds)

def check_is_beacon(x: int, y: int) -> bool:
    '''
    Check if a particular cell is in the beacon list.
    '''
    for beacon in beacon_list:
        if beacon[0] == x and beacon[1] == y:
            return True
    return False
        
read_lists("day15/in.txt")
y_level = 2000000
all_span = (100000000000, -10000000000)
for i in range(len(sensor_list)):
    span = check_sensor_er(sensor_list[i], beacon_list[i], y_level)
    all_span = (min(all_span[0], span[0]), max(all_span[1], span[1]))
print(abs(all_span[1] - all_span[0]))