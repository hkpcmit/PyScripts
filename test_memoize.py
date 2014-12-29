#!/opt/local/bin/pypy


import cPickle
import functools
import unittest2


class Memoize(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = cPickle.dumps(args, 2) + cPickle.dumps(kwargs, 2)
        try:
            return self.cache[key]
        except KeyError:
            self.cache[key] = self.func(*args, **kwargs)
            return self.cache[key]

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, unused_objtype):
        return functools.partial(self.__call__, obj)


class TestMemoize(unittest2.TestCase):

    def testMemoize1(self):
        value = 1
        
        @Memoize
        def func1():
            return value

        def func2():
            return value

        self.assertEqual(1, func1())
        value = 2
        self.assertEqual(1, func1())
        self.assertEqual(2, func2())

    def testMemoize2(self):
        value = 1
        
        @Memoize
        def func1(a1, a2='1'):
            return value

        def func2(a1, a2='1'):
            return value

        self.assertEqual(1, func1(0, a2='2'))
        value = 2
        self.assertEqual(1, func1(0, a2='2'))
        self.assertEqual(2, func2(0, a2='2'))


if __name__ == '__main__':
    unittest2.main()
