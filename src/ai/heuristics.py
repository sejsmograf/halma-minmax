from typing import Callable
from model import Board, FieldState


def manhattan_distance(row: int, col: int, goal: tuple[int, int]) -> float:
    return abs(row - goal[0]) + abs(col - goal[1])


def evaluate_board_state(
    board: Board,
    heuristic: Callable[[int, int, tuple[int, int]], float],
    player: FieldState,
) -> float:
    goal_corner: tuple[int, int] = Board.PLAYER_GOAL_CORNERS[player]
    player_positions: list[tuple[int, int]] = board.get_player_positions(player)
    evalutation = sum(
        [heuristic(row, col, goal_corner) for row, col in player_positions]
    )
    return evalutation
