from copy import deepcopy
from typing import NamedTuple, Optional
from queue import Queue

from .moves import PieceMove, get_player_moves
from .field import FieldState, field_state_from_str


class Board:
    BOARD_SIZE = 16
    INITIAL_ROW_WIDTH = 5

    # fmt: off
    PLAYER_GOALS = {
        FieldState.BLACK: (BOARD_SIZE-1, BOARD_SIZE-1),# bottom right
        FieldState.WHITE: (0, 0)
    }

    PLAYER_CORNERS = {
        FieldState.BLACK: (0, 0),
        FieldState.WHITE: (1,1)
    }

    CORNERS: dict[tuple[int,int], list[tuple[int,int]]] = {
        (0, 0): 
       [ (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
         (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
         (2, 0), (2, 1), (2, 2), (2, 3),
         (3, 0), (3, 1), (3, 2),
         (4, 0), (4, 1)],

        (1, 1): 
       [ (15, 15), (15, 14), (15, 13), (15, 12), (15, 11),
         (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
         (13, 15), (13, 14), (13, 13), (13, 12),
         (12, 15), (12, 14), (12, 13),
         (11, 15), (11, 14) ],
    }
    # fmt: on

    def __init__(self, board_state: Optional[str] = None) -> None:
        self.size = Board.BOARD_SIZE
        self.previous_move: Optional[PieceMove] = None

        if board_state is None:
            self.board_state = [
                [FieldState.EMPTY for _ in range(self.size)] for _ in range(self.size)
            ]
            self.__initialize_board()
        else:
            self.board_state = self.__parse_board_state(board_state)
            if self.__count_field_states(FieldState.BLACK) != self.__count_field_states(
                FieldState.WHITE
            ):
                raise ValueError("Not equal piece counts")

    def get_possible_moves(self, moving_player: FieldState) -> list[PieceMove]:
        return get_player_moves(self.board_state, moving_player)

    def make_move(self, move: PieceMove):
        self.previous_move = move
        from_row, from_col = move.from_field[0], move.from_field[1]
        to_row, to_col = move.to_field[0], move.to_field[1]

        self.board_state[to_row][to_col] = self.board_state[from_row][from_col]
        self.board_state[from_row][from_col] = FieldState.EMPTY

    def undo_previous_move(self):
        if self.previous_move is None:
            raise ValueError("Undo move called without previous move")

        move = self.previous_move
        from_row, from_col = move.from_field[0], move.from_field[1]
        to_row, to_col = move.to_field[0], move.to_field[1]
        self.board_state[from_row][from_col] = self.board_state[to_row][to_col]
        self.board_state[to_row][to_col] = FieldState.EMPTY

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
                count += self.board_state[i][j] == state
        return count

    def __parse_board_row(self, row: str) -> list[FieldState]:
        field_strings = row.split(" ")
        if len(field_strings) != self.size:
            raise ValueError(f"Invalid length for board row: {len(field_strings)}")

        return [field_state_from_str(s) for s in field_strings]

    def __initialize_board(self):
        self.__initialize_player(FieldState.BLACK)
        self.__initialize_player(FieldState.WHITE)

    def __initialize_player(self, field_state: FieldState) -> None:
        corner: tuple[int, int] = Board.PLAYER_CORNERS[field_state]
        fields = Board.CORNERS[corner]
        for field in fields:
            self.board_state[field[0]][field[1]] = field_state

    def print_board(self, board_state=None):
        if board_state is None:
            board_state = self.board_state
        for row in board_state:
            for field in row:
                print(field, end=" ")
            print()
