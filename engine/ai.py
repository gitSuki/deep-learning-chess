import numpy as np
import random
import math

from constants import *

MAX_DEPTH = 2


def find_random_move(legal_moves: list) -> object:
    """
    Choses a random move from the move list given as an argument.
    """
    # randint is inclusive of last value
    if len(legal_moves) >= 1:
        random_index = random.randint(0, len(legal_moves) - 1)
        return legal_moves[random_index]


def find_best_move(game_state: object, legal_moves: list):
    """
    Calculates the best move the AI could make in the next turn.
    """
    # shuffle the move list to randomize which move the AI will make in the case there are multiple moves with the same score
    random.shuffle(legal_moves)
    score, move = ab_negamax(game_state, legal_moves, MAX_DEPTH, 0, -math.inf, math.inf)
    return move


def ab_negamax(
    game_state: object,
    legal_moves: list,
    max_depth: int,
    current_depth: int,
    alpha: int,
    beta: int,
):
    if current_depth == max_depth:
        return score_board(game_state), None

    best_move = None
    best_score = -math.inf

    for move in legal_moves:
        game_state.execute_move(move)
        opponents_moves = game_state.get_legal_moves()
        recursed_score, current_move = ab_negamax(
            game_state,
            opponents_moves,
            max_depth,
            current_depth + 1,
            -beta,
            -alpha,
        )
        current_score = -recursed_score

        if current_score > best_score:
            best_score = current_score
            best_move = move
        game_state.undo_move()

        # pruning
        best_score = max(best_score, alpha)
        if best_score >= beta:
            break
    return best_score, best_move


def score_board(game_state: object) -> int:
    """
    Gives the current game state on the board a score
    """
    turn_multiplier = 1 if game_state.turn is WHITE else -1
    # a positive score is good for white, negative good for black
    if game_state.checkmate:
        if game_state.turn == WHITE:
            return -math.inf  # black wins
        elif game_state.turn == BLACK:
            return math.inf  # white wins
    elif game_state.stalemate:
        return 0

    score = 0
    for row in np.arange(len(game_state.board)):
        for col in np.arange(len(game_state.board)):
            square = game_state.board[row][col]
            if square:
                if square.team == WHITE:
                    score += square.ai_value
                elif square.team == BLACK:
                    score -= square.ai_value

    return score * turn_multiplier
