import unittest

import numpy as np

from srcs.evaluation.pattern_detector import (
    detect_board_patterns,
)


class TestBoardPatterns(unittest.TestCase):

    def setUp(self):
        self.board = np.zeros((19, 19), dtype=int)

    def test_empty_board(self):
        for stone in (1, -1):
            self.assertEqual(
                detect_board_patterns(self.board, stone), 0
            )

    def test_single_stone(self):
        for stone in (1, -1):
            with self.subTest(stone=stone):
                self.board.fill(0)
                self.board[9, 9] = stone

                self.assertEqual(
                    detect_board_patterns(self.board, stone), 0
                )

    def test_stone_patterns(self):
        patterns = [
            ("Five", (1, 1, 1, 1, 1), 1_000_000),
            ("Free Four", (0, 1, 1, 1, 1, 0), 100_000),
            ("Closed Four", (-1, 1, 1, 1, 1, 0), 10_000),
            ("Broken Four", (1, 1, 0, 1, 1), 10_000),
            ("Free Three", (0, 0, 1, 1, 1, 0), 1_000),
            ("Broken Three", (0, 1, 0, 1, 1, 0), 1_000),
            ("Closed Three", (-1, 1, 1, 1, 0, 0), 100),
            ("Free Two", (0, 0, 1, 1, 0, 0), 50),
            ("Closed Two", (-1, 1, 1, 0, 0, 0), 10),
        ]

        for name, pattern, expected in patterns:
            for stone in (1, -1):
                with self.subTest(pattern=name, stone=stone):
                    self.board.fill(0)

                    self.board[9, 5:5 + len(pattern)] = (
                        np.array(pattern) * stone
                    )

                    actual = detect_board_patterns(
                        self.board, stone
                    )

                    self.assertEqual(actual, expected)

    def test_both_players(self):
        # Black: Free Three
        self.board[5, 5:8] = 1

        # White: Free Four
        self.board[10, 5:9] = -1

        self.assertEqual(
            detect_board_patterns(self.board, 1), 1_000
        )
        self.assertEqual(
            detect_board_patterns(self.board, -1), 100_000
        )

    def test_all_directions(self):
        directions = (
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        )

        for dr, dc in directions:
            for stone in (1, -1):
                with self.subTest(
                    direction=(dr, dc), stone=stone
                ):
                    self.board.fill(0)

                    for i in range(4):
                        self.board[9 + dr * i, 9 + dc * i] = stone

                    self.assertEqual(
                        detect_board_patterns(self.board, stone),
                        100_000,
                    )

    def test_board_boundary(self):
        for stone in (1, -1):
            with self.subTest(stone=stone):
                self.board.fill(0)
                self.board[9, 0:4] = stone

                self.assertEqual(
                    detect_board_patterns(self.board, stone),
                    10_000,
                )

    def test_color_symmetry(self):
        self.board[5, 5:8] = 1
        self.board[10, 5:9] = -1

        for stone in (1, -1):
            with self.subTest(stone=stone):
                original_score = detect_board_patterns(
                    self.board, stone
                )

                reversed_score = detect_board_patterns(
                    -self.board, -stone
                )

                self.assertEqual(
                    original_score, reversed_score
                )

    def test_no_board_mutation(self):
        self.board[5, 5:8] = 1
        self.board[10, 5:9] = -1

        original_board = self.board.copy()

        detect_board_patterns(self.board, 1)
        detect_board_patterns(self.board, -1)

        np.testing.assert_array_equal(
            self.board, original_board
        )


if __name__ == "__main__":
    unittest.main()
