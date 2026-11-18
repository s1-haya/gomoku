import sys
import os

# srcs ディレクトリをモジュールの検索パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
srcs_dir = os.path.abspath(os.path.join(current_dir, '../srcs'))
sys.path.append(srcs_dir)

import pygame
import numpy as np

# 分離したボードローダーと update_board をインポート
from board_loader import parse_board_from_file
from update_board import update_board 


# --- 状態切替テスト用ビューアクラス ---
class BoardUpdateTestViewer:
    def __init__(self, board_file_path, move, current_player=1, my_captured=0, opponent_captured=0, cell_size=40, margin=40):
        pygame.init()
        
        # 1. 独立した関数を使ってファイルからボードを読み込む
        self.old_board = parse_board_from_file(board_file_path)
        self.move = move                    
        self.current_player = current_player  
        
        # 2. update_board 関数を呼び出して新しいボードと取得石数を計算
        self.new_board, newly_captured = update_board(self.old_board, self.move, self.current_player)
        
        # 取得石数の更新
        if self.current_player == 1:
            self.my_captured = my_captured + newly_captured
            self.opponent_captured = opponent_captured
        else:
            self.my_captured = my_captured
            self.opponent_captured = opponent_captured + newly_captured

        self.cell_size = cell_size
        self.margin = margin
        
        # 画面サイズ計算
        self.grid_size = 19
        board_pixel_size = self.cell_size * (self.grid_size - 1)
        self.width = board_pixel_size + self.margin * 2
        self.height = board_pixel_size + self.margin * 2 + 70  
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Update Board Test Viewer")
        
        self.font = pygame.font.SysFont(None, 28)
        self.is_updated_view = False

        # 色の定義
        self.COLOR_BOARD = (220, 179, 92)     
        self.COLOR_LINE = (0, 0, 0)           
        self.COLOR_ME = (30, 30, 30)          
        self.COLOR_OPPONENT = (240, 240, 240) 
        self.COLOR_TEXT = (30, 30, 30)
        self.COLOR_HIGHLIGHT = (200, 50, 50)  

    def draw(self):
        self.screen.fill(self.COLOR_BOARD)
        
        current_board = self.new_board if self.is_updated_view else self.old_board
        status_str = "Status: [NEW] After update_board()" if self.is_updated_view else "Status: [OLD] Before update_board() -> Press SPACE to update"
        
        status_surface = self.font.render(status_str, True, self.COLOR_TEXT)
        self.screen.blit(status_surface, (self.margin, 10))

        # アイコン＋カウント
        my_icon_x = self.margin + 20
        my_icon_y = 40
        icon_radius = 10
        pygame.draw.circle(self.screen, self.COLOR_ME, (my_icon_x, my_icon_y), icon_radius)
        my_text = self.font.render(f" : {self.my_captured} / 10", True, self.COLOR_TEXT)
        self.screen.blit(my_text, (my_icon_x + 15, my_icon_y - 10))

        opp_icon_x = self.width // 2 + 20
        opp_icon_y = 40
        pygame.draw.circle(self.screen, self.COLOR_OPPONENT, (opp_icon_x, opp_icon_y), icon_radius)
        pygame.draw.circle(self.screen, self.COLOR_LINE, (opp_icon_x, opp_icon_y), icon_radius, 1)
        opp_text = self.font.render(f" : {self.opponent_captured} / 10", True, self.COLOR_TEXT)
        self.screen.blit(opp_text, (opp_icon_x + 15, opp_icon_y - 10))

        board_top_margin = self.margin + 45

        # 罫線の描画
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

        # 星のポイントを描画
        star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for r, c in star_points:
            x = self.margin + c * self.cell_size
            y = board_top_margin + r * self.cell_size
            pygame.draw.circle(self.screen, self.COLOR_LINE, (x, y), 4)

        # 石の描画
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                val = current_board[r, c]
                if val == 0:
                    continue
                
                x = self.margin + c * self.cell_size
                y = board_top_margin + r * self.cell_size
                radius = self.cell_size // 2 - 3
                
                if val == 1:
                    pygame.draw.circle(self.screen, self.COLOR_ME, (x, y), radius)
                elif val == 2:
                    pygame.draw.circle(self.screen, self.COLOR_OPPONENT, (x, y), radius)

        if self.is_updated_view:
            mr, mc = self.move
            hx = self.margin + mc * self.cell_size
            hy = board_top_margin + mr * self.cell_size
            pygame.draw.circle(self.screen, self.COLOR_HIGHLIGHT, (hx, hy), 6, 2)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        print("\n--- 操作方法 ---")
        print("[SPACE キー] または [画面クリック]: 更新前(OLD) と 更新後(NEW) を切り替え")
        print("[ESC / Q キー]           : 終了\n")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.is_updated_view = not self.is_updated_view
                        print(f"状態切り替え -> {'NEW (更新後)' if self.is_updated_view else 'OLD (更新前)'}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.is_updated_view = not self.is_updated_view
                        print(f"状態切り替え -> {'NEW (更新後)' if self.is_updated_view else 'OLD (更新前)'}")

            self.draw()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


# --- 実行メイン ---
if __name__ == "__main__":
    target_file = os.path.join(current_dir, "../test_case.txt")
    test_move = (9, 7)  
    test_player = 1

    try:
        tester = BoardUpdateTestViewer(
            board_file_path=target_file, 
            move=test_move, 
            current_player=test_player, 
            my_captured=0, 
            opponent_captured=0
        )
        tester.run()
    except FileNotFoundError:
        print(f"'{target_file}' が見つかりませんでした。ファイルの配置を確認してください。")