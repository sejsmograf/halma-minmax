from typing import Optional
from .board import Board


class Halma:
    def __init__(self, board_state: Optional[str] = None) -> None:
        self.board = Board(board_state)

    def print_board(self):
        self.board.print_board()
