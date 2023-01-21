import numpy as np

from constants import *
from game_movement import Movement


class Piece:
    """
    Represents an individual chess piece on the game board.
    """

    def __init__(self, team: str, type: str, location: tuple) -> None:
        self.team = team
        self.type = type
        self.location = location
        self.image_code = f"{self.team[0]}_{self.type}"

    def __str__(self) -> str:
        return f"{self.team} {self.type} at {self.location}"

    def get_moves(self, row: int, col: int, board: list) -> list:
        return []

    def orthogonal_up_movement(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        for i in np.arange(row - 1, -1, -1):
            square_is_occupied = board[i][col]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[i][col])
                if is_enemy:
                    possible_moves.append(Movement((row, col), (i, col), board))
                break

            possible_moves.append(Movement((row, col), (i, col), board))
        return possible_moves

    def orthogonal_down_movement(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        for i in np.arange(row + 1, len(board) - 1):
            square_is_occupied = board[i][col]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[i][col])
                if is_enemy:
                    possible_moves.append(Movement((row, col), (i, col), board))
                break

            possible_moves.append(Movement((row, col), (i, col), board))
        return possible_moves

    def orthogonal_left_movement(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        for i in np.arange(col - 1, -1, -1):
            square_is_occupied = board[row][i]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row][i])
                if is_enemy:
                    possible_moves.append(Movement((row, col), (row, i), board))
                break

            possible_moves.append(Movement((row, col), (row, i), board))
        return possible_moves

    def orthogonal_right_movement(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        for i in np.arange(col + 1, len(board)):
            square_is_occupied = board[row][i]
            if square_is_occupied:
                is_enemy = self.detect_enemy_piece(board[row][i])
                if is_enemy:
                    possible_moves.append(Movement((row, col), (row, i), board))
                break

            possible_moves.append(Movement((row, col), (row, i), board))
        return possible_moves

    def detect_enemy_piece(self, enemy_piece: tuple) -> bool:
        return (enemy_piece.team == WHITE and self.team == BLACK) or (
            enemy_piece.team == BLACK and self.team == WHITE
        )


class Pawn(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, PAWN, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        if self.team == WHITE:
            # move forward
            if not board[row - 1][col]:
                possible_moves.append(Movement((row, col), (row - 1, col), board))
                # pawns can move two squares directly forward on their first move
                # pawns can never move backward so they will always be at their starting row
                # if they haven't moved
                if row == 6 and not board[row - 2][col]:
                    possible_moves.append(Movement((row, col), (row - 2, col), board))
            # capture to the left
            if col - 1 >= 0:
                piece_exists = board[row - 1][col - 1]
                if piece_exists and board[row - 1][col - 1].team == BLACK:
                    possible_moves.append(
                        Movement((row, col), (row - 1, col - 1), board)
                    )
            # capture to the right
            if col + 1 < len(board[row]):
                piece_exists = board[row - 1][col + 1]
                if piece_exists and board[row - 1][col + 1].team == BLACK:
                    possible_moves.append(
                        Movement((row, col), (row - 1, col + 1), board)
                    )

        if self.team == BLACK:
            if (row + 1) < len(board):
                # move forward
                if not board[row + 1][col]:
                    possible_moves.append(Movement((row, col), (row + 1, col), board))
                    # pawns can move two squares directly forward on their first move
                    # pawns can never move backward so they will always be at their starting row
                    # if they haven't moved
                    if row == 1 and not board[row + 2][col]:
                        possible_moves.append(
                            Movement((row, col), (row + 2, col), board)
                        )
                # capture to the left
                if col + 1 < len(board[row]):
                    piece_exists = board[row + 1][col + 1]
                    if piece_exists and board[row + 1][col + 1].team == WHITE:
                        possible_moves.append(
                            Movement((row, col), (row + 1, col + 1), board)
                        )
                # capture to the right
                if col - 1 >= 0:
                    piece_exists = board[row + 1][col - 1]
                    if piece_exists and board[row + 1][col - 1].team == WHITE:
                        possible_moves.append(
                            Movement((row, col), (row + 1, col - 1), board)
                        )

        return possible_moves


class Rook(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, ROOK, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        possible_moves = []
        possible_moves += self.orthogonal_up_movement(row, col, board)
        possible_moves += self.orthogonal_left_movement(row, col, board)
        possible_moves += self.orthogonal_down_movement(row, col, board)
        possible_moves += self.orthogonal_right_movement(row, col, board)
        return possible_moves


class Knight(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KNIGHT, location)


class Bishop(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, BISHOP, location)


class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, QUEEN, location)


class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KING, location)
