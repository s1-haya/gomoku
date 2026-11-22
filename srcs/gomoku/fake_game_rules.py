
import numpy as np

from srcs.gomoku.game_state import GameState


class FakeGameRules:
    """Minimal game rules for testing Minimax."""

    def is_legal_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> bool:
        """Check whether a move targets an empty intersection."""
        row, col = move
        rows, cols = state.board.shape

        return (
            stone in (1, -1)
            and 0 <= row < rows
            and 0 <= col < cols
            and state.board[row, col] == 0
        )

    def apply_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> GameState:
        """Return a new state after placing a stone."""
        if not self.is_legal_move(state, move, stone):
            raise ValueError(f"Illegal move: {move}")

        board = state.board.copy()

        row, col = move
        board[row, col] = stone

        return GameState(
            board=board,
            captures=state.captures,
        )

    def get_winner(
        self,
        state: GameState,
    ) -> int | None:
        """Return no winner (win detection is not implemented)."""
        return None

    def is_terminal(
        self,
        state: GameState,
    ) -> bool:
        """Return True only when the board is full."""
        return not np.any(state.board == 0)
