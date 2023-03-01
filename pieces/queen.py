from constants import *
from pieces.main import *


class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, QUEEN, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += orthogonal_up(row, col, board, self.team)
        moves += orthogonal_left(row, col, board, self.team)
        moves += orthogonal_down(row, col, board, self.team)
        moves += orthogonal_right(row, col, board, self.team)
        moves += diagonal_up_left(row, col, board, self.team)
        moves += diagonal_down_left(row, col, board, self.team)
        moves += diagonal_down_right(row, col, board, self.team)
        moves += diagonal_up_right(row, col, board, self.team)
        return moves
