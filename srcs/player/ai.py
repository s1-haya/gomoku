from srcs.player.basic import Player
from srcs.game_state import GameState
from time import perf_counter
import numpy as np
from __future__ import annotations


class AIPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_move(self, game_state: GameState) -> tuple[int, int]:
        """Choose the best move for the current board."""
        pass

    def _generate_candidates(
        self, game_state: GameState
    ) -> list[tuple[int, int]]:
        """Generate promising legal moves."""
        pass

    def _order_candidates(
        self,
        game_state: GameState,
        candidates: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """Sort candidate moves by their estimated priority."""
        pass

    def _evaluate(self, game_state: GameState) -> float:
        """Evaluate the board from the AI's perspective."""
        pass

    def _minimax(
        self,
        game_state: GameState,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """Search future moves using Minimax with alpha-beta pruning."""
        pass
