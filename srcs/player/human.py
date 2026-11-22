from srcs.player.basic import Player
from srcs.game_state import GameState


class HumanPlayer(Player):
    def get_move(self, game_state: GameState) -> tuple[int, int]:
        pass
