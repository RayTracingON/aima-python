from time import time
from search import *
from assignment1aux import *

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
        
        for i in range(len(state[0][0])):
            if state[0][0][i]!='rock':
                action.append(((0,i),'down'))
            if state[0][len(state[0])-1][i]!='rock':
                action.append(((len(state[0])-1,i),'up'))
        for i in range(len(state[0])):
            if state[0][i][0]!='rock':
                action.append(((i,0),'right'))
            if state[0][i][len(state[0][i])-1]!='rock':
                action.append(((i,len(state[0][i])-1),'left'))
        return action

    def result(self, state, action):
        # Task 2.2
        # Return a new state resulting from a given action being applied to a given state.
        # Replace the line below with your code.
        listState = list(list(row) for row in state[0])
        point=list(action[0])
        direction=action[1]
        while point[0]<len(state[0]) and point[1]>=0 and point[1]<len(state[0][0]) and state[0][point[0]][point[1]]!='rock' and point[0]>=0:
            if direction=='down':
                listState[point[0]][point[1]]='down'
                point[0]+=1
            elif direction=='up':
                listState[point[0]][point[1]]='up'
                point[0]-=1
            elif direction=='right':
                listState[point[0]][point[1]]='right'
                point[1]+=1
            elif direction=='left':
                listState[point[0]][point[1]]='left'
                point[1]-=1
        if point[0]<0 or point[0]>=len(state[0]) or point[1]<0 or point[1]>=len(state[0][0]):
            return (tuple(tuple(row) for row in listState), None, None)
        else:
            return (tuple(tuple(row) for row in state[0]), tuple(point), direction)


    def goal_test(self, state):
        # Task 2.3
        # Return a boolean value indicating if a given state is solved.
        # Replace the line below with your code.
        map=list(state[0])
        print(map)
        for i in map:
            if '' in i:
                return False
        return True
        

# Task 3
# Implement an A* heuristic cost function and assign it to the variable below.
astar_heuristic_cost = None

def beam_search(problem, f, beam_width):
    # Task 4
    # Implement a beam-width version A* search.
    # Return a search node containing a solved state.
    # Experiment with the beam width in the test code to find a solution.
    # Replace the line below with your code.
    raise NotImplementedError

if __name__ == "__main__":

    # Task 1 test code
    
    print('The loaded initial state is visualised below.')
    visualise(read_initial_state_from_file('/Users/rtxon/Library/Mobile Documents/com~apple~CloudDocs/Python/Assignment1/aima-python/assignment1config.txt'))
    

    # Task 2 test code
    
    garden = ZenPuzzleGarden('/Users/rtxon/Library/Mobile Documents/com~apple~CloudDocs/Python/Assignment1/aima-python/assignment1config.txt')
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
    '''
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
    '''

    # Task 4 test code
    '''
    print('Running beam search.')
    before_time = time()
    node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 50)
    after_time = time()
    print(f'Beam search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    '''
