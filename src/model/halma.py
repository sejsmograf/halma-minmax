from typing import Optional

from model.field import FieldState
from .board import Board


class Halma:
    PLAYER_ONE = FieldState.WHITE
    PLAYER_TWO = FieldState.BLACK

    def __init__(self, board_state: Optional[str] = None) -> None:
        self.board = Board(board_state)

    def print_board(self) -> None:
        self.board.print_board()
