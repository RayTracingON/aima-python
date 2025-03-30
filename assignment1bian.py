import os
from search import *
from assignment1aux import animate

# ------------------------- Task 1: File Parser -------------------------
def read_initial_state_from_file(filename):
    """Read configuration file and generate initial state"""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    height = int(lines[0])
    width = int(lines[1])
    rocks = [tuple(map(int, line.split(','))) for line in lines[2:]]
    
    # Initialize garden map (using lists for mutable operations)
    garden = [['' for _ in range(width)] for _ in range(height)]
    for i, j in rocks:
        garden[i][j] = 'rock'
    
    # Convert to immutable tuples
    garden = tuple(tuple(row) for row in garden)
    return (garden, (-1, -1), '')  # (-1,-1) for perimeter position

# ------------------------- Task 2: Puzzle Implementation -------------------------
class ZenPuzzleGarden(Problem):
    """Zen Puzzle Garden problem class"""
    
    def __init__(self, initial=None, filename=None):
        if filename:
            initial = read_initial_state_from_file(filename)
        super().__init__(initial)
    
    # Task 2.1: Action Generator
    def actions(self, state):
        """Generate valid actions for current state"""
        map_data, pos, direction = state
        h, w = len(map_data), len(map_data[0])
        actions = []
        
        if pos == (-1, -1):  # On perimeter
            # Check all edge tiles for possible entry
            for i in range(h):
                for j in range(w):
                    if map_data[i][j] == '' and (i in (0, h-1) or j in (0, w-1)):
                        # Determine entry directions based on edge position
                        if i == 0: actions.append(((i, j), 'down'))
                        elif i == h-1: actions.append(((i, j), 'up'))
                        if j == 0: actions.append(((i, j), 'right'))
                        elif j == w-1: actions.append(((i, j), 'left'))
        else:  # Inside garden
            current_i, current_j = pos
            # Calculate possible turning directions (90-degree turns)
            if direction in ['up', 'down']:
                possible_dirs = ['left', 'right']
            else:
                possible_dirs = ['up', 'down']
            
            # Validate each possible direction
            for new_dir in possible_dirs:
                di, dj = 0, 0
                if new_dir == 'up': di = -1
                elif new_dir == 'down': di = 1
                elif new_dir == 'left': dj = -1
                else: dj = 1
                
                ni, nj = current_i + di, current_j + dj
                # Check next tile validity
                if 0 <= ni < h and 0 <= nj < w:
                    if map_data[ni][nj] == '':
                        actions.append(((current_i, current_j), new_dir))
                else:
                    actions.append(((current_i, current_j), new_dir))
        return actions

    # Task 2.2: State Transition
    def result(self, state, action):
        """Apply action and return new state"""
        old_map, old_pos, old_dir = state
        enter_pos, move_dir = action
        
        # Create mutable map copy
        new_map = [list(row) for row in old_map]
        new_pos, new_dir = (-1, -1), ''  # Default to perimeter
        
        # Entry from perimeter
        if old_pos == (-1, -1):
            ci, cj = enter_pos
            di, dj = 0, 0
            if move_dir == 'up': di = -1
            elif move_dir == 'down': di = 1
            elif move_dir == 'left': dj = -1
            else: dj = 1
            
            path = []
            while True:
                path.append((ci, cj))
                ni, nj = ci + di, cj + dj
                # Boundary check and tile validation
                if 0 <= ni < len(new_map) and 0 <= nj < len(new_map[0]):
                    if new_map[ni][nj] == '':
                        ci, cj = ni, nj
                    else:
                        new_pos = (ci, cj)
                        new_dir = move_dir
                        break
                else:
                    break
            # Update raked tiles
            for i, j in path:
                new_map[i][j] = move_dir
        # Movement inside garden
        else:
            ci, cj = old_pos
            di, dj = 0, 0
            if move_dir == 'up': di = -1
            elif move_dir == 'down': di = 1
            elif move_dir == 'left': dj = -1
            else: dj = 1
            
            path = []
            while True:
                path.append((ci, cj))
                ni, nj = ci + di, cj + dj
                if 0 <= ni < len(new_map) and 0 <= nj < len(new_map[0]):
                    if new_map[ni][nj] == '':
                        ci, cj = ni, nj
                    else:
                        new_pos = (ci, cj)
                        new_dir = move_dir
                        break
                else:
                    break
            # Update raked tiles
            for i, j in path:
                new_map[i][j] = move_dir
        
        return (tuple(map(tuple, new_map)), new_pos, new_dir)

    # Task 2.3: Goal Test
    def goal_test(self, state):
        """Check if state is goal state"""
        map_data, pos, _ = state
        # Must be on perimeter with all tiles raked
        return pos == (-1, -1) and all(cell != '' for row in map_data for cell in row)

# ------------------------- Task 3: Heuristic Function -------------------------
astar_heuristic_cost = lambda node: sum(row.count('') for row in node.state[0])

# ------------------------- Task 4: Beam Search -------------------------
# ------------------------- Task 4: Beam Search -------------------------
def beam_search(problem, f, beam_width):
    """Beam search implementation with width constraint"""
    from search import Node
    
    # Initialize with first node
    node = Node(problem.initial)
    frontier = [node]
    explored = set()
    
    while frontier:
        # Sort and truncate the frontier
        frontier.sort(key=lambda n: f(n))
        current_beam = frontier[:beam_width]
        next_frontier = []
        
        for node in current_beam:
            if problem.goal_test(node.state):
                return node
            explored.add(node.state)
            
            # Expand children using correct Node method
            for action in problem.actions(node.state):
                child = node.child_node(problem, action)  # Changed to child_node
                if child.state not in explored:
                    next_frontier.append(child)
        
        # Update frontier with sorted next generation
        frontier = sorted(next_frontier, key=lambda n: f(n))[:beam_width]
    
    return None


# ------------------------- Main Program -------------------------
if __name__ == '__main__':
    # Initialize puzzle
    garden = ZenPuzzleGarden(filename='assignment1config.txt')
    
    # Search method selection
    print("Select search algorithm:")
    print("1. Breadth-First Search (BFS)")
    print("2. A* Search")
    print("3. Beam Search")
    choice = input("Enter choice (1-3): ")
    
    # Execute selected algorithm
    if choice == '1':
        node = breadth_first_graph_search(garden)
    elif choice == '2':
        node = astar_search(garden, astar_heuristic_cost)
    elif choice == '3':
        node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 50)
    else:
        print("Invalid choice")
        exit()
    
    # Display results
    if node:
        print(f"Solution found with cost {node.path_cost}")
        animate(node)
    else:
        print("No solution found")
