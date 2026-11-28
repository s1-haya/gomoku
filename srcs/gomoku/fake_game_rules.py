
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
        """Detect five or more consecutive stones.
        
        This simplified implementation does not consider captures
        or capture-based exceptions to winning conditions.

        Args:
            state: Game state to inspect.

        Returns:
            The winning stone (1 or -1), or None if no winner exists.
        """
        board = state.board
        rows, cols = board.shape

        directions = (
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        )

        for row, col in np.argwhere(board != 0):
            stone = int(board[row, col])

            for dr, dc in directions:
                end_row = row + dr * 4
                end_col = col + dc * 4

                if not (
                    0 <= end_row < rows
                    and 0 <= end_col < cols
                ):
                    continue

                if all(
                    board[row + dr * i, col + dc * i] == stone
                    for i in range(1, 5)
                ):
                    print(
                        f"[WINNER] stone={stone}, "
                        f"start=({row}, {col}), "
                        f"end=({end_row}, {end_col}), "
                        f"direction=({dr}, {dc})"
                    )
                    return stone
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
        return (
            self.get_winner(state) is not None
            or not np.any(state.board == 0)
        )
