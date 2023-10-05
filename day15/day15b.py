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
    Each range is in a tuple of form (lowest, highest) inclusive, or None if the sensor doesn't affect this height.
    '''
    dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    offset_from_y = abs(sensor[1] - y)
    bounds = dist - offset_from_y
    if bounds < 0:
        return None
    return (sensor[0]-bounds, sensor[0]+bounds)

def check_is_beacon(x: int, y: int) -> bool:
    '''
    Check if a particular cell is in the beacon list.
    '''
    for beacon in beacon_list:
        if beacon[0] == x and beacon[1] == y:
            return True
    return False

def spans_overlap(a, b):
    '''
    Returns whether span a overlaps span b. Since they're integer spans, this can also mean they are adjacent.
    '''
    return (a[1] >= b[0] and b[1] >= a[0]) or (a[1] >= b[0] and b[1] >= a[0]-1) or (a[1]-1 >= b[0] and b[1] >= a[0])

def join_spans(a, b):
    '''
    Return the span formed by overlapping a and b, assuming no discontinuity.
    '''
    return (min(a[0], b[0]), max(a[1], b[1]))

def append_span_with_merging(spans, span):
    '''
    Recursively merge as much as possible after appending this span.
    Resilliant against None spans.
    '''
    if span == None:
        return
    overlap_index = -1
    for i in range(len(spans)):
        if spans_overlap(span, spans[i]):
            overlap_index = i
            break                    
    if overlap_index < 0:
        spans.append(span)
    else:
        other_span = spans.pop(overlap_index)
        append_span_with_merging(spans, join_spans(other_span, span))

def search_one_row(y: int):
    '''
    Search the row at height y for The Hole.
    Returns either the x coordiante of The Hole, or (more likely) None if it isn't in this row.
    '''
    spans = []
    for i in range(len(sensor_list)):
        append_span_with_merging(spans, check_sensor_er(sensor_list[i], beacon_list[i], y))
    
    if len(spans) == 2:
        return spans[0][1] + 1
    return None
        
read_lists("day15/in.txt")
for y in range(4000000):
    if y % 40000 == 0:
        print(int(y/40000), "%", sep='')
    hole = search_one_row(y)
    if not hole == None:
        print("(",hole,", ",y,") ",end="",sep="")
        print(":", hole*4000000+y)
        exit()
print("No holes?")