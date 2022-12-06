class GameState:
    def __init__(self) -> None:
        self.turn = "white"
        self.move_log = []

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
                if controller == "w" and self.turn == "white":
                    if piece == "pawn":
                        possible_moves += self.get_pawn_moves(row, col)
                    elif piece == "rook":
                        pass
                    elif piece == "knight":
                        pass
                    elif piece == "bishop":
                        pass
                    elif piece == "queen":
                        pass
                    elif piece == "king":
                        pass
                elif controller == "b" and self.turn == "black":
                    if piece == "pawn":
                        pass
                    elif piece == "rook":
                        pass
                    elif piece == "knight":
                        pass
                    elif piece == "bishop":
                        pass
                    elif piece == "queen":
                        pass
                    elif piece == "king":
                        pass
        return possible_moves

    def get_pawn_moves(self, row: int, col: int) -> list:
        possible_moves = []
        if self.turn == "white":
            if not self.board[row - 1][col]:
                possible_moves.append(Movement((row, col), (row - 1, col), self.board))
                # pawns can move two squares directly forward on their first move
                # pawns can never move backward so they will always be at their starting row
                # if they haven't moved
                if row == 6 and not self.board[row - 2][col]:
                    possible_moves.append(
                        Movement((row, col), (row - 2, col), self.board)
                    )
        return possible_moves


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
