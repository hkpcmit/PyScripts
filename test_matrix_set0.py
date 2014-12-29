#!/usr/bin/python


import unittest2


class Error(Exception):
    """Base error class."""


def MatrixSet0(matrix):
    if not matrix:
        raise Error('Invalid matrix: {}'.format(matrix))
    rows = len(matrix)
    columns = len(matrix[0])
    for row in xrange(1, rows):
        if len(matrix[row]) != columns:
            raise Error('Invalid row: {} in matrix: {}'.format(matrix[row], matrix))
    zero_rows, zero_columns = set(), set()
    for row in xrange(rows):
        for column in xrange(columns):
            if not matrix[row][column]:
                zero_rows.add(row)
                zero_columns.add(column)
    for row in zero_rows:
        matrix[row] = [0] * columns
    for column in zero_columns:
        for row in xrange(rows):
            matrix[row][column] = 0


class Set0Test(unittest2.TestCase):

    def testInvalidInput(self):
        with self.assertRaises(Error):
            MatrixSet0(None)

    def testInvalidMatrix(self):
        with self.assertRaises(Error):
            MatrixSet0([[1, 2], [3]])

    def testMatrix1(self):
        matrix = [[0, 1],
                  [2, 0]]
        expect = [[0] * 2,
                  [0] * 2]
        MatrixSet0(matrix)
        self.assertEqual(matrix, expect)

    def testMatrix2(self):
        matrix = [[0, 1, 2],
                  [3, 4, 5]]
        expect = [[0, 0, 0],
                  [0, 4, 5]]
        MatrixSet0(matrix)
        self.assertEqual(matrix, expect)

    def testMatrix3(self):
        matrix = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 0]]
        expect = [[0, 0, 0],
                  [0, 4, 0],
                  [0, 0, 0]]
        MatrixSet0(matrix)
        self.assertEqual(matrix, expect)


if __name__ == '__main__':
    unittest2.main()
