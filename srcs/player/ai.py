from __future__ import annotations
from srcs.player.basic import Player
from srcs.gomoku.game_state import GameState
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
        self, game_state: GameState, radius: int = 2
    ) -> list[tuple[int, int]]:
        """Generate empty positions within distance 2 of existing stones."""
        board = game_state.board
        rows, cols = board.shape

        stones = np.argwhere(board != 0)

        if len(stones) == 0:
            return [(rows // 2, cols // 2)]

        candidates = set()

        for row, col in stones:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    r = int(row + dr)
                    c = int(col + dc)

                    if not (0 <= r < rows and 0 <= c < cols):
                        continue

                    if board[r, c] != 0:
                        continue

                    candidates.add((r, c))

        return sorted(candidates)

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
