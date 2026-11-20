import os
import sys

# srcs ディレクトリをモジュールの検索パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
srcs_dir = os.path.abspath(os.path.join(current_dir, "../srcs"))
if srcs_dir not in sys.path:
    sys.path.append(srcs_dir)

import pygame

# 分離した board_loader / draw_board と update_board をインポート
from board_loader import load_board_and_captures
from draw_board import draw_board
from update_board import update_board

# --- Viewer Constants ---
FPS = 30
QUIT_KEYS = (pygame.K_ESCAPE, pygame.K_q)
DEFAULT_TEST_FILE = os.path.join(current_dir, "test_case.txt")
DEFAULT_MOVE = (9, 7)
DEFAULT_PLAYER = 1


# --- 状態切替テスト用ビューアクラス ---
class BoardUpdateTestViewer:
    def __init__(self, board_file_path, move, current_player=1):
        # 1. ファイルから初期ボードと取得石数を読み込む
        base_board, base_my_captured, base_opp_captured = load_board_and_captures(
            board_file_path
        )

        self.old_board = base_board
        self.old_my_captured = base_my_captured
        self.old_opponent_captured = base_opp_captured

        self.move = move
        self.current_player = current_player

        # 2. update_board を呼び出して更新後のボードと新規取得数を計算
        self.new_board, newly_captured = update_board(
            self.old_board, self.move, self.current_player
        )

        if self.current_player == 1:
            self.new_my_captured = self.old_my_captured + newly_captured
            self.new_opponent_captured = self.old_opponent_captured
        else:
            self.new_my_captured = self.old_my_captured
            self.new_opponent_captured = self.old_opponent_captured + newly_captured

        self.is_updated_view = False

    def draw(self):
        if self.is_updated_view:
            draw_board(
                self.new_board,
                self.new_my_captured,
                self.new_opponent_captured,
            )
        else:
            draw_board(
                self.old_board,
                self.old_my_captured,
                self.old_opponent_captured,
            )

    def toggle_view(self):
        self.is_updated_view = not self.is_updated_view
        state_label = "NEW (更新後)" if self.is_updated_view else "OLD (更新前)"
        print(f"状態切り替え -> {state_label}")

    def run(self):
        clock = pygame.time.Clock()
        running = True

        print("\n--- 操作方法 ---")
        print("[SPACE キー] または [画面クリック]: 更新前(OLD) と 更新後(NEW) を切り替え")
        print("[ESC / Q キー]           : 終了\n")

        self.draw()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in QUIT_KEYS:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.toggle_view()
                        self.draw()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.toggle_view()
                        self.draw()

            clock.tick(FPS)

        pygame.quit()
        sys.exit()


# --- 実行メイン ---
if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEST_FILE

    try:
        tester = BoardUpdateTestViewer(
            board_file_path=target_file,
            move=DEFAULT_MOVE,
            current_player=DEFAULT_PLAYER,
        )
        tester.run()
    except FileNotFoundError:
        print(f"'{target_file}' が見つかりませんでした。ファイルの配置を確認してください。")