class GameState:
    def __init__(self) -> None:
        self.turn = "white"
        self.move_log = []
        self.move_methods = {
            "pawn": self.get_pawn_moves,
            "rook": self.get_rook_moves,
            "knight": self.get_knight_moves,
            "bishop": self.get_bishop_moves,
            "queen": self.get_queen_moves,
            "king": self.get_king_moves,
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
                "w_knight",
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

    def swap_player_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def execute_move(self, move: object) -> None:
        self.board[move.start_square[0]][move.start_square[1]] = None
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.swap_player_turn()

    def undo_move(self) -> None:
        if len(self.move_log) == 0:
            return

        most_recent_move = self.move_log.pop()
        self.board[most_recent_move.end_square[0]][
            most_recent_move.end_square[1]
        ] = most_recent_move.captured_piece
        self.board[most_recent_move.start_square[0]][
            most_recent_move.start_square[1]
        ] = most_recent_move.moved_piece
        self.swap_player_turn()

    def get_possible_moves(self) -> list:
        possible_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == None:
                    continue

                controller = self.board[row][col][0]
                piece = self.board[row][col][2:]

                if (
                    controller == "w"
                    and self.turn == "white"
                    or controller == "b"
                    and self.turn == "black"
                ):
                    possible_moves += self.move_methods[piece](row, col)

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
        for i in range(col + 1, len(self.board) - 1):
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
        if (
            not self.board[row - 2][col - 1]
            or (self.board[row - 2][col - 1][0] == "w" and self.turn == "black")
            or (self.board[row - 2][col - 1][0] == "b" and self.turn == "white")
        ):
            possible_moves.append(Movement((row, col), (row - 2, col - 1), self.board))

        # move 2 up 1 right
        if (
            not self.board[row - 2][col + 1]
            or (self.board[row - 2][col + 1][0] == "w" and self.turn == "black")
            or (self.board[row - 2][col + 1][0] == "b" and self.turn == "white")
        ):
            possible_moves.append(Movement((row, col), (row - 2, col + 1), self.board))

        # move 2 left 1 up
        if (
            not self.board[row - 1][col - 2]
            or (self.board[row - 1][col - 2][0] == "w" and self.turn == "black")
            or (self.board[row - 1][col - 2][0] == "b" and self.turn == "white")
        ):
            possible_moves.append(Movement((row, col), (row - 1, col - 2), self.board))

        # move 2 left 1 down
        if (
            not self.board[row + 1][col - 2]
            or (self.board[row + 1][col - 2][0] == "w" and self.turn == "black")
            or (self.board[row + 1][col - 2][0] == "b" and self.turn == "white")
        ):
            possible_moves.append(Movement((row, col), (row + 1, col - 2), self.board))

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
        for i in range(col + 1, len(self.board) - 1):
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
        return []


class Movement:
    def __init__(self, start_square: tuple, end_square: tuple, board: list) -> None:
        self.start_square = start_square
        self.end_square = end_square
        self.moved_piece = board[self.start_square[0]][self.start_square[1]]
        self.captured_piece = board[self.end_square[0]][self.end_square[1]]

    def __eq__(self, other):
        if not isinstance(other, Movement):
            return False
        return (
            self.start_square == other.start_square
            and self.end_square == other.end_square
            and self.moved_piece == other.moved_piece
            and self.captured_piece == other.captured_piece
        )
