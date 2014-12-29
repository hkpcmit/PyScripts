#!/usr/bin/python
#
# A newspaper wants to validate that the crossword puzzles always satisfy a
# few conditions before printing them. Write a function that takes in a
# two-dimensional rectangular array of booleans indicating if the square is
# black and returns true if the following conditions hold:
# - The pattern is identical if it is rotated 180 degrees
# - Every empty space is reachable from every other empty space (aka
#   orthogonally contiguous) 


import unittest2


class Error(Exception):
    """Base error class."""


class InputError(Error): 
    """"Input related error."""


class Puzzle(object):

    def __init__(self, puzzle):
        self.ValidatePuzzle(puzzle)
        self.puzzle = puzzle
        self.white_set = set(self.GetPosition(i, j)
                             for i in xrange(self.length)
                             for j in xrange(self.length)
                             if puzzle[i][j])

    def Check(self):
        # Validate rotation requirement.
        left_bottom = (0,0)
        right_top = (self.length-1, self.length-1)
        if not self.RecCheckRotation(left_bottom, right_top):
            return False
        # Validate reachable requirement.
        if not self.white_set:
            return False
        init_white = list(self.white_set)[0]
        reachable_set = set()
        self.RecCheckReachable(init_white, reachable_set)
        return reachable_set == self.white_set

    def CheckRotation(self, positions):
        for position in positions:
            x, y = self.GetPositionComponents(position)
            rotated_x, rotated_y = [self.length-1-i for i in (x, y)]
            if self.puzzle[x][y] != self.puzzle[rotated_x][rotated_y]:
                return False
        return True

    def GetNeighbors(self, x, y):
        neighbors = []
        if x != self.length-1:
            # Right neighbor.
            neighbor_x = x + 1
            if self.puzzle[neighbor_x][y]:
                neighbors.append((neighbor_x, y))
        if x:
            # Left neighbor.
            neighbor_x = x - 1
            if self.puzzle[neighbor_x][y]:
                neighbors.append((x-1, y))
        if y != self.length-1:
            # Above neighbor.
            neighbor_y = y + 1
            if self.puzzle[x][neighbor_y]:
                neighbors.append((x, neighbor_y))
        if y:
            # Below neighbor.
            neighbor_y = y - 1
            if self.puzzle[x][neighbor_y]:
                neighbors.append((x, y-1))
        return neighbors

    def GetAllWhites(self):
        for i in xrange(self.length):
            for j in xrange(self.length):
                if self.puzzle[i][j]:
                    return i, j
        raise NoWhiteError()

    def GetPosition(self, x, y):
        return ','.join(str(c) for c in (x, y))

    def GetPositionComponents(self, position):
        return [int(c) for c in position.split(',')]

    def RecCheckReachable(self, white_position, reachable_set):
        # Recursively compute set of white positions reachable from white_position
        # via DFS.
        reachable_set.add(white_position)
        x, y = self.GetPositionComponents(white_position)
        neighbors = self.GetNeighbors(x, y)
        for neighbor in neighbors:
            neighbor_position = self.GetPosition(*neighbor)
            if neighbor_position not in reachable_set:
                self.RecCheckReachable(neighbor_position, reachable_set)

    def RecCheckRotation(self, left_bottom, right_top):
        # Recursively check if sub-puzzle defined by boundaries within left_bottom &
        # right_top passes the check.
        if left_bottom[0] > right_top[0]:
            return True
        if self.length == 1:
            return self.puzzle[left_bottom[0]][left_bottom[1]]
        # Get vertical positions of the right-most side of the sub-puzzle.
        positions = set(self.GetPosition(right_top[0], y)
                        for y in xrange(left_bottom[1], right_top[1]+1))
        # Get horizontal positions of the bottom side of the sub-puzzle.
        for x in xrange(left_bottom[0], right_top[0]+1):
            positions.add(self.GetPosition(x, left_bottom[0]))
        if not self.CheckRotation(positions):
            return False
        # Recurse on inner sub-puzzle.
        left_bottom = (left_bottom[0]+1, left_bottom[1]+1)
        right_top = (right_top[0]-1, right_top[1]-1)
        return self.RecCheckRotation(left_bottom, right_top)

    def ValidatePuzzle(self, puzzle):
        if not isinstance(puzzle, list):
            raise InputError('Puzzle: {} is not a list.'.format(puzzle))
        self.length = len(puzzle)
        for row in puzzle:
            row_length = len(row)
            if row_length != self.length:
                raise InputError('Invalid row: {} with length: {}; expect: {}'.format(
                        row, row_length, self.length))


class PuzzleTest(unittest2.TestCase):

    def testInvalidPuzzleType(self):
        with self.assertRaises(InputError):
            Puzzle(None)

    def testInvalidPuzzleSizes(self):
        with self.assertRaises(InputError):
            Puzzle([[True, True], [True]])

    def testSingleSquare(self):
        puzzle = Puzzle([[True]])
        self.assertTrue(puzzle.Check())
        puzzle = Puzzle([[False]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare2_1(self):
        puzzle = Puzzle([[False, True], [True, False]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare2_2(self):
        puzzle = Puzzle([[False, True], [False, False]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare2_3(self):
        puzzle = Puzzle([[False, False], [False, False]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare2_4(self):
        puzzle = Puzzle([[True, True], [True, True]])
        self.assertTrue(puzzle.Check())

    def testPuzzleSquare3_1(self):
        puzzle = Puzzle([[False, True, True],
                         [True, False, True],
                         [False, True, True]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare3_2(self):
        puzzle = Puzzle([[False, True, True],
                         [False, True, False],
                         [True, True, False]])
        self.assertTrue(puzzle.Check())

    def testPuzzleSquare3_3(self):
        puzzle = Puzzle([[False, True, True],
                         [True, True, False],
                         [True, True, False]])
        self.assertFalse(puzzle.Check())

    def testPuzzleSquare4_1(self):
        puzzle = Puzzle([[True, True, True, True],
                         [True, False, False, True],
                         [True, False, False, True],
                         [True, True, True, True]])
        self.assertTrue(puzzle.Check())

    def testPuzzleSquare4_2(self):
        puzzle = Puzzle([[False, True, True, True],
                         [True, True, False, True],
                         [True, False, True, True],
                         [True, True, True, False]])
        self.assertTrue(puzzle.Check())

    def testPuzzleSquare4_3(self):
        puzzle = Puzzle([[True, True, False, False],
                         [True, False, False, False],
                         [False, False, False, True],
                         [False, False, True, True]])
        self.assertFalse(puzzle.Check())


if __name__ == '__main__':
    unittest2.main()
