import pygame as pg


def load_images(square_size: int) -> list:
    images_dict = {}
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
        images_dict[chess_piece_image] = pg.transform.scale(
            pg.image.load(f"./assets/{chess_piece_image}.png"),
            (square_size, square_size),
        )
    return images_dict


def draw_game_state(
    screen: object,
    game_state: object,
    images: list,
    grid_dimension: int,
    square_size: int,
) -> None:
    draw_board(screen, grid_dimension, square_size)
    draw_pieces(screen, game_state, images, grid_dimension, square_size)


def draw_board(screen: object, grid_dimension: int, square_size: int):
    """
    Draws all the background squares on the board. The top left square is always light and the colors alternate between light and dark.
    """
    for row in range(grid_dimension):
        for col in range(grid_dimension):
            location_is_even = (row + col) % 2
            if location_is_even:
                color = pg.Color("white")
            else:
                color = pg.Color("gray")
            pg.draw.rect(
                screen,
                color,
                pg.Rect(col * square_size, row * square_size, square_size, square_size),
            )


def draw_pieces(
    screen: object,
    game_state: object,
    images: list,
    grid_dimension: int,
    square_size: int,
):
    """
    Draws all the chess pieces on the board using based on the current game_state.
    """
    for row in range(grid_dimension):
        for col in range(grid_dimension):
            piece = game_state.board[row][col]
            if piece:
                screen.blit(
                    images[piece],
                    pg.Rect(
                        col * square_size, row * square_size, square_size, square_size
                    ),
                )
