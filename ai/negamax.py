import numpy as np
import chess.engine
import random
import math
from constants import *
import torch

MAX_DEPTH = 2


def find_random_move(legal_moves: list) -> object:
    """
    Choses a random move from the move list given as an argument.
    """
    # randint is inclusive of last value
    if len(legal_moves) >= 1:
        random_index = random.randint(0, len(legal_moves) - 1)
        return legal_moves[random_index]


def find_best_move(model, game_state: object, legal_moves: list, return_queue):
    """
    Calculates the best move the AI could make in the next turn.
    """
    # shuffle the move list to randomize which move the AI will make in the case there are multiple moves with the same score
    global count
    count = 0
    np.random.shuffle(legal_moves)
    _, move = ab_negamax(model, game_state, legal_moves, MAX_DEPTH, 0, -math.inf, math.inf)
    return move


def ab_negamax(model,
    game_state,
    legal_moves,
    max_depth,
    current_depth,
    alpha,
    beta,
):
    """
    The Negamax algorithm is a variant on the minmax algorithm which calculates the best possible move a player could make to maximize their own position and minimize that of their opponments. Negamax simplifies this in the case of a two-player zero-sum game by using a singular score to represent the balance of power within the game. In chess, it usually means a positive score signifies a strong position for White and a negative score a strong position for Black.

    Alpha signifies the minimum score that the current player can be assured to achieve and the Beta is the maximum score that the opponent can be assured to achieve. To increase efficiency we can automatically discard all branches of the game in which Beta < Alpha, because we can reasonably assume the opponent will never make such a move.
    """
    global count
    count += 1

    base_case = current_depth == max_depth
    if base_case:
        return score_board(model, game_state), None

    # initialize values that will be bubbled up from lower in the search tree
    best_move = None
    best_score = -math.inf

    for move in legal_moves:
        game_state.execute_move(move)
        opponents_moves = game_state.get_legal_moves()

        recursed_score, _ = ab_negamax(model,
            game_state,
            opponents_moves,
            max_depth,
            current_depth + 1,
            -beta,
            -max(alpha, best_score),
        )
        current_score = -recursed_score

        if current_score > best_score:
            best_score = current_score
            best_move = move
        game_state.undo_move()

        # pruning out irrelevant nodes of the search tree to increase efficiency
        if best_score >= beta:
            break

    return best_score, best_move



def score_board(model, game_state: object) -> float:
    """
    Gives the current game state on the board a score
    """
    turn_multiplier = 1 if game_state.turn is WHITE else -1
    fen = forsyth_edwards_conversion(game_state)
    bin = fen_to_binary_encoding(fen)
    score = model(torch.from_numpy(bin))
    score = score.item()

    return turn_multiplier * score


def forsyth_edwards_conversion(game_state: object) -> str:
    """
    Converts the current game state to the Forsyth-Edwards Notation which is readable by stockfish.
    """
    # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    algebraic_notation_map = {
        "w_pawn": "P",
        "b_pawn": "p",
        "w_rook": "R",
        "b_rook": "r",
        "w_knight": "N",
        "b_knight": "n",
        "w_bishop": "B",
        "b_bishop": "b",
        "w_queen": "Q",
        "b_queen": "q",
        "w_king": "K",
        "b_king": "k",
    }

    fen = ""
    for row in np.arange(GRID_DIMENSION):
        blank_square_count = 0
        for col in np.arange(GRID_DIMENSION):
            piece = game_state.board[row][col]
            if not piece:
                blank_square_count += 1
                if col == 7:
                    fen += str(blank_square_count)

            else:
                if blank_square_count > 0:
                    fen += str(blank_square_count)
                    blank_square_count = 0
                fen += algebraic_notation_map[piece.image_code]
        if row < 7:
            fen += "/"

    # active color
    if game_state.turn == WHITE:
        fen += " w "
    else:
        fen += " b "

    # castling availibility
    fen += "- "

    # en passant target square
    fen += "- "

    # halfmove clock
    fen += "0 "

    # fullmove clock
    fen += str(len(game_state.move_log) // 2)
    return fen


def fen_to_binary_encoding(fen: str):
    board = chess.Board(fen)
    # get the occupied pieces on the board
    bl, wh = board.occupied_co
    # concatenate the arrays for the pieces
    bitboards = np.array([
        bl & board.pawns,
        bl & board.knights,
        bl & board.bishops,
        bl & board.rooks,
        bl & board.queens,
        bl & board.kings,
        wh & board.pawns,
        wh & board.knights,
        wh & board.bishops,
        wh & board.rooks,
        wh & board.queens,
        wh & board.kings,
    ], dtype=np.uint64)

    # convert to binary encoding
    bitboards = np.asarray(bitboards, dtype=np.uint64)[:, np.newaxis]
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    binary = (bitboards >> s).astype(np.uint8)
    binary = np.unpackbits(binary, bitorder="little")
    return binary.astype(np.single)