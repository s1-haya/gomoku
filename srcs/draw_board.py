import sys
import pygame
import numpy as np

# --- 1. テキストデータをパースして NumPy 配列にする関数 ---
def parse_board_from_text(text_data):
    """
    スペース区切りのテキストデータを 19x19 の 2次元 NumPy 配列に変換する
    """
    lines = text_data.strip().split('\n')
    board_list = []
    for line in lines:
        if line.strip().startswith('#') or not line.strip():
            continue
        row = [int(x) for x in line.strip().split()]
        if len(row) == 19:
            board_list.append(row)
            
    board_arr = np.array(board_list, dtype=int)
    if board_arr.shape != (19, 19):
        raise ValueError(f"ボード全体のサイズが 19x19 ではありません (現在: {board_arr.shape})")
        
    return board_arr


# --- 2. Pygame によるボード描画クラス ---
class GomokuViewer:
    def __init__(self, board_matrix, my_captured=0, opponent_captured=0, cell_size=40, margin=40):
        pygame.init()
        self.board = board_matrix
        self.my_captured = my_captured          # 自分の取得石数
        self.opponent_captured = opponent_captured  # 相手の取得石数
        self.cell_size = cell_size
        self.margin = margin
        
        # 19x19 碁盤の画面サイズ計算 (上部に情報表示用のエリアを 40px 確保)
        self.grid_size = 19
        board_pixel_size = self.cell_size * (self.grid_size - 1)
        self.width = board_pixel_size + self.margin * 2
        self.height = board_pixel_size + self.margin * 2 + 50  
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku Board with Visual Captures")
        
        self.font = pygame.font.SysFont(None, 32)
        
        # 色の定義 (RGB)
        self.COLOR_BOARD = (220, 179, 92)     # 碁盤の色
        self.COLOR_LINE = (0, 0, 0)           # 罫線の色
        self.COLOR_ME = (30, 30, 30)          # 自分 (黒)
        self.COLOR_OPPONENT = (240, 240, 240) # 相手 (白)
        self.COLOR_TEXT = (30, 30, 30)

    def draw_board(self):
        self.screen.fill(self.COLOR_BOARD)
        
        # --- 上部に「石のアイコン ＋ 数字」の形式で取得石数を描画 ---
        # 1. 自分の石アイコンとカウント
        my_icon_x = self.margin + 20
        my_icon_y = 25
        icon_radius = 12
        
        # 黒石アイコン（自分）
        pygame.draw.circle(self.screen, self.COLOR_ME, (my_icon_x, my_icon_y), icon_radius)
        
        # カウント文字列 (例: " : 4 / 10")
        my_text_surface = self.font.render(f" : {self.my_captured} / 10", True, self.COLOR_TEXT)
        self.screen.blit(my_text_surface, (my_icon_x + 15, my_icon_y - 10))

        # 2. 相手の石アイコンとカウント
        # 画面の右側半分に配置
        opp_icon_x = self.width // 2 + 40
        opp_icon_y = 25
        
        # 白石アイコン（相手）＋ 縁取り線
        pygame.draw.circle(self.screen, self.COLOR_OPPONENT, (opp_icon_x, opp_icon_y), icon_radius)
        pygame.draw.circle(self.screen, self.COLOR_LINE, (opp_icon_x, opp_icon_y), icon_radius, 1)
        
        # カウント文字列 (例: " : 2 / 10")
        opp_text_surface = self.font.render(f" : {self.opponent_captured} / 10", True, self.COLOR_TEXT)
        self.screen.blit(opp_text_surface, (opp_icon_x + 15, opp_icon_y - 10))

        # --- ボード描画のオフセット ---
        board_top_margin = self.margin + 30

        # 罫線の描画 (19x19)
        for i in range(self.grid_size):
            start_x = self.margin
            start_y = board_top_margin + i * self.cell_size
            end_x = self.margin + self.cell_size * (self.grid_size - 1)
            end_y = board_top_margin + i * self.cell_size
            pygame.draw.line(self.screen, self.COLOR_LINE, (start_x, start_y), (end_x, end_y), 1)
            
            start_x = self.margin + i * self.cell_size
            start_y = board_top_margin
            end_x = self.margin + i * self.cell_size
            end_y = board_top_margin + self.cell_size * (self.grid_size - 1)
            pygame.draw.line(self.screen, self.COLOR_LINE, (start_x, start_y), (end_x, end_y), 1)

        # 星（天元や星のポイント）を描画
        star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for r, c in star_points:
            x = self.margin + c * self.cell_size
            y = board_top_margin + r * self.cell_size
            pygame.draw.circle(self.screen, self.COLOR_LINE, (x, y), 4)

        # 盤上の石を描画
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                val = self.board[r, c]
                if val == 0:
                    continue
                
                x = self.margin + c * self.cell_size
                y = board_top_margin + r * self.cell_size
                radius = self.cell_size // 2 - 3
                
                if val == 1:  # 自分 (黒石)
                    pygame.draw.circle(self.screen, self.COLOR_ME, (x, y), radius)
                elif val == 2:  # 相手 (白石)
                    pygame.draw.circle(self.screen, self.COLOR_OPPONENT, (x, y), radius)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False

            self.draw_board()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


# --- 3. 実行メイン ---
if __name__ == "__main__":
    raw_board_text = """
    0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    """

    board_matrix = parse_board_from_text(raw_board_text)
    viewer = GomokuViewer(board_matrix, my_captured=4, opponent_captured=2)
    viewer.run()