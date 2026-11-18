import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
srcs_dir = os.path.abspath(os.path.join(current_dir, '../srcs'))
sys.path.append(srcs_dir)

from check_line import check_line
import numpy as np

# 19x19 の空ボードを作成し、横に5つ並べてみる
board = np.zeros((19, 19), dtype=int)
board[5, 2:6] = 1  # 5行目の2列目〜6列目にプレイヤー1の石を5つ配置

# 判定テスト
result = check_line(board, player=1)
print(f"Player 1 has 5-in-a-row? -> {result}")  # 期待値: True