from collections import deque

def has_repeats(buffer: deque):
    '''
    Check if the deque has any repeating items.
    '''
    return len(buffer) > len(set(buffer))

with open("day6/in.txt") as file:
    input = file.read()
    start_marker_buffer = deque()
    message_marker_buffer = deque()
    result = 0
    found_start = False
    for c in list(input):
        if not found_start:
            if len(start_marker_buffer) == 4:
                if not has_repeats(start_marker_buffer):
                    found_start = True
                start_marker_buffer.pop()
            start_marker_buffer.appendleft(c)
        else:
            if len(message_marker_buffer) == 14:
                if not has_repeats(message_marker_buffer):
                    break
                message_marker_buffer.pop()
            message_marker_buffer.appendleft(c)
        result += 1
    print(result)