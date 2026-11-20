import pygame
import sys
import numpy as np

# --- Board & Layout Constants ---
GRID_SIZE = 19
CELL_SIZE = 40
MARGIN = 40
BOARD_TOP_OFFSET = 45
EXTRA_HEIGHT = 70
CAPTURE_GOAL = 10

STATUS_POS = (MARGIN, 10)
ICON_RADIUS = 10
MY_ICON_POS = (MARGIN + 20, 40)
OPP_ICON_Y = 40
OPP_ICON_OFFSET_X = 20
COUNTER_TEXT_OFFSET = (15, -10)
STONE_RADIUS_PADDING = 3
STAR_RADIUS = 4
LINE_WIDTH = 1
FONT_SIZE = 28
WINDOW_TITLE = "19x19 Board Viewer"

EMPTY_CELL = 0
STONE_ME = 1
STONE_OPPONENT = 2

STAR_POINTS = (
    (3, 3), (3, 9), (3, 15),
    (9, 3), (9, 9), (9, 15),
    (15, 3), (15, 9), (15, 15),
)

# --- Color Palette ---
COLOR_BOARD = (220, 179, 92)
COLOR_LINE = (0, 0, 0)
COLOR_ME = (30, 30, 30)
COLOR_OPPONENT = (240, 240, 240)
COLOR_TEXT = (30, 30, 30)


def draw_board(board, my_captured, opponent_captured):
    """Render a 19x19 board with captured stone counts for me and opponent."""
    board_pixel_size = CELL_SIZE * (GRID_SIZE - 1)
    width = board_pixel_size + MARGIN * 2
    height = board_pixel_size + MARGIN * 2 + EXTRA_HEIGHT

    if not pygame.get_init():
        pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    font = pygame.font.SysFont(None, FONT_SIZE)

    screen.fill(COLOR_BOARD)

    # Captured stone counters
    my_x, my_y = MY_ICON_POS
    pygame.draw.circle(screen, COLOR_ME, (my_x, my_y), ICON_RADIUS)
    my_label = font.render(f" : {my_captured} / {CAPTURE_GOAL}", True, COLOR_TEXT)
    screen.blit(my_label, (my_x + COUNTER_TEXT_OFFSET[0], my_y + COUNTER_TEXT_OFFSET[1]))

    opp_x = width // 2 + OPP_ICON_OFFSET_X
    opp_y = OPP_ICON_Y
    pygame.draw.circle(screen, COLOR_OPPONENT, (opp_x, opp_y), ICON_RADIUS)
    pygame.draw.circle(screen, COLOR_LINE, (opp_x, opp_y), ICON_RADIUS, LINE_WIDTH)
    opp_label = font.render(f" : {opponent_captured} / {CAPTURE_GOAL}", True, COLOR_TEXT)
    screen.blit(opp_label, (opp_x + COUNTER_TEXT_OFFSET[0], opp_y + COUNTER_TEXT_OFFSET[1]))

    board_top = MARGIN + BOARD_TOP_OFFSET

    # Grid lines
    for i in range(GRID_SIZE):
        y = board_top + i * CELL_SIZE
        pygame.draw.line(screen, COLOR_LINE, (MARGIN, y), (MARGIN + board_pixel_size, y), LINE_WIDTH)

        x = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, COLOR_LINE, (x, board_top), (x, board_top + board_pixel_size), LINE_WIDTH)

    # Star points
    for r, c in STAR_POINTS:
        sx = MARGIN + c * CELL_SIZE
        sy = board_top + r * CELL_SIZE
        pygame.draw.circle(screen, COLOR_LINE, (sx, sy), STAR_RADIUS)

    # Stones
    stone_radius = CELL_SIZE // 2 - STONE_RADIUS_PADDING
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            if val == EMPTY_CELL:
                continue

            cx = MARGIN + c * CELL_SIZE
            cy = board_top + r * CELL_SIZE

            if val == STONE_ME:
                pygame.draw.circle(screen, COLOR_ME, (cx, cy), stone_radius)
            elif val == STONE_OPPONENT:
                pygame.draw.circle(screen, COLOR_OPPONENT, (cx, cy), stone_radius)
                pygame.draw.circle(screen, COLOR_LINE, (cx, cy), stone_radius, LINE_WIDTH)

    pygame.display.flip()
    return screen


TEST_FPS = 30
TEST_MY_CAPTURED = 3
TEST_OPPONENT_CAPTURED = 2
TEST_QUIT_KEYS = (pygame.K_ESCAPE, pygame.K_q)


def test_draw_board():
    """Run an interactive window to visually test draw_board(board, my_captured, opponent_captured)."""
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # Sample stones for visual verification
    board[3, 3] = STONE_ME
    board[3, 4] = STONE_ME
    board[3, 15] = STONE_OPPONENT
    board[4, 15] = STONE_OPPONENT
    board[9, 9] = STONE_ME
    board[15, 3] = STONE_OPPONENT
    board[15, 15] = STONE_ME

    my_captured = TEST_MY_CAPTURED
    opponent_captured = TEST_OPPONENT_CAPTURED

    draw_board(board, my_captured, opponent_captured)
    clock = pygame.time.Clock()
    running = True

    print("Controls:")
    print("  [1 / 2] : Adjust my captured count (- / +)")
    print("  [3 / 4] : Adjust opponent captured count (- / +)")
    print("  [ESC/Q] : Quit")

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


if __name__ == "__main__":
    test_draw_board()