# srcs/board_loader.py （または srcs/judge.py の一部としてもOK）
import numpy as np

def parse_board_from_text(text_data):
    """
    スペース区切りのテキストデータ（文字列）を 19x19 の 2次元 NumPy 配列に変換する
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


def parse_board_from_file(file_path):
    """
    指定されたファイルパスからファイルを読み込み、parse_board_from_text に渡す
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"エラー: ファイル '{file_path}' が見つかりませんでした。")
        
    return parse_board_from_text(text_data)