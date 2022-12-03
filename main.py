import pygame as pg

GRID_SIZE = 512
SQUARE_SIZE = GRID_SIZE // 8
IMAGES = {}


class GameState:
    def __init__(self):
        self.turn = "WHITE"
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


test = GameState()
