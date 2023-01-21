from enum import Enum


class Team(Enum):
    """
    Defines both teams involved in the game.
    """

    WHITE = "white"
    BLACK = "black"


class Type(Enum):
    """
    Defines all possible types of chess pieces
    """

    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"


class Piece:
    """
    Represents an individual chess piece on the game board
    """

    def __init__(self, team: str, type: str, location: tuple) -> None:
        self.team = team
        self.type = type
        self.location = location

    def __str__(self) -> str:
        return f"{self.team} {self.type} at {self.location}"
