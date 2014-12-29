#!/usr/bin/python


import unittest2


class Error(Exception):
    """Base error class."""


def RotateMatrix(mtx):
    # Rotate matrix clockwise by 90 degrees.
    if not mtx:
        raise Error('Invalid matrix: {}'.format(mtx))
    size = len(mtx)
    for row in mtx:
        if len(row) != size:
            raise Error('Invalid row: {} in matrix {}'.format(row, mtx))
    if size == 1:
        return mtx
    # Transpose the matrix.
    transpose = zip(*mtx)
    # Reverse each column.
    for i in xrange(size):
        column = transpose[i]
        transpose[i] = [element for element in reversed(column)]
    return transpose


class RotateMatrixTest(unittest2.TestCase):

    def testInvalidMatrix(self):
        with self.assertRaises(Error):
            RotateMatrix(None)

    def testInvalidRow(self):
        with self.assertRaises(Error):
            RotateMatrix([[1, 2],
                          [3]])

    def test1x1(self):
        matrix = [[10]]
        self.assertEqual(RotateMatrix(matrix), matrix)

    def test2x2(self):
        matrix = [[1, 2],
                  [3, 4]]
        expect = [[3, 1],
                  [4, 2]]
        self.assertEqual(RotateMatrix(matrix), expect)

    def test3x3(self):
        matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
        expect = [[7, 4, 1],
                  [8, 5, 2],
                  [9, 6, 3]]
        self.assertEqual(RotateMatrix(matrix), expect)

    def test3x3(self):
        matrix = [[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]]
        expect = [[13, 9, 5, 1],
                  [14, 10, 6, 2],
                  [15, 11, 7, 3],
                  [16, 12, 8, 4]]
        self.assertEqual(RotateMatrix(matrix), expect)


if __name__ == '__main__':
    unittest2.main()
