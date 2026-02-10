 # Importing modules and libraries
from maze_visual import maze, agent
import sys
import argparse
import time
import math
import heapq
from collections import deque

# Import any other modules you want to use here

# DO NOT CHANGE THESE LINES OF CODE
# ----------------------------------
ROWS = 20 # Number of rows in the maze
COLS = 20 # Number of columns in the maze
m = maze(ROWS, COLS) # Initialize the maze

# Load the maze from the csv file. You may need to change this path depending on where you save the files.
m.LoadMaze(loadMaze='maze_config.csv', theme="dark")
# ----------------------------------


def DFS_V1(maze, start, goal):
    '''
    This function should implement the Depth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    path_chain = {}
    path_to_goal = []
    path_chain[start] = None
    store = deque([start])
    visited_positions = []

    if start == goal:
        print("Start is the goal!")

    visited_positions.append(start)
    while True:
        current_cell = store.pop()
        row, col = current_cell
        if current_cell == goal:
            trace_back_path_to_goal(goal, path_to_goal, path_chain)
            break
        else: 
            # reversed the order for DFS becasue on pop we want N W S E
            # East
            next_cell = (row, col+1)
            if maze.maze_map[(current_cell)]['E'] == 1 and col+1<=COLS and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)
                visited_positions.append(next_cell)

            # South
            next_cell = (row+1, col)
            if maze.maze_map[(current_cell)]['S'] == 1 and row+1<=ROWS and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)
                visited_positions.append(next_cell)

            # West
            next_cell = (row, col-1)
            if maze.maze_map[(current_cell)]['W'] == 1 and col-1>0 and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)
                visited_positions.append(next_cell)

            # North
            next_cell = (row-1, col)
            if maze.maze_map[(current_cell)]['N'] == 1 and row-1>0 and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)
                visited_positions.append(next_cell)
            
        if not store:
            print("No path to the goal exists.")
            break

    return list(visited_positions), path_to_goal

def DFS_V2(maze, start, goal):
    '''
    This function should implement the Depth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    path_chain = {}
    path_to_goal = []
    path_chain[start] = None
    store = deque([start])
    visited_positions = []

    if start == goal:
        print("Start is the goal!")

    while True:
        current_cell = store.pop()
        if current_cell in visited_positions:
            continue

        visited_positions.append(current_cell)
        row, col = current_cell

        if current_cell == goal:
            trace_back_path_to_goal(goal, path_to_goal, path_chain)
            break
        else: 
            # reversed the order for DFS becasue on pop we want N W S E
            # East
            next_cell = (row, col+1)
            if maze.maze_map[(current_cell)]['E'] == 1 and col+1<=COLS and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)

            # South
            next_cell = (row+1, col)
            if maze.maze_map[(current_cell)]['S'] == 1 and row+1<=ROWS and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)

            # West
            next_cell = (row, col-1)
            if maze.maze_map[(current_cell)]['W'] == 1 and col-1>0 and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)

            # North
            next_cell = (row-1, col)
            if maze.maze_map[(current_cell)]['N'] == 1 and row-1>0 and next_cell not in visited_positions:
                path_chain[next_cell] = current_cell
                store.append(next_cell)
            
            
        if not store:
            print("No path to the goal exists.")
            break

    return list(visited_positions), path_to_goal

def BFS_V1(maze, start, goal):
    '''
    This function should implement the Breadth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    path_chain = {}
    path_to_goal = []
    path_chain[start] = None
    store = deque([start])
    visited_positions = []
    found_cells = set()

    found_cells.add(start)
    if start == goal:
        print("Start is the goal!")
        visited_positions.append(start)
        return visited_positions, [start]

    visited_positions.append(start)
    while True:
        current_cell = store.popleft()
        
        row, col = current_cell
        if current_cell == goal:
            trace_back_path_to_goal(goal, path_to_goal, path_chain)
            break
        else: 
            
            # In this version of my implementation I am appending to visited_positions as soon as we discover the cell and add to store
            # this is different from other BFS where we add to visited when we pop from store
                
            # North
            next_cell = (row-1, col)
            if maze.maze_map[(current_cell)]['N'] == 1 and row-1>0 and next_cell not in visited_positions:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                visited_positions.append(next_cell)

            # West
            next_cell = (row, col-1)
            if maze.maze_map[(current_cell)]['W'] == 1 and col-1>0 and next_cell not in visited_positions:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                visited_positions.append(next_cell)

            # South
            next_cell = (row+1, col)
            if maze.maze_map[(current_cell)]['S'] == 1 and row+1<=ROWS and next_cell not in visited_positions:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                visited_positions.append(next_cell)

            # East
            next_cell = (row, col+1)
            if maze.maze_map[(current_cell)]['E'] == 1 and col+1<=COLS and next_cell not in visited_positions:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                visited_positions.append(next_cell)

            
        if not store:
            print("No path to the goal exists.")
            break
    
    return list(visited_positions), path_to_goal

def BFS_V2(maze, start, goal):
    '''
    This function should implement the Breadth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    path_chain = {}
    path_to_goal = []
    path_chain[start] = None
    store = deque([start])
    visited_positions = []
    found_cells = set()

    found_cells.add(start)
    if start == goal:
        print("Start is the goal!")
        visited_positions.append(start)
        return visited_positions, [start]

    while True:
        current_cell = store.popleft()
        if current_cell in visited_positions:
            continue

        visited_positions.append(current_cell)
        row, col = current_cell

        if current_cell == goal:
            trace_back_path_to_goal(goal, path_to_goal, path_chain)
            break
        else: 
            
            # logically this implementation is more aligned with theroatical approach of BFS that only mark a node as visited after popping it from the queue
            # however to make sure that every thime you select a node from the queue it is not already visited, we need to maintain a set of found cells
            # this is because in BFS we can add the same cell multiple times to the queue from different parent cells, so we need to make sure we do not add a cell to the queue if it is already in the queue or already visited
            # this is different from my other BFS implementation where I add to visited as soon as I discover the cell and add to queue
            # North
            next_cell = (row-1, col)
            if maze.maze_map[(current_cell)]['N'] == 1 and row-1>0 and next_cell not in found_cells:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                found_cells.add(next_cell)

            # West
            next_cell = (row, col-1)
            if maze.maze_map[(current_cell)]['W'] == 1 and col-1>0 and next_cell not in found_cells:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                found_cells.add(next_cell)

            # South
            next_cell = (row+1, col)
            if maze.maze_map[(current_cell)]['S'] == 1 and row+1<=ROWS and next_cell not in found_cells:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                found_cells.add(next_cell)

            # East
            next_cell = (row, col+1)
            if maze.maze_map[(current_cell)]['E'] == 1 and col+1<=COLS and next_cell not in found_cells:
                store.append(next_cell)
                path_chain[next_cell] = current_cell
                found_cells.add(next_cell)

            
        if not store:
            print("No path to the goal exists.")
            break
    
    return list(visited_positions), path_to_goal

def heuristic(position, goal):
    '''
    This function should implement Euclidean Distance as the heuristic function used in A* algorithm.
    The inputs to this function are:
        position: The current position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        the heuristic value of the given position
    '''

    return math.sqrt((position[0] - goal[0])**2 + (position[1] - goal[1])**2)

def explore_cell(priority_queue, current_cell, next_cell, goal, g_scores, path_chain):
    g_of_n = g_scores[current_cell] +  1
    if next_cell in g_scores and g_of_n >= g_scores[next_cell]:
        return

    g_scores[next_cell] = g_of_n
    path_chain[next_cell] = current_cell
    f_of_n = g_of_n + heuristic(next_cell, goal)
    heapq.heappush(priority_queue, (f_of_n, next_cell))

def AStar(maze, start, goal):
    '''
    This function should implement the A* algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    
    path_to_goal = []
    visited_positions = []
    g_scores = {}
    path_chain = {}
    priority_queue = []

    # TODO: Implement A* Search algorithm here
    # NOTE: You can assume the cost of moving one step is 1 for this maze
    #       You can use the Euclidean distance as the heuristic function for this assignment

    g_scores[start] = 0
    path_chain[start] = None
    f_of_n = 0 + heuristic(start, goal)

    if start == goal:
        print("Start is the goal!")
        visited_positions.append(start)
        return visited_positions, [start]
        
    heapq.heappush(priority_queue, (f_of_n, start))

    while True:
        min_cost, current_cell = heapq.heappop(priority_queue) 

        if current_cell in visited_positions:
            continue
        
        visited_positions.append(current_cell)
        
        row, col = current_cell
        if current_cell == goal:
            trace_back_path_to_goal(goal, path_to_goal, path_chain)
            break
        else: 
            # # North
            next_cell = (row-1, col)
            if maze.maze_map[(current_cell)]['N'] == 1 and row-1 > 0:
                explore_cell(priority_queue, current_cell, next_cell, goal, g_scores, path_chain)

            # West
            next_cell = (row, col-1)
            if maze.maze_map[(current_cell)]['W'] == 1 and col-1 > 0:
                explore_cell(priority_queue, current_cell, next_cell, goal, g_scores, path_chain)

            # South
            next_cell = (row+1, col)
            if maze.maze_map[(current_cell)]['S'] == 1 and row <= ROWS:
                explore_cell(priority_queue, current_cell, next_cell, goal, g_scores, path_chain)

            # East
            next_cell = (row, col+1)
            if maze.maze_map[(current_cell)]['E'] == 1 and col <= COLS:
                explore_cell(priority_queue, current_cell, next_cell, goal, g_scores, path_chain)

        if not priority_queue:
            print("No path to the goal exists.")
            break

    return visited_positions, path_to_goal

def trace_back_path_to_goal(goal, path_to_goal, path_chain):
    node = goal
    while node is not None:
        path_to_goal.append(node)
        node = path_chain[node]

    path_to_goal.reverse()
    print("Goal reached!")


# DO NOT CHANGE THE LINES OF CODE BELOW
# -------------------------------------
# This part of the code calls the search algorithms implemented above and displays the results on the maze
def main():

    print('Start')
    print(f'Row: {m.rows}')

    print(f'key type: {type(list(m.maze_map.keys())[0])}')
    
    print(f'cell: {(m.maze_map[(1,1)]['E'])}')
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bfs", help="Run BFS", action="store_true")
    parser.add_argument("-d", "--dfs", help="Run DFS", action="store_true")
    parser.add_argument("-a", "--astar", help="Run A* Search", action="store_true")

    args = parser.parse_args()

    start = (ROWS, COLS)
    goal = (1,1)

    print(f"Start: {start}, Goal: {goal}")

    explored, path_to_goal = [], []
    algorithm_name = ""
    start_time = 0

    if args.bfs:
        algorithm_name = "Breadth-First Search (BFS)"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = BFS_V1(m, start, goal)
    elif args.dfs:
        algorithm_name = "Depth-First Search (DFS)"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = DFS_V2(m, start, goal)
        print(f"Explored: {explored}")
        print(f"Path to goal: {path_to_goal}")
    elif args.astar:
        algorithm_name = "A* Search"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = AStar(m, start, goal)
    else:
        print("No search algorithm specified. See help below.")
        parser.print_help()
        sys.exit()
    
    # --- Statistics Calculation and Printing ---
    if start_time > 0:
        end_time = time.time()
        execution_time = end_time - start_time
        path_length = len(path_to_goal)
        nodes_explored = len(explored)

        print("\n--- Search Algorithm Statistics ---")
        print(f"Algorithm: {algorithm_name}")
        print(f"Execution Time: {execution_time:.4f} seconds")
        print(f"Path Length: {path_length} steps")
        print(f"Nodes Explored: {nodes_explored} nodes")
        print("-------------------------------------\n")
    # -------------------------------------------

    # If a path was found, start visualization
    if path_to_goal:
        print("Starting visualization...")
        a = agent(m, ROWS, COLS, filled=True)
        b = agent(m, ROWS, COLS, color="red")

        m.tracePath({a: explored}, delay=30)
        m.tracePath({b: path_to_goal}, delay=80)

        m.run()
    else:
        print("No path to the goal was found!")


if __name__ == "__main__":
    main()