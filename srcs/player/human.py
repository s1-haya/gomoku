from srcs.player.basic import Player
from srcs.gomoku.game_state import GameState


class HumanPlayer(Player):
    def get_move(self, game_state: GameState) -> tuple[int, int]:
        pass
