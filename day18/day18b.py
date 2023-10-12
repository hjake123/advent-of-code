from collections import deque
model = []
exposed = []
cubes = []
def read_cubes(filename):
    with open(filename) as file:
        for line in file:
            nums = line.split(',')
            cubes.append([int(n) for n in nums])
    max_x = 0
    max_y = 0
    max_z = 0
    for coord in cubes:
        max_x = max(max_x, coord[0]+1)
        max_y = max(max_y, coord[1]+1)
        max_z = max(max_z, coord[2]+1)

    # make the empty space and make sure there is an extra buffer layer around the model also
    for _ in range(max_x+2):
        plate = []
        eplate = []
        for _ in range(max_y+2):
            row = []
            erow = []
            for _ in range(max_z+2):
                row.append(False)
                erow.append(False)
            plate.append(row)
            eplate.append(erow)
        model.append(plate)
        exposed.append(eplate)
                

    for coord in cubes:
        x = coord[0]+1
        y = coord[1]+1
        z = coord[2]+1
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

def face_out_of_bounds(face: tuple):
    return face[0] < 0 or face[0] >= len(model) or face[1] < 0 or face[1] >= len(model[face[0]]) or face[2] < 0 or face[2] >= len(model[face[0]][face[1]])


def check_cube_faces(x, y, z):
    '''
    Check the faces of the given cube and return the number of exposed ones.
    Might want to optimize this someday...
    '''
    exp = 0
    for face in faces(x, y, z):
        if face_out_of_bounds(face):
            exp += 1
            continue
        if exposed[face[0]][face[1]][face[2]]:
            exp += 1
    return exp

def fill_exposure(x, y, z) -> bool:
    '''
    Flood fill the area with water.
    This adds affected areas to the exposed list.
    '''
    fill_queue = deque()
    fill_queue.append((x, y, z))
    exposed[x][y][z] = True
    while len(fill_queue) > 0:
        block = fill_queue.pop()
        for face in faces(block[0], block[1], block[2]):
            if not face_out_of_bounds(face):
                if not model[face[0]][face[1]][face[2]] and not exposed[face[0]][face[1]][face[2]]:
                    exposed[face[0]][face[1]][face[2]] = True
                    fill_queue.append(face)
    
        
read_cubes("day18/in.txt")
total = 0
fill_exposure(0, 0, 0)
for cube in cubes:
    total += check_cube_faces(cube[0]+1, cube[1]+1, cube[2]+1)
print(total)
