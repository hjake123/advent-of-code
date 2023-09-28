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

with open("day10/in.txt") as program:
    # First, 'assemble' the lines of the program into the code queue.
    for line in program:
        inst = line.split()
        code_queue.appendleft(WAIT)
        if inst[0] == 'addx':
            code_queue.appendleft(ADD)
            code_queue.appendleft(int(inst[1]))

x = 1
sum = 0

def cycle(count: int):
    '''
    Perform one processor cycle.
    During a cycle, the processor consumes the top of the code queue and executes it. For items like ADD, it may consume parameters also.
    Also samples the signal before running if count + 20 is a multiple of 40.
    '''
    global x
    global sum

    if (count+20)%40 == 0:
        #print(count, x, count*x, sum)
        sum += count*x

    if code_queue.pop() == ADD:
        x += code_queue.pop()

count = 1
while len(code_queue) > 0:
    cycle(count)
    count += 1

print(sum)