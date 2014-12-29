#!/usr/bin/python


import heapq
import random
from test_qsort import GetPivotMid, Swap
import time
import unittest2


class Error(Exception):
    """Base error class."""


def Partition(input_list, start, end):

    if (end - start) <= 1:
        raise Error('Invalid start: {}, end: {}'.format(start, end))
    input_length = len(input_list)
    if start >= (input_length-1) or end > input_length:
        raise Error('Invalid: start: {}, end: {}, input length: {}'.format(
                start, end, input_length))
    # Pivot is in the first position.
    pivot = input_list[start]
    # i represents the first position after the higher partition; 
    # j represents the first unpartitioned element.
    i = j = start + 1
    while j < end:
        if input_list[j] > pivot:
            Swap(input_list, i, j)
            i += 1
        j += 1
    if start == i-1:
        return start
    Swap(input_list, start, i-1)
    return i-1


def RecMaxN(input_list, num, start, end):

    if end - start == 1:
        return
    piv = GetPivotMid(input_list, start, end)
    if piv != start:
        Swap(input_list, start, piv)
    piv = Partition(input_list, start, end)
    if piv != start:
        RecMaxN(input_list, num, start, piv)
    if piv - start > num or piv+1 == end:
        # No need to find max in the right half.
        return
    RecMaxN(input_list, num+start-piv, piv+1, end)


def MaxN(input_list, num):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if num < 1:
        raise Error('Invalid num: {}'.format(num))
    if len(input_list) < 2:
        return input_list
    if num == 1:
        return [max(input_list)]
    input_length = len(input_list)
    num = min(num, input_length)
    RecMaxN(input_list, num, 0, input_length)
    return input_list[:num]


def MaxNHeap(input_list, num):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if num < 1:
        raise Error('Invalid num: {}'.format(num))
    if len(input_list) < 2:
        return input_list
    if num == 1:
        return [max(input_list)]
    input_length = len(input_list)
    num = min(num, input_length)
    heap = input_list[:num]
    heapq.heapify(heap)
    for element in input_list[num:]:
        if element > heap[0]:
            heapq.heapreplace(heap, element)
    result = [heapq.heappop(heap) for _ in xrange(num)]
    result.reverse()
    return result


class TestMaxN(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, MaxN, None, 0)
        self.assertRaises(Error, MaxN, [], 0)

    def testEmpty(self):
        self.assertEqual([], MaxN([], 100))

    def testSingle(self):
        input_list = [100]
        self.assertEqual(input_list, MaxN(input_list, 1))

    def testNIsOne(self):
        mx = 10
        self.assertEqual([mx], MaxN(range(mx+1), 1))

    def testDecreasing(self):
        input_list = range(10, -1, -1)
        expect = [10, 9, 8]
        self.assertEqual(expect, MaxN(input_list, 3))

    def testIncreasing(self):
        input_list = range(10)
        expect = [9, 8, 7]
        self.assertEqual(expect, MaxN(input_list, 3))

    def testInputLengthEqNum(self):
        num = 10
        input_list = range(num)
        expect = range(num-1, -1, -1)
        self.assertEqual(expect, MaxN(input_list, num))

    def testInputLengthLessThanNum(self):
        num = 10
        input_length = num / 2
        input_list = range(input_length)
        expect = range(input_length-1, -1, -1)
        self.assertEqual(expect, MaxN(input_list, input_length))

    def testMaxN1(self):
        input_list = [2, 4, 3, 1]
        expect = [4, 3]
        self.assertEqual(expect, MaxN(input_list, 2))

    def testMaxN2(self):
        input_list = [5747, 1590, 2539, 540, 
                      5779, 5409, 3281,
                      1353, 987, 1210, 2060, 5041,
                      2580, 5826, 2194, 4013]
        expect = [5826,
                  5779, 5747, 5409, 5041, 4013,
                  3281, 2580, 2539, 2194, 2060,
                  1590, 1353, 1210, 987, 540]
        self.assertEqual(expect, MaxN(input_list, 20))

    def testRandom(self):
        trials = 100
        max_int = 10000
        num = random.randint(1, max_int)
        population = xrange(max_int)
        size = random.randint(10, 1000)
        for _ in xrange(trials):
            input_list = random.sample(population, size)
            expect = sorted(input_list, reverse=True)
            expect = expect[:min(num, len(input_list))]
            self.assertEqual(expect, MaxN(input_list, num))


class TestMaxNHeap(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, MaxNHeap, None, 0)
        self.assertRaises(Error, MaxNHeap, [], 0)

    def testEmpty(self):
        self.assertEqual([], MaxNHeap([], 100))

    def testSingle(self):
        input_list = [100]
        self.assertEqual(input_list, MaxNHeap(input_list, 1))

    def testNIsOne(self):
        mx = 10
        self.assertEqual([mx], MaxNHeap(range(mx+1), 1))

    def testDecreasing(self):
        input_list = range(10, -1, -1)
        expect = [10, 9, 8]
        self.assertEqual(expect, MaxNHeap(input_list, 3))

    def testIncreasing(self):
        input_list = range(10)
        expect = [9, 8, 7]
        self.assertEqual(expect, MaxNHeap(input_list, 3))

    def testInputLengthEqNum(self):
        num = 10
        input_list = range(num)
        expect = range(num-1, -1, -1)
        self.assertEqual(expect, MaxNHeap(input_list, num))

    def testInputLengthLessThanNum(self):
        num = 10
        input_length = num / 2
        input_list = range(input_length)
        expect = range(input_length-1, -1, -1)
        self.assertEqual(expect, MaxNHeap(input_list, input_length))

    def testMaxN1(self):
        input_list = [2, 4, 3, 1]
        expect = [4, 3]
        self.assertEqual(expect, MaxNHeap(input_list, 2))

    def testMaxN2(self):
        input_list = [5747, 1590, 2539, 540, 
                      5779, 5409, 3281,
                      1353, 987, 1210, 2060, 5041,
                      2580, 5826, 2194, 4013]
        expect = [5826,
                  5779, 5747, 5409, 5041, 4013,
                  3281, 2580, 2539, 2194, 2060,
                  1590, 1353, 1210, 987, 540]
        self.assertEqual(expect, MaxNHeap(input_list, 20))

    def testRandom(self):
        trials = 100
        max_int = 10000
        num = random.randint(1, max_int)
        population = xrange(max_int)
        size = random.randint(10, 1000)
        for _ in xrange(trials):
            input_list = random.sample(population, size)
            expect = sorted(input_list, reverse=True)
            expect = expect[:min(num, len(input_list))]
            self.assertEqual(expect, MaxNHeap(input_list, num))

    def testTime(self):
        trials = 100
        max_int = 10000
        num = random.randint(1, max_int)
        population = xrange(max_int)
        size = 1000
        ctimes = [0, 0]
        for _ in xrange(trials):
            input1 = random.sample(population, size)
            input2 = input1[:]
            t1 = time.time()
            MaxN(input1, num)
            t2 = time.time()
            MaxNHeap(input2, num)
            t3 = time.time()
            ctimes[0] += t2 - t1
            ctimes[1] += t3 - t2
        print 'avg1: {:.3}, avg2: {:.3}'.format(
            *(ctimes[i]/trials for i in xrange(2)))


if __name__ == '__main__':
    unittest2.main()
