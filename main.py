import pygame as pg

pg.init()
GRID_SIZE = 512
GRID_DIMENSION = 8
SQUARE_SIZE = GRID_SIZE // GRID_DIMENSION
FPS = 15
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


def main():
    screen = pg.display.set_mode((GRID_SIZE, GRID_SIZE))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    game_state = GameState()
    load_images()

    is_running = True
    while is_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                is_running = False
        draw_game_state(screen, game_state)
        clock.tick(FPS)
        pg.display.flip()


def draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state)


def draw_board(screen):
    """
    Draws all the background squares on the board. The top left square is always light and the colors alternate between light and dark.
    """
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):
            location_is_even = (row + col) % 2
            if location_is_even:
                color = pg.Color("white")
            else:
                color = pg.Color("gray")
            pg.draw.rect(
                screen,
                color,
                pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


def draw_pieces(screen, game_state):
    """
    Draws all the chess pieces on the board using based on the current game_state.
    """
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):
            piece = game_state.board[row][col]
            if piece != "open":
                screen.blit(
                    IMAGES[piece],
                    pg.Rect(
                        col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    ),
                )


if __name__ == "__main__":
    main()
