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

    def execute_move(self, move):
        self.get_possible_moves()
        self.board[move.start_square[0]][move.start_square[1]] = None
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.swap_player_turn()

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
        self.swap_player_turn()

    def get_possible_moves(self):
        possible_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == None:
                    continue

                square_owner = self.board[row][col][0]
                square_piece = self.board[row][col][2:]
                if square_owner == "w" and self.turn == "white":
                    pass
                elif square_owner == "b" and self.turn == "black":
                    pass


class Movement:
    def __init__(self, start_square, end_square, board):
        self.start_square = start_square
        self.end_square = end_square
        self.moved_piece = board[self.start_square[0]][self.start_square[1]]
        self.captured_piece = board[self.end_square[0]][self.end_square[1]]
