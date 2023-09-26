def safe_lookup(grid, i, j):
    if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
        return grid[i][j]
    return -1 # Note that -1 is truthy.

def is_visible(diffgrid, i, j):
    '''
    Returns whether the tree at grid[i][j] is visible in the given diffgrid.
    '''
    return diffgrid[i][j] > 0

def is_visible_in_any_of(diffgrids: list, i, j):
    '''
    Returns whether the tree at grid[i][j] is visible in any of the given diffgrids.
    '''
    visible = False
    for diffgrid in diffgrids:
        visible = visible or is_visible(diffgrid, i, j)
    return visible

with open("day8/in.txt") as file:
    grid = [[int(c) for c in lines if not c == '\n'] for lines in file]
    # The actual grid of tree heights.

    up_max_grid = [[0 for c in line] for line in grid]
    # Stores the maximum height of trees in this line from the top so far. Trees above this height are visible, and increase the height to their own.
    # The other vis grids function similarly, but are each for a distinct cardinal direction.
    up_diff_grid = [[0 for c in line] for line in grid]
    # Stores the difference in maximum height from the previous entry to this one.

    left_max_grid = [[0 for c in line] for line in grid]
    left_diff_grid = [[0 for c in line] for line in grid]

    down_max_grid = [[0 for c in line] for line in grid]
    down_diff_grid = [[0 for c in line] for line in grid]

    right_max_grid = [[0 for c in line] for line in grid]
    right_diff_grid = [[0 for c in line] for line in grid]
    
    # Scan from each direction to fill the visgrids.
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            up_max_grid[i][j] = max(safe_lookup(up_max_grid, i-1, j), grid[i][j])
            up_diff_grid[i][j] = up_max_grid[i][j] - safe_lookup(up_max_grid, i-1, j)
            left_max_grid[i][j] = max(safe_lookup(left_max_grid, i, j-1), grid[i][j])
            left_diff_grid[i][j] = left_max_grid[i][j] - safe_lookup(left_max_grid, i, j-1)

    for i in reversed(range(0, len(grid))):
        for j in reversed(range(0, len(grid[0]))):
            down_max_grid[i][j] = max(safe_lookup(down_max_grid, i+1, j), grid[i][j])
            down_diff_grid[i][j] = down_max_grid[i][j] - safe_lookup(down_max_grid, i+1, j)
            right_max_grid[i][j] = max(safe_lookup(right_max_grid, i, j+1), grid[i][j])
            right_diff_grid[i][j] = right_max_grid[i][j] - safe_lookup(right_max_grid, i, j+1)

    # Now to find the solution.
    tally = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if is_visible_in_any_of([up_diff_grid, left_diff_grid, down_diff_grid, right_diff_grid], i, j):
                tally += 1

    print(tally)