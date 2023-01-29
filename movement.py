class Movement:
    """
    Represents an individual move from a given start square to it's destination end square.
    """

    def __init__(self, start_square: tuple, end_square: tuple, board: list) -> None:
        self.start_square = start_square
        self.end_square = end_square
        self.moved_piece = board[self.start_square[0]][self.start_square[1]]
        self.captured_piece = board[self.end_square[0]][self.end_square[1]]
        self.is_pawn_promotion = self.pawn_promotion()
        self.promotion_choice = "queen"

    def __eq__(self, other):
        if not isinstance(other, Movement):
            return False
        return (
            self.start_square == other.start_square
            and self.end_square == other.end_square
            and self.moved_piece == other.moved_piece
            and self.captured_piece == other.captured_piece
        )

    def __str__(self):
        debug_string = f"Moving {self.moved_piece} from {self.start_square} to {self.end_square}, capturing {self.captured_piece}."
        if self.is_pawn_promotion:
            debug_string += f" Promotion choice: {self.promotion_choice}"
        return debug_string

    def pawn_promotion(self) -> bool:
        white_pawn_can_promote = (
            self.moved_piece == "w_pawn" and self.end_square[0] == 0
        )
        black_pawn_can_promote = (
            self.moved_piece == "b_pawn" and self.end_square[0] == 7
        )

        if white_pawn_can_promote or black_pawn_can_promote:
            return True
        else:
            return False
