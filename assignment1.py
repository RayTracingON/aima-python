from time import time
from search import *
from assignment1aux import *
from heapq import heappush, heappop

def read_initial_state_from_file(filename):
    # Task 1
    # Return an initial state constructed using a configuration in a file.
    # Replace the line below with your code.
    temTuple = ()
    with open(filename, 'r') as file:
        lin = file.readlines()
        lines = [line.strip() for line in lin]
        height=int(lines[1])
        width=int(lines[0])
        map = [[''] * height for _ in range(width)]
        for i in range(2,len(lines)):
            temp=lines[i].split(',')
            map[int(temp[0])][int(temp[1])] = 'rock'
        tuple_map=tuple(tuple(row) for row in map)
        temTuple = (tuple_map, None, None)
    visualise(temTuple)
    return temTuple

class ZenPuzzleGarden(Problem):
    def __init__(self, initial):
        if type(initial) is str:
            super().__init__(read_initial_state_from_file(initial))
        else:
            super().__init__(initial)

    def actions(self, state):
        # Task 2.1
        # Return a list of all allowed actions in a given state.
        # Replace the line below with your code.
        action=[]
        if state[1] is None:
            for i in range(len(state[0][0])):
                if state[0][0][i]=='':
                    action.append(((0,i),'down'))
                if state[0][len(state[0])-1][i]=='':
                    action.append(((len(state[0])-1,i),'up'))
            for i in range(len(state[0])):
                if state[0][i][0]=='':
                    action.append(((i,0),'right'))
                if state[0][i][len(state[0][i])-1]=='':
                    action.append(((i,len(state[0][i])-1),'left'))
        else:
            point=list(state[1])
            if state[2]=='up':
                if point[0]>0 and state[0][point[0]-1][point[1]]=='' or point[0]==0:
                    action.append((tuple(point),'up'))
                else:
                    if point[1]>0 and state[0][point[0]][point[1]-1]=='' or point[1]==0:
                        action.append((tuple(point),'left'))
                    if point[1]<len(state[0][0])-1 and state[0][point[0]][point[1]+1]=='' or point[1]==len(state[0][0])-1:
                        action.append((tuple(point),'right'))
            elif state[2]=='down':
                if point[0]<len(state[0])-1 and state[0][point[0]+1][point[1]]=='' or point[0]==len(state[0])-1:
                    action.append((tuple(point),'down'))
                else:
                    if point[1]>0 and state[0][point[0]][point[1]-1]=='' or point[1]==0:
                        action.append((tuple(point),'left'))
                    if point[1]<len(state[0][0])-1 and state[0][point[0]][point[1]+1]=='' or point[1]==len(state[0][0])-1:
                        action.append((tuple(point),'right'))
            elif state[2]=='left':
                if point[1]>0 and state[0][point[0]][point[1]-1]=='' or point[1]==0:
                    action.append((tuple(point),'left'))
                else:
                    if point[0]<len(state[0])-1 and state[0][point[0]+1][point[1]]=='' or point[0]==len(state[0])-1:
                        action.append((tuple(point),'down'))
                    if point[0]<len(state[0])-1 and state[0][point[0]-1][point[1]]=='' or point[0]==0:
                        action.append((tuple(point),'up'))
            else:
                if point[1]<len(state[0][0])-1 and state[0][point[0]][point[1]+1]=='' or point[1]==len(state[0][0])-1:
                    action.append((tuple(point),'right'))
                else:
                    if point[0]<len(state[0])-1 and state[0][point[0]+1][point[1]]=='' or point[0]==len(state[0])-1:
                        action.append((tuple(point),'down'))
                    if point[0]>0 and state[0][point[0]-1][point[1]]=='' or point[0]==0:
                        action.append((tuple(point),'up'))
        return action

    def result(self, state, action):
        # Task 2.2
        # Return a new state resulting from a given action being applied to a given state.
        # Replace the line below with your code.
        listState = list(list(row) for row in state[0])
        point=list(action[0])
        direction=action[1]
        while point[0]<=len(state[0])-1 and point[1]>=0 and point[1]<=len(state[0][0])-1 and point[0]>=0:
            if direction=='down':
                if point[0]+1>len(state[0])-1:
                    listState[point[0]][point[1]]=direction
                    return (tuple(tuple(row) for row in listState), None, None)
                if state[0][point[0]+1][point[1]]!='':
                    break
                listState[point[0]][point[1]]='down'
                point[0]+=1
            elif direction=='up':
                if point[0]-1<0:
                    listState[point[0]][point[1]]=direction
                    return (tuple(tuple(row) for row in listState), None, None)
                if state[0][point[0]-1][point[1]]!='':
                    break
                listState[point[0]][point[1]]='up'
                point[0]-=1
            elif direction=='right':
                if point[1]+1>len(state[0][0])-1:
                    listState[point[0]][point[1]]=direction
                    return (tuple(tuple(row) for row in listState), None, None) 
                if state[0][point[0]][point[1]+1]!='':
                    break
                listState[point[0]][point[1]]='right'
                point[1]+=1
            elif direction=='left':
                if point[1]-1<0:
                    listState[point[0]][point[1]]=direction
                    return (tuple(tuple(row) for row in listState), None, None) 
                if state[0][point[0]][point[1]-1]!='':
                    break
                listState[point[0]][point[1]]='left'
                point[1]-=1
        return (tuple(tuple(row) for row in listState), tuple(point), direction)

    def goal_test(self, state):
        # Task 2.3
        # Return a boolean value indicating if a given state is solved.
        # Replace the line below with your code.
        map=list(state[0])
        for i in map:
            if '' in i:
                return False
        return True
        
def findhuristic(node):
    state=node.state

    # Add a penalty for disconnected empty regions to encourage filling contiguous areas
    def count_disconnected_regions(grid):
        visited = set()
        regions = 0
        def dfs(x, y):
            if (x, y) in visited or grid[x][y] != '':
                return
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    dfs(nx, ny)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '' and (i, j) not in visited:
                    regions += 1
                    dfs(i, j)
        return regions

    disconnected_regions = count_disconnected_regions(state[0])

    # Combine the two components into the heuristic
    return disconnected_regions
    

# Task 3
# Implement an A* heuristic cost function and assign it to the variable below.
astar_heuristic_cost = lambda n: findhuristic(n)
def beam_search(problem, f, beam_width):
    # Task 4
    # Implement a beam-width version A* search.
    # Return a search node containing a solved state.
    # Experiment with the beam width in the test code to find a solution.
    # Replace the line below with your code.
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = []
    frontier.append(node)
    explored = set()

    while frontier:
        for node in frontier:
            if problem.goal_test(node.state):
                return node
        next_frontier = []
        for node in frontier:
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    next_frontier.append(child)
        next_frontier.sort(key=f)
        frontier = next_frontier[:beam_width]
    return None


if __name__ == "__main__":

    # Task 1 test code
    print('The loaded initial state is visualised below.')
    garden = ZenPuzzleGarden(initial='assignment1config.txt')

    # Task 2 test code
    print('Running breadth-first graph search.')
    before_time = time()
    node = breadth_first_graph_search(garden)
    after_time = time()
    print(f'Breadth-first graph search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')


    # Task 3 test code
    
    print('Running A* search.')
    before_time = time()
    node = astar_search(garden, astar_heuristic_cost)
    after_time = time()
    print(f'A* search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    

    # Task 4 test code
    
    print('Running beam search.')
    before_time = time()
    node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 500)
    after_time = time()
    print(f'Beam search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    
