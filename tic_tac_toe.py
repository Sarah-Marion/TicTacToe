"""
tic_tac_toe
"""
from typing import Any, List, Tuple
import random
import copy


def copy_dict(d: dict) -> dict:
    """
    Return an exact copy of dictionary <d>. The dictionary has to have all
    keys referring to values that are arrays such as tuples, lists, etc.
    """
    new_dict = {}
    for key in d:
        new_dict[key] = d[key]
    return new_dict


def extract_winner(state: 'TicTacToeState') -> str:
    """
    Return the winner of the game, or announce if the game resulted in a
    tie.
    """
    winner = 'No one'
    tictactoe = TicTacToeGame(True)
    tictactoe.current_state = state
    if tictactoe.is_winner('O'):
        winner = 'O'
    elif tictactoe.is_winner('X'):
        winner = 'X'
    return winner


def interactive_strategy(game) -> int:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return int(move)


def recursive_minimax(game: 'TicTacToeGame') -> int:
    """
    Return a valid move that is the optimal move given the current state
    of the game <game>.
    """
    # extract the current_state
    state = game.current_state

    # get the best moves
    best_moves = get_best_moves_rec(state)

    # return a random move from the pool of best moves
    return best_moves[random.randint(0, len(best_moves) - 1)]


def get_best_moves_rec(state: 'TicTacToeState') -> list:
    """
    Return a list of best moves given the current state <state> of the game.
    """
    # get all the possible moves
    moves = state.get_possible_moves()

    # initiates a dict that maps scores to moves
    score_to_move = {}

    # loop over every move and make the move, score the state resulting from
    # that move and multiply it by -1 because that will be the score the
    # opposing player; add the move to the list of the key that is the score
    # of that move
    for move in moves:
        next_state = state.make_move(move)
        if -1 * score_state_rec(next_state) not in score_to_move:
            score_to_move[-1 * score_state_rec(next_state)] = [move]
        else:
            score_to_move[-1 * score_state_rec(next_state)].append(move)

    # extract the list of moves that has the highest score
    best_moves = score_to_move[max(score_to_move)]

    # return that list
    return best_moves


def score_state_rec(state: 'TicTacToeState') -> int:
    """
    Return the score that corresponds with the state <state>.
    """
    # get the current player
    player = state.current_player

    # get the opponent
    opponent = 'X' if player == 'O' else 'O'

    # check if the state is terminal
    if state.get_possible_moves() == []:
        # get the winner
        winner = extract_winner(state)
        # score is default a tie, unless a winner is identified
        score = 0
        if winner == player:
            score = 1
        elif winner == opponent:
            score = -1
        return score

    else:
        next_moves = state.get_possible_moves()
        scores = []
        for next_move in next_moves:
            next_state = state.make_move(next_move)
            scores.append(-1 * score_state_rec(next_state))
        return max(scores)


class TicTacToeGame:
    """
    Good 'ol Tic-Tac-Toe!
    """
    winning_combo = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                     [1, 4, 7], [2, 5, 8], [3, 6, 9],
                     [1, 5, 9], [3, 5, 7]]

    def __init__(self, x_first: bool) -> None:
        """
        Inititates a game of Tic-Tac-Toe.
        """
        self.x_first = x_first
        player = 'X' if self.x_first else 'O'
        self.current_state = \
            TicTacToeState({1: 1, 2: 2, 3: 3,
                            4: 4, 5: 5, 6: 6,
                            7: 7, 8: 8, 9: 9},
                           [1, 2, 3, 4, 5, 6, 7, 8, 9],
                           player)

    def is_over(self) -> bool:
        """
        Return True if the game is over, False otherwise.
        """
        if len(self.current_state.cells_unowned) == 0:
            return True

        player_to_cells = {'X': [], 'O': []}
        cells_owned = self.current_state.cells_owned
        for cell in cells_owned:
            if cells_owned[cell] in player_to_cells:
                player_to_cells[cells_owned[cell]].append(cell)
        for player in player_to_cells:
            if any(
                    [all(
                        [cell in player_to_cells[player]
                         for cell in combo])
                        for combo in self.winning_combo]):
                return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return the winner of the game, or announce if the game resulted in a
        tie.
        """
        player_cells = self.current_state.cells_owned
        cells_owned = [cell for cell in player_cells
                       if player_cells[cell] == player]
        for combo in self.winning_combo:
            if all([cell in cells_owned for cell in combo]):
                return True
        return False


class TicTacToeState:
    """
    A class that keeps track of the current state of the game Tic-Tac-Toe.
    """

    def __init__(self, cells_owned: dict,
                 cells_unowned: list,
                 current_player: str) -> None:
        """
        Initiates an instance of a state of the game Tic-Tac-Toe.
        """
        self.cells_owned = cells_owned
        self.current_player = current_player
        self.cells_unowned = cells_unowned

    def get_possible_moves(self) -> list:
        """
        Return a list of possible moves from the current state <self>.
        """
        game_check = TicTacToeGame(True)
        game_check.current_state = self
        if game_check.is_over():
            return []
        return self.cells_unowned

    def is_valid_move(self, move: Any) -> bool:
        """
        Return True if the move entered is valid, False otherwise.
        """
        return move in self.get_possible_moves()

    def make_move(self, move: int) -> 'TicTacToeState':
        """
        Make the move, and return the resulting state.
        """
        new_cells_unowned = [cell for cell in self.cells_unowned
                             if cell != move]
        new_cells_owned = copy_dict(self.cells_owned)
        new_cells_owned[move] = self.current_player
        new_player = 'O' if self.current_player == 'X' else 'X'
        return TicTacToeState(new_cells_owned, new_cells_unowned, new_player)

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        game_board = \
            f"""
        {self.cells_owned[1]} | {self.cells_owned[2]} | {self.cells_owned[3]}
        _________
                             
        {self.cells_owned[4]} | {self.cells_owned[5]} | {self.cells_owned[6]}
        _________
        
        {self.cells_owned[7]} | {self.cells_owned[8]} | {self.cells_owned[9]}
        """
        return game_board


if __name__ == '__main__':
    first_player = ''
    while not first_player.isalpha() or first_player.upper() not in 'XO':
        first_player = input('Type X if player X is to go first, '
                             'or O if player O is to go first: ')

    x_first = True if first_player == "X" else False

    game = TicTacToeGame(x_first)

    strategy = {'i': interactive_strategy, 'c': recursive_minimax}

    print(f'Please choose a valid strategy for your players, '
          f'interactive strategy (type i) means human players '
          f'and minimax (type c) is a computer opponent '
          f'(it will be hard to beat!).')

    strategy_X = ''
    while strategy_X not in strategy:
        strategy_X = input('Pick a strategy for X: ')

    strategy_O = ''
    while strategy_O not in strategy:
        strategy_O = input('Pick a strategy for O: ')

    strategy_X = strategy[strategy_X.lower()]
    strategy_O = strategy[strategy_O.lower()]

    current_state = game.current_state

    while not game.is_over():
        print(current_state)
        for move in current_state.get_possible_moves():
            print(move)

        move_to_make = ''

        while not current_state.is_valid_move(move_to_make):
            strategy_to_use = strategy_X
            if current_state.current_player == 'O':
                strategy_to_use = strategy_O
            move_to_make = strategy_to_use(game)

        new_state = current_state.make_move(int(move_to_make))
        current_state = new_state
        game.current_state = current_state

    print(game.current_state)
    if game.is_winner('X'):
        print(f'Congratulations X, you won!')
    elif game.is_winner('O'):
        print(f'Congratulations O, you won!')
    else:
        print("It's a tie!")