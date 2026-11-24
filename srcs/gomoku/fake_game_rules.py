
import numpy as np

from srcs.gomoku.game_state import GameState


class FakeGameRules:
    """Provide simplified Gomoku rules for testing Minimax.

    This class simulates basic stone placement without implementing
    the complete Gomoku rules. It allows AIPlayer to explore
    hypothetical game states independently of the actual GameRules.

    Supported:
        - Validate moves within the board boundaries.
        - Allow placing stones only on empty intersections.
        - Return a new GameState without modifying the original.

    Not supported:
        - Capturing opponent stones.
        - Double-three restrictions.
        - Winning conditions based on five consecutive stones.
        - Winning conditions based on captured stones.

    This class is intended only for testing and benchmarking.
    It must not be used to enforce rules in an actual game.
    """

    def is_legal_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> bool:
        """Check whether a stone can be placed at the given position.

        A move is considered legal if the stone value is valid,
        the position is within the board boundaries, and the
        target intersection is empty.

        Args:
            state: Current game state.
            move: Target position as (row, column).
            stone: Stone value (1 or -1).

        Returns:
            True if the move satisfies the simplified rules,
            otherwise False.
        """
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
        """Create a new game state after placing a stone.

        The board is copied before placing the stone so that
        the original GameState remains unchanged. Capture counts
        are preserved because capturing is not implemented.

        Args:
            state: Current game state.
            move: Target position as (row, column).
            stone: Stone value (1 or -1).

        Returns:
            A new GameState containing the updated board.

        Raises:
            ValueError: If the move violates the simplified rules.
        """
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
        """Return None because winning conditions are not implemented.

        This method exists to provide the same interface as the
        actual GameRules. It does not detect five-in-a-row or
        capture-based victories.

        Args:
            state: Game state to inspect.

        Returns:
            Always None, regardless of the board position.
        """
        return None

    def is_terminal(
        self,
        state: GameState,
    ) -> bool:
        """Check whether the board has no remaining empty positions.

        Unlike the actual Gomoku rules, this method does not
        consider winning conditions. A game is treated as
        finished only when the board is completely full.

        Args:
            state: Game state to inspect.

        Returns:
            True if every intersection is occupied,
            otherwise False.
        """
        return not np.any(state.board == 0)
