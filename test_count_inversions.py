#!/usr/bin/python


import unittest2


class Error(Exception):
    """Base error class."""


class MergeResult(object):

    def __init__(self, merge_list=None, inversions=0):
        self.merge_list = merge_list
        self.inversions = inversions


def CIMerger(input_list):

    if not input_list:
        raise Error('Empty input_list: {}'.format(input_list))
    input_length = len(input_list)
    if input_length == 1:
        return MergeResult(merge_list=input_list, inversions=0)
    mid = input_length / 2
    left = CIMerger(input_list[:mid])
    right = CIMerger(input_list[mid:])
    inversions = left.inversions + right.inversions
    merge_list = []
    l, r = 0, 0
    left_length, right_length = [len(side.merge_list) for side in (left, right)]
    while l < left_length and r < right_length:
        if right.merge_list[r] < left.merge_list[l]:
            inversions += left_length - l
            merge_list.append(right.merge_list[r])
            r += 1
        else:
            merge_list.append(left.merge_list[l])
            l += 1
    if l == left_length:
        merge_list.extend(right.merge_list[r:])
    else:
        merge_list.extend(left.merge_list[l:])
    return MergeResult(merge_list=merge_list, inversions=inversions)


def CountInversions(input_list):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if len(input_list) < 2:
        return 0
    result = CIMerger(input_list)
    return result.inversions


def SlowCountInversions(input_list):
    input_length = len(input_list)
    count = 0
    for i in range(input_length-1):
        for j in range(i, input_length):
            if input_list[i] > input_list[j]:
                count += 1
    return count


class TestCountInversions(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, CountInversions, None)

    def testMergerInvalid(self):
        self.assertRaises(Error, CIMerger, [])

    def testEmpty(self):
        self.assertEqual(0, CountInversions([]))

    def testSingle(self):
        self.assertEqual(0, CountInversions([1]))

    def testTwoElements(self):
        self.assertEqual(0, CountInversions([1, 2]))
        self.assertEqual(1, CountInversions([2, 1]))

    def testCountInvesions1(self):
        input_list = [2, 4, 1, 3, 5]
        result = CIMerger(input_list)
        self.assertListEqual(sorted(input_list), result.merge_list)
        self.assertEqual(3, result.inversions)
        self.assertEqual(3, CountInversions(input_list))

    def testCountInvesions2(self):
        input_list = [10, 2, 3, 22, 33, 7, 4, 1, 2]
        self.assertEqual(SlowCountInversions(input_list), CountInversions(input_list))

    def testCountInvesions3(self):
        input_list = [15, 20, 1, 3, 8, 2, 16, 17, 11, 19, 10, 5, 18, 4, 7, 9, 12, 6, 13, 14]
        self.assertEqual(SlowCountInversions(input_list), CountInversions(input_list))

    def testHomework(self):
        input_file = 'IntegerArray.txt'
        input_list = []
        with open(input_file, 'r') as fd:
            for line in fd:
                input_list.append(int(line))
        print 'Result: {}'.format(CountInversions(input_list))


if __name__ == '__main__':
    unittest2.main()
