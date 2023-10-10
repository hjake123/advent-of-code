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

def print_tower_row(row: int):
    '''
    Print one row of the tower.
    '''
    print('|', end='')
    for b in bits(row & 0b01111111, start = 0b1000000):
        if b:
            print('#', end='')
        else:
            print('.', end='')
    print('|', end='')

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
            continue

        # Falling step
        if not collide(pattern, x_offset, height-1) and not height <= 0:
            height -= 1
        else:
            break
    
    # Reaching this point means you have fallen either to the ground or collided while falling.
    write_pattern_to_tower(pattern, x_offset, height)
    for h in reversed(range(len(tower))):
        if not tower[h] == 128:
            return h
    return 0

with open("day17/in.txt") as file:
    top = -1
    for i in range(2022):
        top = drop_rock(i % 5, top+1, file)
    for row in reversed(tower):
        if row == 128:
            continue
        print_tower_row(row)
        print()
    print("+-------+")
    print(top + 1)