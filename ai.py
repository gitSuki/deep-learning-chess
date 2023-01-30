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


# def find_best_move(game_state: object, legal_moves: list) -> object:
#     """
#     Calculates the best move that the AI could take next turn.
#     """
#     # it's good for white if it's a positive score
#     # it's bad for black if it's a negative score
#     turn_multiplier = 1 if game_state.turn is WHITE else -1

#     opponent_minmax_score = CHECKMATE  # calculating from blacks perspective, we want to start from the worst possible score.
#     best_player_move = None
#     random.shuffle(legal_moves)
#     for player_move in legal_moves:
#         game_state.execute_move(player_move)
#         opponents_moves = game_state.get_legal_moves()

#         opponent_max_score = -CHECKMATE

#         if game_state.checkmate:
#             opponent_max_score = -CHECKMATE
#         elif game_state.stalemate:
#             opponent_max_score = STALEMATE
#         else:
#             opponent_max_score = -CHECKMATE
#             for opponent_move in opponents_moves:
#                 game_state.execute_move(opponent_move)
#                 game_state.get_legal_moves()
#                 if game_state.checkmate:
#                     score = CHECKMATE * -turn_multiplier
#                 elif game_state.stalemate:
#                     score = STALEMATE
#                 else:
#                     score = -score_board(game_state.board) * turn_multiplier

#                 if score > opponent_max_score:
#                     opponent_max_score = score

#                 game_state.undo_move()
#         if opponent_max_score < opponent_minmax_score:
#             opponent_minmax_score = opponent_max_score
#             best_player_move = player_move
#         game_state.undo_move()
#     return best_player_move


def find_best_move(game_state: object, legal_moves: list):
    global next_move
    next_move = None
    random.shuffle(legal_moves)
    turn_multiplier = 1 if game_state.turn is WHITE else -1
    negamax(game_state, legal_moves, DEPTH, turn_multiplier)
    return next_move


# def minmax(game_state: object, legal_moves: list, depth: int, turn: str):
#     global next_move
#     if depth == 0:
#         return score_board(game_state)

#     if game_state.turn == WHITE:
#         max_score = -CHECKMATE
#         for move in legal_moves:
#             game_state.execute_move(move)
#             next_moves = game_state.get_legal_moves()
#             score = minmax(game_state, next_moves, depth - 1, BLACK)
#             if score > max_score:
#                 max_score = score
#                 if depth == DEPTH:
#                     next_move = move
#             game_state.undo_move()
#         return max_score

#     elif game_state.turn == BLACK:
#         min_score = CHECKMATE
#         for move in legal_moves:
#             game_state.execute_move(move)
#             next_moves = game_state.get_legal_moves()
#             score = minmax(game_state, next_moves, depth - 1, WHITE)
#             if score < min_score:
#                 min_score = score
#                 if depth == DEPTH:
#                     next_move = move
#             game_state.undo_move()
#         return min_score


def negamax(game_state: object, legal_moves: list, depth: int, turn_multiplier: int):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = -CHECKMATE
    for move in legal_moves:
        game_state.execute_move(move)
        opponents_moves = game_state.get_legal_moves()
        score = -negamax(game_state, opponents_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
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
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board)):
            square = game_state.board[row][col]
            if square:
                if square.team == WHITE:
                    score += square.ai_value
                elif square.team == BLACK:
                    score -= square.ai_value

    return score
