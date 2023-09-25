from collections import deque

inventory = []
'''
This will store a list of the stacks in order. 
Element 0 is left empty for ease of access. (This way 'list 1' will be the first, like in the drawing.)
Each stack is a deque, to be interacted with exclusively as a stack would be.
'''

def parse_one_cell(line: str, pos: int):
    '''
    Read the next three characters as a cell of the stack diagram.
    Returns the character identifying the item in that cell, or ' ' if it was an empty cell.
    '''
    cell = line[pos:pos+3]
    return cell[1]

def parse_one_line(line:str):
    '''
    Parse one line of the diagram.
    The line must actually be a line of the diagram, not the line of numbers after it.
    '''
    stack_number = 1
    pos_in_line = 0
    while pos_in_line < len(line): 
        c = parse_one_cell(line, pos_in_line)
        if not c == ' ':
            inventory[stack_number].appendleft(c)
        pos_in_line += 4
        stack_number += 1

def read_initial_stacks(file):
    '''
    Read the stack diagram at the file start.
    '''
    inventory_initialized = False

    # This loop continues until we detect the line of numbers at the end of the diagram.
    while True:
        line = file.readline()
        if not inventory_initialized:
            inventory.append(None)
            # Create all the deques based on the length of the line.
            # Since each cell takes up 4 chars except the last one, the number of stacks
            # is equal to (len(line)+1)/4
            for i in range(1, int((len(line)+1)/4) + 1):
                inventory.append(deque())
            inventory_initialized = True
        if not '[' in line:
            break # Escape from infinite loop.
        parse_one_line(line)

def execute_one_line(line):
    '''
    Executes one stack movement instruction.
    The syntax is as follows:
        move count from a to b
    where count is an integer number of elements,
    and a and b are stack numbers.
    '''
    tokens = line.split()
    count = int(tokens[1])
    a = int(tokens[3])
    b = int(tokens[5])

    for i in range(0, count):
        inventory[b].append(inventory[a].pop())

with open("day5/in.txt") as file:
    read_initial_stacks(file)
    file.readline() # consume the empty line
    for instruction in file:
        execute_one_line(instruction)
    for stack in inventory:
        if not stack == None:
            print(stack.pop(), end="")