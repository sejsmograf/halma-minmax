from typing import NamedTuple
from enum import Enum
from queue import Queue


class Color(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __str__(self) -> str:
        representations = {Color.EMPTY: ".", Color.WHITE: "1", Color.BLACK: "2"}
        return representations[self]


class PieceMove(NamedTuple):
    from_field: tuple[int, int]
    to_field: tuple[int, int]


class Board:
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

    def __init__(self) -> None:
        self.size = 16
        self.board = [[Color.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()

    def get_piece_moves(self, row: int, col: int) -> list[PieceMove]:
        if self.board[row][col] == Color.EMPTY:
            return []

        adjacent_moves: list[PieceMove] = self.get_adjacent_moves(row, col)
        jump_moves: list[PieceMove] = self.get_jump_moves(row, col)

        return adjacent_moves + jump_moves

    def get_adjacent_moves(self, row: int, col: int) -> list[PieceMove]:
        moves: list[PieceMove] = []

        for dx, dy in Board.directions:
            adj_row = row + dy
            adj_col = col + dx
            if (
                self.is_within_bounds(adj_row, adj_col)
                and self.board[adj_row][adj_col] == Color.EMPTY
            ):
                moves.append(PieceMove((row, col), (adj_row, adj_col)))

        return moves

    def get_jump_moves(self, row: int, col: int) -> list[PieceMove]:
        moves: list[PieceMove] = []

        to_visit: Queue[tuple[int, int]] = Queue()
        visited: set[tuple[int, int]] = set()

        to_visit.put((row, col))
        visited.add((row, col))

        while not to_visit.empty():
            curr_field = to_visit.get()

            for dx, dy in Board.directions:
                adj_row = curr_field[0] + dy
                adj_col = curr_field[1] + dx
                if (
                    not self.is_within_bounds(adj_row, adj_col)
                    or self.board[adj_row][adj_col] == Color.EMPTY
                ):
                    continue

                jump_row = adj_row + dy
                jump_col = adj_col + dx
                if (
                    not self.is_within_bounds(jump_row, jump_col)
                    or self.board[jump_row][jump_col] != Color.EMPTY
                ):
                    continue

                if (jump_row, jump_col) not in visited:
                    visited.add((jump_row, jump_col))
                    to_visit.put((jump_row, jump_col))
                    moves.append(PieceMove((row, col), (jump_row, jump_col)))

        return moves

    def is_within_bounds(self, row: int, col: int) -> bool:
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def initialize_board(self):
        self.initialize_corner((0, 0), Color.BLACK)
        self.initialize_corner((1, 1), Color.WHITE)

    def initialize_corner(self, corner: tuple[int, int], color: Color) -> None:
        if corner not in ((0, 0), (0, 1), (1, 0), (1, 1)):
            raise ValueError(f"Invalid corner passed: {corner}")

        top_to_bottom: bool = corner[0] == 0
        left_to_right: bool = corner[1] == 0

        curr_row_width = 5
        start_row = 0 if top_to_bottom else self.size - 1
        start_col = 0 if left_to_right else self.size - 1

        for i in range(curr_row_width):
            col = start_col + i if left_to_right else start_col - i
            self.board[start_row][col] = color

        row = start_row
        while curr_row_width >= 2:
            row = row + 1 if top_to_bottom else row - 1
            for i in range(curr_row_width):
                col = start_col + i if left_to_right else start_col - i
                self.board[row][col] = color

            curr_row_width -= 1

    def print_board(self):
        for row in self.board:
            for field in row:
                print(field, end=" ")
            print()
