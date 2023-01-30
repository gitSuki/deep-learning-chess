from constants import *
from movement import Movement
from pieces.main import Piece

class Pawn(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, PAWN, location)
        self.ai_value = 1

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