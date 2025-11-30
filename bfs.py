def bfs(grid, start, end):
    #the queue structure.
    queue = []
    i=0 #the iterator for the queue
    
    height = len(grid)
    width = len(grid[0])

    #setting up the table of previous nodes with all [-1,-1] indicating no valid previous nodes for now.
    prevnodes = [[[-1, -1] for _ in range(width)] for _ in range(height)]

    #setiing false for all values in the visited table.
    visited = [[False for _ in range(width)] for _ in range(height)]

    #makring the start node the first element in the queue
    queue.append(start)
    sy, sx = start
    prevnodes[sy][sx] = start
    visited[sy][sx] = True

    found_path = False
    

    while not found_path and i < len(queue):
        y, x = queue[i] 
        
        #checking for the neighbours and adding them to the queue if they are not walls and not visited.

        #the right neighbor
        if x + 1 < width and grid[y][x + 1] != 0 and not visited[y][x + 1]:
            prevnodes[y][x + 1] = [y, x] 
            visited[y][x + 1] = True
            queue.append([y, x + 1])
            if [y, x + 1] == end:
                found_path = True
                break

        #the left neighbor
        if x - 1 >= 0 and grid[y][x - 1] != 0 and not visited[y][x - 1]:
            prevnodes[y][x - 1] = [y, x]
            visited[y][x - 1] = True
            queue.append([y, x - 1])
            if [y, x - 1] == end:
                found_path = True
                break

        
        #the top neighbor
        if y + 1 < height and grid[y + 1][x] != 0 and not visited[y + 1][x]:

            prevnodes[y + 1][x] = [y, x]
            visited[y + 1][x] = True
            queue.append([y + 1, x])
            if [y + 1, x] == end:
                found_path = True
                break

        #the bottom neighbor
        if y - 1 >= 0 and grid[y - 1][x] != 0 and not visited[y - 1][x]:
            prevnodes[y - 1][x] = [y, x]
            visited[y - 1][x] = True
            queue.append([y - 1, x])
            if [y - 1, x] == end:
                found_path = True
                break

        i += 1

    #constructing the path
    path = [end]
    while path[-1] != start:
        py, px = path[-1]
        path.append(prevnodes[py][px])
    
    num_nodes_visited = 0
    for i in visited:
        for j in i:
            if j:
                num_nodes_visited +=1

    #reversing to get the actual path and returning it, along with other variables.
    return path[::-1], num_nodes_visited, len(path)