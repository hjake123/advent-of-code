heightmap = []
start = {"x": 0, "y": 0, "f": 0, "g": 0}
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
                    start["x"] = x
                    start["y"] = y
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

def A_star():
    '''
    Attempts to use A* to find the best path.
    Parameter is the cost to this point, for use when recursing.
    '''

    open_list = [start]
    closed_list = []

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
                print(s)
                return
            s['g'] = node['g'] + 1
            s['f'] = s['g'] + heuristic_distance(s['x'], s['y'])
            if not len([e for e in open_list if nodes_overlap(e, s) and e['f'] <= s['f']]) == 0:
                continue
            if not len([e for e in closed_list if nodes_overlap(e, s) and e['f'] <= s['f']]) == 0:
                continue
            open_list.append(s)
        closed_list.append(node)
    
read_graph("day12/in.txt")
print(heightmap)
A_star()
