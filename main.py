import pygame as pg
import game_engine as engine

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


def main():
    screen = pg.display.set_mode((GRID_SIZE, GRID_SIZE))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    game_state = engine.GameState()
    load_images()

    selected_square = ()  # tuple to represent (row, col) of last selected square
    select_log = []

    is_running = True
    while is_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                is_running = False
            elif e.type == pg.KEYDOWN:
                game_state.undo_move()
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # (x, y) location of mouse
                row = location[1] // SQUARE_SIZE
                col = location[0] // SQUARE_SIZE

                was_already_selected = selected_square == (row, col)
                if was_already_selected:
                    # prevents the user from being able to move their piece to the same square it started on
                    selected_square = ()
                    select_log = []
                else:
                    selected_square = (row, col)
                    select_log.append(selected_square)

                if len(select_log) >= 2:
                    move = engine.Movement(
                        select_log[0], select_log[1], game_state.board
                    )
                    game_state.execute_move(move)
                    selected_square = ()
                    select_log = []

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
