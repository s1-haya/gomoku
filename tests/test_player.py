
import unittest
import numpy as np

from srcs.player.basic import Player


class MockPlayer(Player):
    """Concrete implementation of Player for testing."""

    def get_move(self, board: np.ndarray) -> tuple[int, int]:
        return (9, 9)


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Create a new player before each test."""
        self.player = MockPlayer()

    def test_default_values(self):
        """Player attributes should have correct default values."""
        self.assertEqual(self.player.captured_stones, 0)
        self.assertFalse(self.player.is_five)

    def test_set_captured_stones(self):
        """Capture count should be updated correctly."""
        self.player.captured_stones = 4

        self.assertEqual(self.player.captured_stones, 4)

    def test_set_negative_captured_stones(self):
        """Negative capture counts should raise ValueError."""
        with self.assertRaises(ValueError):
            self.player.captured_stones = -1

        self.assertEqual(self.player.captured_stones, 0)

    def test_set_is_five_true(self):
        """is_five should accept True."""
        self.player.is_five = True

        self.assertTrue(self.player.is_five)

    def test_set_is_five_false(self):
        """is_five should accept False."""
        self.player.is_five = True
        self.player.is_five = False

        self.assertFalse(self.player.is_five)

    def test_set_is_five_invalid_type(self):
        """is_five should reject non-boolean values."""
        for value in (1, 0, "True", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    self.player.is_five = value

        self.assertFalse(self.player.is_five)

    def test_player_is_abstract(self):
        """Abstract Player cannot be instantiated."""
        with self.assertRaises(TypeError):
            Player()

    def test_get_move_is_required(self):
        """A subclass without get_move remains abstract."""

        class IncompletePlayer(Player):
            pass

        with self.assertRaises(TypeError):
            IncompletePlayer()

    def test_get_move(self):
        """get_move should return the mock position."""
        board = np.zeros((19, 19), dtype=np.int8)

        move = self.player.get_move(board)

        self.assertEqual(move, (9, 9))


if __name__ == "__main__":
    unittest.main()
