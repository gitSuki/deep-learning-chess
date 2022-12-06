import pygame as pg
import game_engine as engine
import gui as gui

pg.init()
GRID_SIZE = 512
GRID_DIMENSION = 8
SQUARE_SIZE = GRID_SIZE // GRID_DIMENSION
FPS = 15
IMAGES = gui.load_images(SQUARE_SIZE)


def main() -> None:
    screen = pg.display.set_mode((GRID_SIZE, GRID_SIZE))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    game_state = engine.GameState()
    legal_moves = game_state.get_possible_moves()
    game_state_has_changed = (
        False  # used to recalculate legal moves any time the board changes
    )

    selected_square = ()  # tuple to represent (row, col) of last selected square
    select_log = []

    is_running = True
    while is_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                is_running = False

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    game_state.undo_move()
                    game_state_has_changed = True

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
                    if move in legal_moves:
                        game_state.execute_move(move)
                        game_state_has_changed = True
                    selected_square = ()
                    select_log = []

        if game_state_has_changed:
            legal_moves = game_state.get_possible_moves()
            game_state_has_changed = False

        gui.draw_game_state(screen, game_state, IMAGES, GRID_DIMENSION, SQUARE_SIZE)
        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
