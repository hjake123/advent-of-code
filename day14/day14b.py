def read_pair(line: str, index: int):
    '''
    Read the indexed pair as a tuple from the line.
    Returns None if a too-high index is used.
    '''
    words = line.strip().split(' -> ')
    if index >= len(words):
        return None
    return (int(words[index].split(',')[0]), int(words[index].split(',')[1]))

min_x = 10000
max_x = 0
max_y = 0

def update_bounds(point: tuple):
    global min_x
    global max_x
    global max_y
    min_x = min(point[0], min_x)
    max_x = max(point[0], max_x)
    max_y = max(point[1], max_y)

def place_rock_path(point_a: tuple, point_b: tuple):
    '''
    Draw a rock path between the points.
    This assumes that at most either [0] or [1] is distinct between the two; diagonals are impossible.
    '''
    if point_a[0] == point_b[0]:
        for i in range(point_a[1], min(point_b[1] + 1, max_y)):
            cave[point_a[0] - min_x][i] = '#'
        for i in range(point_b[1], min(point_a[1] + 1, max_y)):
            cave[point_a[0] - min_x][i] = '#'
    else:
        for i in range(point_a[0] - min_x, min(max_x, point_b[0] - min_x + 1)):
            cave[i][point_a[1]] = '#'
        for i in range(point_b[0] - min_x, min(max_x, point_a[0] - min_x + 1)):
            cave[i][point_a[1]] = '#'

def draw_cave():
    '''
    Draw the cave diagram.
    '''
    for y in range(len(cave[0])):
        for x in range(len(cave)):
            print(cave[x][y], end='')
        print('')

def drop_sand() -> bool:
    '''
    Simulate one unit of sand falling.
    Mutates cave.
    Returns whether the sand fell any before coming to rest.
    '''
    global min_x
    global max_x
    x = 500 - min_x
    y = 0
    while True: 
        if y > max_y:
            cave[x][y] = 'o'
            return True

        if x-1 < 0:
            cave.insert(0, ['.' for _ in range(max_y+2)])
            min_x -= 1
            x += 1
        
        if min_x + x >= max_x:
            cave.append(['.' for _ in range(max_y+2)])
            max_x += 1

        if cave[x][y+1] == '.':
            y += 1
        elif cave[x-1][y+1] == '.':
            x -= 1
            y += 1
        elif cave[x+1][y+1] == '.':
            x += 1
            y += 1
        else:
            cave[x][y] = 'o'
            return not (x == 500 - min_x and y == 0)

with open("day14/in.txt") as file:
    grid = []
    for line in file:
        points = []
        i = 0
        point = read_pair(line, i)
        while not point == None:
            points.append(point)
            update_bounds(point)
            i += 1
            point = read_pair(line, i)
        grid.append(points)

cave = [['.' for _ in range(max_y+2)] for _ in range(min_x, max_x+1)]
cave[500 - min_x][0] = '+'
for points in grid:
    for i in range(len(points) - 1):
            place_rock_path(points[i], points[i+1])

unfinished = True
count = 0
while unfinished:
    unfinished = drop_sand()
    count += 1
print(count)