from typing import Callable
from model import Board, FieldState


def manhattan_distance(row: int, col: int, goal: tuple[int, int]) -> float:
    return abs(row - goal[0]) + abs(col - goal[1])


def evaluate_board_state(
    board: Board,
    player: FieldState,
    heuristic_distance: Callable[[int, int, tuple[int, int]], float],
) -> float:
    goal_camp: list[tuple[int, int]] = board.get_player_goal_camp(player)
    goal_position = board.get_goal_position(goal_camp)

    player_positions: list[tuple[int, int]] = board.get_player_positions(player)
    evaluation = 0

    for row, col in player_positions:
        # bigger distance means worse score
        evaluation -= heuristic_distance(row, col, goal_position)

        # give big reward to piecees in goal camp
        if (row, col) in goal_camp:
            evaluation += 100

    return evaluation
