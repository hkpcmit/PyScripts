#!/usr/bin/python

import unittest


def CountChange(value, denomination):
    cache = {}
    denomination = sorted(denomination)

    def _CountChangeRec(val, index):
        if index < 0:
            return 0
        key = '{}-{}'.format(val, index)
        if key in cache:
            return cache[key]
        if not val:
            cache[key] = 0
            return 0
        if val < denomination[index]:
            cache[key] = _CountChangeRec(val, index-1)
            return cache[key]
        if val == denomination[index]:
            cache[key] = 1 + _CountChangeRec(val, index-1)
            return cache[key]
        # At this point, val > denomination[index]
        cache[key] = (_CountChangeRec(val-denomination[index], index) +
                      _CountChangeRec(val, index-1))
        return cache[key]
            
    return _CountChangeRec(value, len(denomination)-1)


class CountTest(unittest.TestCase):

    def testExample(self):
        self.assertEqual(3, CountChange(4, [1, 2]))

    def testSortedCount(self):
        self.assertEqual(
            1022,
            CountChange(300, [5, 10, 20, 50, 100, 200, 500]))

    def testNoPennies(self):
        self.assertEqual(
            0,
            CountChange(301, [5, 10, 20, 50, 100, 200, 500]))

    def testUnsortedCount(self):
        self.assertEqual(
            1022,
            CountChange(300, [500, 5, 50, 100, 20, 200, 10]))


if __name__ == '__main__':
    unittest.main()
