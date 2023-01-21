from game_movement import Movement

class GameState:
    def __init__(self) -> None:
        self.turn = "white"
        self.checkmate = False
        self.stalemate = False
        self.move_log = []
        self.move_methods = {
            "pawn": self.get_pawn_moves,
            "rook": self.get_rook_moves,
            "knight": self.get_knight_moves,
            "bishop": self.get_bishop_moves,
            "queen": self.get_queen_moves,
            "king": self.get_king_moves,
        }
        self.king_locations = {
            "white": (7, 4),
            "black": (0, 4),
        }

        # board is a 2d list representation of an 8x8 chess board
        self.board = [
            [
                "b_rook",
                "b_knight",
                "b_bishop",
                "b_queen",
                "b_king",
                "b_bishop",
                "b_knight",
                "b_rook",
            ],
            [
                "b_pawn",
                "b_pawn",
                "b_pawn",
                "b_pawn",
                "b_pawn",
                "b_pawn",
                "b_pawn",
                "b_pawn",
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                "w_pawn",
                "w_pawn",
                "w_pawn",
                "w_pawn",
                "w_pawn",
                "w_pawn",
                "w_pawn",
                "w_pawn",
            ],
            [
                "w_rook",
                "w_knight",
                "w_bishop",
                "w_queen",
                "w_king",
                "w_bishop",
                "w_knight",
                "w_rook",
            ],
        ]

    def swap_player_turn(self) -> None:
        self.turn = "black" if self.turn == "white" else "white"

    def execute_move(self, move: object) -> None:
        self.board[move.start_square[0]][move.start_square[1]] = None
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.update_king_locations(move)

        if move.is_pawn_promotion:
            controller = move.moved_piece[0]
            promoted_piece = f"{controller}_{move.promotion_choice}"
            self.board[move.end_square[0]][move.end_square[1]] = promoted_piece

        self.swap_player_turn()

    def undo_move(self) -> None:
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        self.board[move.end_square[0]][move.end_square[1]] = move.captured_piece
        self.board[move.start_square[0]][move.start_square[1]] = move.moved_piece
        self.update_king_locations(move)
        self.swap_player_turn()
        self.checkmate = False
        self.stalemate = False

    def update_king_locations(self, move: object) -> None:
        if move.moved_piece == "w_king":
            self.king_locations["white"] = move.end_square
        elif move.moved_piece == "b_king":
            self.king_locations["black"] = move.end_square

    def get_legal_moves(self) -> list:
        """
        Calculates all moves, accounting for checks and checkmate
        Explanation:
        1) Generates all the player's possible moves
        2) For each move, execute the move
        3) Generate all opponent's moves
        4) For each of the opponent's moves, see if they will check the player's King
        5) If any of the opponent's move check's the player's king, the player's move is not valid
        """
        players_possible_moves = self.get_possible_moves()

        for move in players_possible_moves[::-1]:
            self.execute_move(move)
            # execute_move() automatically swaps player's turns, we need to reswap turns again otherwise our
            # helper methods will calculate for the wrong player
            self.swap_player_turn()
            would_put_king_in_check = self.in_check()

            if would_put_king_in_check:
                players_possible_moves.remove(move)

            self.swap_player_turn()
            self.undo_move()

        if len(players_possible_moves) == 0:
            king_is_in_check = self.in_check()
            if king_is_in_check:
                self.checkmate = True
            else:
                self.stalemate = True

        for move in players_possible_moves:
            print(move)
        print(" ")
        return players_possible_moves

    def in_check(self) -> bool:
        """
        Calculates if the current player is in check
        """
        if self.turn == "white":
            return self.square_under_attack(self.king_locations["white"])
        else:
            return self.square_under_attack(self.king_locations["black"])

    def square_under_attack(self, square: object) -> bool:
        """
        Calculates if the square given as an argument could come under attack by the opponent.
        """
        self.swap_player_turn()
        opponents_possible_moves = self.get_possible_moves()

        for opponent_move in opponents_possible_moves:
            square_is_under_attack = opponent_move.end_square == square
            if square_is_under_attack:
                self.swap_player_turn()
                return True
        self.swap_player_turn()
        return False

    def get_possible_moves(self) -> list:
        """
        Calculates all potential moves, regardless of checks and checkmate
        """
        possible_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == None:
                    continue

                controller = self.board[row][col][0]
                piece = self.board[row][col][2:]
                is_white = controller == "w" and self.turn == "white"
                is_black = controller == "b" and self.turn == "black"

                if is_white or is_black:
                    move_method = self.move_methods[piece]
                    possible_moves += move_method(row, col)

        return possible_moves

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
