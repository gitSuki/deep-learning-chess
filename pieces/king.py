from constants import *
from movement import Movement
from pieces.main import Piece

class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KING, location)
        self.ai_value = 0

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
