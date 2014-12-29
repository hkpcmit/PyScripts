#!/usr/bin/python


import heapq
import random
import time
import unittest2


class Error(Exception):
    """Base error class."""


class MinHeap(object):

    def __init__(self):
        self.heap = []

    def Push(self, item):
        heapq.heappush(self.heap, item)

    def Pop(self):
        try:
            return heapq.heappop(self.heap)
        except IndexError:
            raise Error('Empty heap.')

    def Top(self):
        try:
            return self.heap[0]
        except IndexError:
            raise Error('Empty heap.')

    @property
    def length(self):
        return len(self.heap)


class MaxHeap(MinHeap):

    def Push(self, item):
        super(MaxHeap, self).Push(-item)

    def Pop(self):
        return -1 * super(MaxHeap, self).Pop()

    def Top(self):
        return -1 * super(MaxHeap, self).Top()


class Median(object):

    def __init__(self):
        self.median = None
        self.left = MaxHeap()
        self.right = MinHeap()

    def UpdateMedian(self):
        if self.left.length < self.right.length:
            self.median = self.right.Top()
        else:
            self.median = self.left.Top()

    def Add(self, number):
        if not isinstance(number, int):
            raise Error('Invalid number: {}'.format(number))
        # Always ensure abs(length of right heap - length of left) <= 1.
        if self.median is None:
            self.median = number
            self.right.Push(number)
            return
        if number < self.median:
            if self.left.length > self.right.length:
                self.right.Push(self.left.Pop())
            self.left.Push(number)
        else:
            if self.right.length > self.left.length:
                self.left.Push(self.right.Pop())
            self.right.Push(number)
        self.UpdateMedian()
        
    def Get(self):
        if self.median is None:
            raise Error('No median.')
        return self.median


class TestMedian(unittest2.TestCase):

    def GetMedian(self, input_list):
        sorted_list = sorted(input_list)
        length = len(input_list)
        half_length = length / 2
        if length % 2:
            return sorted_list[half_length]
        return sorted_list[half_length-1]

    def testInvalidAdd(self):
        median = Median()
        self.assertRaises(Error, median.Add, None)

    def testNoMedian(self):
        median = Median()
        self.assertRaises(Error, median.Get)

    def testDecreasing(self):
        median = Median()
        input_list = range(10, -1, -1)
        for i, input in enumerate(input_list):
            median.Add(input)
            self.assertEqual(self.GetMedian(input_list[:i+1]), median.Get())

    def testIncreasing(self):
        median = Median()
        input_list = range(10)
        for i, input in enumerate(input_list):
            median.Add(input)
            self.assertEqual(self.GetMedian(input_list[:i+1]), median.Get())

    def testRandom(self):
        trials = 1000
        size = 100
        for _ in xrange(trials):
            median = Median()
            input_list = [random.randint(0, 1000000) for _ in xrange(size)]
            for i, input in enumerate(input_list):
                median.Add(input)
                self.assertEqual(self.GetMedian(input_list[:i+1]), median.Get())

    def testTime(self):
        trials = 1000
        size = 100
        for _ in xrange(trials):
            median = Median()
            input_list = [random.randint(0, 1000000) for _ in xrange(size)]
            atimes = [0, 0]
            for i, input in enumerate(input_list):
                t1 = time.time()
                self.GetMedian(input_list[:i+1])
                t2 = time.time()
                median.Add(input)
                t3 = time.time()
                atimes[0] += t2 - t1
                atimes[1] += t3 - t2
        print 'avg1: {:.3}, avg2: {:.3}'.format(*(atimes[i] / trials for i in (0, 1)))


class TestMinHeap(unittest2.TestCase):

    def testEmpty(self):
        heap = MinHeap()
        self.assertRaises(Error, heap.Top)
        self.assertRaises(Error, heap.Pop)

    def testPush(self):
        heap = MinHeap()
        input_list = range(10, -1, -1)
        for input in input_list:
            heap.Push(input)
            self.assertEqual(input, heap.Top())

    def testPop(self):
        heap = MinHeap()
        input_list = range(10, -1, -1)
        for input in input_list:
            heap.Push(input)
        pop_list = [heap.Pop() for _ in xrange(len(input_list))]
        self.assertEqual(sorted(input_list), pop_list)


class TestMaxHeap(unittest2.TestCase):

    def testEmpty(self):
        heap = MaxHeap()
        self.assertRaises(Error, heap.Top)
        self.assertRaises(Error, heap.Pop)

    def testPush(self):
        heap = MaxHeap()
        input_list = range(10)
        for input in input_list:
            heap.Push(input)
            self.assertEqual(input, heap.Top())

    def testPop(self):
        heap = MaxHeap()
        input_list = range(10)
        for input in input_list:
            heap.Push(input)
        pop_list = [heap.Pop() for _ in xrange(len(input_list))]
        input_list.reverse()
        self.assertEqual(input_list, pop_list)


class HWTest(unittest2.TestCase):

    def setUp(self):
        with open('Median.txt', 'r') as fd:
            self.input = [int(line) for line in fd]

    def testSum(self):
        median = Median()
        sum = 0
        for inp in self.input:
            median.Add(inp)
            sum += median.Get()
        print 'sum mod 10000: {}'.format(sum % 10000)


if __name__ == '__main__':
    unittest2.main()
