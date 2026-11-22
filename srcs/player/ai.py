
from __future__ import annotations

from math import inf
from time import perf_counter

import numpy as np

from srcs.player.basic import Player
from srcs.gomoku.game_state import GameState
from srcs.evaluation.base import MoveEvaluator
from srcs.evaluation.simple import SimpleMoveEvaluator


class AIPlayer(Player):
    def __init__(
        self,
        evaluator: MoveEvaluator | None = None,
        *,
        rules=None,
        stone: int = 1,
        depth: int = 2,
    ):
        super().__init__()

        if stone not in (-1, 1):
            raise ValueError("stone must be 1 or -1")
        if depth < 1:
            raise ValueError("depth must be at least 1")

        self._evaluator = (
            evaluator
            if evaluator is not None
            else SimpleMoveEvaluator()
        )
        self._rules = rules
        self._stone = stone
        self._depth = depth

        self.nodes = 0
        self.elapsed_time = 0.0

    def get_move(self, game_state: GameState) -> tuple[int, int]:
        """Choose the best move using Minimax."""
        if self._rules is None:
            raise ValueError("GameRules must be provided")

        start = perf_counter()
        self.nodes = 0

        candidates = self._generate_candidates(game_state)
        candidates = [
            move for move in candidates
            if self._rules.is_legal_move(
                game_state, move, self._stone
            )
        ]
        candidates = self._order_candidates(
            game_state, candidates, self._stone
        )

        if not candidates:
            raise ValueError("No legal candidate moves")

        best_move = candidates[0]
        best_score = -inf
        alpha = -inf
        beta = inf

        for move in candidates:
            next_state = self._rules.apply_move(
                game_state, move, self._stone
            )

            score = self._minimax(
                next_state,
                self._depth - 1,
                maximizing=False,
                alpha=alpha,
                beta=beta,
            )

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        self.elapsed_time = perf_counter() - start
        return best_move

    def _generate_candidates(
        self, game_state: GameState, radius: int = 2
    ) -> list[tuple[int, int]]:
        """Generate empty positions near existing stones."""
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
        stone: int,
    ) -> list[tuple[int, int]]:
        """Order candidates using the injected evaluator."""
        return sorted(
            candidates,
            key=lambda move: self._evaluator.score(
                game_state,
                move,
                stone,
            ),
            reverse=True,
        )

    def _evaluate(self, game_state: GameState) -> float:
        """Evaluate the board from the AI's perspective."""
        candidates = self._generate_candidates(game_state)

        if not candidates:
            return 0.0

        ai_score = max(
            self._evaluator.score(
                game_state, move, self._stone
            )
            for move in candidates
        )

        opponent_score = max(
            self._evaluator.score(
                game_state, move, -self._stone
            )
            for move in candidates
        )

        return float(ai_score - opponent_score)

    def _minimax(
        self,
        game_state: GameState,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """Search future moves using Minimax with alpha-beta pruning."""
        self.nodes += 1

        winner = self._rules.get_winner(game_state)

        if winner == self._stone:
            return 1_000_000 + depth

        if winner == -self._stone:
            return -1_000_000 - depth

        if self._rules.is_terminal(game_state):
            return 0.0

        if depth == 0:
            return self._evaluate(game_state)

        stone = self._stone if maximizing else -self._stone

        candidates = self._generate_candidates(game_state)
        candidates = [
            move for move in candidates
            if self._rules.is_legal_move(
                game_state, move, stone
            )
        ]
        candidates = self._order_candidates(
            game_state, candidates, stone
        )

        if not candidates:
            return self._evaluate(game_state)

        if maximizing:
            best_score = -inf

            for move in candidates:
                next_state = self._rules.apply_move(
                    game_state, move, stone
                )

                score = self._minimax(
                    next_state,
                    depth - 1,
                    maximizing=False,
                    alpha=alpha,
                    beta=beta,
                )

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break

            return best_score

        else:
            best_score = inf

            for move in candidates:
                next_state = self._rules.apply_move(
                    game_state, move, stone
                )

                score = self._minimax(
                    next_state,
                    depth - 1,
                    maximizing=True,
                    alpha=alpha,
                    beta=beta,
                )

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if alpha >= beta:
                    break

            return best_score
