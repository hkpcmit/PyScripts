#!/usr/bin/python


import bisect
from test_memoize import Memoize
import unittest2


class Error(Exception):
    """"Error class."""


class LisResult(object):
    
    def __init__(self, start, end, length=1):
        self.start = start
        self.end = end
        self.length = length


class DPLis(object):

    def __init__(self, input_list):
        if not isinstance(input_list, list):
            raise Error('Invalid input_list: {}'.format(input_list))
        self.input_list = input_list
        self.input_length = len(input_list)
        self.predecessors = [None] * self.input_length
        self.end = None

    @Memoize
    def Find(self, i):
        """Find LIS that ends in position i."""
        result_list = [(1+self.Find(j), j)
                       for j, input in enumerate(self.input_list[:i])
                       if input < self.input_list[i]]
        result_list.append((1, None))
        lis_length, self.predecessors[i] = max(result_list)
        return lis_length

    @Memoize
    def Length(self):
        if self.input_length < 2:
            return self.input_length
        length, self.end = max((self.Find(i), i) for i in xrange(self.input_length))
        return length

    def Get(self):
        if self.input_length < 2:
            return self.input_list
        lis_list = []
        for _ in xrange(self.Length()):
            if not lis_list:
                lis_list.append(self.input_list[self.end])
                predessor = self.predecessors[self.end]
                continue
            lis_list.append(self.input_list[predessor])
            predessor = self.predecessors[predessor]
        lis_list.reverse()
        return lis_list


@Memoize
def RecDPLis(input_list, i):
    result_list = [LisResult(i, i)]
    for j, input in enumerate(input_list[:i]):
        if input < input_list[i]:
            lis_result = RecDPLis(input_list, j)
            # Extend end position of LIS(j) to i.
            this_result = LisResult(lis_result.start, i, lis_result.length+1)
            result_list.append(this_result)
    return max((res.length, res) for res in result_list)[1]


def DPFindLis(input_list):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    return max(RecDPLis(input_list, i).length for i in xrange(len(input_list)))        


class Lis(object):

    def __init__(self, input_list):
        if not isinstance(input_list, list):
            raise Error('Invalid input_list: {}'.format(input_list))
        self.input_list = input_list
        self.lis_end_list = []
        self.input_length = len(input_list)
        self.predessors = {}

    def FindLis(self):
        if self.lis_end_list:
            return len(self.lis_end_list)
        for element in self.input_list:
            # Check for the first LIS with length=1.
            if not self.lis_end_list:
                self.lis_end_list.append(element)
                continue
            position = bisect.bisect_left(self.lis_end_list, element)
            # Check for duplicate element.
            if (position < len(self.lis_end_list) and
                element == self.lis_end_list[position]):
                raise Error('Invalid duplicate element: {}'.format(element))
            # Check when element is greater than all current LISs.
            if position == len(self.lis_end_list):
                self.lis_end_list.append(element)
                self.predessors[element] = self.lis_end_list[position-1]
                continue
            # Check when element is less than all current LISs.
            if not position:
                self.lis_end_list[0] = element
                continue
            # Element lies between the smallest and greatest of all current LISs.  The
            # corresponding LIS will replace the one in position: position.
            self.lis_end_list[position] = element
            self.predessors[element] = self.lis_end_list[position-1]
        return len(self.lis_end_list)

    def Length(self):
        if self.input_length < 2:
            return self.input_length
        return self.FindLis()

    def Get(self):
        if self.input_length < 2:
            return self.input_list
        length = self.Length()
        end = self.lis_end_list[-1]
        # Start from the end and work backward.
        lis_list = [end]
        for _ in xrange(length-1):
            predessor = self.predessors[lis_list[-1]]
            lis_list.append(predessor)
        lis_list.reverse()
        return lis_list


class TestDPLis(unittest2.TestCase):

    def testDPLisInvalid(self):
        self.assertRaises(Error, DPLis, None)

    def testEmpty(self):
        input_list = []
        lis = DPLis(input_list)
        self.assertEqual(0, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testSingle(self):
        input_list = [1]
        lis = DPLis(input_list)
        self.assertEqual(1, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testDecreasing(self):
        lis = DPLis(range(10, -1, -1))
        self.assertEqual(1, lis.Length())

    def testIncreasing(self):
        input_list = range(10)
        lis = DPLis(input_list)
        self.assertEqual(10, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testLis1(self):
        lis = DPLis([3, 1, 2])
        self.assertEqual(2, lis.Length())
        self.assertListEqual([1, 2], lis.Get())

    def testLis2(self):
        lis = DPLis([10, 22, 9, 33, 21, 50, 41, 60, 80])
        self.assertEqual(6, lis.Length())

    def testLis3(self):
        input_list = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        lis = DPLis(input_list)
        self.assertEqual(6, lis.Length())

    def testLis4(self):
        lis = DPLis([0, 8, 4, 12, 1])
        self.assertEqual(3, lis.Length())
        self.assertListEqual([0, 4, 12], lis.Get())


class TestLis(unittest2.TestCase):

    def testLisInvalid(self):
        self.assertRaises(Error, Lis, None)

    def testEmpty(self):
        input_list = []
        lis = Lis(input_list)
        self.assertEqual(0, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testSingle(self):
        input_list = [1]
        lis = Lis(input_list)
        self.assertEqual(1, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testDuplicateElements(self):
        lis = Lis([1, 1])
        self.assertRaises(Error, lis.FindLis)

    def testIncreasing(self):
        size = 10
        input_list = range(size)
        lis = Lis(input_list)
        self.assertEqual(size, lis.Length())
        self.assertListEqual(input_list, lis.Get())

    def testDecreasing(self):
        input_list = range(5, -1, -1)
        lis = Lis(input_list)
        self.assertEqual(1, lis.Length())

    def testLis1(self):
        lis = Lis([3, 1, 2])
        self.assertEqual(2, lis.Length())
        self.assertListEqual([1, 2], lis.Get())

    def testLis2(self):
        lis = Lis([10, 22, 9, 33, 21, 50, 41, 60, 80])
        self.assertEqual(6, lis.Length())

    def testLis3(self):
        input_list = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        lis = Lis(input_list)
        self.assertEqual(6, lis.Length())

    def testLis4(self):
        lis = Lis([0, 8, 4, 12, 1])
        self.assertEqual(3, lis.Length())
        self.assertListEqual([0, 4, 12], lis.Get())


if __name__ == '__main__':
    unittest2.main()
