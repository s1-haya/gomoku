
from __future__ import annotations

from math import inf
from time import perf_counter

import numpy as np

from srcs.player.basic import Player
from srcs.gomoku.game_state import GameState
from srcs.evaluation.base import Evaluator
from srcs.evaluation.heuristic import HeuristicEvaluator
from srcs.search_debugger import SearchDebugger


class AIPlayer(Player):
    """Select Gomoku moves using Minimax with alpha-beta pruning.

    The AI searches possible future game states by alternating
    between its own moves (maximizing) and the opponent's moves
    (minimizing).

    Candidate moves are generated near existing stones and ordered
    using an interchangeable Evaluator. Game rules are provided
    externally, keeping the AI independent of rule implementations.

    The current board evaluation is a simple heuristic intended
    for initial testing and benchmarking, not competitive play.
    """
    def __init__(
        self,
        evaluator: Evaluator | None = None,
        *,
        rules=None,
        stone: int = 1,
        depth: int = 2,
        debug: bool = False,
    ):
        super().__init__()

        if stone not in (-1, 1):
            raise ValueError("stone must be 1 or -1")
        if depth < 1:
            raise ValueError("depth must be at least 1")

        self._evaluator = (
            evaluator if evaluator is not None
            else HeuristicEvaluator()
        )
        self._rules = rules
        self._stone = stone
        self._depth = depth
        self._debugger = SearchDebugger() if debug else None

    def get_move(self, game_state: GameState) -> tuple[int, int]:
        """Select the highest-scoring legal move using Minimax.

        Generate nearby candidate moves, filter out illegal moves,
        and order the remaining moves using the evaluator.

        Each candidate is simulated and searched to the configured
        depth. The move with the highest Minimax score is selected,
        assuming the opponent also plays optimally.

        The search uses alpha-beta pruning to skip branches that
        cannot improve the result.

        Args:
            game_state: Current board and capture counts.

        Returns:
            The selected move as (row, column).

        Raises:
            ValueError: If no rules object was provided or no legal
                candidate moves are available.
        """
        if self._rules is None:
            raise ValueError("GameRules must be provided")

        if self._debugger is not None:
            self._debugger.start()

        try:
            candidates = self._generate_candidates(game_state)
            candidates = [
                move for move in candidates
                if self._rules.is_legal_move(
                    game_state, move, self._stone
                )
            ]

            if not candidates:
                raise ValueError("No legal candidate moves")

            candidates = self._order_candidates(
                game_state, candidates, self._stone
            )

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

            if self._debugger is not None:
                self._debugger.record_result(
                    best_score, self._depth
                )

            return best_move

        finally:
            if self._debugger is not None:
                self._debugger.finish()
                self._debugger.print_stats()

    def _generate_candidates(
        self,
        game_state: GameState,
        radius: int = 2,
    ) -> list[tuple[int, int]]:
        """Generate empty positions near existing stones.

        Search within a square neighborhood around every occupied
        intersection, including stones belonging to both players.

        Duplicate positions and occupied intersections are excluded.
        Candidates are returned in sorted order for deterministic
        behavior.

        Args:
            game_state: Current game state.
            radius: Maximum row and column distance from each stone.
                Defaults to 2.

        Returns:
            A sorted list of unique empty positions as (row, column).
            Returns the board center if the board is empty.

        Note:
            This method does not check game-specific move restrictions.
            Legal moves must be filtered separately using GameRules.
        """
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
        """Sort candidate moves by their heuristic scores.

        Evaluate each candidate from the specified player's perspective
        and return moves in descending score order.

        Promising moves are searched first to improve the effectiveness
        of alpha-beta pruning.

        Args:
            game_state: Current game state.
            candidates: Candidate positions to order.
            stone: Player whose moves are being evaluated (1 or -1).

        Returns:
            A new list of candidate moves sorted from highest to
            lowest heuristic score.

        Note:
            Move ordering affects search efficiency but does not
            change the Minimax objective.
        """
        return sorted(
            candidates,
            key=lambda move: self._evaluator.score_move(
                game_state,
                move,
                stone,
            ),
            reverse=True,
        )

    def _evaluate(self, game_state: GameState) -> float:
        """Estimate the board's advantage from the AI's perspective.

        Generate nearby candidate moves and find the highest heuristic
        move score for both the AI and its opponent.

        The board score is calculated as:

            best_ai_move_score - best_opponent_move_score

        Positive values favor the AI, while negative values favor
        the opponent.

        Args:
            game_state: Game state to evaluate.

        Returns:
            The difference between the best available move scores.
            Returns 0.0 if no candidates are generated.

        Note:
            This is a temporary board evaluation heuristic.
            It does not directly evaluate winning patterns, captures,
            or immediate threats.
        """
        return self._evaluator.score_board(
            game_state, self._stone
        )

    def _minimax(
        self,
        game_state: GameState,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """Evaluate future game states using Minimax with alpha-beta pruning.

        Recursively simulate legal moves while alternating between
        maximizing (AI) and minimizing (opponent) turns.

        The search stops when a winner is detected, the game ends,
        or the remaining depth reaches zero.c Non-terminal leaf
        states are evaluated using the board heuristic.

        Alpha and beta track the best bounds found so far, allowing
        branches that cannot affect the final decision to be skipped.

        Args:
            game_state: Current game state at this search node.
            depth: Number of remaining plies to explore.
            maximizing: True for the AI's turn (MAX), False for
                the opponent's turn (MIN).
            alpha: Best score guaranteed to the maximizing player
                along the current search path.
            beta: Best score guaranteed to the minimizing player
                along the current search path.

        Returns:
            The Minimax score of the current state from the AI's
            perspective. Positive scores favor the AI; negative
            scores favor the opponent.

        Note:
            Terminal wins receive large positive or negative scores.
            The remaining depth is added to favor faster wins and
            slower losses.

            If no legal candidates are generated, the current
            implementation falls back to the heuristic evaluation.
        """
        if self._debugger is not None:
            self._debugger.record_node()

        winner = self._rules.get_winner(game_state)
        win_score = 1_000_000_000

        if winner == self._stone:
            return win_score + depth

        if winner == -self._stone:
            return -win_score - depth

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
                    if self._debugger is not None:
                        self._debugger.record_pruning()
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
                    if self._debugger is not None:
                        self._debugger.record_pruning()
                    break

            return best_score
