import numpy as np

def check_line(board, player):
    """
    指定されたプレイヤー（player: 1 または 2）の石が、
    ボード上に 5個以上連続して並んでいる箇所があるかをチェックする。
    
    チェックする4方向:
    - 横方向 (右)
    - 縦方向 (下)
    - 斜め右下方向 (右下)
    - 斜め右上方向 (右上)
    """
    board_arr = np.array(board, dtype=int)
    rows, cols = board_arr.shape
    
    # 探索する4つの方向（DR, DC）
    directions = [
        (0, 1),   # 横
        (1, 0),   # 縦
        (1, 1),   # 斜め右下
        (-1, 1)   # 斜め右上
    ]
    
    for r in range(rows):
        for c in range(cols):
            # 現在のマスが対象プレイヤーの石でなければスキップ
            if board_arr[r, c] != player:
                continue
                
            for dr, dc in directions:
                count = 0
                # 連続して何個同じ石が並んでいるか数える
                for i in range(5):  # まず5個連続するかチェック
                    nr, nc = r + dr * i, c + dc * i
                    # 盤面の範囲外、または違う色の石であれば終了
                    if not (0 <= nr < rows and 0 <= nc < cols) or board_arr[nr, nc] != player:
                        break
                    count += 1
                
                # 5個以上並んでいれば True を返す
                if count >= 5:
                    return True
                    
    return False