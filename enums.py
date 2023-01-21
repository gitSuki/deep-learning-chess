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


WHITE = Team.WHITE.value
BLACK = Team.BLACK.value

PAWN = Type.PAWN.value
ROOK = Type.ROOK.value
KNIGHT = Type.KNIGHT.value
BISHOP = Type.BISHOP.value
QUEEN = Type.QUEEN.value
KING = Type.KING.value
