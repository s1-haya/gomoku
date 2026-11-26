from typing import Protocol
from srcs.gomoku.game_state import GameState


class Evaluator(Protocol):
    """Define the interface for move and board evaluation.

    Implementations provide two types of heuristic evaluation:

    - Move evaluation ranks candidate moves by their potential value.
    - Board evaluation estimates the advantage of a game state
      from the specified player's perspective.

    AIPlayer uses this interface without depending on a specific
    evaluation strategy.
    """

    def score_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
        """Score a candidate move for the given stone."""

    def score_board(
        self,
        state: GameState,
        stone: int,
    ) -> float:
        """Evaluate the board from the given player's perspective."""
