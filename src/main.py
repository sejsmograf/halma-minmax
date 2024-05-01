from model import Halma
from sys import stdin

from model.field import FieldState


if __name__ == "__main__":
    if stdin.isatty():
        print("Standard input empty, initializing board")
        h = Halma()
    else:
        print("Reading board from stdin")
        board_state: str = stdin.read()
        h = Halma(board_state)
    h.print_board()
    count = 0
    count += len(h.board.get_player_moves(FieldState.BLACK))
    count += len(h.board.get_player_moves(FieldState.WHITE))
    print(count)
