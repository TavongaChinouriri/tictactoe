X="X"
O="O"
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
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If the counts are equal, it's X's turn. Otherwise, it's O's turn.
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action.")

    # Create a deep copy of the board
    new_board = [row.copy() for row in board]

    # Make the move
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = [list(row) for row in board] + \
            [list(col) for col in zip(*board)] + \
            [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]

    if [X, X, X] in lines:
        return X
    elif [O, O, O] in lines:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is a terminal board, return None
    if terminal(board):
        return None

    # Define the utility function for minimax
    def minimax_utility(board, player):
        if terminal(board):
            return utility(board)

        if player == X:
            return max(minimax_utility(result(board, action), O) for action in actions(board))
        else:  # player == O
            return min(minimax_utility(result(board, action), X) for action in actions(board))

    # Player X aims to maximize the utility; Player O aims to minimize it
    if player(board) == X:
        _, action = max((minimax_utility(result(board, action), O), action) for action in actions(board))
    else:  # player(board) == O
        _, action = min((minimax_utility(result(board, action), X), action) for action in actions(board))

    return action
