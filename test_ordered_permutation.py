#!/usr/bin/python

# You are given an array and a permutation rule. Apply the permutation to the array.
# For example: array A: [a, b, c] permutation rule: R: [1, 2, 0] output O: [c, a, b]
# More formally: O[R[i]] = A[i]
# More specifically, we want to do permutation in place O(1) auxiliary space complexity and
# we don't want to modify permutation array R. To formalize, implement the function with a signature:
# void f(int* A, const int* R, int len) where:
# A - input array R - permutation rule array len - length of both arrays

import unittest


class Error(Exception):
    """Base error."""


def RecOP(A, R, current_position, tmp_position):
    if current_position == len(A)-1:
        # We have reached the last position.  Put the appropriate element in this position.
        A[current_position] = A[R[current_position]]
        return
    A[tmp_position] = A[R[current_position]]
    RecOP(A, R, current_position+1, R[current_position])
    A[current_position] = A[tmp_position]


def OP(A, R):
    if len(set(R)) != len(A):
        raise Error('Invalid R: {}'.format(R))
    first_index = R[0]
    first_element = A[first_index]
    RecOP(A, R, 1, first_index)
    A[0] = first_element
    return A


class OrderedPermutationTest(unittest.TestCase):

    def testOPInvalidR(self):
        A = ['a', 'b', 'c']
        R = [1, 2, 1]
        with self.assertRaises(Error):
            OP(A, R)

    def testOPNoOrder(self):
        A = ['a', 'b', 'c']
        R = [0, 1, 2]
        self.assertEqual(A, OP(A, R))

    def testOP(self):
        A = ['a', 'b', 'c']
        R = [1, 2, 0]
        self.assertEqual(['b', 'c', 'a'], OP(A, R))


if __name__ == '__main__':
    unittest.main()
