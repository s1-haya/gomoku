import numpy as np

def update_board(board, move, current_player=1):
    new_board = np.array(board, dtype=int)
    r, c = move
    
    if new_board[r, c] != 0:
        return new_board, 0

    new_board[r, c] = current_player

    opponent_player = 2 if current_player == 1 else 1
    newly_captured = 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in directions:
        r1, c1 = r + dr, c + dc
        r2, c2 = r + 2 * dr, c + 2 * dc
        r3, c3 = r + 3 * dr, c + 3 * dc

        if (0 <= r1 < 19 and 0 <= c1 < 19 and
            0 <= r2 < 19 and 0 <= c2 < 19 and
            0 <= r3 < 19 and 0 <= c3 < 19):
            
            if (new_board[r1, c1] == opponent_player and
                new_board[r2, c2] == opponent_player and
                new_board[r3, c3] == current_player):
                
                new_board[r1, c1] = 0
                new_board[r2, c2] = 0
                newly_captured += 2

    return new_board, newly_captured