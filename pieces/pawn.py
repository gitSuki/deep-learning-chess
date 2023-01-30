from constants import *
from engine.movement import Movement
from pieces.main import Piece, detect_enemy_piece


class Pawn(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, PAWN, location)
        self.ai_value = 1

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += forward_movement((row, col), board, self.team)
        moves += capture_left_movement((row, col), board, self.team)
        moves += capture_right_movement((row, col), board, self.team)
        return moves


def forward_movement(start: tuple, board: list, team: str) -> list:
    """
    Generates a list of forward movement objects for a Pawn. Returns an empty list if the offset is not a valid movement.
    """
    moves = []
    forward_multiplier = -1 if team is WHITE else 1
    row = start[0]
    col = start[1]
    forward_one_square = row + forward_multiplier

    is_in_bounds = forward_one_square >= 0 and forward_one_square < len(board)
    if is_in_bounds:
        square_is_occupied = board[forward_one_square][col]
        if square_is_occupied:
            return moves
        moves.append(Movement(start, (forward_one_square, col), board))

        forward_two_squres = row + (forward_multiplier * 2)
        forward_two_squares_is_occupied = board[forward_two_squres][col]
        is_first_move = (team == WHITE and row == 6) or (team is BLACK and row == 1)
        can_move_two_squares = is_first_move and not forward_two_squares_is_occupied
        if can_move_two_squares:
            moves.append(Movement(start, (forward_two_squres, col), board))
    return moves


def capture_left_movement(start: tuple, board: list, team: str) -> list:
    """
    Generates a list of movement objects for a Pawn based on if it can capture to the left on the board. Returns an empty list if the offset is not a valid movement.
    """
    moves = []
    row = start[0] - 1 if team is WHITE else start[0] + 1
    col = start[1] - 1

    is_in_bounds = col >= 0 and col < len(board)
    if is_in_bounds:
        square_is_occupied = board[row][col]
        if square_is_occupied:
            is_enemy = detect_enemy_piece(board[row][col], team)
            if is_enemy:
                moves.append(Movement(start, (row, col), board))
    return moves


def capture_right_movement(start: tuple, board: list, team: str) -> list:
    """
    Generates a list of movement objects for a Pawn based on if it can capture to the right on the board. Returns an empty list if the offset is not a valid movement.
    """
    moves = []
    row = start[0] - 1 if team is WHITE else start[0] + 1
    col = start[1] + 1

    is_in_bounds = col >= 0 and col < len(board)
    if is_in_bounds:
        square_is_occupied = board[row][col]
        if square_is_occupied:
            is_enemy = detect_enemy_piece(board[row][col], team)
            if is_enemy:
                moves.append(Movement(start, (row, col), board))
    return moves
