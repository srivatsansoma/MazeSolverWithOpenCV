import cv2
import numpy as np
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

#loading the image.
maze_colored = cv2.imread("img/maze.png")

#making it black and white
maze_black_and_white = cv2.cvtColor(maze_colored, cv2.COLOR_BGR2GRAY)

#extracitng the green pixels
start = cv2.cvtColor(maze_colored, cv2.COLOR_RGB2HSV)
lower_green = np.array([35, 100, 100]) 
upper_green = np.array([85, 255, 255]) 
green_mask = cv2.inRange(start, lower_green, upper_green)
start = cv2.bitwise_and(maze_colored, maze_colored, mask=green_mask)
start = cv2.cvtColor(start, cv2.COLOR_RGB2GRAY)
cv2.imwrite("./img/green.png", start)

#extracting the blue pixels
end = cv2.cvtColor(maze_colored, cv2.COLOR_BGR2HSV)
lower_blue = np.array([100, 150, 50]) 
upper_blue = np.array([140, 255, 255]) 
blue_mask = cv2.inRange(end, lower_blue, upper_blue)
end = cv2.bitwise_and(maze_colored, maze_colored, mask=blue_mask)
end= cv2.cvtColor(end, cv2.COLOR_RGB2GRAY)
cv2.imwrite("./img/blue.png" , end)

#finding the center point of the green and blue pixels and making them start and end.
start_points = [[], []]
end_points   = [[], []]
for i in range(0, len(start)):
    for j in range(0, len(start[i])):
        if (start[i][j] > 30):
            start_points[0].append(i)
            start_points[1].append(j)
        if (end[i][j] > 30):
            end_points[0].append(i)
            end_points[1].append(j)


start_points = [np.average(start_points[0]).astype(int), np.average(start_points[1]).astype(int)]
end_points = [np.average(end_points[0]).astype(int), np.average(end_points[1]).astype(int)]

#converting it into a binary. it is a wall if it has a greyscale value <5
grid_in_binary  = [
    [0 for i in range(0, len(maze_black_and_white[0]))] for i in range(0, len(maze_black_and_white))
]
for i in range(0, len(maze_black_and_white)):
    for j in range(0, len(maze_black_and_white[i])):
        if maze_black_and_white[i][j] > 5:
            grid_in_binary[i][j] = 1


path, number_of_points_explored, len_path = bfs(grid_in_binary, start_points, end_points)

#coloring the path red
for point in path:
    cv2.circle(maze_colored, (point[1],point[0]), 1,(0,0,255),1) 

#coloring the start and end points yellow
cv2.circle(maze_colored, (start_points[1], start_points[0]), 3,(0,255,255),3) 
cv2.circle(maze_colored, (end_points[1], end_points[0]), 3,(0,255,255),3)

cv2.imwrite("./img/path_drawn.png", maze_colored)

#final output-text
print("start: ", start_points)
print("end: ", end_points)
print("number of nodes explorred: ", number_of_points_explored)
print("lenght of the optimum path in pixels: ", len_path)