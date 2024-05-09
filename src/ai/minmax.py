from math import inf
from typing import Callable, Optional
from model.halma import Halma
from model.moves import PieceMove
from model.field import FieldState
from .heuristics import evaluate_board_state, manhattan_distance


def minmax(
    halma: Halma,
    depth: int,
    minimizing_player: FieldState,
    heuristic: Callable[[int, int, tuple[int, int]], float],
) -> tuple[float, Optional[PieceMove]]:
    if depth == 0:
        return (
            evaluate_board_state(halma.board.board_state, heuristic, minimizing_player),
            None,
        )
    print(f"Evaluation minimizing player {minimizing_player} at depth {depth}")

    minimize: bool = halma.current_player == minimizing_player
    best_evaluation = inf if minimize else -inf
    best_move = None

    possible_moves = halma.board.get_possible_moves(halma.current_player)
    print(f"{len(possible_moves)=} of player{halma.current_player}")
    for move in possible_moves:
        halma.make_move(move)
        evaluation, _ = minmax(halma, depth - 1, minimizing_player, heuristic)
        halma.undo_move()

        if minimize:
            if evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move
        else:
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move

    return best_evaluation, best_move
