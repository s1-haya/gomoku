
from typing import Protocol
from srcs.gomoku.game_state import GameState


class MoveEvaluator(Protocol):
    """Define the interface for evaluating candidate moves.

    Implementations assign a score to a potential move based on
    the current game state. Higher scores indicate more promising
    moves for the specified player.

    AIPlayer uses this interface to rank candidate moves without
    depending on a specific evaluation strategy.
    """
    def score(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
        """Score a candidate move for the given stone."""
