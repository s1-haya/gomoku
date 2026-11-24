import numpy as np

from srcs.constants import DIRECTIONS
from srcs.evaluation.constants import (
    STONE_PATTERN_SCORES,
    PATTERN_LENGTHS,
    PATTERN_RADIUS,
)

def _extract_lines(
    board: np.ndarray,
    move: tuple[int, int],
    stone: int,
) -> tuple[tuple[int, ...], ...]:
    """Extract four directional lines around a given position.

    Args:
        board: Current board state.
        move: Center position as (row, col).
        stone: Stone representing the player's perspective.

    Returns:
        Four tuples representing horizontal, vertical,
        diagonal, and anti-diagonal lines.

        Values are normalized as follows:
            1: Own stone.
            0: Empty intersection.
           -1: Opponent's stone or board boundary.
    """
    rows, cols = board.shape
    row, col = move
    lines = []

    for dr, dc in DIRECTIONS:
        line = []

        for offset in range(-PATTERN_RADIUS, PATTERN_RADIUS + 1):
            r = row + dr * offset
            c = col + dc * offset

            if 0 <= r < rows and 0 <= c < cols:
                line.append(int(board[r, c]) * stone)
            else:
                line.append(-1)

        lines.append(tuple(line))

    return tuple(lines)


def _match_patterns(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Calculate the highest pattern score in each direction.

    Only patterns containing the center position are evaluated.

    Args:
        lines: Four normalized directional lines.

    Returns:
        The highest matching pattern score for each direction.
    """
    scores = []

    for line in lines:
        best_score = 0
        center = len(line) // 2

        for length in PATTERN_LENGTHS:
            start = max(0, center - length + 1)
            end = min(center, len(line) - length)

            for i in range(start, end + 1):
                pattern = line[i:i + length]
                score = STONE_PATTERN_SCORES.get(pattern, 0)

                best_score = max(best_score, score)

        scores.append(best_score)

    return tuple(scores)
