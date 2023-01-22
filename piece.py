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
        for row_up in range(row - 1, -1, -1):
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
        for row_down in range(row + 1, len(board)):
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
        for row_down in range(row + 1, len(board)):
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
        for row_up in range(row - 1, -1, -1):
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


class Pawn(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, PAWN, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        if self.team == WHITE:
            # move forward
            if not board[row - 1][col]:
                moves.append(Movement((row, col), (row - 1, col), board))
                # pawns can move two squares directly forward on their first move
                # pawns can never move backward so they will always be at their starting row
                # if they haven't moved
                if row == 6 and not board[row - 2][col]:
                    moves.append(Movement((row, col), (row - 2, col), board))
            # capture to the left
            if col - 1 >= 0:
                piece_exists = board[row - 1][col - 1]
                if piece_exists and board[row - 1][col - 1].team == BLACK:
                    moves.append(Movement((row, col), (row - 1, col - 1), board))
            # capture to the right
            if col + 1 < len(board[row]):
                piece_exists = board[row - 1][col + 1]
                if piece_exists and board[row - 1][col + 1].team == BLACK:
                    moves.append(Movement((row, col), (row - 1, col + 1), board))

        if self.team == BLACK:
            if (row + 1) < len(board):
                # move forward
                if not board[row + 1][col]:
                    moves.append(Movement((row, col), (row + 1, col), board))
                    # pawns can move two squares directly forward on their first move
                    # pawns can never move backward so they will always be at their starting row
                    # if they haven't moved
                    if row == 1 and not board[row + 2][col]:
                        moves.append(Movement((row, col), (row + 2, col), board))
                # capture to the left
                if col + 1 < len(board[row]):
                    piece_exists = board[row + 1][col + 1]
                    if piece_exists and board[row + 1][col + 1].team == WHITE:
                        moves.append(Movement((row, col), (row + 1, col + 1), board))
                # capture to the right
                if col - 1 >= 0:
                    piece_exists = board[row + 1][col - 1]
                    if piece_exists and board[row + 1][col - 1].team == WHITE:
                        moves.append(Movement((row, col), (row + 1, col - 1), board))

        return moves


class Rook(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, ROOK, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += self.orthogonal_up(row, col, board)
        moves += self.orthogonal_left(row, col, board)
        moves += self.orthogonal_down(row, col, board)
        moves += self.orthogonal_right(row, col, board)
        return moves


class Knight(Piece):
    def __init__(self, team: str, location: tuple) -> list:
        super().__init__(team, KNIGHT, location)

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


class Bishop(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, BISHOP, location)

    def get_moves(self, row: int, col: int, board: list) -> list:
        moves = []
        moves += self.diagonal_up_left(row, col, board)
        moves += self.diagonal_down_left(row, col, board)
        moves += self.diagonal_down_right(row, col, board)
        moves += self.diagonal_up_right(row, col, board)
        return moves


class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, QUEEN, location)

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


class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KING, location)

    def get_moves(self, row: int, col: int, board: list):
        moves = []

        # move up
        if (row - 1) >= 0:
            if (
                not board[row - 1][col]
                or (board[row - 1][col].team == WHITE and self.team == BLACK)
                or (board[row - 1][col].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row - 1, col), board))

        # move up-left
        if (row - 1) >= 0 and (col - 1) >= 0:
            if (
                not board[row - 1][col - 1]
                or (board[row - 1][col - 1].team == WHITE and self.team == BLACK)
                or (board[row - 1][col - 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row - 1, col - 1), board))

        # move left
        if (col - 1) >= 0:
            if (
                not board[row][col - 1]
                or (board[row][col - 1].team == WHITE and self.team == BLACK)
                or (board[row][col - 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row, col - 1), board))

        # move down-left
        if (row + 1) < len(board) and (col - 1) >= 0:
            if (
                not board[row + 1][col - 1]
                or (board[row + 1][col - 1].team == WHITE and self.team == BLACK)
                or (board[row + 1][col - 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row + 1, col - 1), board))

        # move down
        if (row + 1) < len(board):
            if (
                not board[row + 1][col]
                or (board[row + 1][col].team == WHITE and self.team == BLACK)
                or (board[row + 1][col].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row + 1, col), board))

        # move down-right
        if (row + 1) < len(board) and (col + 1) < len(board):
            if (
                not board[row + 1][col + 1]
                or (board[row + 1][col + 1].team == WHITE and self.team == BLACK)
                or (board[row + 1][col + 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row + 1, col + 1), board))

        # move right
        if (col + 1) < len(board):
            if (
                not board[row][col + 1]
                or (board[row][col + 1].team == WHITE and self.team == BLACK)
                or (board[row][col + 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row, col + 1), board))

        # move up-right
        if (row - 1) >= 0 and (col + 1) < len(board):
            if (
                not board[row - 1][col + 1]
                or (board[row - 1][col + 1].team == WHITE and self.team == BLACK)
                or (board[row - 1][col + 1].team == BLACK and self.team == WHITE)
            ):
                moves.append(Movement((row, col), (row - 1, col + 1), board))
        return moves