import pygame as pg

from constants import *
from game_engine import GameState
from gui import draw_game_state, draw_text, animate_move
from game_movement import Movement
from game_ai import find_random_move

pg.init()


def main() -> None:
    screen = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    clock = pg.time.Clock()
    game_state = GameState()
    legal_moves = game_state.get_legal_moves()
    legal_moves = []
    selected_square = ()  # tuple to represent (row, col) of last selected square
    select_log = []
    is_running = True
    should_be_animated = False  # used as a flag for if a move should be animated
    game_state_has_changed = (
        False  # used to recalculate legal moves any time the board changes
    )
    white_is_player = True
    black_is_player = True
    game_over = False

    while is_running:
        is_human_turn = (game_state.turn == WHITE and white_is_player) or (
            game_state.turn == BLACK and black_is_player
        )
        for e in pg.event.get():
            if e.type == pg.QUIT:
                is_running = False

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    should_be_animated = False
                    game_state.undo_move()
                    game_state_has_changed = True

                if e.key == pg.K_r:
                    game_state = GameState()
                    legal_moves = game_state.get_legal_moves()
                    selected_square = ()
                    select_log = []
                    should_be_animated = False
                    game_state_has_changed = False
                    game_over = False

            elif e.type == pg.MOUSEBUTTONDOWN and is_human_turn and not game_over:
                location = pg.mouse.get_pos()  # gets (x, y) location of mouse
                row = location[1] // SQUARE_SIZE
                col = location[0] // SQUARE_SIZE

                square_was_already_selected = selected_square == (row, col)
                if square_was_already_selected:
                    # prevents the user from being able to move their piece to the same square it started on
                    selected_square = ()
                    select_log = []
                else:
                    selected_square = (row, col)
                    select_log.append(selected_square)

                user_has_clicked_movement_destination = len(select_log) == 2
                if user_has_clicked_movement_destination:
                    row = select_log[0]
                    col = select_log[1]
                    move = Movement(row, col, game_state.board)

                    if move in legal_moves:
                        if move.is_pawn_promotion:
                            while True:
                                possible_choices = ["queen", "rook", "bishop", "knight"]
                                choice = input(
                                    "Which piece do you want to promote to? (queen, rook, bishop, or knight)\n"
                                )
                                if choice in possible_choices:
                                    break
                            move.set_promotion_choice(choice)

                        game_state.execute_move(move)
                        game_state_has_changed = True
                        should_be_animated = True
                        selected_square = ()
                        select_log = []
                    else:
                        # prevents the user from having to click twice if they made an invalid move
                        select_log = [selected_square]

        if not is_human_turn and not game_over:
            move = find_random_move(legal_moves)
            game_state.execute_move(move)
            game_state_has_changed = True
            should_be_animated = True

        if game_state_has_changed:
            if should_be_animated:
                animate_move(game_state.move_log[-1], game_state, screen, clock)
            legal_moves = game_state.get_legal_moves()
            should_be_animated = False
            game_state_has_changed = False

        draw_game_state(screen, game_state, legal_moves, selected_square)

        if game_state.checkmate:
            game_over = True
            draw_text(screen, game_state.turn, "checkmate")
        elif game_state.stalemate:
            game_over = True
            draw_text(screen, game_state.turn, "stalemate")

        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
