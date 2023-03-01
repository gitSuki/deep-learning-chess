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


def find_best_move(model, game_state: object, legal_moves: list):
    """
    Calculates the best move the AI could make in the next turn.
    """
    # shuffle the move list to randomize which move the AI will make in the case there are multiple moves with the same score
    np.random.shuffle(legal_moves)
    _, move = ab_negamax(
        model, game_state, legal_moves, MAX_DEPTH, 0, -math.inf, math.inf
    )
    return move


def ab_negamax(
    model,
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
    base_case = current_depth == max_depth
    if base_case:
        return score_board(model, game_state), None

    # initialize values that will be bubbled up from lower in the search tree
    best_move = None
    best_score = -math.inf

    for move in legal_moves:
        game_state.execute_move(move)
        opponents_moves = game_state.get_legal_moves()

        recursed_score, _ = ab_negamax(
            model,
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
    Gives the current game state on the board a score.
    """
    turn_multiplier = 1 if game_state.turn is WHITE else -1
    fen = forsyth_edwards_conversion(game_state)
    binary = fen_to_binary_encoding(fen)
    score = model(torch.from_numpy(binary))
    score = score.item()

    return turn_multiplier * score


def forsyth_edwards_conversion(game_state: object) -> str:
    """
    Converts the current game state to the Forsyth-Edwards Chess Notation.
    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """
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

    # castling availibility (castling is not implemented)
    fen += "- "

    # en passant target square (en passant is not implemented)
    fen += "- "

    # halfmove clock (does not need to be calculated since this function is only called by the AI)
    fen += "0 "

    # fullmove clock
    fen += str(len(game_state.move_log) // 2)
    return fen


def fen_to_binary_encoding(fen: str) -> float:
    """
    Converts a string in Forsyth-Edwards Chess Notation into binary
    """
    # get the bitboards for each team from the board
    board = chess.Board(fen)
    black_squares, white_squares = board.occupied_co

    # Create the bitboards for each individual type of chess piece per team
    b_pawn_bitboard = black_squares & board.pawns
    b_knight_bitboard = black_squares & board.knights
    b_bishop_bitboard = black_squares & board.bishops
    b_rook_bitboard = black_squares & board.rooks
    b_queen_bitboard = black_squares & board.queens
    b_king_bitboard = black_squares & board.kings
    w_pawn_bitboard = white_squares & board.pawns
    w_knight_bitboard = white_squares & board.knights
    w_bishop_bitboard = white_squares & board.bishops
    w_rook_bitboard = white_squares & board.rooks
    w_queen_bitboard = white_squares & board.queens
    w_king_bitboard = white_squares & board.kings

    # Combine the bitboards for each chess piece into a single array
    bitboards = np.array(
        [
            b_pawn_bitboard,
            b_knight_bitboard,
            b_bishop_bitboard,
            b_rook_bitboard,
            b_queen_bitboard,
            b_king_bitboard,
            w_pawn_bitboard,
            w_knight_bitboard,
            w_bishop_bitboard,
            w_rook_bitboard,
            w_queen_bitboard,
            w_king_bitboard,
        ],
        dtype=np.uint64,
    )

    # add a new dimension to the bitboards array to make bitwise operations simpler for conversion into binary
    bitboards = np.asarray(bitboards, dtype=np.uint64)[:, np.newaxis]
    shift_amounts = GRID_DIMENSION * np.arange(
        GRID_DIMENSION - 1, -1, -1, dtype=np.uint64
    )
    # shift the bits in the bitboards array by the shift amounts and convert to uint8 data type
    binary = (bitboards >> shift_amounts).astype(np.uint8)
    # converts the binary values to a 1D array of individual bits
    binary = np.unpackbits(binary, bitorder="little")
    # returns a float data type to be used by the deep learning model
    return binary.astype(np.single)
