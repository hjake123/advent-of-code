class vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

def contact(h:vec2, t: vec2):
    '''
    Returns whether two vec2 are touching.
    '''
    return t.x - h.x <= 1 and t.x - h.x >= -1 and t.y - h.y <= 1 and t.y - h.y >= -1

head = vec2(0, 0)
tails = [vec2(0, 0) for _ in range(0, 9)]

def update_one_tail(i):
    '''
    Update the tail with index i's position based on the position of the thing before it in the chain.
    Returns the displacement generated, so that the next call can use it.
    '''
    if i == 0:
        prev_tail = head
    else:
        prev_tail = tails[i-1]

    x_offset = tails[i].x - prev_tail.x
    y_offset = tails[i].y - prev_tail.y

    displacement = vec2(0, 0)

    if not contact(prev_tail, tails[i]):
        if x_offset >= 1:
            displacement.x = -1
        elif x_offset <= -1:
            displacement.x = 1
        
        if y_offset >= 1:
            displacement.y = -1
        elif y_offset <= -1:
            displacement.y = 1

    tails[i].x += displacement.x
    tails[i].y += displacement.y

def do_movement(direction: vec2, steps: int):
    '''
    Perform the movement specified by the direction steps times.
    This moves the head, and then updates the tails' position to match.
    '''
    for _ in range(0, steps):
        head.x += direction.x
        head.y += direction.y
        
        for i in range(len(tails)):
            update_one_tail(i)     
        
        tail_visitations.add(str(tails[8].x) + ', '+ str(tails[8].y))
    
# Used for solution.
tail_visitations = set()

with open("day9/in.txt") as file:
    for line in file:
        glyphs = line.split()
        match glyphs[0]:
            case 'R':
                do_movement(vec2(1, 0), int(glyphs[1]))
            case 'U':
                do_movement(vec2(0, 1), int(glyphs[1]))
            case 'D':
                do_movement(vec2(0, -1), int(glyphs[1]))
            case 'L':
                do_movement(vec2(-1, 0), int(glyphs[1]))

print(len(tail_visitations))