class vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

head = vec2(0, 0)
tail = vec2(0, 0)

def head_tail_contact():
    '''
    Returns whether the head and tail are touching.
    '''
    return tail.x - head.x <= 1 and tail.x - head.x >= -1 and tail.y - head.y <= 1 and tail.y - head.y >= -1

def plot(lrange, rrange):
    '''
    Plot the relative positions of head and tail.
    '''
    for y in reversed(range(lrange, rrange)):
        for x in range(lrange, rrange):
            if x == head.x and y == head.y:
                print('H', end='')
            elif x == tail.x and y == tail.y:
                print('T', end='')
            else:
                print('.', end='')
        print('')
    print('')

# Used for solution.
tail_visitations = set()

def do_movement(direction: vec2, steps: int):
    '''
    Perform the movement specified by the direction steps times.
    This moves the head, and then updates the tail's position to match.
    '''
    for _ in range(0, steps):
        head.x += direction.x
        head.y += direction.y

        x_dist = abs(tail.x - head.x)
        y_dist = abs(tail.y - head.y)

        if not head_tail_contact():
            if x_dist > 1 and y_dist == 1:
                tail.y -= tail.y - head.y
            elif y_dist > 1 and x_dist == 1:
                tail.x -= tail.x - head.x

        if not head_tail_contact():
            tail.x += direction.x
            tail.y += direction.y     

        tail_visitations.add(str(tail.x) + ', '+ str(tail.y))

        plot(0, 6)

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