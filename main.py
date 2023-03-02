import pygame as pg
from multiprocessing import Process, Queue
from constants import *
from engine.game_state import GameState
from gui import draw_game_state, draw_text, animate_move
from engine.movement import Movement
from ai.negamax import find_random_move, find_best_move
import torch
from torch import nn
import pytorch_lightning as pl
from collections import OrderedDict

pg.init()

class EvaluationModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-3, batch_size=1024, layer_count=10):
        super().__init__()
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        layers = []
        for i in range(layer_count - 1):
            layers.append((f"linear-{i}", nn.Linear(768, 768)))
            layers.append((f"relu-{i}", nn.ReLU()))
        layers.append((f"linear-{layer_count - 1}", nn.Linear(768, 1)))
        self.seq = nn.Sequential(OrderedDict(layers))

    def forward(self, x):
        return self.seq(x)


def main(model) -> None:
    screen = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    clock = pg.time.Clock()
    game_state = GameState()
    legal_moves = game_state.get_legal_moves()
    selected_square = ()  # tuple to represent (row, col) of last selected square
    select_log = []
    is_running = True
    should_be_animated = False  # used as a flag for if a move should be animated
    game_state_has_changed = (
        False  # used to recalculate legal moves any time the board changes
    )
    white_is_player = True
    black_is_player = False
    ai_is_thinking = False
    move_finder_process = None
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
                    game_over = False
                    # go back two moves if playing against an AI
                    if (
                        game_state.turn == BLACK
                        and white_is_player
                        and not black_is_player
                    ) or (
                        game_state.turn == WHITE
                        and black_is_player
                        and not white_is_player
                    ):
                        should_be_animated = False
                        game_state.undo_move()
                        game_state_has_changed = True
                        game_over = False

                if e.key == pg.K_r:
                    game_state = GameState()
                    legal_moves = game_state.get_legal_moves()
                    selected_square = ()
                    select_log = []
                    should_be_animated = False
                    game_state_has_changed = False
                    game_over = False

            elif e.type == pg.MOUSEBUTTONDOWN:
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
                if user_has_clicked_movement_destination and is_human_turn:
                    row = select_log[0]
                    col = select_log[1]
                    move = Movement(row, col, game_state.board)

                    if move in legal_moves:
                        if move.is_pawn_promotion:
                            while True:
                                possible_choices = [ROOK, KNIGHT, BISHOP, QUEEN]
                                choice = input(
                                    "Which piece do you want to promote to? (queen, rook, bishop, or knight)\n"
                                )
                                if choice in possible_choices:
                                    break
                            move.promotion_choice = choice

                        game_state.execute_move(move)
                        game_state_has_changed = True
                        should_be_animated = True
                        selected_square = ()
                        select_log = []
                    else:
                        # prevents the user from having to click twice if they made an invalid move
                        select_log = [selected_square]

        # AI movement
        if not is_human_turn and not game_over:
            if not ai_is_thinking:
                ai_is_thinking = True
                move = find_best_move(model, game_state, legal_moves)

                if move is None:
                    # search for a random move if there were was an error with our main ai algorithm
                    move = find_random_move(legal_moves)

                game_state.execute_move(move)
                game_state_has_changed = True
                should_be_animated = True
                ai_is_thinking = False

        if game_state_has_changed:
            if should_be_animated:
                animate_move(game_state.move_log[-1], game_state, screen, clock)
            legal_moves = game_state.get_legal_moves()

            should_be_animated = False
            game_state_has_changed = False

        draw_game_state(screen, game_state, legal_moves, selected_square)

        if game_state.checkmate:
            game_over = True
            victor = BLACK if game_state.turn == WHITE else WHITE
            draw_text(screen, victor, "checkmate")
        elif game_state.stalemate:
            game_over = True
            victor = BLACK if game_state.turn == WHITE else WHITE
            draw_text(screen, victor, "stalemate")

        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    """
    The deep learning model is loaded directly into the main script to prevent having to load it repeatedly when the AI is calculating it's best move.
    """
    model = EvaluationModel(layer_count=2, batch_size=1024, learning_rate=1e-3)
    model.load_state_dict(torch.load("model/chkpt.pt"))
    model.eval()
    main(model)
