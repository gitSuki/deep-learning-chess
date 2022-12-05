class GameState:
    def __init__(self):
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
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
            ],
            [
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
            ],
            [
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
            ],
            [
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
                "open",
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

    def execute_move(self, move):
        self.board[move.start_square[0]][move.start_square[1]] = "open"
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.turn = "black" if self.turn == "white" else "white"

    def undo_move(self):
        if len(self.move_log) == 0:
            return

        most_recent_move = self.move_log.pop()
        self.board[most_recent_move.end_square[0]][
            most_recent_move.end_square[1]
        ] = most_recent_move.captured_piece
        self.board[most_recent_move.start_square[0]][
            most_recent_move.start_square[1]
        ] = most_recent_move.moved_piece
        self.turn = "black" if self.turn == "white" else "white"


class Movement:
    def __init__(self, start_square, end_square, board):
        self.start_square = start_square
        self.end_square = end_square
        self.moved_piece = board[self.start_square[0]][self.start_square[1]]
        self.captured_piece = board[self.end_square[0]][self.end_square[1]]
