def safe_lookup(grid, i, j):
    if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
        return grid[i][j]
    return -1 # Note that -1 is truthy.

with open("day8/in.txt") as file:
    # The actual grid of tree heights.
    grid = [[int(c) for c in lines if not c == '\n'] for lines in file]

    # The grid of final scores for each tree.
    score_grid = [[1 for c in line] for line in grid]
    
    # Scan from left to right.    
    for i in range(0, len(grid)):
        # Stores the distance to the last tree of at most the index's height FROM each direction
        distance_to_last_heights = [0 for n in range(0, 10)] 
        for j in range(0, len(grid[0])):
            score_grid[i][j] *= distance_to_last_heights[grid[i][j]]

            for n in range(0, 10):
                if grid[i][j] < n:
                    distance_to_last_heights[n] += 1
                else:
                    distance_to_last_heights[n] = 1

    # Scan from up to down   
    for i in range(0, len(grid)):
        # Stores the distance to the last tree of at most the index's height FROM each direction
        distance_to_last_heights = [0 for n in range(0, 10)] 
        for j in range(0, len(grid[0])):
            score_grid[j][i] *= distance_to_last_heights[grid[j][i]]

            for n in range(0, 10):
                if grid[j][i] < n:
                    distance_to_last_heights[n] += 1
                else:
                    distance_to_last_heights[n] = 1

    # Scan from right to left.    
    for i in reversed(range(0, len(grid))):
        # Stores the distance to the last tree of at most the index's height FROM each direction
        distance_to_last_heights = [0 for n in range(0, 10)] 
        for j in reversed(range(0, len(grid[0]))):
            score_grid[i][j] *= distance_to_last_heights[grid[i][j]]

            for n in range(0, 10):
                if grid[i][j] < n:
                    distance_to_last_heights[n] += 1
                else:
                    distance_to_last_heights[n] = 1

    # Scan from down to up
    for i in reversed(range(0, len(grid))):
        # Stores the distance to the last tree of at most the index's height FROM each direction
        distance_to_last_heights = [0 for n in range(0, 10)] 
        for j in reversed(range(0, len(grid[0]))):
            score_grid[j][i] *= distance_to_last_heights[grid[j][i]]

            for n in range(0, 10):
                if grid[j][i] < n:
                    distance_to_last_heights[n] += 1
                else:
                    distance_to_last_heights[n] = 1

    # Now to find the solution
    max = 0
    for line in score_grid:
        for number in line:
            if number > max:
                max = number

    print(max)
