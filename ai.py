import random

from constants import *

CHECKMATE = 1000
STALEMATE = 0


def find_random_move(legal_moves):
    # randint is inclusive of last value
    if len(legal_moves) >= 1:
        random_index = random.randint(0, len(legal_moves) - 1)
        return legal_moves[random_index]


def find_best_move(game_state, legal_moves):
    pass


def score_board(board: list) -> int:
    score = 0
    for row in board:
        for col in board:
            square = board[row][col]
            if square.team == WHITE:
                score += square.ai_value
            elif square.team == BLACK:
                score -= square.ai_value

    return score
