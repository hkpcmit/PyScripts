#!/usr/bin/python

import collections
import unittest2


class Error(Exception):
    """Base error class."""


class PeekIter(object):

    def __init__(self, it):
        if not isinstance(it, collections.Iterable):
            raise Error('Invalid it: {}'.format(it))
        self.it = iter(it)
        self.GetNext()

    def __iter__(self):
        return self

    def next(self):
        if self.peek is None:
            raise StopIteration
        result = self.peek
        self.GetNext()
        return result

    def GetNext(self):
        try:
            self.peek = self.it.next()
        except StopIteration:
            self.peek = None

    def Peek(self):
        return self.peek


class TestPeekIter(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, PeekIter, None)

    def testEmpty(self):
        peek_iter = PeekIter([])
        self.assertEqual(None, peek_iter.Peek())
        self.assertRaises(StopIteration, peek_iter.next)

    def testSingle(self):
        single = 1
        peek_iter = PeekIter((single,))
        self.assertEqual(single, peek_iter.Peek())
        self.assertListEqual([single], [element for element in peek_iter])
        self.assertEqual(None, peek_iter.Peek())
        self.assertRaises(StopIteration, peek_iter.next)

    def testMultiple(self):
        lst = range(1, 4)
        peek_iter = PeekIter(lst)
        self.assertEqual(1, peek_iter.Peek())
        self.assertEqual(1, peek_iter.next())
        self.assertEqual(2, peek_iter.Peek())
        self.assertEqual(2, peek_iter.next())
        self.assertEqual(3, peek_iter.Peek())
        self.assertEqual(3, peek_iter.next())
        self.assertEqual(None, peek_iter.Peek())
        self.assertRaises(StopIteration, peek_iter.next)

    def testIterable(self):
        lst = range(10)
        peek_iter = PeekIter(lst)
        self.assertListEqual(lst, [element for element in peek_iter])


if __name__ == '__main__':
    unittest2.main()
