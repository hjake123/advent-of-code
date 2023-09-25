def range_fully_contains(range_left, range_right, subrange_left, subrange_right):
    '''
    Returns whether the range [range_left, range_right] fully contains the range [subrange_left, subrange_right].
    '''
    return range_left <= subrange_left and subrange_right <= range_right

def parse_ranges(str):
    '''
    Returns a list of two lists of two integers each specifying the ranges written in str in the format "int-int, int-int", crashing on parse errors.
    '''
    return [[int(n) for n in part.split('-')] for part in str.split(',')]


with open("day4/in.txt") as input:
    tally = 0
    for line in input:
        ranges = parse_ranges(line)
        if range_fully_contains(ranges[0][0], ranges[0][1], ranges[1][0], ranges[1][1]) or range_fully_contains(ranges[1][0], ranges[1][1], ranges[0][0], ranges[0][1]):
            tally += 1

    print(tally)