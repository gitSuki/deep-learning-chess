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
    legal_moves: list,
    selected_square: tuple,
    images: list,
    grid_dimension: int,
    square_size: int,
) -> None:
    draw_board(screen, grid_dimension, square_size)
    draw_pieces(screen, game_state, images, grid_dimension, square_size)
    highlight_squares(screen, game_state, legal_moves, selected_square, square_size)


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
) -> None:
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


def highlight_squares(
    screen: object,
    game_state: object,
    legal_moves: list,
    selected_square: tuple,
    square_size: int,
) -> None:
    """
    Highlights the selected square and all valid movements the piece may make
    """
    valid_square_selected = (
        selected_square != ()
        and game_state.board[selected_square[0]][selected_square[1]] != None
    )
    if valid_square_selected:
        selected_piece_is_players = (
            game_state.board[selected_square[0]][selected_square[1]][0]
            == game_state.turn[0]
        )
        if selected_piece_is_players:
            highlight_individual_square(screen, "yellow", selected_square, square_size)
            highlight_movement_options(
                screen, legal_moves, selected_square, square_size
            )


def highlight_movement_options(
    screen: object,
    legal_moves: list,
    selected_square: tuple,
    square_size: int,
) -> None:
    """
    Highlights all valid movements the piece may make
    """
    for move in legal_moves:
        color = "blue"
        if move.start_square == selected_square:
            if move.captured_piece:
                color = "green"
            highlight_individual_square(screen, color, move.end_square, square_size)


def highlight_individual_square(
    screen: object,
    color: str,
    square_location: tuple,
    square_size: int,
) -> None:
    """
    Highlights a specific individual square
    """
    highlight_surface = pg.Surface((square_size, square_size))
    highlight_surface.set_alpha(100)
    pixel_coordinates = (
        square_location[1] * square_size,
        square_location[0] * square_size,
    )
    highlight_surface.fill(pg.Color(color))
    screen.blit(highlight_surface, pixel_coordinates)
