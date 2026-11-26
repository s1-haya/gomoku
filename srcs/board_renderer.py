import sys
import numpy as np
import pygame

# --- Board & Layout Constants ---
GRID_SIZE = 19
CELL_SIZE = 40
MARGIN = 40
BOARD_TOP_OFFSET = 45
EXTRA_HEIGHT = 70
CAPTURE_GOAL = 10

ICON_RADIUS = 10
MY_ICON_POS = (MARGIN + 20, 40)
OPP_ICON_Y = 40
OPP_ICON_OFFSET_X = 20
COUNTER_TEXT_OFFSET = (15, -10)
STONE_RADIUS_PADDING = 3
STAR_RADIUS = 4
LAST_MOVE_RADIUS = 5
HOVER_ALPHA = 110
LINE_WIDTH = 1
FONT_SIZE = 28
FPS = 30
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
COLOR_LAST_MOVE = (220, 50, 50)
COLOR_STATUS_BG = (255, 250, 230)


class BoardRenderer:
    """19x19 board renderer with capture counters, hover preview, and last-move marker."""

    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        self.board_pixel_size = CELL_SIZE * (GRID_SIZE - 1)
        self.width = self.board_pixel_size + MARGIN * 2
        self.height = self.board_pixel_size + MARGIN * 2 + EXTRA_HEIGHT
        self.board_top = MARGIN + BOARD_TOP_OFFSET
        self.stone_radius = CELL_SIZE // 2 - STONE_RADIUS_PADDING

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.board_bg = self._build_board_background()

    def _build_board_background(self) -> pygame.Surface:
        """Pre-render static board background, grid lines, and star points."""
        bg = pygame.Surface((self.width, self.height))
        bg.fill(COLOR_BOARD)

        board_right = MARGIN + self.board_pixel_size
        board_bottom = self.board_top + self.board_pixel_size

        for i in range(GRID_SIZE):
            y = self.board_top + i * CELL_SIZE
            pygame.draw.line(bg, COLOR_LINE, (MARGIN, y), (board_right, y), LINE_WIDTH)

            x = MARGIN + i * CELL_SIZE
            pygame.draw.line(bg, COLOR_LINE, (x, self.board_top), (x, board_bottom), LINE_WIDTH)

        for r, c in STAR_POINTS:
            sx, sy = self.grid_to_pixel(r, c)
            pygame.draw.circle(bg, COLOR_LINE, (sx, sy), STAR_RADIUS)

        return bg

    def grid_to_pixel(self, row: int, col: int) -> tuple[int, int]:
        """Convert grid coordinates (row, col) to screen pixel center (cx, cy)."""
        cx = MARGIN + col * CELL_SIZE
        cy = self.board_top + row * CELL_SIZE
        return cx, cy

    def pixel_to_grid(self, x: int, y: int) -> tuple[int, int] | None:
        """Convert screen pixel (x, y) to nearest grid intersection (row, col) if close enough."""
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - self.board_top) / CELL_SIZE)

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return None

        cx, cy = self.grid_to_pixel(row, col)
        max_dist = CELL_SIZE * 0.45
        if (x - cx) ** 2 + (y - cy) ** 2 > max_dist ** 2:
            return None

        return row, col

    def draw_counters(self, my_captured: int, opponent_captured: int) -> None:
        """Draw captured stone icons and counts at the top of the screen."""
        my_x, my_y = MY_ICON_POS
        pygame.draw.circle(self.screen, COLOR_ME, (my_x, my_y), ICON_RADIUS)
        my_label = self.font.render(f" : {my_captured} / {CAPTURE_GOAL}", True, COLOR_TEXT)
        self.screen.blit(my_label, (my_x + COUNTER_TEXT_OFFSET[0], my_y + COUNTER_TEXT_OFFSET[1]))

        opp_x = self.width // 2 + OPP_ICON_OFFSET_X
        opp_y = OPP_ICON_Y
        pygame.draw.circle(self.screen, COLOR_OPPONENT, (opp_x, opp_y), ICON_RADIUS)
        pygame.draw.circle(self.screen, COLOR_LINE, (opp_x, opp_y), ICON_RADIUS, LINE_WIDTH)
        opp_label = self.font.render(f" : {opponent_captured} / {CAPTURE_GOAL}", True, COLOR_TEXT)
        self.screen.blit(opp_label, (opp_x + COUNTER_TEXT_OFFSET[0], opp_y + COUNTER_TEXT_OFFSET[1]))

    def draw_stones(self, board: np.ndarray) -> None:
        """Draw placed stones on the board."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = board[r, c]
                if val == EMPTY_CELL:
                    continue

                cx, cy = self.grid_to_pixel(r, c)
                if val == STONE_ME:
                    pygame.draw.circle(self.screen, COLOR_ME, (cx, cy), self.stone_radius)
                elif val == STONE_OPPONENT:
                    pygame.draw.circle(self.screen, COLOR_OPPONENT, (cx, cy), self.stone_radius)
                    pygame.draw.circle(self.screen, COLOR_LINE, (cx, cy), self.stone_radius, LINE_WIDTH)

    def draw_hover(self, hover_pos: tuple[int, int] | None, stone_type: int = STONE_ME) -> None:
        """Draw a semi-transparent stone preview at the hovered grid intersection."""
        if hover_pos is None:
            return

        r, c = hover_pos
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
            return

        cx, cy = self.grid_to_pixel(r, c)
        size = self.stone_radius * 2 + 4
        hover_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        base_color = COLOR_ME if stone_type == STONE_ME else COLOR_OPPONENT
        rgba = (*base_color, HOVER_ALPHA)
        pygame.draw.circle(hover_surf, rgba, (center, center), self.stone_radius)
        if stone_type == STONE_OPPONENT:
            pygame.draw.circle(hover_surf, (*COLOR_LINE, HOVER_ALPHA), (center, center), self.stone_radius, LINE_WIDTH)

        self.screen.blit(hover_surf, (cx - center, cy - center))

    def draw_last_move(self, last_move: tuple[int, int] | None) -> None:
        """Draw a marker on the most recently placed stone."""
        if last_move is None:
            return

        r, c = last_move
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
            return

        cx, cy = self.grid_to_pixel(r, c)
        pygame.draw.circle(self.screen, COLOR_LAST_MOVE, (cx, cy), LAST_MOVE_RADIUS)

    def draw_status(self, status_text: str | None) -> None:
        """Draw an optional status/result banner near the bottom of the window."""
        if not status_text:
            return

        text_surf = self.font.render(status_text, True, COLOR_TEXT)
        pad_x, pad_y = 16, 8
        box_w = text_surf.get_width() + pad_x * 2
        box_h = text_surf.get_height() + pad_y * 2
        box_x = (self.width - box_w) // 2
        box_y = self.height - box_h - 12

        pygame.draw.rect(self.screen, COLOR_STATUS_BG, (box_x, box_y, box_w, box_h), border_radius=6)
        pygame.draw.rect(self.screen, COLOR_LINE, (box_x, box_y, box_w, box_h), LINE_WIDTH, border_radius=6)
        self.screen.blit(text_surf, (box_x + pad_x, box_y + pad_y))

    def render(
        self,
        board: np.ndarray,
        my_captured: int,
        opponent_captured: int,
        hover_pos: tuple[int, int] | None = None,
        hover_stone: int = STONE_ME,
        last_move: tuple[int, int] | None = None,
        status_text: str | None = None,
    ) -> None:
        """Render a full frame."""
        self.screen.blit(self.board_bg, (0, 0))
        self.draw_counters(my_captured, opponent_captured)
        self.draw_stones(board)
        self.draw_last_move(last_move)
        self.draw_hover(hover_pos, hover_stone)
        self.draw_status(status_text)
        pygame.display.flip()


def test_loop() -> None:
    """Continuous loop test for BoardRenderer with mouse hover and dummy placement."""
    renderer = BoardRenderer()
    clock = pygame.time.Clock()

    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    board[3, 3] = STONE_ME
    board[3, 15] = STONE_OPPONENT
    board[9, 9] = STONE_ME

    my_captured = 3
    opponent_captured = 2
    last_move: tuple[int, int] | None = (9, 9)
    status_text: str | None = "Hover test: Click empty cell to place dummy stone"

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_pos = renderer.pixel_to_grid(*mouse_pos)
        if hover_pos is not None and board[hover_pos] != EMPTY_CELL:
            hover_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_1:
                    my_captured = max(0, my_captured - 1)
                elif event.key == pygame.K_2:
                    my_captured += 1
                elif event.key == pygame.K_3:
                    opponent_captured = max(0, opponent_captured - 1)
                elif event.key == pygame.K_4:
                    opponent_captured += 1
                elif event.key == pygame.K_c:
                    status_text = None if status_text else "Test Banner Shown"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = renderer.pixel_to_grid(*event.pos)
                if clicked is not None and board[clicked] == EMPTY_CELL:
                    board[clicked] = STONE_ME
                    last_move = clicked

        renderer.render(
            board=board,
            my_captured=my_captured,
            opponent_captured=opponent_captured,
            hover_pos=hover_pos,
            hover_stone=STONE_ME,
            last_move=last_move,
            status_text=status_text,
        )
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    test_loop()