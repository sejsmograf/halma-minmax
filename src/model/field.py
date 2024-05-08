from enum import Enum


class FieldState(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __str__(self) -> str:
        representations = {
            FieldState.EMPTY: ".",
            FieldState.WHITE: "1",
            FieldState.BLACK: "2",
        }
        return representations[self]


def field_state_from_str(color_str: str) -> FieldState:
    if color_str == "0" or color_str == ".":
        return FieldState.EMPTY
    elif color_str == "1":
        return FieldState.WHITE
    elif color_str == "2":
        return FieldState.BLACK
    else:
        raise ValueError(f"Invalid color string: {color_str}")
