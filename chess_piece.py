from enum import Enum


class Team(Enum):
    """
    Defines both teams involved in the game.
    """

    WHITE = "white"
    BLACK = "black"


class Type(Enum):
    """
    Defines all possible types of chess pieces.
    """

    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"


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
        super().__init__(team, Type.PAWN.value, location)


class Rook(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, Type.ROOK.value, location)


class Knight(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, Type.KNIGHT.value, location)


class Bishop(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, Type.BISHOP.value, location)


class Queen(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, Type.QUEEN.value, location)


class King(Piece):
    def __init__(self, team: str, location: tuple) -> None:
        super().__init__(team, Type.KING.value, location)
