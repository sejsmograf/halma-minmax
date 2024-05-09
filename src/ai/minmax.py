from math import inf
from typing import Callable, Optional
from model import Halma, PieceMove, FieldState
from .heuristics import evaluate_board_state


def minmax(
    halma: Halma,
    depth: int,
    minimizing_player: FieldState,
    heuristic: Callable[[int, int, tuple[int, int]], float],
) -> tuple[float, PieceMove]:

    if depth == 0:
        return (
            evaluate_board_state(halma.board, heuristic, minimizing_player),
            PieceMove((-1, -1), (-1, -1)),  # return invalid move, it will never be used
        )

    minimize: bool = halma.current_player == minimizing_player
    best_evaluation = inf if minimize else -inf
    best_move = None

    possible_moves = halma.board.get_possible_moves(halma.current_player)
    for move in possible_moves:
        halma.make_move(move)
        evaluation, _ = minmax(halma, depth - 1, minimizing_player, heuristic)
        halma.undo_move(move)

        if minimize:
            if evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move
        else:
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move

    # pseudo unpack the move (just for the LSP to not complain)
    if best_move is None:
        raise ValueError("Best move not found")

    return best_evaluation, best_move
