from srcs.player.basic import Player
from numpy import ndarray


class AIPlayer(Player):
    def get_move(self, board: ndarray) -> tuple[int, int]:
        pass