import numpy as np

from constants import *


class Player:
    def __init__(self, team: str, is_human: bool) -> None:
        self.team = team
        self.is_human = is_human
        self.piece_list = []

    def update_piece_list(self, board: list) -> None:
        """
        Update's the player's piece list based on the board given as an argument.
        """
        self.piece_list = self._traverse_board(board)

    def _traverse_board(self, board: list) -> list:
        """
        Create's a new piece list based on the board given as an argument.
        """
        piece_list = []
        for row in np.arange(len(board)):
            for col in np.arange(len(board[row])):
                piece = board[row][col]
                if self._piece_is_owned_by_player(piece):
                    piece_list.append(board[row][col])
        return piece_list

    def _piece_is_owned_by_player(self, piece: object) -> bool:
        """
        Returns true or false if a given piece is owned by the current player.
        """
        if piece:
            piece_is_player_team = piece.team == self.team
            if piece_is_player_team:
                return True
        return False