import os


def read_maze(file):
    with open(file, 'r') as f:
        maze = f.read().splitlines()
    return maze


def print_maze(maze):
    for line in maze:
        print(line)
    print()

def save_sol(maze, filename):
    with open(filename, 'w') as f:
        for line in maze:
            f.write(line)
            f.write('\n')


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(maze):
    # find start and goal
    start = None
    goals = []
    for i, line in enumerate(maze):
        for j, c in enumerate(line):
            if c == 'P':
                start = (i, j)
            if c == '.':
                goals.append((i, j))

    # search
    queue = [start]
    nodes_expanded = 0
    cost = 0
    depth = 0
    fringe_size = 0
    came_from = {}
    came_from[start] = None
    visited = set()
    while queue:
        current = queue.pop(0)
        if current[0] < 0 or current[0] >= len(maze) or current[1] < 0 or current[1] >= len(maze[0]) or maze[current[0]][current[1]] == '%':
            continue
        if current in goals:
            maze[current[0]] = maze[current[0]][:current[1]] + '*' + maze[current[0]][current[1] + 1:]
            goals.remove(current)
            if not goals:
                break
        if current not in visited:
            visited.add(current)
            maze[current[0]] = maze[current[0]][:current[1]] + '*' + maze[current[0]][current[1] + 1:]
            queue.append((current[0], current[1] - 1))
            queue.append((current[0], current[1] + 1))
            queue.append((current[0] - 1, current[1]))
            queue.append((current[0] + 1, current[1]))
            nodes_expanded += 1
            cost += 1
            depth = max(depth, len(queue))
            fringe_size = max(fringe_size, len(queue))
            queue.sort(key=lambda x: manhattan_distance(x, goals[0]))
            came_from[current] = came_from.get(current, None)

    maze[start[0]] = maze[start[0]][:start[1]] + 'P' + maze[start[0]][start[1] + 1:]
    
    return {'maze': maze, 'cost': cost, 'nodes_expanded': nodes_expanded, 'depth': depth, 'fringe_size': fringe_size}


def bfs(maze):
    MAX_BREADTH = 1000
    # find start and goal
    start = None
    goals = []
    for i, line in enumerate(maze):
        for j, c in enumerate(line):
            if c == 'P':
                start = (i, j)
            if c == '.':
                goals.append((i, j))

    # search
    queue = [start]
    nodes_expanded = 0
    cost = 0
    depth = 0
    fringe_size = 0
    came_from = {}
    came_from[start] = None
    visited = set()
    while queue:
        current = queue.pop(0)
        # check if current is within the maze
        if current[0] < 0 or current[0] >= len(maze) or current[1] < 0 or current[1] >= len(maze[0]) or maze[current[0]][current[1]] == '%':
            continue
        if current in goals:
            maze[current[0]] = maze[current[0]][:current[1]] + '*' + maze[current[0]][current[1] + 1:]
            goals.remove(current)
            if not goals:
                break
        if current not in visited:
            visited.add(current)
            maze[current[0]] = maze[current[0]][:current[1]] + '*' + maze[current[0]][current[1] + 1:]
            queue.append((current[0], current[1] - 1))
            queue.append((current[0], current[1] + 1))
            queue.append((current[0] - 1, current[1]))
            queue.append((current[0] + 1, current[1]))
            nodes_expanded += 1
            cost += 1
            depth = max(depth, len(queue))
            fringe_size = max(fringe_size, len(queue))
            came_from[current] = came_from.get(current, None)
     
    maze[start[0]] = maze[start[0]][:start[1]] + 'P' + maze[start[0]][start[1] + 1:]

    return {'maze': maze, 'cost': cost, 'nodes_expanded': nodes_expanded, "depth":depth, 'fringe_size': fringe_size}


# '%' stands for the walls
# 'P' stands for the starting position
# '.' stands for all the goal positions to be visited
data_folder = "Maze"
files = ['tinySearch.lay','smallSearch.lay','trickySearch.lay']
for f in files:
    print(f"\n{f}")
    maze = read_maze(os.path.join(data_folder, f))

    a = a_star(maze.copy())
    b = bfs(maze.copy())

    print(f"{'Algorithm':<15}{'Cost':<15}{'Nodes Expanded':<15}{'Max Depth':<15}{'Max Fringe Size':<15}")
    print(f"{'A*':<15}{a['cost']:<15}{a['nodes_expanded']:<15}{a['depth']:<15}{a['fringe_size']:<15}")
    print(f"{'BFS':<15}{b['cost']:<15}{b['nodes_expanded']:<15}{b['depth']:<15}{b['fringe_size']:<15}")

    save_sol(a['maze'], os.path.join(data_folder, f"a_star_multi_{f}"))
    save_sol(b['maze'], os.path.join(data_folder, f"bfs_multi_{f}"))

    print_maze(maze)
    print_maze(a['maze'])
    print_maze(b['maze'])
