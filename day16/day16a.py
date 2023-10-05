class ValveNode:
    def __init__(self, label: str, score: int, exits: list):
        self.label = label
        self.children = []
        self.exits = exits
        self.score = score
    
    def score_depth_first(self, moves, should_redeem_score = False, parent = None, valves_opened = []) -> int:
        '''
        Returns the best score of any exit from this node
        Takes into account move limitations.
        '''
        base_score = 0

        if should_redeem_score:
            moves -= 1
            valves_opened.append(self)
            base_score += self.score * moves

        if moves <= 0:
            return base_score
        
        best_score = base_score

        # First, check all children without redeeming the next one's score.
        for child in self.children:
            score = child.score_depth_first(moves-1, parent = self, valves_opened = valves_opened.copy())
            if score > best_score:
                best_score = score + base_score
        
        # Then, check all children if you do redeeming the next one's score.
        for child in self.children:
            if child in valves_opened:
                continue
            score = child.score_depth_first(moves-1, should_redeem_score = True, parent = self, valves_opened = valves_opened.copy())
            if score > best_score:
                best_score = score + base_score

        return best_score

AA = None
def read_graph(filename):
    '''
    Read the graph.
    '''
    global AA
    valves = []
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
            valves.append(ValveNode(label, score, exits))
            if len(valves) == 1:
                AA = valves[0]
    
    for valve in valves:
        for exit in valve.exits:
            child = [v for v in valves if v.label == exit][0]
            valve.children.append(child)

read_graph('day16/short.txt')
print(AA.score_depth_first(30))