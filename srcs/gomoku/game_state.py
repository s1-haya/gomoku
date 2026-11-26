from dataclasses import dataclass
from numpy import ndarray


@dataclass(frozen=True)
class GameState:
    board: ndarray
    captures: tuple(int, int)
