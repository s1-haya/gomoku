from srcs.gomoku.game_state import GameState
from srcs.evaluation.pattern_detector import (
    detect_local_patterns,
    detect_board_patterns,
)


class HeuristicEvaluator:
    """Provide move and board heuristic evaluations."""

    def score_move(
        self,
        state: GameState,
        move: tuple[int, int],
        stone: int,
    ) -> float:
        """Evaluate the offensive and defensive value of a move."""
        board = state.board.copy()

        board[move] = stone
        attack_score = detect_local_patterns(board, move, stone)

        board[move] = -stone
        defense_score = detect_local_patterns(board, move, -stone)

        return float(attack_score + defense_score)

    def score_board(
        self,
        state: GameState,
        stone: int,
    ) -> float:
        """Evaluate the board from the given player's perspective."""
        own_score = detect_board_patterns(state.board, stone)
        opponent_score = detect_board_patterns(state.board, -stone)
        # print(
        #     f"Perspective: {stone}, "
        #     f"Own: {own_score}, "
        #     f"Opponent: {opponent_score}, "
        #     f"Evaluation: {own_score - opponent_score}"
        # )
        return float(own_score - opponent_score)