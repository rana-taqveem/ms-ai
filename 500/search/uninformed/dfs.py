import numpy as np
from typing import Any
from collections import deque

def dfs(maze, start, goal) -> Any:
    row_count, col_count = maze.shape

    path = [start]
    stack = deque([(start, path)])
    visited = set()

    if start == goal:
        print("Start is the goal!")

    while True:
        state, path = stack.pop()
        if state in visited:
            continue

        visited.add(state)

        x, y = state
        if state == goal:
            print("Goal reached!")
            print("Path to goal:", path)
            break
        else:
            if x + 1 < row_count and maze[x + 1, y] == 0 and (x + 1, y) not in visited:
                stack.append(((x + 1, y), path + [(x + 1, y)]))
                print("Path so far:", path) 
            if x - 1 >= 0 and maze[x - 1, y] == 0 and (x - 1, y) not in visited:
                stack.append(((x - 1, y), path + [(x - 1, y)]))
                print("Path so far:", path)
            if y + 1 < col_count and maze[x, y + 1] == 0 and (x, y + 1) not in visited:
                stack.append(((x, y + 1), path + [(x, y + 1)]))
                print("Path so far:", path)
            if y - 1 >= 0 and maze[x, y - 1] == 0 and (x, y - 1) not in visited:
                stack.append(((x, y - 1), path + [(x, y - 1)]))
                print("Path so far:", path)

        if not stack:
            print("No path to the goal exists.")
            break

    return path

maze = np.array([
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0]
])

maze1 = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0]
])

maze2 = np.array([
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])

start = (0, 0)  # Starting position
goal = (4, 4)   # Goal position

result = dfs(maze, start, goal)
        



