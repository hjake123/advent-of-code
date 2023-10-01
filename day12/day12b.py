heightmap = []
end = {"x": 0, "y": 0}

def read_graph(filename):
    '''
    Reads the file into the global graph as a 2D array where each element is the height from [0, 25].
    '''
    global open_list
    global close_list
    with open(filename) as file:
        y = 0
        for line in file:
            hline = []
            x = 0
            for c in list(line.strip()):
                if c == 'S':
                    hline.append(0)
                elif c == 'E':
                    end["x"] = x
                    end["y"] = y
                    hline.append(25)
                else:
                    hline.append(ord(c) - ord('a'))
                x += 1
            heightmap.append(hline)
            y += 1


def heuristic_distance(x, y):
    '''
    A simple heuristic that returns a low-balled estimate of the distance from (x,y) to (end_x,end_y).
    '''
    return abs((end['x'] - x) + (end['y'] - y))

def nodes_overlap(a, b):
    '''
    Return whether the node dictionaries in a and b overlap.
    '''
    return a['x'] == b['x'] and a['y'] == b['y']

def iterpeek(iterable):
    return len([iterable]) > 0

def A_star(x, y):
    '''
    Attempts to use A* to find the best path from (x, y).
    Parameter is the cost to this point, for use when recursing.
    Returns the number of steps taken.
    '''

    # Part 2: Try just adding everything to the open list. It's not great but like... maybe it'd still work?

    open_list = [{'x': x, 'y': y, 'f': 0, 'g': 0}]
    closed_array = [[False for _ in line] for line in heightmap]

    while len(open_list) > 0:
        open_list.sort(key = lambda d: d['f'], reverse=True)
        node = open_list.pop()
        successors = []
        if node['x'] + 1 < len(heightmap[0]):
            if heightmap[node['y']][node['x']] + 1 >= heightmap[node['y']][node['x'] + 1]:
                succ = node.copy()
                succ['x'] += 1
                successors.append(succ)
        
        if node['x'] > 0:
            if heightmap[node['y']][node['x']] + 1 >= heightmap[node['y']][node['x'] - 1]:
                succ = node.copy()
                succ['x'] -= 1
                successors.append(succ)

        if node['y'] + 1 < len(heightmap):
            if heightmap[node['y']][node['x']] + 1 >= heightmap[node['y'] + 1][node['x']]:
                succ = node.copy()
                succ['y'] += 1
                successors.append(succ)

        if node['y'] > 0: 
            if heightmap[node['y']][node['x']] + 1 >= heightmap[node['y'] - 1][node['x']]:
                succ = node.copy()
                succ['y'] -= 1
                successors.append(succ)
        
        for s in successors:
            if nodes_overlap(s, end):
                return s['f']

            if any([nodes_overlap(e, s) and e['f'] <= s['f'] for e in open_list]):
                continue
            if closed_array[y][x]:
                continue

            s['g'] = node['g'] + 1
            s['f'] = s['g'] + heuristic_distance(s['x'], s['y'])

            open_list.append(s)
        closed_array[node['y']][node['x']] = True
    
read_graph("day12/short.txt")
m = len(heightmap)*len(heightmap[0])
for y in range(len(heightmap)):
    for x in range(len(heightmap[0])):
        if heightmap[y][x] == 0:
            dist = A_star(x, y)
            m = min(m, dist)
            print(m)
print(m)
