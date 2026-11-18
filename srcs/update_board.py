import numpy as np

def update_board(board, move, current_player=1):
    """
    指定された指し手(move)をボードに反映し、必要であれば挟み取った石を除去（キャプチャ）して、
    新しいボードの状態と、今回新しく取得した石の数を返す。

    引数:
        board: np.ndarray または list の 19x19 の2次元配列 (0: 空き, 1: 自分, 2: 相手)
        move: tuple (r, c) 今回の指し手（行, 列）
        current_player: int 現在の手番プレイヤー (1: 自分, 2: 相手)

    戻り値:
        new_board: np.ndarray 更新後の新しい2次元ボード
        newly_captured: int 今回の指し手で新しく取得した石の数
    """
    # 元のボードを変更しないようにコピーを作成（NumPy配列として扱う）
    new_board = np.array(board, dtype=int)
    r, c = move
    
    # 1. 指し手が空きマスでなければそのまま返す（不正手などの安全ガード）
    if new_board[r, c] != 0:
        return new_board, 0

    # 2. 石を置く
    new_board[r, c] = current_player

    # 3. キャプチャ（挟み取り）の判定
    # 五目並べのキャプチャルール：「相手のペア（2個並び）」を自分の石で挟んだら取り除く
    opponent_player = 2 if current_player == 1 else 1
    newly_captured = 0

    # 8方向のベクトル (上下左右・斜めの全方向)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in directions:
        # 挟み取りのパターン: [自分] [相手] [相手] [自分]
        # 置いた場所から見て dr, dc の方向に相手が2個並び、その向こうが自分の石であるか確認
        r1, c1 = r + dr, c + dc
        r2, c2 = r + 2 * dr, c + 2 * dc
        r3, c3 = r + 3 * dr, c + 3 * dc

        # 盤面内にあるかチェック
        if (0 <= r1 < 19 and 0 <= c1 < 19 and
            0 <= r2 < 19 and 0 <= c2 < 19 and
            0 <= r3 < 19 and 0 <= c3 < 19):
            
            # パターンマッチング: 自分の石で相手の2個の石を挟んでいるか
            if (new_board[r1, c1] == opponent_player and
                new_board[r2, c2] == opponent_player and
                new_board[r3, c3] == current_player):
                
                # 挟んだ相手の2個の石を取り除く（0に戻す）
                new_board[r1, c1] = 0
                new_board[r2, c2] = 0
                newly_captured += 2

    return new_board, newly_captured