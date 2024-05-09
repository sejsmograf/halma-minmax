import argparse
from sys import stdin
from ai import heuristics, minmax
from model import Halma


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

    print(minmax.minmax(h, 2, h.current_player, heuristics.manhattan_distance))
