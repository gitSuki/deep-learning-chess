import numpy as np

from constants import *
from movement import Movement


class Piece:
    """
    Represents an individual chess piece on the game board.
    """

    def __init__(self, team: str, type: str, location: tuple) -> None:
        self.team = team
        self.type = type
        self.location = location
        self.image_code = f"{self.team[0]}_{self.type}"
        self.ai_value = None

    def __str__(self) -> str:
        return f"{self.team} {self.type} at {self.location}"

    def get_moves(self, row: int, col: int, board: list) -> list:
        return []

    def orthogonal_up(self, row: int, col: int, board: list) -> list:
        moves = []
        for i in np.arange(row - 1, -1, -1):
            square_is_occupied = board[i][col]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[i][col])
                if is_enemy:
                    moves.append(Movement((row, col), (i, col), board))
                break

            moves.append(Movement((row, col), (i, col), board))
        return moves

    def orthogonal_left(self, row: int, col: int, board: list) -> list:
        moves = []
        for i in np.arange(col - 1, -1, -1):
            square_is_occupied = board[row][i]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row][i])
                if is_enemy:
                    moves.append(Movement((row, col), (row, i), board))
                break

            moves.append(Movement((row, col), (row, i), board))
        return moves

    def orthogonal_down(self, row: int, col: int, board: list) -> list:
        moves = []
        for i in np.arange(row + 1, len(board)):
            square_is_occupied = board[i][col]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[i][col])
                if is_enemy:
                    moves.append(Movement((row, col), (i, col), board))
                break

            moves.append(Movement((row, col), (i, col), board))
        return moves

    def orthogonal_right(self, row: int, col: int, board: list) -> list:
        moves = []
        for i in np.arange(col + 1, len(board)):
            square_is_occupied = board[row][i]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row][i])
                if is_enemy:
                    moves.append(Movement((row, col), (row, i), board))
                break

            moves.append(Movement((row, col), (row, i), board))
        return moves

    def diagonal_up_left(self, row: int, col: int, board: list) -> list:
        moves = []
        for row_up in np.arange(row - 1, -1, -1):
            col_left = col + (row_up - row)
            square_is_occupied = board[row_up][col_left]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row_up][col_left])
                if is_enemy:
                    moves.append(Movement((row, col), (row_up, col_left), board))
                break

            moves.append(Movement((row, col), (row_up, col_left), board))
        return moves

    def diagonal_down_left(self, row: int, col: int, board: list) -> list:
        moves = []
        for row_down in np.arange(row + 1, len(board)):
            col_left = col - (row_down - row)
            square_is_occupied = board[row_down][col_left]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row_down][col_left])
                if is_enemy:
                    moves.append(Movement((row, col), (row_down, col_left), board))
                break

            moves.append(Movement((row, col), (row_down, col_left), board))
        return moves

    def diagonal_down_right(self, row: int, col: int, board: list) -> list:
        moves = []
        for row_down in np.arange(row + 1, len(board)):
            col_right = col + (row_down - row)
            is_in_bounds = col_right < len(board)
            if is_in_bounds:
                square_is_occupied = board[row_down][col_right]
                if square_is_occupied:
                    is_enemy = self.detect_enemy_piece(board[row_down][col_right])
                    if is_enemy:
                        moves.append(Movement((row, col), (row_down, col_right), board))
                    break

                moves.append(Movement((row, col), (row_down, col_right), board))
        return moves

    def diagonal_up_right(self, row: int, col: int, board: list) -> list:
        moves = []
        for row_up in np.arange(row - 1, -1, -1):
            col_right = col - (row_up - row)
            is_in_bounds = col_right < len(board)
            if is_in_bounds:
                square_is_occupied = board[row_up][col_right]
                if square_is_occupied:
                    is_enemy = self.detect_enemy_piece(board[row_up][col_right])
                    if is_enemy:
                        moves.append(Movement((row, col), (row_up, col_right), board))
                    break

                moves.append(Movement((row, col), (row_up, col_right), board))
        return moves

    def detect_enemy_piece(self, enemy_piece: tuple) -> bool:
        return (enemy_piece.team == WHITE and self.team == BLACK) or (
            enemy_piece.team == BLACK and self.team == WHITE
        )


def detect_enemy_piece(enemy_piece: tuple, team: str) -> bool:
    return (enemy_piece.team == WHITE and team == BLACK) or (
        enemy_piece.team == BLACK and team == WHITE
    )
