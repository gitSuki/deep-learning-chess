from constants import *
from pieces.main import Piece

class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, QUEEN, location)
        self.ai_value = 10

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += self.orthogonal_up(row, col, board)
        moves += self.orthogonal_left(row, col, board)
        moves += self.orthogonal_down(row, col, board)
        moves += self.orthogonal_right(row, col, board)
        moves += self.diagonal_up_left(row, col, board)
        moves += self.diagonal_down_left(row, col, board)
        moves += self.diagonal_down_right(row, col, board)
        moves += self.diagonal_up_right(row, col, board)
        return moves

