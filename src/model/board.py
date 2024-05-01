from typing import NamedTuple, Optional
from queue import Queue
from .field import FieldState, field_state_from_str


class PieceMove(NamedTuple):
    from_field: tuple[int, int]
    to_field: tuple[int, int]


class Board:
    BOARD_SIZE = 16
    INITIAL_ROW_WIDTH = 5

    # fmt: off
    CORNERS: dict[tuple[int,int], list[tuple[int,int]]] = { (0,0): 
       [ (15, 15), (15, 14), (15, 13), (15, 12), (15, 11),
         (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
         (13, 15), (13, 14), (13, 13), (13, 12),
         (12, 15), (12, 14), (12, 13),
         (11, 15), (11, 14) ],
        (1,1): 
       [ (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
         (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
         (2, 0), (2, 1), (2, 2), (2, 3),
         (3, 0), (3, 1), (3, 2),
         (4, 0), (4, 1)]}

    directions = [ (-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1), ]
    # fmt: on

    def __init__(self, board_state: Optional[str] = None) -> None:
        self.size = Board.BOARD_SIZE

        if board_state is None:
            self.board = [
                [FieldState.EMPTY for _ in range(self.size)] for _ in range(self.size)
            ]
            self.__initialize_board()
        else:
            self.board = self.__parse_board_state(board_state)
            if self.__count_field_states(FieldState.BLACK) != self.__count_field_states(
                FieldState.WHITE
            ):
                raise ValueError("Not equal piece counts")

    def get_player_moves(self, player_field: FieldState) -> list[PieceMove]:
        all_moves: list[PieceMove] = []

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == player_field:
                    all_moves += self.__get_piece_moves(row, col)

        return all_moves

    def __parse_board_state(self, board_state: str) -> list[list[FieldState]]:
        board_state_rows: list[str] = board_state.splitlines()

        if len(board_state_rows) != self.size:
            raise ValueError(
                f"Invalid board state passed: Row count of {len(board_state_rows)} is not equal to board size"
            )

        board_result: list[list[FieldState]] = []
        for row in board_state_rows:
            board_result.append(self.__parse_board_row(row))

        return board_result

    def __count_field_states(self, state: FieldState) -> int:
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                count += self.board[i][j] == state
        return count

    def __parse_board_row(self, row: str) -> list[FieldState]:
        field_strings = row.split(" ")
        if len(field_strings) != self.size:
            raise ValueError(f"Invalid length for board row: {len(field_strings)}")

        return [field_state_from_str(s) for s in field_strings]

    def __get_piece_moves(self, row: int, col: int) -> list[PieceMove]:
        if self.board[row][col] == FieldState.EMPTY:
            raise ValueError(f"FieldState at {row, col} is empty")

        adjacent_moves: list[PieceMove] = self.__get_adjacent_moves(row, col)
        jump_moves: list[PieceMove] = self.__get_jump_moves(row, col)

        return adjacent_moves + jump_moves

    def __get_adjacent_moves(self, row: int, col: int) -> list[PieceMove]:
        moves: list[PieceMove] = []

        for dx, dy in Board.directions:
            adj_row = row + dy
            adj_col = col + dx
            if (
                self.__is_within_bounds(adj_row, adj_col)
                and self.board[adj_row][adj_col] == FieldState.EMPTY
            ):
                moves.append(PieceMove((row, col), (adj_row, adj_col)))

        return moves

    def __get_jump_moves(self, row: int, col: int) -> list[PieceMove]:
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
                    not self.__is_within_bounds(adj_row, adj_col)
                    or self.board[adj_row][adj_col] == FieldState.EMPTY
                ):
                    continue

                jump_row = adj_row + dy
                jump_col = adj_col + dx
                if (
                    not self.__is_within_bounds(jump_row, jump_col)
                    or self.board[jump_row][jump_col] != FieldState.EMPTY
                ):
                    continue

                if (jump_row, jump_col) not in visited:
                    visited.add((jump_row, jump_col))
                    to_visit.put((jump_row, jump_col))
                    moves.append(PieceMove((row, col), (jump_row, jump_col)))

        return moves

    def __is_within_bounds(self, row: int, col: int) -> bool:
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def __initialize_board(self):
        self.__initialize_corner((0, 0), FieldState.BLACK)
        self.__initialize_corner((1, 1), FieldState.WHITE)

    def __initialize_corner(
        self, corner: tuple[int, int], field_state: FieldState
    ) -> None:
        fields = Board.CORNERS[corner]
        for field in fields:
            self.board[field[0]][field[1]] = field_state

    def print_board(self):
        for row in self.board:
            for field in row:
                print(field, end=" ")
            print()
