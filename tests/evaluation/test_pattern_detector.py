"""Unit tests for Gomoku stone pattern detection."""

import unittest

import numpy as np

from srcs.evaluation.constants import PATTERN_RADIUS
from srcs.evaluation.pattern_detector import (
    _extract_lines,
    _match_patterns,
    detect_board_patterns,
    detect_local_patterns,
)


class TestDetectBoardPatterns(unittest.TestCase):
    """Test full-board stone pattern evaluation."""

    def setUp(self):
        self.board = np.zeros((19, 19), dtype=np.int8)

    def test_empty_board(self):
        self.assertEqual(detect_board_patterns(self.board, 1), 0)
        self.assertEqual(detect_board_patterns(self.board, -1), 0)

    def test_single_stone(self):
        self.board[9, 9] = 1

        self.assertEqual(detect_board_patterns(self.board, 1), 0)

    def test_free_four(self):
        self.board[9, 7:11] = 1

        self.assertEqual(
            detect_board_patterns(self.board, 1),
            100_000,
        )

    def test_white_free_four(self):
        self.board[9, 7:11] = -1

        self.assertEqual(
            detect_board_patterns(self.board, -1),
            100_000,
        )
        self.assertEqual(
            detect_board_patterns(self.board, 1),
            0,
        )

    def test_board_boundary(self):
        self.board[9, 0:4] = 1

        # The board boundary blocks one side.
        self.assertEqual(
            detect_board_patterns(self.board, 1),
            10_000,
        )

    def test_multiple_directions(self):
        self.board[9, 7:11] = 1
        self.board[2:5, 2] = 1

        # Horizontal Free Four + Vertical Free Three.
        self.assertEqual(
            detect_board_patterns(self.board, 1),
            101_000,
        )

    def test_duplicate_patterns(self):
        self.board[9, 8:11] = 1

        # Overlapping Free Three patterns count only once.
        self.assertEqual(
            detect_board_patterns(self.board, 1),
            1_000,
        )

    def test_independent_patterns_on_same_line(self):
        self.board[9, 2:6] = 1
        self.board[9, 12:15] = 1

        # Free Four + Free Three.
        self.assertEqual(
            detect_board_patterns(self.board, 1),
            101_000,
        )

    def test_before_and_after_move(self):
        self.board[9, 7:10] = 1

        before = detect_board_patterns(self.board, 1)

        self.board[9, 10] = 1

        after = detect_board_patterns(self.board, 1)

        self.assertEqual(before, 1_000)
        self.assertEqual(after, 100_000)
        self.assertEqual(after - before, 99_000)

    def test_board_is_not_modified(self):
        self.board[9, 7:11] = 1
        original = self.board.copy()

        detect_board_patterns(self.board, 1)
        detect_board_patterns(self.board, -1)

        np.testing.assert_array_equal(self.board, original)


class TestDetectLocalPatterns(unittest.TestCase):
    """Test local stone pattern evaluation."""

    def setUp(self):
        self.board = np.zeros((19, 19), dtype=np.int8)
        self.move = (9, 9)

    def test_empty_board(self):
        self.assertEqual(
            detect_local_patterns(self.board, self.move, 1),
            0,
        )

    def test_free_four(self):
        self.board[9, 7:11] = 1

        self.assertEqual(
            detect_local_patterns(self.board, self.move, 1),
            100_000,
        )

    def test_white_free_four(self):
        self.board[9, 7:11] = -1

        self.assertEqual(
            detect_local_patterns(self.board, self.move, -1),
            100_000,
        )

    def test_board_boundary(self):
        self.board[9, 0:4] = 1

        self.assertEqual(
            detect_local_patterns(self.board, (9, 0), 1),
            10_000,
        )

    def test_multiple_directions(self):
        self.board[9, 7:11] = 1
        self.board[8:11, 9] = 1
        self.board[8, 8] = 1
        self.board[10, 10] = 1

        # Free Four + Free Three + Free Three.
        self.assertEqual(
            detect_local_patterns(self.board, self.move, 1),
            102_000,
        )

    def test_duplicate_patterns(self):
        self.board[9, 8:11] = 1

        self.assertEqual(
            detect_local_patterns(self.board, self.move, 1),
            1_000,
        )

    def test_ignore_distant_patterns(self):
        self.board[9, 7:11] = 1
        self.board[2, 2:6] = 1

        local_score = detect_local_patterns(
            self.board, self.move, 1
        )
        board_score = detect_board_patterns(self.board, 1)

        self.assertEqual(local_score, 100_000)
        self.assertEqual(board_score, 200_000)

    def test_before_and_after_move(self):
        self.board[9, 7:10] = 1
        move = (9, 10)

        before = detect_local_patterns(self.board, move, 1)

        self.board[move] = 1

        after = detect_local_patterns(self.board, move, 1)

        self.assertEqual(before, 1_000)
        self.assertEqual(after, 100_000)
        self.assertEqual(after - before, 99_000)

    def test_board_is_not_modified(self):
        self.board[9, 7:11] = 1
        original = self.board.copy()

        detect_local_patterns(self.board, self.move, 1)

        np.testing.assert_array_equal(self.board, original)

    def test_consistency_with_board_detection(self):
        self.board[9, 7:11] = 1

        local_score = detect_local_patterns(
            self.board, self.move, 1
        )
        board_score = detect_board_patterns(self.board, 1)

        self.assertEqual(local_score, board_score)


class TestExtractLines(unittest.TestCase):
    """Test directional line extraction."""

    def setUp(self):
        self.board = np.zeros((19, 19), dtype=np.int8)
        self.move = (9, 9)
        self.radius = PATTERN_RADIUS
        self.line_length = self.radius * 2 + 1

    def test_empty_board(self):
        lines = _extract_lines(self.board, self.move, 1)

        expected = (0,) * self.line_length

        self.assertEqual(len(lines), 4)
        self.assertEqual(lines, (expected,) * 4)

    def test_horizontal(self):
        self.board[9, 7:11] = 1

        lines = _extract_lines(self.board, self.move, 1)

        expected = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(lines[0], expected)

    def test_vertical(self):
        self.board[7:11, 9] = 1

        lines = _extract_lines(self.board, self.move, 1)

        expected = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(lines[1], expected)

    def test_diagonal(self):
        for i in range(7, 11):
            self.board[i, i] = 1

        lines = _extract_lines(self.board, self.move, 1)

        expected = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(lines[2], expected)

    def test_anti_diagonal(self):
        for i in range(-2, 2):
            self.board[9 + i, 9 - i] = 1

        lines = _extract_lines(self.board, self.move, 1)

        expected = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(lines[3], expected)

    def test_white_perspective(self):
        self.board[9, 8] = -1
        self.board[9, 9] = -1
        self.board[9, 10] = 1

        lines = _extract_lines(self.board, self.move, -1)

        expected = (0, 0, 0, 0, 1, 1, -1, 0, 0, 0, 0)

        self.assertEqual(lines[0], expected)

    def test_board_boundary(self):
        self.board[0, 0] = 1

        lines = _extract_lines(self.board, (0, 0), 1)

        expected = (-1,) * self.radius + (1,) + (0,) * self.radius

        self.assertEqual(lines[0], expected)
        self.assertEqual(lines[1], expected)
        self.assertEqual(lines[2], expected)

        expected_anti = (
            (-1,) * self.radius
            + (1,)
            + (-1,) * self.radius
        )

        self.assertEqual(lines[3], expected_anti)

    def test_board_is_not_modified(self):
        self.board[9, 9] = 1
        original = self.board.copy()

        _extract_lines(self.board, self.move, 1)

        np.testing.assert_array_equal(self.board, original)


class TestMatchPatterns(unittest.TestCase):
    """Test stone pattern score calculation."""

    def setUp(self):
        self.empty = (0,) * (PATTERN_RADIUS * 2 + 1)

    def _score(self, line):
        """Return the horizontal pattern score."""
        lines = (line, self.empty, self.empty, self.empty)
        return _match_patterns(lines)[0]

    def test_empty_line(self):
        self.assertEqual(self._score(self.empty), 0)

    def test_five(self):
        line = (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0)

        self.assertEqual(self._score(line), 1_000_000)

    def test_free_four(self):
        line = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 100_000)

    def test_closed_four(self):
        line = (0, 0, -1, 1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 10_000)

    def test_broken_four(self):
        line = (0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0)

        self.assertEqual(self._score(line), 10_000)

    def test_free_three(self):
        line = (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 1_000)

    def test_broken_free_three(self):
        line = (0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 1_000)

    def test_closed_three(self):
        line = (0, 0, 0, -1, 1, 1, 1, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 100)

    def test_free_two(self):
        line = (0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 50)

    def test_closed_two(self):
        line = (0, 0, 0, -1, 1, 1, 0, 0, 0, 0, 0)

        self.assertEqual(self._score(line), 10)

    def test_overlapping_patterns(self):
        line = (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0)

        # Two overlapping Free Three patterns must not
        # be added together.
        self.assertEqual(self._score(line), 1_000)

    def test_pattern_outside_center(self):
        line = (1, 1, 1, 1, 1, -1, 0, 0, 0, 0, 0)

        # The Five pattern does not contain the center.
        self.assertEqual(self._score(line), 0)

    def test_multiple_directions(self):
        lines = (
            (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
            self.empty,
        )

        scores = _match_patterns(lines)

        self.assertEqual(scores, (100_000, 1_000, 1_000, 0))
        self.assertEqual(sum(scores), 102_000)


if __name__ == "__main__":
    unittest.main()
