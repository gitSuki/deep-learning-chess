from constants import *
from engine.movement import Movement
from pieces.main import Piece, detect_enemy_piece


class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KING, location)
        self.ai_value = 0

    def get_moves(self, row: int, col: int, board: list):
        moves = []
        moves += king_movement((row, col), (-1, 0), board, self.team)
        moves += king_movement((row, col), (-1, -1), board, self.team)
        moves += king_movement((row, col), (0, -1), board, self.team)
        moves += king_movement((row, col), (1, -1), board, self.team)
        moves += king_movement((row, col), (1, 0), board, self.team)
        moves += king_movement((row, col), (1, 1), board, self.team)
        moves += king_movement((row, col), (0, 1), board, self.team)
        moves += king_movement((row, col), (-1, 1), board, self.team)
        return moves


def king_movement(start: tuple, offset: tuple, board: list, team: str) -> list:
    """
    Generates a list of movement objects for a King based on a given offset. Returns an empty list if the offset is not a valid movement.
    """
    moves = []
    end = (start[0] + offset[0], start[1] + offset[1])
    row_is_in_bounds = end[0] < len(board) and end[0] >= 0
    col_is_in_bounds = end[1] < len(board) and end[1] >= 0
    if row_is_in_bounds and col_is_in_bounds:
        square_is_occupied = board[end[0]][end[1]]
        if not square_is_occupied:
            moves.append(Movement(start, end, board))
            return moves

        is_enemy = detect_enemy_piece(board[end[0]][end[1]], team)
        if is_enemy:
            moves.append(Movement(start, end, board))
    return moves
