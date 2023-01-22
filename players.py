import numpy as np

from constants import *


class Player:
    def __init__(self, team: str, piece_list: list, is_player: bool) -> None:
        self.team = team
        self.piece_list = piece_list
        self.is_player = is_player

    def update_piece_list(self, board: list) -> None:
        piece_list = []
        for row in np.arange(len(board)):
            for col in np.arange(len(board[row])):
                piece_exists = board[row][col]
                if piece_exists:
                    piece_is_player_team = board[row][col].team == self.team
                    if piece_is_player_team:
                        piece_list.append(board[row][col])
        self.piece_list = piece_list
