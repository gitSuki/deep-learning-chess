from constants import *


class Piece:
    """
    Represents an individual chess piece on the game board.
    """

    def __init__(self, team: str, type: str, location: tuple) -> None:
        self.team = team
        self.type = type
        self.location = location

    def __str__(self) -> str:
        return f"{self.team} {self.type} at {self.location}"


class Pawn(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, PAWN, location)


class Rook(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, ROOK, location)


class Knight(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KNIGHT, location)


class Bishop(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, BISHOP, location)


class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, QUEEN, location)


class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, KING, location)
