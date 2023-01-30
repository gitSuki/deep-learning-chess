import numpy as np
import random

from constants import *

DEPTH = 2
CHECKMATE = 1000
STALEMATE = 0


def find_random_move(legal_moves: list) -> object:
    """
    Choses a random move from the move list given as an argument
    """
    # randint is inclusive of last value
    if len(legal_moves) >= 1:
        random_index = random.randint(0, len(legal_moves) - 1)
        return legal_moves[random_index]


def find_best_move(game_state: object, legal_moves: list):
    global next_move
    next_move = None
    random.shuffle(legal_moves)
    turn_multiplier = 1 if game_state.turn is WHITE else -1
    negamax(game_state, legal_moves, DEPTH, -CHECKMATE, CHECKMATE, turn_multiplier)
    return next_move


def negamax(game_state: object, legal_moves: list, depth: int, alpha: int, beta: int, turn_multiplier: int):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = -CHECKMATE
    for move in legal_moves:
        game_state.execute_move(move)
        opponents_moves = game_state.get_legal_moves()
        score = -negamax(game_state, opponents_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()

        # pruning
        max_score = max(max_score, alpha)
        if alpha >= beta:
            break
    return max_score


def score_board(game_state: object) -> int:
    """
    Gives the current game state on the board a score
    """
    # a positive score is good for white, negative good for black
    if game_state.checkmate:
        if game_state.turn == WHITE:
            return -CHECKMATE  # black wins
        elif game_state.turn == BLACK:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE

    score = 0
    for row in np.arange(len(game_state.board)):
        for col in np.arange(len(game_state.board)):
            square = game_state.board[row][col]
            if square:
                if square.team == WHITE:
                    score += square.ai_value
                elif square.team == BLACK:
                    score -= square.ai_value

    return score
