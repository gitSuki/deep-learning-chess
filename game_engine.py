import numpy as np

from constants import *
from chess_piece import *
from game_board import game_board
from game_movement import Movement


class GameState:
    """
    Represents the game engine and the current state of the game.
    """

    def __init__(self) -> None:
        self.board = game_board()
        self.move_log = []
        self.move_methods = {
            PAWN: self.get_pawn_moves,
            ROOK: self.get_rook_moves,
            KNIGHT: self.get_knight_moves,
            BISHOP: self.get_bishop_moves,
            QUEEN: self.get_queen_moves,
            KING: self.get_king_moves,
        }
        self.king_locations = {
            WHITE: (7, 4),
            BLACK: (0, 4),
        }
        self.turn = WHITE
        self.checkmate = False
        self.stalemate = False

    def swap_player_turn(self) -> None:
        """
        Swaps the current player in the game between white or black.
        """
        self.turn = BLACK if self.turn == WHITE else WHITE

    def execute_move(self, move: object) -> None:
        """
        Executes the move given as an argument.
        """
        self.board[move.start_square[0]][move.start_square[1]] = None
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.update_king_locations(move)

        if move.is_pawn_promotion:
            # Automatically promotes to Queen
            # promoted_piece = move.promotion_choice
            team = move.moved_piece.team
            promoted_piece = Queen(team, move.end_square)
            self.board[move.end_square[0]][move.end_square[1]] = promoted_piece

        self.swap_player_turn()

    def undo_move(self) -> None:
        """
        Undoes the most recent move in the move log.
        """
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        self.board[move.end_square[0]][move.end_square[1]] = move.captured_piece
        self.board[move.start_square[0]][move.start_square[1]] = move.moved_piece
        self.update_king_locations(move)
        self.swap_player_turn()
        self.checkmate = False
        self.stalemate = False

    def get_legal_moves(self) -> list:
        """
        Calculates all legal moves, accounting for checks and checkmate.
        """
        players_possible_moves = self.get_possible_moves()

        if len(players_possible_moves) == 0:
            self.check_gameover_conditions()

        # loops through list of moves backwards to prevent bugs from occuring when deleting invalid moves
        for move in players_possible_moves[::-1]:
            # execute_move() automatically swaps player's turns, we need to reswap turns again otherwise our
            # helper methods will calculate for the wrong player
            self.execute_move(move)
            self.swap_player_turn()
            move_would_put_king_in_check = self.king_in_check()
            if move_would_put_king_in_check:
                players_possible_moves.remove(move)
            self.swap_player_turn()
            self.undo_move()

        for move in players_possible_moves:
            print(move)
        print(" ")
        return players_possible_moves

    def check_gameover_conditions(self) -> None:
        """
        Checks if the game is in either a checkmate or stalemate situation.
        """
        king_is_in_check = self.king_in_check()
        if king_is_in_check:
            self.checkmate = True
        else:
            self.stalemate = True

    def king_in_check(self) -> bool:
        """
        Calculates if the current player's king is in a check situation.
        """
        if self.turn == WHITE:
            return self.square_under_attack(self.king_locations[WHITE])
        else:
            return self.square_under_attack(self.king_locations[BLACK])

    def square_under_attack(self, square: object) -> bool:
        """
        Calculates if the square given as an argument could come under attack by the opponent.
        """
        self.swap_player_turn()
        opponents_possible_moves = self.get_possible_moves()

        for move in opponents_possible_moves:
            square_is_under_attack = move.end_square == square
            if square_is_under_attack:
                self.swap_player_turn()
                return True
        self.swap_player_turn()
        return False

    def get_possible_moves(self) -> list:
        """
        Calculates all potential moves, regardless of checks and checkmate.
        """
        possible_moves = []
        for row in np.arange(len(self.board)):
            for col in np.arange(len(self.board[row])):
                square_is_empty = self.board[row][col] == None
                if square_is_empty:
                    continue

                piece_team = self.board[row][col].team
                piece_type = self.board[row][col].type
                piece_is_opponents = piece_team != self.turn
                if piece_is_opponents:
                    continue

                move_method = self.move_methods[piece_type]
                possible_moves += move_method(row, col)

        return possible_moves

    def update_king_locations(self, move: object) -> None:
        """
        Updates the dictionary that keeps track of the location for each teams king.
        """
        if move.moved_piece.type == KING:
            if move.moved_piece.team == WHITE:
                self.king_locations[WHITE] = move.end_square
            elif move.moved_piece.team == BLACK:
                self.king_locations[BLACK] = move.end_square

    def get_pawn_moves(self, row: int, col: int) -> list:
        possible_moves = []
        if self.turn == "white":
            # move forward
            if not self.board[row - 1][col]:
                possible_moves.append(Movement((row, col), (row - 1, col), self.board))
                # pawns can move two squares directly forward on their first move
                # pawns can never move backward so they will always be at their starting row
                # if they haven't moved
                if row == 6 and not self.board[row - 2][col]:
                    possible_moves.append(
                        Movement((row, col), (row - 2, col), self.board)
                    )
            # capture to the left
            if col - 1 >= 0:
                piece_exists = self.board[row - 1][col - 1]
                if piece_exists and self.board[row - 1][col - 1][0] == "b":
                    possible_moves.append(
                        Movement((row, col), (row - 1, col - 1), self.board)
                    )
            # capture to the right
            if col + 1 < len(self.board[row]):
                piece_exists = self.board[row - 1][col + 1]
                if piece_exists and self.board[row - 1][col + 1][0] == "b":
                    possible_moves.append(
                        Movement((row, col), (row - 1, col + 1), self.board)
                    )

        if self.turn == "black":
            if (row + 1) < len(self.board):
                # move forward
                if not self.board[row + 1][col]:
                    possible_moves.append(
                        Movement((row, col), (row + 1, col), self.board)
                    )
                    # pawns can move two squares directly forward on their first move
                    # pawns can never move backward so they will always be at their starting row
                    # if they haven't moved
                    if row == 1 and not self.board[row + 2][col]:
                        possible_moves.append(
                            Movement((row, col), (row + 2, col), self.board)
                        )
                # capture to the left
                if col + 1 < len(self.board[row]):
                    piece_exists = self.board[row + 1][col + 1]
                    if piece_exists and self.board[row + 1][col + 1][0] == "w":
                        possible_moves.append(
                            Movement((row, col), (row + 1, col + 1), self.board)
                        )
                # capture to the right
                if col - 1 >= 0:
                    piece_exists = self.board[row + 1][col - 1]
                    if piece_exists and self.board[row + 1][col - 1][0] == "w":
                        possible_moves.append(
                            Movement((row, col), (row + 1, col - 1), self.board)
                        )
        return possible_moves

    def get_rook_moves(self, row: int, col: int) -> list:
        possible_moves = []

        # moving down
        for i in range(row + 1, len(self.board) - 1):
            if self.board[i][col]:
                if (
                    self.board[i][col][0] == "w"
                    and self.turn == "black"
                    or self.board[i][col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (i, col), self.board))
                break

            possible_moves.append(Movement((row, col), (i, col), self.board))

        # moving up
        for i in range(row - 1, -1, -1):
            # stops if runs into another piece
            if self.board[i][col]:
                if (
                    self.board[i][col][0] == "w"
                    and self.turn == "black"
                    or self.board[i][col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (i, col), self.board))
                break

            possible_moves.append(Movement((row, col), (i, col), self.board))

        # moving left
        for i in range(col - 1, -1, -1):
            # stops if runs into another piece
            if self.board[row][i]:
                if (
                    self.board[row][i][0] == "w"
                    and self.turn == "black"
                    or self.board[row][i][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (row, i), self.board))
                break

            possible_moves.append(Movement((row, col), (row, i), self.board))

        # moving right
        for i in range(col + 1, len(self.board)):
            # stops if runs into another piece
            if self.board[row][i]:
                if (
                    self.board[row][i][0] == "w"
                    and self.turn == "black"
                    or self.board[row][i][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (row, i), self.board))
                break

            possible_moves.append(Movement((row, col), (row, i), self.board))

        return possible_moves

    def get_knight_moves(self, row: int, col: int) -> list:
        possible_moves = []

        # move 2 up 1 left
        if (row - 2) >= 0 and (col - 1) >= 0:
            if (
                not self.board[row - 2][col - 1]
                or (self.board[row - 2][col - 1][0] == "w" and self.turn == "black")
                or (self.board[row - 2][col - 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 2, col - 1), self.board)
                )

        # move 2 up 1 right
        if (row - 2) >= 0 and (col + 1) < len(self.board):
            if (
                not self.board[row - 2][col + 1]
                or (self.board[row - 2][col + 1][0] == "w" and self.turn == "black")
                or (self.board[row - 2][col + 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 2, col + 1), self.board)
                )

        # move 2 left 1 up
        if (row - 1) >= 0 and (col - 2) >= 0:
            if (
                not self.board[row - 1][col - 2]
                or (self.board[row - 1][col - 2][0] == "w" and self.turn == "black")
                or (self.board[row - 1][col - 2][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 1, col - 2), self.board)
                )

        # move 2 left 1 down
        if (row + 1) < len(self.board) and (col - 2) >= 0:
            if (
                not self.board[row + 1][col - 2]
                or (self.board[row + 1][col - 2][0] == "w" and self.turn == "black")
                or (self.board[row + 1][col - 2][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 1, col - 2), self.board)
                )

        # move 2 down 1 left
        if (row + 2) < len(self.board) and (col - 1) >= 0:
            if (
                not self.board[row + 2][col - 1]
                or (self.board[row + 2][col - 1][0] == "w" and self.turn == "black")
                or (self.board[row + 2][col - 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 2, col - 1), self.board)
                )

        # move 2 down 1 right
        if (row + 2) < len(self.board) and (col + 1) < len(self.board):
            if (
                not self.board[row + 2][col + 1]
                or (self.board[row + 2][col + 1][0] == "w" and self.turn == "black")
                or (self.board[row + 2][col + 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 2, col + 1), self.board)
                )

        # move 2 right 1 down
        if (row + 1) < len(self.board) and (col + 2) < len(self.board):
            if (
                not self.board[row + 1][col + 2]
                or (self.board[row + 1][col + 2][0] == "w" and self.turn == "black")
                or (self.board[row + 1][col + 2][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 1, col + 2), self.board)
                )

        # move 2 right 1 up
        if (row - 1) >= 0 and (col + 2) < len(self.board):
            if (
                not self.board[row - 1][col + 2]
                or (self.board[row - 1][col + 2][0] == "w" and self.turn == "black")
                or (self.board[row - 1][col + 2][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 1, col + 2), self.board)
                )

        return possible_moves

    def get_bishop_moves(self, row: int, col: int) -> list:
        possible_moves = []

        # moving down-right
        for new_row in range(row + 1, len(self.board)):
            new_col = col + (new_row - row)
            if new_col < len(self.board):
                if self.board[new_row][new_col]:
                    if (
                        self.board[new_row][new_col][0] == "w"
                        and self.turn == "black"
                        or self.board[new_row][new_col][0] == "b"
                        and self.turn == "white"
                    ):
                        possible_moves.append(
                            Movement((row, col), (new_row, new_col), self.board)
                        )
                    break

                possible_moves.append(
                    Movement((row, col), (new_row, new_col), self.board)
                )

        # moving down-left
        for new_row in range(row + 1, len(self.board)):
            new_col = col - (new_row - row)
            if self.board[new_row][new_col]:
                if (
                    self.board[new_row][new_col][0] == "w"
                    and self.turn == "black"
                    or self.board[new_row][new_col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(
                        Movement((row, col), (new_row, new_col), self.board)
                    )
                break

            possible_moves.append(Movement((row, col), (new_row, new_col), self.board))

        # moving up-right
        for new_row in range(row - 1, -1, -1):
            new_col = col - (new_row - row)
            if new_col < len(self.board):
                if self.board[new_row][new_col]:
                    if (
                        self.board[new_row][new_col][0] == "w"
                        and self.turn == "black"
                        or self.board[new_row][new_col][0] == "b"
                        and self.turn == "white"
                    ):
                        possible_moves.append(
                            Movement((row, col), (new_row, new_col), self.board)
                        )
                    break

                possible_moves.append(
                    Movement((row, col), (new_row, new_col), self.board)
                )

        # moving up-left
        for new_row in range(row - 1, -1, -1):
            new_col = col + (new_row - row)
            if self.board[new_row][new_col]:
                if (
                    self.board[new_row][new_col][0] == "w"
                    and self.turn == "black"
                    or self.board[new_row][new_col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(
                        Movement((row, col), (new_row, new_col), self.board)
                    )
                break

            possible_moves.append(Movement((row, col), (new_row, new_col), self.board))

        return possible_moves

    def get_queen_moves(self, row: int, col: int) -> list:
        possible_moves = []

        # moving down
        for i in range(row + 1, len(self.board) - 1):
            if self.board[i][col]:
                if (
                    self.board[i][col][0] == "w"
                    and self.turn == "black"
                    or self.board[i][col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (i, col), self.board))
                break

            possible_moves.append(Movement((row, col), (i, col), self.board))

        # moving up
        for i in range(row - 1, -1, -1):
            # stops if runs into another piece
            if self.board[i][col]:
                if (
                    self.board[i][col][0] == "w"
                    and self.turn == "black"
                    or self.board[i][col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (i, col), self.board))
                break

            possible_moves.append(Movement((row, col), (i, col), self.board))

        # moving left
        for i in range(col - 1, -1, -1):
            # stops if runs into another piece
            if self.board[row][i]:
                if (
                    self.board[row][i][0] == "w"
                    and self.turn == "black"
                    or self.board[row][i][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (row, i), self.board))
                break

            possible_moves.append(Movement((row, col), (row, i), self.board))

        # moving right
        for i in range(col + 1, len(self.board)):
            # stops if runs into another piece
            if self.board[row][i]:
                if (
                    self.board[row][i][0] == "w"
                    and self.turn == "black"
                    or self.board[row][i][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(Movement((row, col), (row, i), self.board))
                break

            possible_moves.append(Movement((row, col), (row, i), self.board))

        # moving down-right
        for new_row in range(row + 1, len(self.board)):
            new_col = col + (new_row - row)
            if new_col < len(self.board):
                if self.board[new_row][new_col]:
                    if (
                        self.board[new_row][new_col][0] == "w"
                        and self.turn == "black"
                        or self.board[new_row][new_col][0] == "b"
                        and self.turn == "white"
                    ):
                        possible_moves.append(
                            Movement((row, col), (new_row, new_col), self.board)
                        )
                    break

                possible_moves.append(
                    Movement((row, col), (new_row, new_col), self.board)
                )

        # moving down-left
        for new_row in range(row + 1, len(self.board)):
            new_col = col - (new_row - row)
            if self.board[new_row][new_col]:
                if (
                    self.board[new_row][new_col][0] == "w"
                    and self.turn == "black"
                    or self.board[new_row][new_col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(
                        Movement((row, col), (new_row, new_col), self.board)
                    )
                break

            possible_moves.append(Movement((row, col), (new_row, new_col), self.board))

        # moving up-right
        for new_row in range(row - 1, -1, -1):
            new_col = col - (new_row - row)
            if new_col < len(self.board):
                if self.board[new_row][new_col]:
                    if (
                        self.board[new_row][new_col][0] == "w"
                        and self.turn == "black"
                        or self.board[new_row][new_col][0] == "b"
                        and self.turn == "white"
                    ):
                        possible_moves.append(
                            Movement((row, col), (new_row, new_col), self.board)
                        )
                    break

                possible_moves.append(
                    Movement((row, col), (new_row, new_col), self.board)
                )

        # moving up-left
        for new_row in range(row - 1, -1, -1):
            new_col = col + (new_row - row)
            if self.board[new_row][new_col]:
                if (
                    self.board[new_row][new_col][0] == "w"
                    and self.turn == "black"
                    or self.board[new_row][new_col][0] == "b"
                    and self.turn == "white"
                ):
                    possible_moves.append(
                        Movement((row, col), (new_row, new_col), self.board)
                    )
                break

            possible_moves.append(Movement((row, col), (new_row, new_col), self.board))

        return possible_moves

    def get_king_moves(self, row: int, col: int) -> list:
        possible_moves = []

        # move up
        if (row - 1) >= 0:
            if (
                not self.board[row - 1][col]
                or (self.board[row - 1][col][0] == "w" and self.turn == "black")
                or (self.board[row - 1][col][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(Movement((row, col), (row - 1, col), self.board))

        # move up-left
        if (row - 1) >= 0 and (col - 1) >= 0:
            if (
                not self.board[row - 1][col - 1]
                or (self.board[row - 1][col - 1][0] == "w" and self.turn == "black")
                or (self.board[row - 1][col - 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 1, col - 1), self.board)
                )

        # move left
        if (col - 1) >= 0:
            if (
                not self.board[row][col - 1]
                or (self.board[row][col - 1][0] == "w" and self.turn == "black")
                or (self.board[row][col - 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(Movement((row, col), (row, col - 1), self.board))

        # move down-left
        if (row + 1) < len(self.board) and (col - 1) >= 0:
            if (
                not self.board[row + 1][col - 1]
                or (self.board[row + 1][col - 1][0] == "w" and self.turn == "black")
                or (self.board[row + 1][col - 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 1, col - 1), self.board)
                )

        # move down
        if (row + 1) < len(self.board):
            if (
                not self.board[row + 1][col]
                or (self.board[row + 1][col][0] == "w" and self.turn == "black")
                or (self.board[row + 1][col][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(Movement((row, col), (row + 1, col), self.board))

        # move down-right
        if (row + 1) < len(self.board) and (col + 1) < len(self.board):
            if (
                not self.board[row + 1][col + 1]
                or (self.board[row + 1][col + 1][0] == "w" and self.turn == "black")
                or (self.board[row + 1][col + 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row + 1, col + 1), self.board)
                )

        # move right
        if (col + 1) < len(self.board):
            if (
                not self.board[row][col + 1]
                or (self.board[row][col + 1][0] == "w" and self.turn == "black")
                or (self.board[row][col + 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(Movement((row, col), (row, col + 1), self.board))

        # move up-right
        if (row - 1) >= 0 and (col + 1) < len(self.board):
            if (
                not self.board[row - 1][col + 1]
                or (self.board[row - 1][col + 1][0] == "w" and self.turn == "black")
                or (self.board[row - 1][col + 1][0] == "b" and self.turn == "white")
            ):
                possible_moves.append(
                    Movement((row, col), (row - 1, col + 1), self.board)
                )

        return possible_moves
