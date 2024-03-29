import numpy as np
import pygame as pg

from constants import *


def load_images() -> list:
    """
    Creates a dictionary, mapping every piece and color combination to it's respective image file"
    """
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

    for image in image_list:
        images_dict[image] = pg.transform.scale(
            pg.image.load(f"./assets/{image}.png"),
            (SQUARE_SIZE, SQUARE_SIZE),
        )
    return images_dict


IMAGES = load_images()


def draw_game_state(
    screen: object,
    game_state: object,
    legal_moves: list,
    selected_square: tuple,
) -> None:
    """
    Handles all the GUI code for visually representing the current game state.
    """
    draw_board(screen)
    draw_pieces(screen, game_state)
    highlight_squares(screen, game_state, legal_moves, selected_square)
    highlight_previous_move(screen, game_state)


def draw_board(screen: object):
    """
    Draws all the background squares on the board. The top left square is always light and the colors alternate between light and dark.
    """
    for row in np.arange(GRID_DIMENSION):
        for col in np.arange(GRID_DIMENSION):
            location_is_even = (row + col) % 2
            if location_is_even:
                color = pg.Color("white")
            else:
                color = pg.Color("burlywood4")
            pg.draw.rect(
                screen,
                color,
                pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


def draw_pieces(screen: object, game_state: object) -> None:
    """
    Draws all the chess pieces on the board using based on the current game_state.
    """
    for row in np.arange(GRID_DIMENSION):
        for col in np.arange(GRID_DIMENSION):
            piece = game_state.board[row][col]
            if piece:
                screen.blit(
                    IMAGES[piece.image_code],
                    pg.Rect(
                        col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    ),
                )


def highlight_squares(
    screen: object, game_state: object, legal_moves: list, selected_square: tuple
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
            game_state.board[selected_square[0]][selected_square[1]].team
            == game_state.turn
        )
        if selected_piece_is_players:
            highlight_individual_square(screen, "yellow", selected_square)
            highlight_movement_options(screen, legal_moves, selected_square)


def highlight_movement_options(
    screen: object, legal_moves: list, selected_square: tuple
) -> None:
    """
    Highlights all valid movements that a piece may make.
    """
    for move in legal_moves:
        color = "blue"
        if move.start_square == selected_square:
            if move.captured_piece:
                color = "red"
            highlight_individual_square(screen, color, move.end_square)


def highlight_individual_square(
    screen: object, color: str, square_location: tuple
) -> None:
    """
    Highlights a specific individual square.
    """
    highlight_surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
    highlight_surface.set_alpha(100)
    pixel_coordinates = (
        square_location[1] * SQUARE_SIZE,
        square_location[0] * SQUARE_SIZE,
    )
    highlight_surface.fill(pg.Color(color))
    screen.blit(highlight_surface, pixel_coordinates)


def highlight_previous_move(screen: object, game_state: object):
    """
    Highlights the previous move made by the last player.
    """
    if len(game_state.move_log) >= 1:
        highlight_individual_square(
            screen, "yellow", game_state.move_log[-1].start_square
        )
        highlight_individual_square(
            screen, "yellow", game_state.move_log[-1].end_square
        )


def animate_move(move, game_state, screen, clock):
    """
    Handles all the code for animating a piece moving from one square to another.
    """
    change_row = move.end_square[0] - move.start_square[0]
    change_col = move.end_square[1] - move.start_square[1]
    frames_per_square = 10
    frame_count = (abs(change_row) + abs(change_col)) * frames_per_square

    for frame in np.arange(frame_count + 1):
        row = move.start_square[0] + change_row * frame / frame_count
        col = move.start_square[1] + change_col * frame / frame_count
        draw_board(screen)
        draw_pieces(screen, game_state)

        location_is_even = (move.end_square[0] + move.end_square[1]) % 2
        if location_is_even:
            color = pg.Color("white")
        else:
            color = pg.Color("burlywood4")
        end_square = pg.Rect(
            move.end_square[1] * SQUARE_SIZE,
            move.end_square[0] * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        pg.draw.rect(screen, color, end_square)

        if move.captured_piece:
            screen.blit(IMAGES[move.captured_piece.image_code], end_square)

        animated_piece_location = pg.Rect(
            col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
        )
        screen.blit(IMAGES[move.moved_piece.image_code], animated_piece_location)
        pg.display.flip()
        clock.tick(60)


def draw_text(screen, victor, victory_condition):
    """
    Handles the code for displaying the victory or defeat conditions on the screen.
    """
    FONT_SIZE = 40
    font = pg.font.SysFont("calibri", FONT_SIZE, True, False)
    string = f"{victor} wins by {victory_condition}!".capitalize()
    text = font.render(string, 0, pg.Color("black"))
    text_location = pg.Rect(0, 0, BOARD_SIZE, BOARD_SIZE).move(
        BOARD_SIZE / 2 - text.get_width() / 2, BOARD_SIZE / 2 - text.get_height() / 2
    )
    screen.blit(text, text_location)
