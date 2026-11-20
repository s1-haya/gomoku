import numpy as np

def check_line(board, player):
    board_arr = np.array(board, dtype=int)
    rows, cols = board_arr.shape
    
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (-1, 1)
    ]
    
    for r in range(rows):
        for c in range(cols):
            if board_arr[r, c] != player:
                continue
                
            for dr, dc in directions:
                count = 0
                for i in range(5):
                    nr, nc = r + dr * i, c + dc * i
                    if not (0 <= nr < rows and 0 <= nc < cols) or board_arr[nr, nc] != player:
                        break
                    count += 1
                
                if count >= 5:
                    return True
                    
    return False
