import math
import sys


def a_star(start, end, connections, weights, r_size):
    if start == end:
        return [[0, start]]

    shortest_dist_and_prev_node = [[sys.maxsize, -1] for _ in range(len(connections))]
    visited = [False for _ in range(len(connections))]

    shortest_dist_and_prev_node[start] = [0, start]

    run_while = True
    next_node = start

    iter = 0
    while run_while:
        for i in range(len(connections[next_node])):
            new_dist = shortest_dist_and_prev_node[next_node][0] + weights[next_node][i]
            if (
                not visited[connections[next_node][i]]
                and new_dist < shortest_dist_and_prev_node[connections[next_node][i]][0]
            ):
                shortest_dist_and_prev_node[connections[next_node][i]][0] = new_dist
                shortest_dist_and_prev_node[connections[next_node][i]][1] = next_node

        visited[next_node] = True

        shortest_dist = sys.maxsize
        for i in range(len(shortest_dist_and_prev_node)):
            if i != start and not visited[i]:
                if shortest_dist_and_prev_node[i][0] < shortest_dist:
                    next_node = i
                    shortest_dist = shortest_dist_and_prev_node[i][0]

        if next_node == end or iter >= len(connections):
            run_while = False
        iter += 1

    return shortest_dist_and_prev_node


def reconstruct_path(start, end, shortest_dist_and_prev_node):
    path = []
    at = end

    if shortest_dist_and_prev_node[at][0] == sys.maxsize:
        return []

    while at != start:
        path.append(at)
        at = shortest_dist_and_prev_node[at][1]
        if at == -1:
            return []

    path.append(start)
    path.reverse()
    return path
