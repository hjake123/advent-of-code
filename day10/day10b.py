from collections import deque

code_queue = deque()
'''
Will hold a queue of codes to execute, in the following format:
noop: WAIT
addx: WAIT ADD n

addx is encoded this way to simulate its two-cycle execution time.
'''

WAIT = 0
ADD = 1

def read_program(filename: str):
    with open(filename) as program:
    # First, 'assemble' the lines of the program into the code queue.
        for line in program:
            inst = line.split()
            code_queue.appendleft(WAIT)
            if inst[0] == 'addx':
                code_queue.appendleft(ADD)
                code_queue.appendleft(int(inst[1]))

x = 1

def CPU_cycle(count: int):
    '''
    Perform one processor cycle.
    During a cycle, the processor consumes the top of the code queue and executes it. For items like ADD, it may consume parameters also.
    Also samples the signal before running if count + 20 is a multiple of 40.
    '''
    global x
    global sum

    if code_queue.pop() == ADD:
        x += code_queue.pop()

screen = [False for _ in range(240)]
'''
The screen is 40 across x 6 high, but is stored linearly for ease of use.
Each bool indicates whether that pixel has been turned on.
'''

def is_lit(index: int):
    '''
    Determines whether the index is lit based on the value in the x register.
    Remember, x is the center of a three pixel sprite.
    '''
    return abs(index % 40 - x) < 2

def draw():
    '''
    Draws the image in screen.
    '''
    for y in range(6):
        for x in range(40):
            if screen[40*y + x]:
                print('#', end='')
            else:
                print('.', end='')
        print('')


read_program("day10/in.txt")
count = 0
while len(code_queue) > 0:
    screen[count] = is_lit(count)
    CPU_cycle(count)
    count += 1
draw()
