import sys
import numpy as np
import pygame

from srcs.board_renderer import (
    CAPTURE_GOAL,
    EMPTY_CELL,
    FPS,
    GRID_SIZE,
    STONE_ME,
    STONE_OPPONENT,
    BoardRenderer,
)
from srcs.check_line import check_line
from srcs.check_three_double import check_three_double
from srcs.update_board import update_board
from srcs.player.ai import AIPlayer
from srcs.gomoku.game_state import GameState
from srcs.gomoku.game_rules import GameRules


class Gomoku:
    def __init__(self) -> None:
        self.renderer = BoardRenderer()
        self.clock = pygame.time.Clock()
        self.rules = GameRules()
        self.ai = AIPlayer(stone=-1, rules=self.rules, debug=True)
        self.reset_game()

    def reset_game(self) -> None:
        """Reset all game state fields to their initial values."""
        self.board: np.ndarray = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.my_captured: int = 0
        self.opponent_captured: int = 0
        self.current_turn: int = STONE_ME
        self.last_move: tuple[int, int] | None = None
        self.winner: int | None = None

    @property
    def is_game_over(self) -> bool:
        return self.winner is not None

    @property
    def is_my_turn(self) -> bool:
        return (not self.is_game_over) and (self.current_turn == STONE_ME)

    @property
    def is_ai_turn(self) -> bool:
        return (not self.is_game_over) and (self.current_turn == STONE_OPPONENT)

    def can_place_at(self, row: int, col: int) -> bool:
        """Check bounds and whether the target cell is empty."""
        return (
            0 <= row < GRID_SIZE
            and 0 <= col < GRID_SIZE
            and self.board[row, col] == EMPTY_CELL
        )

    def apply_move(self, pos: tuple[int, int], player: int) -> None:
        """Apply a player's move, evaluate win/foul conditions, and switch turns."""
        opponent = STONE_OPPONENT if player == STONE_ME else STONE_ME

        new_board, captured = update_board(self.board, pos, current_player=player)
        self.board = new_board
        self.last_move = pos

        if player == STONE_ME:
            self.my_captured += captured
            total_captured = self.my_captured
        else:
            self.opponent_captured += captured
            total_captured = self.opponent_captured

        if total_captured >= CAPTURE_GOAL or check_line(self.board, player):
            self.winner = player
        elif check_three_double(self.board, player):
            self.winner = opponent
        else:
            self.current_turn = opponent

    def _get_hover_pos(self) -> tuple[int, int] | None:
        """Return the hovered grid cell only during the player's turn on an empty cell."""
        if not self.is_my_turn:
            return None
        candidate = self.renderer.pixel_to_grid(*pygame.mouse.get_pos())
        if candidate is not None and self.can_place_at(*candidate):
            return candidate
        return None

    def _handle_events(self) -> bool:
        """Process Pygame events and return False if the loop should exit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                return False
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.is_my_turn
            ):
                clicked = self.renderer.pixel_to_grid(*event.pos)
                if clicked is not None and self.can_place_at(*clicked):
                    self.apply_move(clicked, STONE_ME)
        return True

    def _get_status_text(self) -> str | None:
        """Return the banner text corresponding to the current winner, if any."""
        if self.winner == STONE_ME:
            return "You Win!"
        if self.winner == STONE_OPPONENT:
            return "AI Wins!"
        return None

    def _render_frame(self, hover_pos: tuple[int, int] | None) -> None:
        """Render the current board, scores, hover preview, and status banner."""
        self.renderer.render(
            board=self.board,
            my_captured=self.my_captured,
            opponent_captured=self.opponent_captured,
            hover_pos=hover_pos,
            hover_stone=STONE_ME,
            last_move=self.last_move,
            status_text=self._get_status_text(),
        )

    def _process_ai_turn(self) -> None:
        """Compute and apply the AI move if it is currently the AI's turn."""
        if not self.is_ai_turn:
            return

        game_state = GameState(
            self.board, (self.opponent_captured, self.my_captured)
        )
        ai_move = self.ai.get_move(game_state)
        if ai_move is not None:
            self.apply_move(ai_move, STONE_OPPONENT)
        else:
            self.winner = STONE_ME

    def main(self) -> None:
        running = True
        while running:
            hover_pos = self._get_hover_pos()
            running = self._handle_events()
            if not running:
                break

            self._render_frame(hover_pos)
            self._process_ai_turn()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()