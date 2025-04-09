from search import *
from random import randint
from assignment2aux import *

def read_tiles_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    tiles = []
    for line in lines:
        tile_row = []
        for i in range(len(line)):
            char = line[i]
            if char == ' ':
                tile_row.append(())
            elif char == 'i':
                tile_row.append((0,))
            elif char == 'L':
                tile_row.append((0,1))
            elif char == 'I':
                tile_row.append((0,2))
            elif char == 'T':
                tile_row.append((0,1,2))
        tiles.append(tile_row)
    return tuple(tuple(row) for row in tiles)


class KNetWalk(Problem):
    def __init__(self, tiles):
        if type(tiles) is str:
            self.tiles = read_tiles_from_file(tiles)
        else:
            self.tiles = tiles
        height = len(self.tiles)
        width = len(self.tiles[0])
        self.max_fitness = sum(sum(len(tile) for tile in row) for row in self.tiles)
        super().__init__(self.generate_random_state())

    def generate_random_state(self):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [randint(0, 3) for _ in range(height) for _ in range(width)]

    def actions(self, state):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [(i, j, k) for i in range(height) for j in range(width) for k in [0, 1, 2, 3] if state[i * width + j] != k]

    def result(self, state, action):
        pos = action[0] * len(self.tiles[0]) + action[1]
        return state[:pos] + [action[2]] + state[pos + 1:]

    def goal_test(self, state):
        return self.value(state) == self.max_fitness

    def value(self, state):
        count=0
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                for z in self.tiles[i][j]:
                    k=state[i*len(self.tiles[0])+j]+z
                    k=k%4
                    if k == 0 and j+1<len(self.tiles[i]):
                        if (2-state[i*len(self.tiles[0])+j+1])%4 in self.tiles[i][j+1]:
                            count+=1
                    if k==1 and i-1>=0:
                        if (3-state[(i-1)*len(self.tiles[0])+j])%4 in self.tiles[i-1][j]:
                            count+=1
                    if k==2 and j-1>=0:
                        if (4-state[i*len(self.tiles[0])+j-1])%4 in self.tiles[i][j-1]:
                            count+=1
                    if k==3 and i+1<len(self.tiles):
                        if (1-state[(i+1)*len(self.tiles[0])+j])%4 in self.tiles[i+1][j]:
                            count+=1
        return count
        
# Task 3
# Configure an exponential schedule for simulated annealing.
sa_schedule = exp_schedule(k=40, lam=0.5, limit=100)

# Task 4
# Configure parameters for the genetic algorithm.
pop_size = None
num_gen = 1000
mutation_prob = 0.1

def local_beam_search(problem, population):
    # Task 5
    # Implement local beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the next population contains no fitter state.
    # Replace the line below with your code.
    raise NotImplementedError

def stochastic_beam_search(problem, population, limit=1000):
    # Task 6
    # Implement stochastic beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the generation limit is reached.
    # Replace the line below with your code.
    raise NotImplementedError

if __name__ == '__main__':

    # Task 1 test code
    
    network = KNetWalk('assignment2config.txt')
    visualise(network.tiles, network.initial)
    

    # Task 2 test code
    '''
    run = 0
    method = 'hill climbing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = hill_climbing(network)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 3 test code
    
    run = 0
    method = 'simulated annealing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = simulated_annealing(network, schedule=sa_schedule)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    

    # Task 4 test code
    '''
    run = 0
    method = 'genetic algorithm'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = genetic_algorithm([network.generate_random_state() for _ in range(pop_size)], network.value, [0, 1, 2, 3], network.max_fitness, num_gen, mutation_prob)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 5 test code
    '''
    run = 0
    method = 'local beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = local_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 6 test code
    '''
    run = 0
    method = 'stochastic beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = stochastic_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''
