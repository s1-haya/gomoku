
from srcs.gomoku.game_state import GameState


class SimpleMoveEvaluator:
    def score(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
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
