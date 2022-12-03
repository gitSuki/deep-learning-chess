import pygame as pg

pg.init()
GRID_SIZE = 512
SQUARE_SIZE = GRID_SIZE // 8
IMAGES = {}


def load_images():
    image_list = [
        "w_pawn",
        "b_pawn",
        "w_rook",
        "b_rook",
        "w_knight",
        "b_knight",
        "w_bishop",
        "b_bishop",
        "w_queen",
        "b_queen",
        "w_king",
        "b_king",
    ]

    for chess_piece_image in image_list:
        IMAGES[chess_piece_image] = pg.transform.scale(
            pg.image.load(f"./assets/{chess_piece_image}.png"),
            (SQUARE_SIZE, SQUARE_SIZE),
        )


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
