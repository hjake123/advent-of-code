class ValveNode:
    def __init__(self, label: str, score: int, exits: list):
        self.label = label
        self.children = []
        self.parent = None
        self.exits = exits
        self.score = score
        self.index = 0

    def rdistance(self, other, visited = [], maxdepth = float('inf')):
        '''
        Returns the int distance between this and the other node by scanning our children recursively,
        or floating point infinity if it can't be found.
        '''
        if self == other or maxdepth == 0:
            return 0
        if get_distance_key(self, other) in distance_cache:
            return distance_cache[get_distance_key(self, other)]

        dist = float('inf')
        for child in self.children:
            if child in visited:
                continue
            res = child.rdistance(other, visited + [self], min(dist, maxdepth-1)) + 1
            if res == float('inf'):
                continue
            dist = min(res, dist)
            if dist == 1:
                return dist
        return dist
    
    def distance(self, other):
        '''
        Returns the int distance between this and the other node by scanning our children recursively,
        or floating point infinity if it can't be found.
        '''
        ret = self.rdistance(other)
        distance_cache.update({get_distance_key(self, other): ret})
        return ret

distance_cache = {}
def get_distance_key(current: ValveNode, other: ValveNode):
    '''
    Return the unique state key for this state.
    '''
    return current.label + ":" + other.label

valves = []
nonzero_valves = []
AA = None
def read_graph(filename):
    '''
    Read the graph.
    '''
    global AA
    with open(filename) as file:
        for line in file:
            label = line[6:8]
            nindex = line.find('=') + 1
            buf = []
            while line[nindex].isdigit():
                buf.append(line[nindex])
                nindex += 1
            score = int("".join([str(p) for p in buf]))
            words = line.split()
            exits = words[9:]
            exits = [exit.strip(',') for exit in exits]
            valve = ValveNode(label, score, exits)
            valves.append(valve)
            if not score == 0:
                nonzero_valves.append(valve)
            if valve.label == 'AA':
                AA = valve
    
    i = 0
    for valve in valves:
        for exit in valve.exits:
            child = [v for v in valves if v.label == exit][0]
            valve.children.append(child)
        valve.index = i
        i += 1

memos = {}
def get_state_key(current: ValveNode, past = [], minute = 0, cur_delay = 0):
    '''
    Return the unique state key for this state.
    '''
    key = current.label + ':'
    for p in past:
        key += p.label + ','
    key += str(minute)
    return key + "|" + str(cur_delay)

def score_state(you: ValveNode, elephant: ValveNode, past = [], minute = 4, you_delay = 0, ele_delay = 0) -> int:
    '''
    Choose the next valve to OPEN based on the previous state of affairs. 
    Uses globals to scan the list of non-zero valves.
    Uses recursion to determine the best answers, and stores them in the global memos.
    Returns the best score if you follow this path.
    NOTE: Minute starts at 4 to accomodate elephant training time.
    '''
    if minute >= 30:
        return 0

    if you_delay > 0 and ele_delay > 0:
        m = min(you_delay, ele_delay)
        return score_state(you, elephant, past, minute + m, you_delay - m, ele_delay - m)

    valves_left = [valve for valve in nonzero_valves if (valve not in past)]

    you_max = 0
    ele_max = 0

    if you_delay <= 0:
        if get_state_key(you, past, minute, you_delay) in memos:
            you_max = memos[get_state_key(you, past, minute, you_delay)]
        else:
            for your_next in valves_left:
                delay = you.distance(your_next) + 1
                if minute + delay >= len(max_potentials):
                    continue
                next_potential = max_potentials[minute + delay][your_next.index]
                next_potential += score_state(your_next, elephant, past + [your_next], minute, delay, ele_delay)
                if next_potential > you_max:
                    you_max = next_potential
            memos.update({get_state_key(you, past, minute, you_delay): you_max})
    
    if ele_delay <= 0:
        if get_state_key(elephant, past, minute, ele_delay) in memos:
            ele_max = memos[get_state_key(elephant, past, minute, ele_delay)]
        for ele_next in valves_left:
            delay = elephant.distance(ele_next) + 1
            if minute + delay >= len(max_potentials):
                continue
            next_potential = max_potentials[minute + delay][ele_next.index]
            next_potential += score_state(you, ele_next, past + [ele_next], minute, you_delay, delay)
            if next_potential > ele_max:
                ele_max = next_potential
            memos.update({get_state_key(elephant, past, minute, ele_delay): ele_max})

    return max(you_max, ele_max)

# AND NOW, THE SCRIPT ITSELF--!
read_graph('day16/in.txt')
max_potentials = [[max(0, (30-i) * v.score) for v in valves] for i in range(30)]
print(score_state(AA, AA))