import random

WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def get_winner(board):
    """Return the winning player symbol or None if there is no winner."""
    for a, b, c in WIN_COMBINATIONS:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None


def available_moves(board):
    """Return a list of available indices on the board."""
    return [index for index, value in enumerate(board) if value == ' ']


def minimax(board, is_maximizing, computer_letter, human_letter, depth=0):
    """
    Minimax algorithm for Tic-Tac-Toe.

    Args:
        board: List of 9 strings representing the board.
        is_maximizing: Whether it is the computer's turn.
        computer_letter: The AI letter ('X' or 'O').
        human_letter: The opponent's letter.
        depth: Recursion depth used for scoring.

    Returns:
        The best score for the current position from the perspective of the computer.
    """
    winner = get_winner(board)

    if winner == computer_letter:
        return 10 - depth
    if winner == human_letter:
        return depth - 10
    if not available_moves(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for move in available_moves(board):
            board[move] = computer_letter
            score = minimax(board, False, computer_letter, human_letter, depth + 1)
            board[move] = ' '
            best_score = max(best_score, score)
        return best_score

    best_score = float('inf')
    for move in available_moves(board):
        board[move] = human_letter
        score = minimax(board, True, computer_letter, human_letter, depth + 1)
        board[move] = ' '
        best_score = min(best_score, score)
    return best_score


def best_move(board, computer_letter, human_letter):
    """Choose the best legal move for the computer using minimax."""
    best_score = float('-inf')
    best_move_index = None

    for move in available_moves(board):
        board[move] = computer_letter
        score = minimax(board, False, computer_letter, human_letter, 0)
        board[move] = ' '

        if score > best_score:
            best_score = score
            best_move_index = move
            print(move)
    return best_move_index

def cpui(board, computer_letter, human_letter, difficulty):
    if difficulty ==  1:
        smart_chance = 0.2
    if difficulty ==  2:
        smart_chance = 0.6
    if difficulty ==  3:
        smart_chance = 0.9

    if random.random() < smart_chance:
        return best_move(board, computer_letter, human_letter)
    else:
        return random.choice(available_moves(board))


__all__ = ["best_move", "minimax", "get_winner", "available_moves", "cpui"]


