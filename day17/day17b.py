# This project will use bitwise operators because I wanted to try something different.
def bits(number: int, start = 0x8000) -> iter:
    '''
    Iterator for the bits in a number. 
    '''
    bit = start
    while bit > 0:
       yield number & bit
       bit >>= 1

patterns = [0x000F, 0x04E4, 0x022E, 0x8888, 0x00CC]

def print_rock(index: int):
    '''
    Prints a rock according to its binary representation.
    '''
    counter = 1
    for b in bits(patterns[index]):
        if b:
            print('#', end='')
        else:
            print('.', end='')
        if counter % 4 == 0:
            print()
        counter += 1

def pattern_row(pattern: int, row: int):
    '''
    Returns the nibble representing the given row of the given pattern.
    row counts from the bottom of the pattern.
    '''
    while row > 0:
        row -= 1
        pattern >>= 4
    return pattern & 15
    
tower = []
'''
Stores a list of 7-bit numbers, representing the terrain at the moment. 
Entry 0 is the lowest level, and levels ascend with their indecies.
'''

def print_tower_row(row: int, file = None):
    '''
    Print one row of the tower.
    '''
    print('|', end='', file = file)
    for b in bits(row & 0b01111111, start = 0b1000000):
        if b:
            print('#', end='', file = file)
        else:
            print('.', end='', file = file)
    print('|', end='', file = file)

def collide_row(figure_row, x_offset: int, height: int):
    '''
    Return whether the given height and row of bits collides with existing terrain.
    x_offset is the column of the leftmost part of figure_row
    '''
    s = (7-x_offset) - 4
    if s > 0:
        figure_row <<= s
    elif s < 0:
        figure_row >>= s*-1
    return bool((tower[height] & 0b01111111) & figure_row)

def collide(pattern, x_offset: int, height: int):
    '''
    Returns whether any part of the given pattern collides with existing terrain.
    height is the height of the bottom of the pattern.
    '''
    for i in range(4):
        if collide_row(pattern_row(pattern, i), x_offset, height+i):
            return True
    return False

def write_pattern_to_tower(pattern, x_offset, height):
    '''
    Write the pattern to the tower at that location.
    '''
    for i in range(4):
        pr = pattern_row(pattern, i)
        s = (7-x_offset) - 4
        if s > 0:
            row = 0b10000000 | (pr << s)
        elif s < 0:
            row = 0b10000000 | (pr >> s*-1)
        else:
            row = 0b10000000 | pr
        tower[height + i] |= row

def x_in_bounds(x, pattern_index):
    '''
    Returns whether x is within allowable bounds for the x_offset.
    '''
    match pattern_index:
        case 0:
            return x >= 0 and x < 4
        case 1 | 2:
            return x >= 0 and x < 5
        case 3:
            return x >= 0 and x < 7
        case 4:
            return x >= 0 and x < 6

def drop_rock(pattern_index: int, prev_max_height: int, push_step_stream):
    '''
    Simulates one rock falling with the given pattern index and previous max height.
    Adjusts tower and returns the new max height.
    When the input file runs out, calculates the projected height at 1 quadrillion and exits.
    '''
    pattern = patterns[pattern_index]
    x_offset = 2
    height = prev_max_height + 3

    while len(tower) < prev_max_height + 7:
        tower.append(0b10000000)

    while height >= 0:
        # Pushing step
        inst = push_step_stream.read(1)
        if inst == '>':
            if x_in_bounds(x_offset + 1, pattern_index):
                if not collide(pattern, x_offset + 1, height):
                    x_offset += 1
        elif inst == '<':
            if x_in_bounds(x_offset - 1, pattern_index):
                if not collide(pattern, x_offset - 1, height):
                    x_offset -= 1
        else:
            push_step_stream.seek(0)
        
        # Falling step
        if not collide(pattern, x_offset, height-1) and not height <= 0:
            height -= 1
        else:
            break
    
    # Reaching this point means you have fallen either to the ground or collided while falling.
    write_pattern_to_tower(pattern, x_offset, height)
    top = 0
    for h in reversed(range(len(tower))):
        if not tower[h] == 128:
            top = h
            break

    return top

def has_run_4_zeros(row: int):
    '''
    Returns whether there is a run of 4 zeros anywhere in the row.
    '''
    r = 0
    for b in bits(row, start=0b1000000):
        if b == 0:
            r += 1
        else:
            r = 0
        if r == 4:
            return True
    return False

def scan_top_depths(top: int):
    '''
    Scans and returns the depths of the seven columns compared to the given height.
    '''
    depths = []
    mask = 1
    for i in reversed(range(7)):
        depth = top
        while depth > 0 and not bool(tower[depth] & (mask << i) & 0b01111111):
            depth -= 1
        depths.append(top-depth)
    return depths

big_number = 1000000000000
filename = "day17/short.txt"
file_len = 0

with open(filename) as file:
    file_len = len(file.read())

with open(filename) as file:
    top = -1
    cycle_period = file_len
    snapshot_time = 0
    snapshot_height = 0
    snapshot_depths = []
    for i in range(big_number):
        if i % cycle_period == 0 and not i == 0:
            # Analyze the tower to see if we are in a true cycle yet.
            if snapshot_time == 0:
                snapshot_time = i
                snapshot_height = top
                snapshot_depths = scan_top_depths(top)
            else:
                current_depths = scan_top_depths(top)
                if current_depths == snapshot_depths:
                    c_length = i - snapshot_time
                    print("Cycle found in", c_length, "drops.")
                    c_height = top - snapshot_height
                    print("Cycle adds", c_height, "height.")
                    print("Estimating", int((big_number-snapshot_time)/c_length * c_height + snapshot_height), "total height.")
                    exit()
                
        top = drop_rock(i % 5, top+1, file)
    print(top + 1)