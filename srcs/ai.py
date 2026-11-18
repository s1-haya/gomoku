from constants import BOARD_SIZE

def ai_move(board):
    """
    Finds the first available empty cell from top-left (AI logic).
    """
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                return x, y
    return None, None