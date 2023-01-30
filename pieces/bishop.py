from constants import *
from pieces.main import Piece

class Bishop(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, BISHOP, location)
        self.ai_value = 3

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += self.diagonal_up_left(row, col, board)
        moves += self.diagonal_down_left(row, col, board)
        moves += self.diagonal_down_right(row, col, board)
        moves += self.diagonal_up_right(row, col, board)
        return moves