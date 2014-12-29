#!/usr/bin/python


import random
import unittest2


class Error(Exception):
    """Base error class."""


def HasTriangleNumbers1(input_list):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if len(input_list) < 3:
        return False
    input_list.sort(reverse=True)
    for i, element in enumerate(input_list[:len(input_list)-2]):
        if (input_list[i+1] + input_list[i+2]) > element:
            return True
    return False
        

def HasTriangleNumbers2(input_list):

    if not isinstance(input_list, list):
        raise Error('Invalid input_list: {}'.format(input_list))
    if len(input_list) < 3:
        return False
    input_list.sort()
    input_length = len(input_list)
    for i, element in enumerate(input_list[:input_length-2]):
        for j in xrange(i+1, input_length-1):
            if (element + input_list[j]) > input_list[j+1]:
                return True
    return False


class TestTriangleNumbers(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, HasTriangleNumbers1, None)
        self.assertRaises(Error, HasTriangleNumbers2, None)

    def testEmpty(self):
        input_list = []
        self.assertFalse(HasTriangleNumbers1(input_list))
        self.assertFalse(HasTriangleNumbers2(input_list))

    def testSingle(self):
        input_list = [1]
        self.assertFalse(HasTriangleNumbers1(input_list))
        self.assertFalse(HasTriangleNumbers2(input_list))

    def testDouble(self):
        input_list = range(2)
        self.assertFalse(HasTriangleNumbers1(input_list))
        self.assertFalse(HasTriangleNumbers2(input_list))

    def testInputList1(self):
        input_list = range(1, 4)
        self.assertFalse(HasTriangleNumbers1(input_list))
        self.assertFalse(HasTriangleNumbers2(input_list))

    def testInputList2(self):
        input_list = [3, 11, 10, 2]
        self.assertTrue(HasTriangleNumbers1(input_list))
        self.assertTrue(HasTriangleNumbers2(input_list))

    def testLarge(self):
        max_int = 100000
        max_size = 1000
        population = xrange(max_int)
        num = 1000
        for _ in xrange(num):
            input_list = random.sample(population, random.randint(3, max_size))
            self.assertEqual(HasTriangleNumbers1(input_list),
                             HasTriangleNumbers2(input_list))


if __name__ == '__main__':
    unittest2.main()
