
from typing import Protocol
from srcs.gomoku.game_state import GameState


class MoveEvaluator(Protocol):
    def score(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
        """Score a candidate move for the given stone."""
