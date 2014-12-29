#!/usr/bin/python


import random
import unittest2


class Error(Exception):
    """Base error class."""


def MaxUnimodal(input):
    if not input:
        raise Error('Invalid input: {}'.format(input))
    if not isinstance(input, list):
        return input
    input_length = len(input)
    if input_length <= 2:
        return max(input)
    low, high = 0, input_length-1
    while low+2 < high:
        mid = (low + high) / 2
        low_mid = (low + mid) / 2
        high_mid = (mid + high) / 2
        if ((input[low] <= input[mid] <= input[high]) or 
            (input[high_mid] >= input[low] and input[high_mid] >= input[mid])):
            # Max must occur between [mid, high].
            low = mid
        elif ((input[low] >= input[mid] >= input[high]) or
              (input[low_mid] >= input[low] and input[low_mid] >= input[mid])):
            # Max must occur between [low, mid].
            high = mid
        else:
            # Shorten the range by 2.
            low += 1
            high -= 1
    return max(input[low:low+3])


class MaxUnimodalTest(unittest2.TestCase):

    def testNullInput(self):
        with self.assertRaises(Error):
            MaxUnimodal(None)

    def testSingleInput(self):
        self.assertEqual(MaxUnimodal(100), 100)
        
    def testDoubleInput(self):
        input = random.sample(xrange(100), 2)
        self.assertEqual(MaxUnimodal(input), max(input))

    def testTripleInput(self):
        max_number = 100 * random.random()
        input = [max_number - 1, max_number, max_number - 2]
        self.assertEqual(MaxUnimodal(input), max_number)

    def testIncreasingInput(self):
        max_number = 10
        input = range(max_number+1)
        self.assertEqual(MaxUnimodal(input), max_number)

    def testDecreasingInput(self):
        max_number = 15
        input = range(max_number, -1, -1)
        self.assertEqual(MaxUnimodal(input), max_number)

    def testInputWithUniqueMax(self):
        max_number = 20
        input = range(max_number+1) + range(max_number-1, 5, -1)
        self.assertEqual(MaxUnimodal(input), max_number)

    def testInputWithDuplicateMax(self):
        max_number = 30
        input = range(max_number+1) + range(max_number, 5, -1)
        self.assertEqual(MaxUnimodal(input), max_number)

    def testInputWithLongTail(self):
        max_number = 40
        input = range(max_number+1) + range(max_number-1, -15, -1)
        self.assertEqual(MaxUnimodal(input), max_number)

    def testRandomInput(self):
        for _ in xrange(50):
            left_size, right_size = random.randrange(1, 100), random.randrange(1, 100)
            left, right = [random.sample(xrange(1000), size)
                           for size in (left_size, right_size)]
            left.sort()
            right.sort(reverse=True)
            input = left + right
            max_number = max(input)
            self.assertEqual(MaxUnimodal(input), max_number)


if __name__ == '__main__':
    unittest2.main()
