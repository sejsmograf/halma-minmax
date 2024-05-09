from typing import Optional

from .field import FieldState
from .board import Board, PieceMove


class Halma:
    PLAYER_ONE = FieldState.WHITE
    PLAYER_TWO = FieldState.BLACK

    def __init__(self, board_state: Optional[str] = None) -> None:
        self.board = Board(board_state)
        self.current_player = Halma.PLAYER_ONE

    def print_board(self) -> None:
        self.board.print_board()

    def switch_player_turn(self):
        self.current_player = (
            FieldState.BLACK
            if self.current_player == FieldState.WHITE
            else FieldState.WHITE
        )

    def make_move(self, move: PieceMove):
        self.switch_player_turn()
        self.board.make_move(move)

    def undo_move(self, move: PieceMove):
        self.switch_player_turn()
        self.board.undo_move(move)
