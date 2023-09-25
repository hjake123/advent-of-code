def ranges_overlap(a: int, b: int, c: int, d: int):
    '''
    Returns whether the range [a, b] overlaps the range [c, d].
    '''
    # If the sequence if not a b c d or c d a b, there must be some overlap.
    # Since we know that a <= b and c <= d by definition, we only need to check these.
    return not (b < c or d < a) 

def parse_ranges(str):
    '''
    Returns a list of two lists of two integers each specifying the ranges written in str in the format "int-int, int-int", crashing on parse errors.
    '''
    return [[int(n) for n in part.split('-')] for part in str.split(',')]


with open("day4/in.txt") as input:
    tally = 0
    for line in input:
        ranges = parse_ranges(line)
        if ranges_overlap(ranges[0][0], ranges[0][1], ranges[1][0], ranges[1][1]):
            tally += 1

    print(tally)