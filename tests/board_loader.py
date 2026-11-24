import os
import sys

# srcs ディレクトリをモジュールの検索パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
srcs_dir = os.path.abspath(os.path.join(current_dir, "../srcs"))
sys.path.append(srcs_dir)

import numpy as np
import pygame

# 分離した draw_board をインポート
from draw_board import draw_board

# --- Parser Constants ---
BOARD_SIZE = 19
HEADER_LINE_COUNT = 2
BOARD_DTYPE = int
DEFAULT_FILE_NAME = os.path.join(current_dir, "test_case.txt")

# --- Tester Constants ---
TEST_FPS = 30
TEST_QUIT_KEYS = (pygame.K_ESCAPE, pygame.K_q)


def _resolve_input_path(file_path):
    if os.path.exists(file_path):
        return file_path
    fallback_path = os.path.join(current_dir, file_path)
    if os.path.exists(fallback_path):
        return fallback_path
    return file_path


def load_board_and_captures(file_path):
    """Read capture counts and a 19x19 board from a text file.

    Expected file format:
        Line 1: my_captured (int)
        Line 2: opponent_captured (int)
        Remaining 19 non-empty lines: 19 space-separated ints each

    Returns:
        tuple[np.ndarray, int, int]: (board, my_captured, opponent_captured)
    """
    target_path = _resolve_input_path(file_path)

    with open(target_path, "r", encoding="utf-8") as f:
        non_empty_lines = [line.strip() for line in f if line.strip()]

    if len(non_empty_lines) < HEADER_LINE_COUNT + BOARD_SIZE:
        raise ValueError(
            f"Expected at least {HEADER_LINE_COUNT + BOARD_SIZE} non-empty lines, "
            f"got {len(non_empty_lines)} in '{target_path}'."
        )

    my_captured = int(non_empty_lines[0])
    opponent_captured = int(non_empty_lines[1])

    grid_lines = non_empty_lines[HEADER_LINE_COUNT : HEADER_LINE_COUNT + BOARD_SIZE]
    rows = []
    for row_idx, line in enumerate(grid_lines):
        values = [int(token) for token in line.split()]
        if len(values) != BOARD_SIZE:
            raise ValueError(
                f"Row {row_idx} in '{target_path}' has {len(values)} columns; expected {BOARD_SIZE}."
            )
        rows.append(values)

    board = np.array(rows, dtype=BOARD_DTYPE)
    return board, my_captured, opponent_captured


if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME
    board, my_captured, opponent_captured = load_board_and_captures(file_arg)

    draw_board(board, my_captured, opponent_captured)
    clock = pygame.time.Clock()
    running = True

    while running:
        updated = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in TEST_QUIT_KEYS:
                    running = False
                elif event.key == pygame.K_1:
                    my_captured = max(0, my_captured - 1)
                    updated = True
                elif event.key == pygame.K_2:
                    my_captured += 1
                    updated = True
                elif event.key == pygame.K_3:
                    opponent_captured = max(0, opponent_captured - 1)
                    updated = True
                elif event.key == pygame.K_4:
                    opponent_captured += 1
                    updated = True

        if updated:
            draw_board(board, my_captured, opponent_captured)

        clock.tick(TEST_FPS)

    pygame.quit()
    sys.exit()