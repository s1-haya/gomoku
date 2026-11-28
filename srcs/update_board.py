import numpy as np


EMPTY_CELL = 0

CAPTURE_DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)


def update_board(
    board: np.ndarray,
    move: tuple[int, int],
    current_player: int = 1,
) -> tuple[np.ndarray, int]:
    """Place a stone and capture surrounded opponent pairs.

    Returns:
        A new board and the number of captured stones.
    """
    new_board = board.copy()
    rows, cols = board.shape
    row, col = move

    if current_player not in (1, -1):
        return new_board, 0

    if not (0 <= row < rows and 0 <= col < cols):
        return new_board, 0

    if new_board[row, col] != EMPTY_CELL:
        return new_board, 0

    new_board[row, col] = current_player

    opponent_player = -current_player
    captured = 0

    for dr, dc in CAPTURE_DIRECTIONS:
        r1, c1 = row + dr, col + dc
        r2, c2 = row + 2 * dr, col + 2 * dc
        r3, c3 = row + 3 * dr, col + 3 * dc

        if not (0 <= r3 < rows and 0 <= c3 < cols):
            continue

        if (
            new_board[r1, c1] == opponent_player
            and new_board[r2, c2] == opponent_player
            and new_board[r3, c3] == current_player
        ):
            new_board[r1, c1] = EMPTY_CELL
            new_board[r2, c2] = EMPTY_CELL
            captured += 2

    return new_board, captured
