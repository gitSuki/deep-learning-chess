from constants import *
from movement import Movement
from pieces.main import Piece

class Knight(Piece):
    def __init__(self, team: str, location: tuple) -> list:
        super().__init__(team, KNIGHT, location)
        self.ai_value = 3

    def knight_movement(self, start: tuple, offset: tuple, board: list) -> object:
        moves = []
        end = (start[0] + offset[0], start[1] + offset[1])
        row_is_in_bounds = end[0] < len(board) and end[0] >= 0
        col_is_in_bounds = end[1] < len(board) and end[1] >= 0
        if row_is_in_bounds and col_is_in_bounds:
            square_is_occupied = board[end[0]][end[1]]
            if not square_is_occupied:
                moves.append(Movement(start, end, board))
                return moves

            is_enemy = self.detect_enemy_piece(board[end[0]][end[1]])
            if is_enemy:
                moves.append(Movement(start, end, board))
        return moves

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += self.knight_movement((row, col), (-2, -1), board)
        moves += self.knight_movement((row, col), (-1, -2), board)
        moves += self.knight_movement((row, col), (1, -2), board)
        moves += self.knight_movement((row, col), (2, -1), board)
        moves += self.knight_movement((row, col), (2, 1), board)
        moves += self.knight_movement((row, col), (1, 2), board)
        moves += self.knight_movement((row, col), (-1, 2), board)
        moves += self.knight_movement((row, col), (-2, 1), board)
        return moves

