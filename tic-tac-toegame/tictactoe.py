"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    current_state = board
    player_x = 0
    player_o = 0
    first_move = 0
    current_player = "X"
    subsequent_player = "O"
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] == "X":
                player_x += 1
            elif current_state[i][j] == "O":
                player_o += 1
            elif current_state[i][j] == None:
                first_move += 1

    if first_move == 9:
        return current_player
    elif player_x > player_o:
        return subsequent_player
    elif player_o == player_x:
        return current_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    current_state = board
    available_actions = []
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] == None:
                temp = [0, 0]
                temp[0] = i
                temp[1] = j
                available_actions.append(temp)

    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    action = tuple(action)
    updated_state = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if updated_state[i][j] == "X" or updated_state[i][j] == "O":
        raise NameError ("Not Valid Move")
    current_player = player(updated_state)
    if updated_state[i][j] == None:
        updated_state[i][j] = current_player
        return updated_state




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    current_state = board

    i = 0
    j = 0

    foo = current_state[i][j]
    boo = current_state[i + 1][j]
    baz = current_state[i + 2][j]
    oo = current_state[i + 1][j + 2]
    booj = current_state[i][j + 1]
    bazj = current_state[i][j + 2]
    booij = current_state[i + 1][j + 1]
    bazij = current_state[i + 2][j + 2]
    zoo = current_state[i + 2][j + 1]

    if foo == boo and foo == baz:#

        return foo

    if foo == booj and foo == bazj:#

        return foo

    if foo == booij and foo == bazij:#

        return foo

    if  zoo == booij and zoo == booj:#

        return zoo

    if oo == booij and oo == boo:#

        return oo

    if booij == booj and booij == zoo:#

        return booij

    if booij == bazj and booij == baz:#

        return booij

    if baz == zoo and baz == bazij:#

        return baz

    if bazij == oo and bazij == bazj:#

        return bazij

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    current_state = board
    if winner(current_state) == "X" or winner(current_state) == "O" and winner(current_state) != None:
        return True
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    elif win == None:
        return 0
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_state = board
    current_player = player(current_state)
    maxmin = 0
    opt_action = [0,0]
    if current_player == "X":
        player_check = 1
    else:
        player_check = -1
    if terminal(current_state) == True:
        return None

    act = actions(current_state)
    if player_check == 1:
        for i in range(len(act)):
            max = min_value(result(current_state, act[i]))
            if max >= maxmin:
                maxmin = max
                opt_action[0] = act[i][0]
                opt_action[1] = act[i][1]

    if player_check == -1:
        for i in range(len(act)):
            max = max_value(result(current_state, act[i]))
            if max <= maxmin:
                maxmin = max
                opt_action[0] = act[i][0]
                opt_action[1] = act[i][1]

    return opt_action


def max_value(board):
    val = -math.inf
    if terminal(board) == True:
        return utility(board)
    for action in actions(board):
        val = max(val, min_value(result(board, action)))
    return val


def min_value(board):
    val = math.inf
    if terminal(board) == True:
        return utility(board)
    for action in actions(board):
        val = min(val, max_value(result(board, action)))
    return val
