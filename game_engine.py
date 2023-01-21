import numpy as np

from constants import *
from piece import *
from players import Player
from game_board import game_board


class GameState:
    """
    Represents the game engine and the current state of the game.
    """

    def __init__(self) -> None:
        self.board = game_board()
        self.players = {
            WHITE: Player(WHITE, [], True),
            BLACK: Player(BLACK, [], True),
        }
        self.move_log = []
        self.turn = WHITE
        self.checkmate = False
        self.stalemate = False

    def swap_player_turn(self) -> None:
        """
        Swaps the current player in the game between white or black.
        """
        self.turn = BLACK if self.turn == WHITE else WHITE

    def execute_move(self, move: object) -> None:
        """
        Executes the move given as an argument.
        """
        move.moved_piece.location = move.end_square
        self.board[move.start_square[0]][move.start_square[1]] = None
        self.board[move.end_square[0]][move.end_square[1]] = move.moved_piece
        self.move_log.append(move)
        self.players[self.turn].update_piece_list(self.board)

        if move.is_pawn_promotion:
            # Automatically promotes to Queen
            # promoted_piece = move.promotion_choice
            team = move.moved_piece.team
            promoted_piece = Queen(team, move.end_square)
            self.board[move.end_square[0]][move.end_square[1]] = promoted_piece

        self.swap_player_turn()

    def undo_move(self) -> None:
        """
        Undoes the most recent move in the move log.
        """
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        move.moved_piece.location = move.start_square
        self.board[move.end_square[0]][move.end_square[1]] = move.captured_piece
        self.board[move.start_square[0]][move.start_square[1]] = move.moved_piece
        self.players[self.turn].update_piece_list(self.board)
        self.swap_player_turn()
        self.checkmate = False
        self.stalemate = False

    def get_legal_moves(self) -> list:
        """
        Calculates all legal moves, accounting for checks and checkmate.
        """
        players_possible_moves = self.get_possible_moves()

        # loops through list of moves backwards to prevent bugs from occuring when deleting invalid moves
        for move in players_possible_moves[::-1]:
            # execute_move() automatically swaps player's turns, we need to reswap turns again otherwise our
            # helper methods will calculate for the wrong player
            self.execute_move(move)
            self.swap_player_turn()
            move_would_put_king_in_check = self.king_in_check()
            if move_would_put_king_in_check:
                players_possible_moves.remove(move)
            self.swap_player_turn()
            self.undo_move()

        if len(players_possible_moves) == 0:
            self.check_gameover_conditions()

        # for move in players_possible_moves:
        #     print(move)
        # print(len(players_possible_moves))
        # print(" ")
        return players_possible_moves

    def check_gameover_conditions(self) -> None:
        """
        Checks if the game is in either a checkmate or stalemate situation.
        """
        king_is_in_check = self.king_in_check()
        if king_is_in_check:
            self.checkmate = True
        else:
            self.stalemate = True

    def king_in_check(self) -> bool:
        """
        Calculates if the current player's king is in a check situation.
        """
        if self.turn == WHITE:
            for piece in self.players[WHITE].piece_list:
                if piece.type == KING:
                    return self.piece_under_attack(piece)
        else:
            for piece in self.players[BLACK].piece_list:
                if piece.type == KING:
                    return self.piece_under_attack(piece)

    def piece_under_attack(self, piece: object) -> bool:
        """
        Calculates if the piece given as an argument could come under attack by the opponent.
        """
        self.swap_player_turn()
        opponents_possible_moves = self.get_possible_moves()

        for move in opponents_possible_moves:
            square_is_under_attack = piece.location == move.end_square
            if square_is_under_attack:
                self.swap_player_turn()
                return True
        self.swap_player_turn()
        return False

    def get_possible_moves(self) -> list:
        """
        Calculates all potential moves, regardless of checks and checkmate.
        """
        possible_moves = []
        for row in np.arange(len(self.board)):
            for col in np.arange(len(self.board[row])):
                square_is_empty = self.board[row][col] == None
                if square_is_empty:
                    continue

                piece = self.board[row][col]
                piece_is_opponents = piece.team != self.turn
                if piece_is_opponents:
                    continue

                possible_moves += piece.get_moves(row, col, self.board)
        return possible_moves
