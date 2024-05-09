from typing import Callable
from model.field import FieldState
from model.board import Board
from model.moves import get_player_pieces


def manhattan_distance(row: int, col: int, goal: tuple[int, int]) -> float:
    return abs(row - goal[0]) + abs(col - goal[1])


def evaluate_board_state(
    board_state: list[list[FieldState]],
    heuristic: Callable[[int, int, tuple[int, int]], float],
    player: FieldState,
) -> float:
    goal_corner: tuple[int, int] = Board.PLAYER_GOALS[player]
    player_pieces: list[tuple[int, int]] = get_player_pieces(board_state, player)

    state_evalutation = sum(
        [heuristic(row, col, goal_corner) for row, col in player_pieces]
    )

    return state_evalutation
