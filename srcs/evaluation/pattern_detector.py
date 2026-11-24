import numpy as np

from srcs.constants import DIRECTIONS
from srcs.evaluation.constants import (
    STONE_PATTERN_SCORES,
    PATTERN_LENGTHS,
    PATTERN_RADIUS,
)

def detect_board_patterns(
    board: np.ndarray,
    stone: int,
) -> int:
    """Calculate the total stone pattern score of the board.

    Each horizontal, vertical, and diagonal line is
    evaluated once.

    Args:
        board: Current board state.
        stone: Stone representing the player's perspective.

    Returns:
        Total stone pattern score for the specified player.
    """
    rows, cols = board.shape
    total_score = 0

    for dr, dc in DIRECTIONS:
        for row in range(rows):
            for col in range(cols):
                prev_row = row - dr
                prev_col = col - dc

                # Skip positions that are not line starting points.
                if (
                    0 <= prev_row < rows
                    and 0 <= prev_col < cols
                ):
                    continue

                line = []
                r, c = row, col

                while 0 <= r < rows and 0 <= c < cols:
                    line.append(int(board[r, c]) * stone)

                    r += dr
                    c += dc

                total_score += _score_full_line(tuple(line))

    return total_score

def detect_local_patterns(
    board: np.ndarray,
    move: tuple[int, int],
    stone: int,
) -> int:
    """Calculate the local pattern score around a position.

    Args:
        board: Current board state.
        move: Center position as (row, col).
        stone: Stone representing the player's perspective.

    Returns:
        Sum of the highest pattern scores in four directions.
    """
    lines = _extract_lines(board, move, stone)
    scores = _match_patterns(lines)

    return sum(scores)

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

def _score_full_line(line: tuple[int, ...]) -> int:
    """Calculate the pattern score of an entire line.

    Args:
        line: Normalized sequence of board intersections.

    Returns:
        Total score of selected non-overlapping stone patterns.
    """
    line = (-1,) + line + (-1,)
    matches = []

    for length in PATTERN_LENGTHS:
        for start in range(len(line) - length + 1):
            pattern = line[start:start + length]
            score = STONE_PATTERN_SCORES.get(pattern, 0)

            if score == 0:
                continue

            positions = {
                start + i
                for i, value in enumerate(pattern)
                if value == 1
            }

            matches.append((score, positions))

    matches.sort(key=lambda match: match[0], reverse=True)

    total_score = 0
    used_positions = set()

    for score, positions in matches:
        if used_positions.intersection(positions):
            continue

        total_score += score
        used_positions.update(positions)

    return total_score
