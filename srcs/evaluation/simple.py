
from srcs.gomoku.game_state import GameState


class SimpleMoveEvaluator:
    """Evaluate candidate moves using nearby stones and board position.

    This is a lightweight heuristic intended for initial AI testing
    and move ordering, rather than competitive Gomoku play.

    Scoring rules:
        - +2 for each adjacent friendly stone.
        - +1 for each adjacent opponent stone.
        - -0.01 per Manhattan distance from the board center.

    This evaluator does not consider captures, winning patterns,
    or threats that require immediate defense.
    """
    def score(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
        """Score a candidate move based on its eight neighbors and center distance.

		Args:
			state: Current game state before the move.
			move: Board position (row, column) to evaluate.
			stone: Player's stone value (1 or -1).

		Returns:
			A heuristic score; higher values indicate preferred moves.
		"""
        board = state.board
        row, col = move
        rows, cols = board.shape

        score = 0.0

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue

                r = row + dr
                c = col + dc

                if not (0 <= r < rows and 0 <= c < cols):
                    continue

                if board[r, c] == stone:
                    score += 2.0
                elif board[r, c] == -stone:
                    score += 1.0

        center_row = rows // 2
        center_col = cols // 2

        distance = (
            abs(row - center_row)
            + abs(col - center_col)
        )

        score -= distance * 0.01

        return score
