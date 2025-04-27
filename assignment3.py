import math

from copy import deepcopy
from games4e import *

class EinStein(Game):

    def __init__(self):
        self.initial = GameState(to_move='R', utility=0, board={'R': (0, 0), 'B': (2, 2)}, moves=[(1, 1), (1, 0), (0, 1)])

    def compute_moves(self, board, to_move):
        moves = []
        if board[to_move]:
            if to_move == 'R':
                if board[to_move][0] < 2:
                    moves.append((board[to_move][0] + 1, board[to_move][1]))
                    if board[to_move][1] < 2:
                        moves.append((board[to_move][0] + 1, board[to_move][1] + 1))
                if board[to_move][1] < 2:
                    moves.append((board[to_move][0], board[to_move][1] + 1))
            if to_move == 'B':
                if board[to_move][0] > 0:
                    moves.append((board[to_move][0] - 1, board[to_move][1]))
                    if board[to_move][1] > 0:
                        moves.append((board[to_move][0] - 1, board[to_move][1] - 1))
                if board[to_move][1] > 0:
                    moves.append((board[to_move][0], board[to_move][1] - 1))
        return moves

    def display(self, state):
        displayed_board = [[' ' for _ in range(3)] for _ in range(3)]
        for player_i in ['R', 'B']:
            if state.board[player_i] is not None:
                displayed_board[state.board[player_i][0]][state.board[player_i][1]] = f'{player_i}'
        print('\n'.join(['|' + '|'.join(row) + '|' for row in displayed_board]), end='\n\n')

    def terminal_test(self, state):
        return state.utility != 0

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        # Task 1.1
        # Return a state resulting from the move.
        # Replace the line below with your code.
        new_board = deepcopy(state.board)
        if state.to_move == 'R':
            new_board['R'] = move
            if new_board['B'] == move:
                new_board['B'] = None
            new_utility = self.compute_utility(new_board)
            new_moves = self.compute_moves(new_board, 'B')
            return GameState(to_move='B', utility=new_utility, board=new_board, moves=new_moves)
        else:
            new_board['B'] = move
            if new_board['R'] == move:
                new_board['R'] = None
            new_utility = self.compute_utility(new_board)
            new_moves = self.compute_moves(new_board, 'R')
            return GameState(to_move='R', utility=new_utility, board=new_board, moves=new_moves)


    def utility(self, state, player):
        # Task 1.2
        # Return the state's utility to the player.
        # Replace the line below with your code.
        if player == 'R':
            return state.utility
        elif player == 'B':
            return -state.utility

    def compute_utility(self, board):
        # Task 1.3
        # Return the utility of the board.
        # Replace the line below with your code.
        if board['R'] == (2, 2) or board['B'] == None:
            return 1
        elif board['B'] == (0, 0) or board['R'] == None:
            return -1
        else:
            return 0

class MehrSteine(StochasticGame):

    def __init__(self, board_size):
        self.board_size = board_size
        self.num_piece = int((board_size - 1) * (board_size - 2) / 2)
        board = {'R': [], 'B': []}
        for i in range(board_size - 2):
            for j in range(board_size - 2 - i):
                board['R'].append((i, j))
                board['B'].append((board_size - 1 - i, board_size - 1 - j))
        self.initial = StochasticGameState(to_move='R', utility=0, board=board, moves=None, chance=None)

    def compute_moves(self, board, to_move, index):
        print(to_move, index,"co")
        moves = []
        coordinates = board[to_move][index]
        if to_move == 'R':
            if coordinates[0] < self.board_size - 1:
                moves.append((index, (coordinates[0] + 1, coordinates[1])))
                if coordinates[1] < self.board_size - 1:
                    moves.append((index, (coordinates[0] + 1, coordinates[1] + 1)))
            if coordinates[1] < self.board_size - 1:
                moves.append((index, (coordinates[0], coordinates[1] + 1)))
        if to_move == 'B':
            if coordinates[0] > 0:
                moves.append((index, (coordinates[0] - 1, coordinates[1])))
                if coordinates[1] > 0:
                    moves.append((index, (coordinates[0] - 1, coordinates[1] - 1)))
            if coordinates[1] > 0:
                moves.append((index, (coordinates[0], coordinates[1] - 1)))
        print(moves,"comfinal")
        return moves

    def display(self, state):
        spacing = 1 if self.num_piece == 1 else math.floor(math.log(self.num_piece - 1, 10)) + 1
        displayed_board = [[' ' * (spacing + 1) for _ in range(self.board_size)] for _ in range(self.board_size)]
        for player_i in ['R', 'B']:
            for piece_i in range(self.num_piece):
                if state.board[player_i][piece_i] is not None:
                    displayed_board[state.board[player_i][piece_i][0]][state.board[player_i][piece_i][1]] = player_i + str(piece_i).rjust(spacing)
        print('\n'.join(['|' + '|'.join(row) + '|' for row in displayed_board]), end='\n\n')

    def terminal_test(self, state):
        return state.utility != 0

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        # Task 2.1
        # Return a state resulting from the move.
        # Replace the line below with your code.
            
        print(state,move,"res")
        new_board = deepcopy(state.board) 
        if state.to_move == 'R':
            if move[1] in new_board['B']:                
                eaten_index = new_board['B'].index(move[1])
                new_board['B'][eaten_index] = None
            elif new_board['R'].count(move[1])==1:
                eaten_index = new_board['R'].index(move[1])
                new_board['R'][eaten_index] = None
            new_utility = self.compute_utility(new_board)
            if new_utility != 0:
                return StochasticGameState(to_move=None, utility=new_utility, board=new_board,moves=None, chance=None)
            new_board['R'][move[0]] = move[1]
            print(new_board,"resfinalR")
            return StochasticGameState(to_move='B', utility=new_utility, board=new_board,moves=None, chance=None)
        else:
            if move[1] in new_board['R']:
                eaten_index = new_board['R'].index(move[1])
                new_board['R'][eaten_index] = None
            elif new_board['B'].count(move[1])==1:
                eaten_index = new_board['B'].index(move[1])
                new_board['B'][eaten_index] = None
            new_utility = self.compute_utility(new_board)
            if new_utility != 0:
                return StochasticGameState(to_move=None, utility=new_utility, board=new_board,moves=None, chance=None)
            new_board['B'][move[0]] = move[1]
            print(new_board,"resfinalB")
            return StochasticGameState(to_move='R', utility=new_utility, board=new_board,moves=None, chance=None)

    def utility(self, state, player):
        # Task 2.2
        # Return the state's utility to the player.
        # Replace the line below with your code.
        if player == 'R':
            return state.utility
        elif player == 'B':
            return -state.utility

    def compute_utility(self, board):
        # Task 2.3
        # Return the utility of the board.
        # Replace the line below with your code.
        print(board,"comut")
        if (0,0) in board['B'] or board['R'].count(None)==self.num_piece:
            print("Bwin")
            return -1
        elif (self.board_size - 1, self.board_size - 1) in board['R'] or board['B'].count(None)==self.num_piece:
            print("Rwin")
            return 1
        else:
            return 0

    def chances(self, state):
        # Task 2.4
        # Return a list of possible chance outcomes.
        # Replace the line below with your code.
        num= self.num_piece
        a=[]
        for i in range(num):
            a.append(i)
        return a

    def outcome(self, state, chance):
        # Task 2.5
        # Return a state resulting from the chance outcome.
        # Replace the line below with your code.
        print(state.to_move,chance,"outcome")
        saved = None
        if state.board[state.to_move][chance] == None:#问题在这里
            while chance<self.num_piece-1:
                chance+=1
                if state.board[state.to_move][chance] != None:
                    saved=chance
                    break
            while chance>0:
                chance-=1
                if state.board[state.to_move][chance] != None:
                    break
            if saved:
                chance=saved
        move=self.compute_moves(state.board, state.to_move, chance)
        return StochasticGameState(to_move=state.to_move, utility=state.utility, board=state.board, moves=move, chance=state.chance)

    def probability(self, chance):
        # Task 2.6
        # Return the probability of a chance outcome.
        # Replace the line below with your code.
        return 1 / self.num_piece

def stochastic_monte_carlo_tree_search(state, game, playout_policy, N=1000):

    def select(n):
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.outcome(game.result(n.state, action), chance), parent=n): action for action in game.actions(n.state) for chance in game.chances(game.result(n.state, action))}
        return select(n)

    def simulate(game, state):
        player = game.to_move(state)
        while not game.terminal_test(state):
            action = playout_policy(game, state)
            state = game.result(state, action)
            if game.terminal_test(state):
                break
            chance = random.choice(game.chances(state))
            state = game.outcome(state, chance)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        if utility > 0:
            n.U += utility
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)

def schwarz_score(game, state):
    schwarz = {}
    valid_pieces = [piece_i for piece_i in range(game.num_piece) if state.board['R'][piece_i] is not None]
    if len(valid_pieces) == 0:
        schwarz['R'] = (game.board_size - 1) * game.num_piece
    elif len(valid_pieces) == 1:
        schwarz['R'] = game.board_size - 1 - min(state.board['R'][valid_pieces[0]])
    else:
        schwarz_per_piece = []
        for index_i, piece_i in enumerate(valid_pieces):
            if index_i == 0:
                schwarz_per_piece.append((game.board_size - 1 - min(state.board['R'][piece_i])) * game.num_piece / valid_pieces[1])
            elif index_i == len(valid_pieces) - 1:
                schwarz_per_piece.append((game.board_size - 1 - min(state.board['R'][piece_i])) * game.num_piece / (game.num_piece - valid_pieces[-2] - 1))
            else:
                schwarz_per_piece.append((game.board_size - 1 - min(state.board['R'][piece_i])) * game.num_piece / (valid_pieces[index_i + 1] - valid_pieces[index_i - 1] - 1))
        schwarz['R'] = min(schwarz_per_piece)
    valid_pieces = [piece_i for piece_i in range(game.num_piece) if state.board['B'][piece_i] is not None]
    if len(valid_pieces) == 0:
        schwarz['B'] = (game.board_size - 1) * game.num_piece
    elif len(valid_pieces) == 1:
        schwarz['B'] = max(state.board['B'][valid_pieces[0]])
    else:
        schwarz_per_piece = []
        for index_i, piece_i in enumerate(valid_pieces):
            if index_i == 0:
                schwarz_per_piece.append(max(state.board['B'][piece_i]) * game.num_piece / valid_pieces[1])
            elif index_i == len(valid_pieces) - 1:
                schwarz_per_piece.append(max(state.board['B'][piece_i]) * game.num_piece / (game.num_piece - valid_pieces[-2] - 1))
            else:
                schwarz_per_piece.append(max(state.board['B'][piece_i]) * game.num_piece / (valid_pieces[index_i + 1] - valid_pieces[index_i - 1] - 1))
        schwarz['B'] = min(schwarz_per_piece)
    return schwarz

def schwarz_diff_to_weight(diff, max_schwarz):
    # Task 3
    # Return a weight value based on the relative difference in Schwarz scores.
    # Replace the line below with your code.
    raise NotImplementedError

def random_policy(game, state):
    return random.choice(list(game.actions(state)))

def schwarz_policy(game, state):
    actions = list(game.actions(state))
    to_move = state.to_move
    opponent = 'B' if to_move == 'R' else 'R'
    weights = []
    for action in actions:
        state_prime = game.result(state, action)
        schwarz = schwarz_score(game, state_prime)
        schwarz_diff = schwarz[opponent] - schwarz[to_move]
        weights.append(schwarz_diff_to_weight(schwarz_diff, (game.board_size - 1) * game.num_piece))
    return random.choices(actions, weights=weights)[0]

def random_mcts_player(game, state):
    return stochastic_monte_carlo_tree_search(state, game, random_policy, 100)

def schwarz_mcts_player(game, state):
    return stochastic_monte_carlo_tree_search(state, game, schwarz_policy, 100)

if __name__ == '__main__':

    # Task 1 test code
    
    num_win = 0
    num_loss = 0
    for _ in range(50):
        if EinStein().play_game(alpha_beta_player, random_player) == 1:
            num_win += 1
        else:
            num_loss += 1
    for _ in range(50):
        if EinStein().play_game(random_player, alpha_beta_player) == 1:
            num_loss += 1
        else:
            num_win += 1
    print(f'alpha-beta pruned minimax player vs. random-move player: {num_win} wins and {num_loss} losses', end='\n\n')
    

    # Task 2 test code
    
    num_win = 0
    num_loss = 0
    for _ in range(50):
        if MehrSteine(4).play_game(random_mcts_player, random_player) == 1:
            num_win += 1
        else:
            num_loss += 1
    for _ in range(50):
        if MehrSteine(4).play_game(random_player, random_mcts_player) == 1:
            num_loss += 1
        else:
            num_win += 1
    print(f'MCTS with random playout vs. random-move player: {num_win} wins and {num_loss} losses', end='\n\n')
    

    # Task 3 test code
    '''
    num_win = 0
    num_loss = 0
    for _ in range(50):
        if MehrSteine(4).play_game(schwarz_mcts_player, random_mcts_player) == 1:
            num_win += 1
        else:
            num_loss += 1
    for _ in range(50):
        if MehrSteine(4).play_game(random_mcts_player, schwarz_mcts_player) == 1:
            num_loss += 1
        else:
            num_win += 1
    print(f'MCTS with Schwarz-based playout vs. MCTS with random playout: {num_win} wins and {num_loss} losses', end='\n\n')
    '''
