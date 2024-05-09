import argparse
from model import Halma
from sys import stdin
from ai import heuristics
from model.field import FieldState
from model.moves import get_player_moves, get_piece_moves, get_player_pieces


def create_halma_game(use_stdin: bool) -> Halma:
    if use_stdin:
        if stdin.isatty():
            raise ValueError("Standard input argument passed, but stdin is empty")
        input = stdin.read()
        return Halma(input)

    return Halma()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="halma-minmax", description="Halma game with minmax AI"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read board state from standard input",
    )

    args = parser.parse_args()

    h = create_halma_game(args.stdin)
    h.print_board()

    for state in h.board.get_possible_board_states(h.PLAYER_ONE):
        print(heuristics.evaluate_board_state(state, heuristics.manhattan_distance))
        h.board.print_board(state)
        print("\n\n\n\n\n\n\n")
