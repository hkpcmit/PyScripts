#!/usr/bin/python


import random
from test_memoize import Memoize
import time
import unittest2


class Error(Exception):
    """Base error class."""


@Memoize
def CountSet1(number):

    if not isinstance(number, int):
        raise Error('Invalid number: {}'.format(number))
    if not number:
        return 0
    count = 0
    while number:
        count += number & 0x1
        number >>= 1
    return count


def CountSet2(number):

    if not isinstance(number, int):
        raise Error('Invalid number: {}'.format(number))
    if not number:
        return 0
    count_map = {0: 0,
                 1: 1,
                 2: 1,
                 3: 2,
                 4: 1,
                 5: 2,
                 6: 2,
                 7: 3,
                 8: 1,
                 9: 2,
                 10: 2,
                 11: 3,
                 12: 2,
                 13: 3,
                 14: 3,
                 15: 4}
    count = 0
    while number:
        count += count_map[number % 16]
        number >>= 4
    return count


def CountSet3(number):

    if not isinstance(number, int):
        raise Error('Invalid number: {}'.format(number))
    if not number:
        return 0
    count = 0
    while number:
        count += CountSet1(number % 256)
        number >>= 8
    return count
    


class TestCountSet(unittest2.TestCase):

    def setUp(self):
        self.test_func = CountSet3

    def testInvalidNumber(self):
        self.assertRaises(Error, self.test_func, None)

    def testZero(self):
        self.assertEqual(0, self.test_func(0))

    def testCountOdd(self):
        self.assertEqual(1, self.test_func(1))
        self.assertEqual(2, self.test_func(3))
        self.assertEqual(2, self.test_func(5))
        self.assertEqual(3, self.test_func(7))
        self.assertEqual(2, self.test_func(9))
        self.assertEqual(3, self.test_func(11))
        self.assertEqual(3, self.test_func(13))
        self.assertEqual(4, self.test_func(15))

    def testCountEven(self):
        self.assertEqual(1, self.test_func(2))
        self.assertEqual(1, self.test_func(4))
        self.assertEqual(2, self.test_func(6))
        self.assertEqual(1, self.test_func(8))
        self.assertEqual(2, self.test_func(10))
        self.assertEqual(2, self.test_func(12))
        self.assertEqual(3, self.test_func(14))

    def testCountLarge(self):
        self.assertEqual(4, self.test_func(0xe8))
        self.assertEqual(9, self.test_func(0x6cba))

    def testRandom(self):
        trials = 1000
        max = 1000000
        for _ in xrange(trials):
            num = random.randint(0, max)
            s1 = CountSet1(num)
            s2 = CountSet2(num)
            s3 = CountSet3(num)
            self.assertEqual(s1, s2)
            self.assertEqual(s2, s3)

    def testTime(self):
        trials = 1000
        max = 1000000
        atimes = [0] * 3
        for _ in xrange(trials):
            num = random.randint(0, max)
            t1 = time.time()
            s1 = CountSet1(num)
            t2 = time.time()
            s2 = CountSet2(num)
            t3 = time.time()
            s3 = CountSet3(num)
            t4 = time.time()
            atimes[0] += t2 - t1
            atimes[1] += t3 - t2
            atimes[2] += t4 - t3
        print 'avg1: {:.3}, avg2: {:.3}, avg3: {:.3}'.format(
            *(atimes[i]/1000 for i in xrange(3)))


if __name__ == '__main__':
    unittest2.main()
