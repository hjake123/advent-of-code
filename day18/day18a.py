model = [[[False]]]
cubes = []
def read_cubes(filename):
    with open(filename) as file:
        for line in file:
            nums = line.split(',')
            cubes.append([int(n) for n in nums])
    for coord in cubes:
        x = coord[0]
        y = coord[1]
        z = coord[2]
        while x >= len(model):
            model.append([[False]])
        while y >= len(model[x]):
            model[x].append([False])
        while z >= len(model[x][y]):
            model[x][y].append(False)

        model[x][y][z] = True

def faces(x, y, z):
    '''
    Return the offsets of the faces for this cube, one at a time.
    '''
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y - 1, z)
    yield (x, y + 1, z)
    yield (x, y, z - 1)
    yield (x, y, z + 1)

def check_cube_faces(x, y, z):
    '''
    Check the faces of the given cube and return the number of unoccupied ones.
    Might want to optimize this someday...
    '''
    unoccupied = 0
    for face in faces(x, y, z):
        if face[0] < 0 or face[0] >= len(model) or face[1] < 0 or face[1] >= len(model[face[0]]) or face[2] < 0 or face[2] >= len(model[face[0]][face[1]]):
            unoccupied += 1
            continue
        if not model[face[0]][face[1]][face[2]]:
            unoccupied += 1
    return unoccupied
        
read_cubes("day18/in.txt")
total = 0
for cube in cubes:
    total += check_cube_faces(cube[0], cube[1], cube[2])
print(total)
