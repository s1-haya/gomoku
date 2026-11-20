import numpy as np

# --- Board & Rule Constants ---
BOARD_SIZE = 19
EMPTY = 0
DOUBLE_THREE_COUNT = 2
LIVE_THREE_LENGTH = 3

# 4 directions: horizontal, vertical, main diagonal, anti-diagonal
DIRECTIONS = (
    (0, 1),
    (1, 0),
    (1, 1),
    (1, -1),
)


def _in_bounds(row, col, size=BOARD_SIZE):
    return 0 <= row < size and 0 <= col < size


def _extract_line(board, start_r, start_c, dr, dc):
    """Extract a contiguous line starting at (start_r, start_c) in direction (dr, dc)."""
    cells = []
    coords = []
    r, c = start_r, start_c
    while _in_bounds(r, c, len(board)):
        cells.append(int(board[r][c]))
        coords.append((r, c))
        r += dr
        c += dc
    return cells, coords


def _find_open_threes_in_line(cells, coords, player):
    """Find open-three stone groups along a single 1D line.

    An open three here is a contiguous run of `LIVE_THREE_LENGTH` stones for `player`
    with an EMPTY cell immediately before and immediately after the run, and at least
    one further EMPTY cell on at least one side so it can form a live four.
    """
    found_groups = []
    n = len(cells)
    i = 0

    while i < n:
        if cells[i] != player:
            i += 1
            continue

        j = i
        while j < n and cells[j] == player:
            j += 1

        run_len = j - i
        if run_len == LIVE_THREE_LENGTH:
            has_left_open = (i - 1 >= 0) and (cells[i - 1] == EMPTY)
            has_right_open = (j < n) and (cells[j] == EMPTY)

            if has_left_open and has_right_open:
                can_extend_left = (i - 2 >= 0) and (cells[i - 2] == EMPTY)
                can_extend_right = (j + 1 < n) and (cells[j + 1] == EMPTY)
                if can_extend_left or can_extend_right:
                    found_groups.append(tuple(coords[i:j]))

        i = j

    return found_groups


def check_three_double(board, player):
    """Check whether `player` has at least two open threes (double-three) on `board`.

    Args:
        board: 19x19 grid (NumPy array or 2D list) with 0 (empty), 1 (me), 2 (opponent).
        player: Player ID to check (e.g., 1 or 2).

    Returns:
        bool: True if two or more open threes exist for `player`, else False.
    """
    rows = len(board)
    cols = len(board[0])
    open_three_groups = set()

    # Starting coordinates along top edge, left edge, and right edge (for anti-diagonal)
    starts = []
    for c in range(cols):
        starts.append((0, c, 1, 0))   # vertical down
        starts.append((0, c, 1, 1))   # diagonal down-right
        starts.append((0, c, 1, -1))  # diagonal down-left

    for r in range(rows):
        starts.append((r, 0, 0, 1))   # horizontal right
        if r > 0:
            starts.append((r, 0, 1, 1))       # diagonal down-right
            starts.append((r, cols - 1, 1, -1))  # diagonal down-left

    for sr, sc, dr, dc in starts:
        cells, coords = _extract_line(board, sr, sc, dr, dc)
        if len(cells) < LIVE_THREE_LENGTH + 2:
            continue
        groups = _find_open_threes_in_line(cells, coords, player)
        for group in groups:
            # Canonicalize stone coordinates so an intersection stone is tracked cleanly
            open_three_groups.add((dr, dc, group))

    return len(open_three_groups) >= DOUBLE_THREE_COUNT


