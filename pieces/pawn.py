from constants import *
from movement import Movement
from pieces.main import Piece, detect_enemy_piece


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
                moves += capture_left_movement((row, col), board, self.team)
                moves += capture_right_movement((row, col), board, self.team)

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
                moves += capture_left_movement((row, col), board, self.team)
                moves += capture_right_movement((row, col), board, self.team)
        return moves


def pawn_movement(start: tuple, offset: tuple, board: list, team: str) -> list:
    """
    Generates a list of movement objects for a Knight based on a given offset. Returns an empty list if the offset is not a valid movement.
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


def capture_left_movement(start: tuple, board: list, team: str) -> list:
    moves = []
    row = start[0] - 1 if team is WHITE else start[0] + 1
    col = start[1] - 1

    in_bounds = col >= 0 and col < len(board)
    if in_bounds:
        square_is_occupied = board[row][col]
        if square_is_occupied:
            is_enemy = detect_enemy_piece(board[row][col], team)
            if is_enemy:
                moves.append(Movement(start, (row, col), board))
    return moves


def capture_right_movement(start: tuple, board: list, team: str) -> list:
    moves = []
    row = start[0] - 1 if team is WHITE else start[0] + 1
    col = start[1] + 1

    in_bounds = col >= 0 and col < len(board)
    if in_bounds:
        square_is_occupied = board[row][col]
        if square_is_occupied:
            is_enemy = detect_enemy_piece(board[row][col], team)
            if is_enemy:
                moves.append(Movement(start, (row, col), board))
    return moves
