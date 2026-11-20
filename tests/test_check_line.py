import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
srcs_dir = os.path.abspath(os.path.join(current_dir, '../srcs'))
sys.path.append(srcs_dir)

from check_line import check_line
import numpy as np
import pygame
from board_loader import load_board_and_captures
from draw_board import draw_board
from update_board import update_board

TEST_FPS = 30
TEST_QUIT_KEYS = (pygame.K_ESCAPE, pygame.K_q)

if __name__ == "__main__":
    board, my_captured, opponent_captured = load_board_and_captures("test_case.txt")
    draw_board(board, my_captured, opponent_captured)
    # print(check_line(board,1))
    clock = pygame.time.Clock()
    running = True
    is_updated = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE and not is_updated:
                    # 次の盤面に更新して再描画
                    new_board, newly_captured = update_board(board, [10, 10], 1)
                    board, my_captured, opponent_captured = (
                        new_board,
                        my_captured + newly_captured,
                        opponent_captured,
                    )
                    draw_board(board, my_captured, opponent_captured)
                    is_updated = True

        clock.tick(30)

    pygame.quit()
    sys.exit()