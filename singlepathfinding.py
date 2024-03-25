"""
 Program: Maze Search
"""

import os


def bfs(maze):
    sol_maze = maze.copy()

    # find the starting position
    start = (0, 0)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                start = (i, j)
                sol_maze[i] = sol_maze[i][:j] + ' ' + sol_maze[i][j+1:]
                break

    # find the goal
    goal = (0, 0)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '.':
                goal = (i, j)
                break

    # search
    queue = [start]
    nodes_expanded = 0
    cost = 0
    depth = 0
    fringe_size = 0

    while queue:
        current = queue.pop(0)
        if current == goal:
            # print('Found the goal!')
            break
        if sol_maze[current[0]][current[1]] == ' ':
            sol_maze[current[0]] = sol_maze[current[0]][:current[1]] + '.' + sol_maze[current[0]][current[1]+1:]
            queue.append((current[0], current[1]-1))
            queue.append((current[0], current[1]+1))
            queue.append((current[0]-1, current[1]))
            queue.append((current[0]+1, current[1]))
            nodes_expanded += 1
            cost += 1
            depth = max(depth, len(queue))
            fringe_size = max(fringe_size, len(queue))
    
    # sol_maze[start[0]] = sol_maze[start[0]][:start[1]] + 'P' + sol_maze[start[0]][start[1]+1:]
    return {'maze': sol_maze, 'cost': cost, 'nodes_expanded': nodes_expanded, 'depth': depth, 'fringe_size': fringe_size}

def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star(maze):
    sol_maze = maze.copy()

    # find the starting position
    start = (0, 0)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                start = (i, j)
                sol_maze[i] = sol_maze[i][:j] + ' ' + sol_maze[i][j+1:]
                break

    # find the goal
    goal = (0, 0)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '.':
                goal = (i, j)
                break

    # search
    queue = [start]
    nodes_expanded = 0
    cost = 0
    depth = 0
    fringe_size = 0
    
    while queue:
        current = queue.pop(0)
        if current == goal:
            # print('Found the goal!')
            break
        if sol_maze[current[0]][current[1]] == ' ':
            sol_maze[current[0]] = sol_maze[current[0]][:current[1]] + '.' + sol_maze[current[0]][current[1]+1:]
            queue.append((current[0], current[1]-1))
            queue.append((current[0], current[1]+1))
            queue.append((current[0]-1, current[1]))
            queue.append((current[0]+1, current[1]))
            nodes_expanded += 1
            cost += 1
            depth = max(depth, len(queue))
            fringe_size = max(fringe_size, len(queue))
            queue.sort(key=lambda x: manhattan_distance(x, goal))
    
    sol_maze[start[0]] = sol_maze[start[0]][:start[1]] + 'P' + sol_maze[start[0]][start[1]+1:]
    return {'maze': sol_maze, 'cost': cost, 'nodes_expanded': nodes_expanded, 'depth': depth, 'fringe_size': fringe_size}


def read_maze(filename):
    with open(filename, 'r') as f:
        maze = []
        for line in f:
            maze.append(line.strip())
    return maze

def print_maze(maze):
    for line in maze:
        print(line)

def save_sol(maze, filename):
    with open(filename, 'w') as f:
        for line in maze:
            f.write(line)
            f.write('\n')


# '%' stands for the walls
# 'P' stands for the starting position
# '.' stands for the goal 
data_folder = "Maze"
files = ['smallMaze.lay', 'mediumMaze.lay', 'bigMaze.lay', 'openMaze.lay']
for f in files:
    print(f"\n{f}")
    maze = read_maze(os.path.join(data_folder, f))
    b = bfs(maze)
    a = a_star(maze)
    
    # print table
    print(f"{'Algorithm':<15}{'Cost':<15}{'Nodes Expanded':<15}{'Max Depth':<15}{'Max Fringe Size':<15}")
    print(f"{'BFS':<15}{b['cost']:<15}{b['nodes_expanded']:<15}{b['depth']:<15}{b['fringe_size']:<15}")
    print(f"{'A*':<15}{a['cost']:<15}{a['nodes_expanded']:<15}{a['depth']:<15}{a['fringe_size']:<15}")

    save_sol(b['maze'], os.path.join(data_folder, f"bfs_{f}"))
    save_sol(a['maze'], os.path.join(data_folder, f"a_star_{f}"))

    print_maze(b['maze'])
    print_maze(a['maze'])

