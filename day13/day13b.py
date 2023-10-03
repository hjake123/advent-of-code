from functools import cmp_to_key
def read_list(line):
    '''
    Convert a list of characters into the list that it describes.
    Recurses and consumes characters in place.
    '''
    list = []
    while len(line) > 0:
        line.pop(0)
        match line[0]:
            case ']':
                return list
            case '[':
                list.append(read_list(line))
            case ',':
                pass
            case default:
                j = 0
                buf = []
                while line[j].isdigit():
                    buf.append(line[j])
                    j += 1
                num = int("".join([str(p) for p in buf]))
                list.append(num)
                while j > 1:
                    line.pop(0)
                    j -= 1

def is_sorted(left, right):
    '''
    Compare the two lists. The heart of the operation.
    Returns a bool declaring if the lines are in the right order, or None if there is a tie.
    '''
    for i in range(len(left)):
        if i >= len(right):
            # Right list ran out first; return False.
            return False
        if isinstance(left[i], int) and isinstance(right[i], int):
            # Compare the two ints. If they deside the sorting, we're done. Otherwise, move on.
            if left[i] > right[i]:
                return False
            if left[i] < right[i]:
                return True
            continue
        if isinstance(left[i], list) and isinstance(right[i], list):
            # Have recursion compare the lists. If they deside the sorting, we're done. Otherwise, move on.
            result = is_sorted(left[i], right[i])
            if not result == None:
                return result  
            continue
        if isinstance(left[i], int) and isinstance(right[i], list):
            result = is_sorted([left[i]], right[i])
            if not result == None:
                return result  
            continue
        if isinstance(left[i], list) and isinstance(right[i], int):
            result = is_sorted(left[i], [right[i]])
            if not result == None:
                return result  
            continue
        # The sorting must have been inconclusive. Return None.
        return None
    # Left list runs out of items; return True if left is shorter or None if they are even length.
    if len(left) == len(right):
        return None
    return True

def cmp(l, r):
    '''
    Use is_sorted to write a classical comparator, which cmp_to_key will convert.
    I would have written a key function instead if I knew how those work...
    '''
    if is_sorted(l, r):
        return 1
    elif is_sorted(r, l):
        return -1
    return 0

lists = []
with open("day13/in.txt") as input:
    for line in input:
        line = line.strip()
        if line == '':
            continue
        lists.append(read_list(list(line.strip())))

lists.append([[2]])
lists.append([[6]])
lists.sort(key = cmp_to_key(cmp), reverse=True)
x = 0
y = 0
for i in range(len(lists)):
    if len(lists[i]) == 1 and isinstance(lists[i][0], list) and len(lists[i][0]) == 1 and lists[i][0][0] == 2:
        x = i + 1
    if len(lists[i]) == 1 and isinstance(lists[i][0], list) and len(lists[i][0]) == 1 and lists[i][0][0] == 6:
        y = i + 1
print(x*y)