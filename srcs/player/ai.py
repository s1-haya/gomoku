from srcs.player.basic import Player
from numpy import ndarray
from time import perf_counter
import numpy as np
from __future__ import annotations


class AIPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_move(self, board: ndarray) -> tuple[int, int]:
        """Choose the best move for the current board."""
        pass

    def _generate_candidates(
        self, board: ndarray
    ) -> list[tuple[int, int]]:
        """Generate promising legal moves."""
        pass

    def _order_candidates(
        self,
        board: ndarray,
        candidates: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """Sort candidate moves by their estimated priority."""
        pass

    def _evaluate(self, board: ndarray) -> float:
        """Evaluate the board from the AI's perspective."""
        pass

    def _minimax(
        self,
        board: ndarray,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """Search future moves using Minimax with alpha-beta pruning."""
        pass
