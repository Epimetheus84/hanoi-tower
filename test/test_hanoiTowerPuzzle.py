from unittest import TestCase

from puzzle import HanoiTowerPuzzle


class TestHanoiTowerPuzzle(TestCase):
    def test_load_from_file(self):
        puzzle = HanoiTowerPuzzle.load_from_file('test/resources/test_0.txt')
        self.assertEqual(puzzle.pegs, [[2, 1, 0], [], []])
        self.assertEqual(puzzle.costs, [1, 1, 1])
        self.assertEqual(len(puzzle.check_decision), 7)

        puzzle = HanoiTowerPuzzle.load_from_file('test/resources/test_1.txt')
        self.assertEqual(puzzle.pegs, [[2, 1, 0], [], []])
        self.assertEqual(puzzle.costs, [1, 1, 1])
        self.assertEqual(len(puzzle.check_decision), 7)

        puzzle = HanoiTowerPuzzle.load_from_file('test/resources/test_2.txt')
        self.assertEqual(puzzle.pegs, [[2, 1, 0], []])
        self.assertEqual(puzzle.costs, [1, 1])
        self.assertEqual(len(puzzle.check_decision), 7)

        puzzle = HanoiTowerPuzzle.load_from_file('test/resources/test_3.txt')
        self.assertEqual(puzzle.pegs, [[2, 1, 0], [], [], []])
        self.assertEqual(puzzle.costs, [1, 1, 1, 1])
        self.assertEqual(len(puzzle.check_decision), 3)

        puzzle = HanoiTowerPuzzle.load_from_file('test/resources/test_4.txt')
        self.assertEqual(puzzle.pegs, [[3, 2, 1, 0], [], [], []])
        self.assertEqual(puzzle.costs, [1, 2, 4, 6])
        self.assertEqual(len(puzzle.check_decision), 9)

    def test_solve(self):
        pass
