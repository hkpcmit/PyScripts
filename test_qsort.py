#!/usr/bin/python


import random
import unittest2


class Error(Exception):
    """Base error class."""


def Swap(input_list, a, b):

    tmp = input_list[a]
    input_list[a] = input_list[b]
    input_list[b] = tmp


def Partition(input_list, start, end):

    if (end - start) <= 1:
        raise Error('Invalid start: {}, end: {}'.format(start, end))
    input_length = len(input_list)
    if start >= (input_length-1) or end > input_length:
        raise Error('Invalid: start: {}, end: {}, input length: {}'.format(
                start, end, input_length))
    # Pivot is in the first position.
    pivot = input_list[start]
    # i represents the first position after the lower partition; 
    # j represents the first unpartitioned element.
    i = j = start + 1
    while j < end:
        if input_list[j] < pivot:
            Swap(input_list, i, j)
            i += 1
        j += 1
    if start == i-1:
        return start
    Swap(input_list, start, i-1)
    return i-1


def GetPivotStart(unused_list, start, unused_end):
    return start


def GetPivotEnd(unused_list, unused_start, end):
    return end - 1


def GetPivotMid(input_list, start, end):
    lst = [(input_list[i], i) for i in (start, end-1)]
    length = end - start
    if length % 2:
        mid = (start + end - 1) / 2
    else:
        mid = start - 1 + length/2
    lst.append((input_list[mid], mid))
    return sorted(lst)[1][1]


def RecQsort(input_list, start, end, pivot_func, counter):

    if (end - start) < 1:
        raise Error('Invalid start: {}, end: {}'.format(start, end))
    input_length = len(input_list)
    if start > (input_length-1) or end > input_length:
        raise Error('Index error: start: {}, end: {}, input length: {}'.format(
                start, end, input_length))
    if end - start == 1:
        return
    piv = pivot_func(input_list, start, end)
    if piv != start:
        Swap(input_list, piv, start)
    piv = Partition(input_list, start, end)
    if piv != start:
        RecQsort(input_list, start, piv, pivot_func, counter)
        counter['comparisons'] += (piv - start - 1)
    if piv != end - 1:
        RecQsort(input_list, piv+1, end, pivot_func, counter)
        counter['comparisons'] += (end - piv - 2)
    return


def Qsort(input_list, pivot_func):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    input_length = len(input_list)
    counter = {'comparisons': input_length-1}
    RecQsort(input_list, 0, input_length, pivot_func, counter)
    return {'sorted': input_list, 'comparisons': counter['comparisons']}


class TestQsort(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, Qsort, None, None)

    def testInvalidStartEnd(self):
        self.assertRaises(Error, RecQsort, [1, 2], 1, 0, None, None)
        self.assertRaises(Error, RecQsort, [1, 2], 1, 3, None, None)
        self.assertRaises(Error, RecQsort, [1, 2], 0, 3, None, None)


class TestQsortPivotStart(unittest2.TestCase):

    def setUp(self):
        self.pivot_func = GetPivotStart
        self.comparisons = {'QuickSort10.txt': 25, 'QuickSort100.txt': 615,
                            'QuickSort1000.txt': 10297}
        self.pivot_msg = 'PivotStart'

    def GetInputFromFile(self, file_name):
        with open(file_name, 'r') as fd:
            input_list = [int(line) for line in fd]
        return input_list

    def testSingle(self):
        input_list = [0]
        expect = input_list[:]
        self.assertEqual(expect, Qsort(input_list, self.pivot_func)['sorted'])

    def testDouble(self):
        input_list = [0, 1]
        expect = input_list[:]
        self.assertEqual(expect, Qsort(input_list, self.pivot_func)['sorted'])

    def testDecreasing(self):
        input_list = range(7, -1, -1)
        expect = input_list[:]
        expect.reverse()
        self.assertEqual(expect, Qsort(input_list, self.pivot_func)['sorted'])

    def testIncreasing(self):
        input_list = range(10)
        expect = input_list[:]
        self.assertEqual(expect, Qsort(input_list, self.pivot_func)['sorted'])

    def test10(self):
        file_name = 'QuickSort10.txt'
        input_list = self.GetInputFromFile(file_name)
        expect = {'sorted': sorted(input_list),
                  'comparisons': self.comparisons[file_name]}
        self.assertEqual(expect, Qsort(input_list, self.pivot_func))

    def test100(self):
        file_name = 'QuickSort100.txt'
        input_list = self.GetInputFromFile(file_name)
        expect = {'sorted': sorted(input_list),
                  'comparisons': self.comparisons[file_name]}
        self.assertEqual(expect, Qsort(input_list, self.pivot_func))

    def test1000(self):
        file_name = 'QuickSort1000.txt'
        input_list = self.GetInputFromFile(file_name)
        expect = {'sorted': sorted(input_list),
                  'comparisons': self.comparisons[file_name]}
        self.assertEqual(expect, Qsort(input_list, self.pivot_func))

    def testRandom(self):
        trials = 100
        size = 1000
        population = range(100000)
        for _ in xrange(trials):
            input_list = random.sample(population, size)
            expect = sorted(input_list)
            self.assertEqual(expect, Qsort(input_list, self.pivot_func)['sorted'])

    def testHomework(self):
        input_list = self.GetInputFromFile('QuickSort.txt')
        expect = sorted(input_list)
        result = Qsort(input_list, self.pivot_func)
        self.assertEqual(expect, result['sorted'])
        print '{} comparisons: {}'.format(self.pivot_msg, result['comparisons'])


class TestQsortPivotEnd(TestQsortPivotStart):

    def setUp(self):
        self.pivot_func = GetPivotEnd
        self.comparisons = {'QuickSort10.txt': 29, 'QuickSort100.txt': 587,
                            'QuickSort1000.txt': 10184}
        self.pivot_msg = 'PivotEnd'


class TestQsortPivotMid(TestQsortPivotStart):

    def setUp(self):
        self.pivot_func = GetPivotMid
        self.comparisons = {'QuickSort10.txt': 21, 'QuickSort100.txt': 518,
                            'QuickSort1000.txt': 8921}
        self.pivot_msg = 'PivotMid'


class TestPartition(unittest2.TestCase):

    def testInvalidStartEnd(self):
        self.assertRaises(Error, Partition, [1, 2], 1, 0)
        self.assertRaises(Error, Partition, [1, 2], 1, 2)
        self.assertRaises(Error, Partition, [1, 2], 0, 3)

    def testInputList1(self):
        input_list = [1, 0]
        piv = Partition(input_list, 0, len(input_list))
        self.assertEqual(1, piv)
        expect = [0, 1]
        self.assertListEqual(expect, input_list)

    def testInputList2(self):
        input_list = [10, 1, 0]
        piv = Partition(input_list, 1, len(input_list))
        self.assertEqual(2, piv)
        expect = [10, 0, 1]
        self.assertListEqual(expect, input_list)

    def testInputList3(self):
        input_list = [1, 0, 10]
        piv = Partition(input_list, 0, len(input_list)-1)
        self.assertEqual(1, piv)
        expect = [0, 1, 10]
        self.assertListEqual(expect, input_list)

    def testInputList4(self):
        input_list = [2, 3]
        piv = Partition(input_list, 0, len(input_list))
        self.assertEqual(0, piv)
        expect = [2, 3]
        self.assertListEqual(expect, input_list)

    def testInputList5(self):
        input_list = [10, 2, 3]
        piv = Partition(input_list, 1, len(input_list))
        self.assertEqual(1, piv)
        expect = [10, 2, 3]
        self.assertListEqual(expect, input_list)

    def testInputList6(self):
        input_list = [2, 3, 10]
        piv = Partition(input_list, 0, len(input_list)-1)
        self.assertEqual(0, piv)
        expect = [2, 3, 10]
        self.assertListEqual(expect, input_list)

    def testInputList7(self):
        input_list = [2, 0, 1]
        piv = Partition(input_list, 0, len(input_list))
        self.assertEqual(2, piv)
        expect = [1, 0, 2]
        self.assertListEqual(expect, input_list)

    def testInputList8(self):
        input_list = [20, 2, 0, 1]
        piv = Partition(input_list, 1, len(input_list))
        self.assertEqual(3, piv)
        expect = [20, 1, 0, 2]
        self.assertListEqual(expect, input_list)

    def testInputList9(self):
        input_list = [2, 0, 1, 20]
        piv = Partition(input_list, 0, len(input_list)-1)
        self.assertEqual(2, piv)
        expect = [1, 0, 2, 20]
        self.assertListEqual(expect, input_list)

    def testInputList10(self):
        input_list = [3, 8, 2, 5, 1, 4, 7, 6]
        piv = Partition(input_list, 0, len(input_list))
        self.assertEqual(2, piv)
        expect = [1, 2, 3, 5, 8, 4, 7, 6]
        self.assertListEqual(expect, input_list)


if __name__ == '__main__':
    unittest2.main()
