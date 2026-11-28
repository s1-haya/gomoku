import numpy as np

from srcs.gomoku.game_state import GameState
from srcs.check_line import check_line
from srcs.check_three_double import check_three_double
from srcs.update_board import update_board


CAPTURE_GOAL = 10
EMPTY_CELL = 0


class GameRules:
    """Manage move validation, captures and winning conditions."""

    def is_legal_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> bool:
        """Check whether a move satisfies the game rules."""
        row, col = move
        rows, cols = state.board.shape

        if not (
            stone in (1, -1)
            and 0 <= row < rows
            and 0 <= col < cols
            and state.board[row, col] == EMPTY_CELL
        ):
            return False

        board, _ = update_board(
            state.board.copy(),
            move,
            current_player=stone,
        )

        return not check_three_double(board, stone)

    def apply_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> GameState:
        """Return a new game state after applying a legal move."""
        if not self.is_legal_move(state, move, stone):
            raise ValueError(f"Illegal move: {move}")

        board, captured = update_board(
            state.board.copy(),
            move,
            current_player=stone,
        )

        black_captured, white_captured = state.captures

        if stone == 1:
            black_captured += captured
        else:
            white_captured += captured

        return GameState(
            board=board,
            captures=(black_captured, white_captured),
        )

    def get_winner(
        self,
        state: GameState,
    ) -> int | None:
        """Return the winning stone, or None if no winner exists."""
        black_captured, white_captured = state.captures

        if black_captured >= CAPTURE_GOAL:
            return 1

        if white_captured >= CAPTURE_GOAL:
            return -1

        if check_line(state.board, 1):
            return 1

        if check_line(state.board, -1):
            return -1

        return None

    def is_terminal(
        self,
        state: GameState,
    ) -> bool:
        """Check whether the game has ended."""
        return (
            self.get_winner(state) is not None
            or not np.any(state.board == EMPTY_CELL)
        )
