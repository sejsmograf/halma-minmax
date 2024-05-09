from math import inf
from typing import Callable, Optional
from model import Halma, PieceMove, FieldState
from .heuristics import evaluate_board_state


def minmax(
    halma: Halma,
    depth: int,
    maximizing_player: FieldState,
    heuristic_distance: Callable[[int, int, tuple[int, int]], float],
) -> tuple[float, PieceMove]:

    if depth == 0:
        return (
            evaluate_board_state(halma.board, maximizing_player, heuristic_distance),
            PieceMove((-1, -1), (-1, -1)),  # return invalid move, it will never be used
        )

    maximize: bool = halma.current_player == maximizing_player
    best_evaluation = -inf if maximize else inf
    best_move = None

    possible_moves = halma.board.get_possible_moves(halma.current_player)
    for move in possible_moves:
        halma.make_move(move)
        evaluation, _ = minmax(halma, depth - 1, maximizing_player, heuristic_distance)
        halma.undo_move(move)

        if maximize:
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move
        else:
            if evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move

    # pseudo unpack the move (just for the LSP to not complain)
    if best_move is None:
        raise ValueError("Best move not found")

    return best_evaluation, best_move
