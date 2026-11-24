from abc import ABC, abstractmethod
from srcs.gomoku.game_state import GameState


class Player(ABC):
    def __init__(self):
        self._captured_stones: int = 0
        self._is_five: bool = False

    @abstractmethod
    def get_move(self, game_state: GameState) -> tuple[int, int]:
        """
        Select a position for the player's next move.

        Args:
            game_state: the state Gomoku Game required.

        Returns:
            A tuple (row, col) representing the selected position.

        Note:
            This method does not validate or update the board.
            Gomoku is responsible for validating and applying moves.
        """
        pass

    @property
    def captured_stones(self) -> int:
        """Get the number of captured opponent stones."""
        return self._captured_stones

    @captured_stones.setter
    def captured_stones(self, count: int) -> None:
        """Set the number of captured opponent stones."""
        if count < 0:
            raise ValueError("Captured stones cannot be negative.")
        self._captured_stones = count

    @property
    def is_five(self) -> bool:
        """Get the player's five-in-a-row status."""
        return self._is_five

    @is_five.setter
    def is_five(self, value: bool) -> None:
        """Set the player's five-in-a-row status."""
        if not isinstance(value, bool):
            raise TypeError("is_five must be a boolean.")
        self._is_five = value
