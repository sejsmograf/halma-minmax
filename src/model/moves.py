from typing import NamedTuple
from queue import Queue
from .field import FieldState


directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


class PieceMove(NamedTuple):
    from_field: tuple[int, int]
    to_field: tuple[int, int]


def get_player_pieces(
    board_state: list[list[FieldState]], player_field: FieldState
) -> list[tuple[int, int]]:
    positions = []
    for row in range(len(board_state)):
        for col in range(len(board_state[0])):
            if board_state[row][col] == player_field:
                positions.append((row, col))

    return positions


def get_player_moves(
    board_state: list[list[FieldState]], player_field: FieldState
) -> list[PieceMove]:
    all_moves: list[PieceMove] = []

    for row in range(len(board_state)):
        for col in range(len(board_state[row])):
            if board_state[row][col] == player_field:
                all_moves += get_piece_moves(board_state, row, col)

    return all_moves


def get_piece_moves(
    board_state: list[list[FieldState]], row: int, col: int
) -> list[PieceMove]:
    if board_state[row][col] == FieldState.EMPTY:
        raise ValueError(f"FieldState at {row, col} is empty")

    direct_moves: list[PieceMove] = get_direct_moves(board_state, row, col)
    jump_moves: list[PieceMove] = get_jump_moves(board_state, row, col)

    return direct_moves + jump_moves


def get_direct_moves(
    board_state: list[list[FieldState]], row: int, col: int
) -> list[PieceMove]:
    moves: list[PieceMove] = []

    for dx, dy in directions:
        adj_row = row + dy
        adj_col = col + dx
        if (
            is_within_bounds(board_state, adj_row, adj_col)
            and board_state[adj_row][adj_col] == FieldState.EMPTY
        ):
            moves.append(PieceMove((row, col), (adj_row, adj_col)))

    return moves


def get_jump_moves(
    board_state: list[list[FieldState]], row: int, col: int
) -> list[PieceMove]:
    moves: list[PieceMove] = []

    to_visit: Queue[tuple[int, int]] = Queue()
    visited: set[tuple[int, int]] = set()

    to_visit.put((row, col))
    visited.add((row, col))

    while not to_visit.empty():
        curr_field = to_visit.get()

        for dx, dy in directions:
            adj_row = curr_field[0] + dy
            adj_col = curr_field[1] + dx
            if (
                not is_within_bounds(board_state, adj_row, adj_col)
                or board_state[adj_row][adj_col] == FieldState.EMPTY
            ):
                continue

            jump_row = adj_row + dy
            jump_col = adj_col + dx
            if (
                not is_within_bounds(board_state, jump_row, jump_col)
                or board_state[jump_row][jump_col] != FieldState.EMPTY
            ):
                continue

            if (jump_row, jump_col) not in visited:
                visited.add((jump_row, jump_col))
                to_visit.put((jump_row, jump_col))
                moves.append(PieceMove((row, col), (jump_row, jump_col)))

    return moves


def is_within_bounds(board_state: list[list[FieldState]], row: int, col: int) -> bool:
    return row >= 0 and row < len(board_state) and col >= 0 and col < len(board_state)
