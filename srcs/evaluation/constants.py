"""
Define constants used in Gomoku heuristic evaluation.

This module provides stone pattern scores, capture patterns,
and capture scores for evaluating candidate moves and board states.

Notation:
    1: Own stone.
    0: Empty intersection.
   -1: Opponent's stone or board boundary.
"""

STONE_PATTERN_SCORES: dict[tuple[int, ...], int] = {
    # Five
    (1, 1, 1, 1, 1): 1_000_000,

    # Free Four
    (0, 1, 1, 1, 1, 0): 100_000,

    # Closed Four
    (-1, 1, 1, 1, 1, 0): 10_000,
    (0, 1, 1, 1, 1, -1): 10_000,

    # Broken Four
    (1, 0, 1, 1, 1): 10_000,
    (1, 1, 0, 1, 1): 10_000,
    (1, 1, 1, 0, 1): 10_000,

    # Free Three
    (0, 0, 1, 1, 1, 0): 1_000,
    (0, 1, 1, 1, 0, 0): 1_000,

    # Broken Free Three
    (0, 1, 0, 1, 1, 0): 1_000,
    (0, 1, 1, 0, 1, 0): 1_000,

    # Closed Three
    (-1, 1, 1, 1, 0, 0): 100,
    (0, 0, 1, 1, 1, -1): 100,

    # Free Two
    (0, 0, 1, 1, 0, 0): 50,

    # Closed Two
    (-1, 1, 1, 0, 0, 0): 10,
    (0, 0, 0, 1, 1, -1): 10,
}

# Patterns that allow a player to capture an opponent's pair.
CAPTURE_PATTERNS: tuple[tuple[int, ...], ...] = (
    (0, -1, -1, 1),
    (1, -1, -1, 0),
)

# Heuristic scores based on the total number of captured stones.
CAPTURE_SCORES: dict[int, int] = {
    0: 0,
    2: 500,
    4: 2_000,
    6: 10_000,
    8: 100_000,
}

# Unique pattern lengths in descending order.
PATTERN_LENGTHS = tuple(
    sorted(
        {len(pattern) for pattern in STONE_PATTERN_SCORES},
        reverse=True,
    )
)

# Maximum distance required to detect stone patterns.
PATTERN_RADIUS = max(PATTERN_LENGTHS) - 1
