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
from srcs.gomoku.fake_game_rules import FakeGameRules


def can_place_at(board: np.ndarray, row: int, col: int) -> bool:
    """Check only bounds and whether the cell is empty."""
    return (
        0 <= row < GRID_SIZE
        and 0 <= col < GRID_SIZE
        and board[row, col] == EMPTY_CELL
    )


def dummy_ai_move(board: np.ndarray) -> tuple[int, int] | None:
    """Simple placeholder AI: returns the first empty cell found."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if can_place_at(board, r, c):
                return (r, c)
    return None


def main() -> None:
    renderer = BoardRenderer()
    clock = pygame.time.Clock()

    def reset_game():
        return {
            "board": np.zeros((GRID_SIZE, GRID_SIZE), dtype=int),
            "my_captured": 0,
            "opponent_captured": 0,
            "current_turn": STONE_ME,
            "last_move": None,
            "winner": None,
        }

    state = reset_game()
    rules = FakeGameRules()
    ai: AIPlayer = AIPlayer(stone=-1, rules=rules, debug=True)

    running = True
    while running:
        game_over = state["winner"] is not None
        is_my_turn = (not game_over) and (state["current_turn"] == STONE_ME)

        # 1. Hover preview (only on player's turn and empty cell)
        hover_pos = None
        if is_my_turn:
            candidate = renderer.pixel_to_grid(*pygame.mouse.get_pos())
            if candidate is not None and can_place_at(state["board"], *candidate):
                hover_pos = candidate

        # 2. Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_my_turn:
                    clicked = renderer.pixel_to_grid(*event.pos)
                    if clicked is not None and can_place_at(state["board"], *clicked):
                        new_board, captured = update_board(
                            state["board"], clicked, current_player=STONE_ME
                        )
                        state["board"] = new_board
                        state["my_captured"] += captured
                        state["last_move"] = clicked

                        if state["my_captured"] >= CAPTURE_GOAL or check_line(
                            state["board"], STONE_ME
                        ):
                            state["winner"] = STONE_ME
                        elif check_three_double(state["board"], STONE_ME):
                        # elif check_three_double(state["board"], STONE_OPPONENT):
                            state["winner"] = STONE_OPPONENT
                        else:
                            state["current_turn"] = STONE_OPPONENT

        # 3. Status banner text
        status_text = None
        if state["winner"] == STONE_ME:
            status_text = "You Win!"
        elif state["winner"] == STONE_OPPONENT:
            status_text = "AI Wins!"

        # 4. Render frame
        renderer.render(
            board=state["board"],
            my_captured=state["my_captured"],
            opponent_captured=state["opponent_captured"],
            hover_pos=hover_pos,
            hover_stone=STONE_ME,
            last_move=state["last_move"],
            status_text=status_text,
        )

        # 5. AI move after rendering
        if (not game_over) and (state["current_turn"] == STONE_OPPONENT):
            game_state = GameState(state["board"], (state["opponent_captured"], state["my_captured"]))
            ai_move = ai.get_move(game_state)
            # ai_move = dummy_ai_move(state["board"])
            if ai_move is not None:
                new_board, captured = update_board(
                    state["board"], ai_move, current_player=STONE_OPPONENT
                )
                state["board"] = new_board
                state["opponent_captured"] += captured
                state["last_move"] = ai_move

                if state["opponent_captured"] >= CAPTURE_GOAL or check_line(
                    state["board"], STONE_OPPONENT
                ):
                    state["winner"] = STONE_OPPONENT
                elif check_three_double(state["board"], STONE_OPPONENT):
                    state["winner"] = STONE_ME
                else:
                    state["current_turn"] = STONE_ME
            else:
                state["winner"] = STONE_ME

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()