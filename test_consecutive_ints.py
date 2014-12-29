#!/usr/bin/python


import unittest2


class Error(Exception):
    """Base error class."""


def GetMinMax(input_set, i, inc):
    
    end = i + inc
    while end in input_set:
        end += inc
    return end - inc


def ConsInts(input_list):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if len(input_list) < 2:
        return input_list
    best_length = 0
    best = []
    input_set = set(input_list)
    while input_set:
        i = input_set.pop()
        int_range = [GetMinMax(input_set, i, inc) for inc in (-1, 1)]
        this_length = int_range[1] - int_range[0] + 1 
        if this_length > best_length:
            best_length = this_length
            best = int_range
        input_set = input_set.difference(xrange(int_range[0], int_range[1]+1))
    return range(best[0], best[1]+1)


class TestConsecutiveInts(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, ConsInts, None)

    def testEmpty(self):
        self.assertEqual([], ConsInts([]))

    def testSingle(self):
        input_list = [1]
        self.assertEqual(input_list, ConsInts(input_list))

    def testInput1(self):
        input_list = range(10)
        self.assertEqual(input_list, ConsInts(input_list))

    def testInput2(self):
        expect = range(100, 200)
        input_list = range(10)
        input_list.extend(expect)
        self.assertEqual(expect, ConsInts(input_list))


if __name__ == '__main__':
    unittest2.main()
