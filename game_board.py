import numpy as np

from enums import *
from chess_piece import *


def game_board() -> np.array:
    """
    Returns a 2d array representing the individual pieces as objects and the status of the chess board at round start.
    """
    return np.array(
        [
            [
                Rook(BLACK, (0, 0)),
                Knight(BLACK, (0, 1)),
                Bishop(BLACK, (0, 2)),
                Queen(BLACK, (0, 3)),
                King(BLACK, (0, 4)),
                Bishop(BLACK, (0, 5)),
                Knight(BLACK, (0, 6)),
                Rook(BLACK, (0, 7)),
            ],
            [
                Pawn(BLACK, (1, 0)),
                Pawn(BLACK, (1, 1)),
                Pawn(BLACK, (1, 2)),
                Pawn(BLACK, (1, 3)),
                Pawn(BLACK, (1, 4)),
                Pawn(BLACK, (1, 5)),
                Pawn(BLACK, (1, 6)),
                Pawn(BLACK, (1, 7)),
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
                Pawn(WHITE, (6, 0)),
                Pawn(WHITE, (6, 1)),
                Pawn(WHITE, (6, 2)),
                Pawn(WHITE, (6, 3)),
                Pawn(WHITE, (6, 4)),
                Pawn(WHITE, (6, 5)),
                Pawn(WHITE, (6, 6)),
                Pawn(WHITE, (6, 7)),
            ],
            [
                Rook(WHITE, (7, 0)),
                Knight(WHITE, (7, 1)),
                Bishop(WHITE, (7, 2)),
                Queen(WHITE, (7, 3)),
                King(WHITE, (7, 4)),
                Bishop(WHITE, (7, 5)),
                Knight(WHITE, (7, 6)),
                Rook(WHITE, (7, 7)),
            ],
        ]
    )
