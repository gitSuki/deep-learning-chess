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
    highlight_last_move(screen, game_state, square_size)


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
                color = "red"
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


def highlight_last_move(
    screen: object,
    game_state: object,
    square_size: int,
):
    if len(game_state.move_log) >= 1:
        highlight_individual_square(
            screen, "yellow", game_state.move_log[-1].start_square, square_size
        )
        highlight_individual_square(
            screen, "yellow", game_state.move_log[-1].end_square, square_size
        )


def animate_move(move, game_state, screen, images, grid_dimension, square_size, clock):
    change_row = move.end_square[0] - move.start_square[0]
    change_col = move.end_square[1] - move.start_square[1]
    frames_per_square = 10
    frame_count = (abs(change_row) + abs(change_col)) * frames_per_square

    for frame in range(frame_count + 1):
        row = move.start_square[0] + change_row * frame / frame_count
        col = move.start_square[1] + change_col * frame / frame_count
        draw_board(screen, grid_dimension, square_size)
        draw_pieces(screen, game_state, images, grid_dimension, square_size)

        location_is_even = (move.end_square[0] + move.end_square[1]) % 2
        if location_is_even:
            color = pg.Color("white")
        else:
            color = pg.Color("gray")
        end_square = pg.Rect(
            move.end_square[1] * square_size,
            move.end_square[0] * square_size,
            square_size,
            square_size,
        )
        pg.draw.rect(screen, color, end_square)

        if move.captured_piece:
            screen.blit(images[move.captured_piece], end_square)

        animated_piece_location = pg.Rect(
            col * square_size, row * square_size, square_size, square_size
        )
        screen.blit(images[move.moved_piece], animated_piece_location)
        pg.display.flip()
        clock.tick(60)

def draw_text(screen, victor, victory_condition, grid_size):
    font = pg.font.SysFont("calibri", 32, True, False)
    string = f"{victor} wins by {victory_condition}!".capitalize()
    text = font.render(string, 0, pg.Color("black"))
    text_location = pg.Rect(0, 0, grid_size, grid_size).move(grid_size/2 - text.get_width()/2, grid_size/2 - text.get_height()/2)
    screen.blit(text, text_location)