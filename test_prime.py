#!/usr/bin/python


import math
import random
import time
import unittest2


class Error(Exception):
    """Base error class."""


def InitStream():

    num = 2
    while True:
        yield num
        num += 1


def RemoveMultipleOf(stream, base):

    for element in stream:
        if element % base:
            yield element


def GetPrime():

    stream = InitStream()
    while True:
        next_prime = stream.next()
        yield next_prime
        stream = RemoveMultipleOf(stream, next_prime)
        

def IsPrime1(number):

    if number < 2:
        raise Error('Invalid number: {}'.format(number))
    if number == 2:
        return True
    if not number % 2:
        return False
    for n in xrange(3, int(math.sqrt(number)+1), 2):
        if not number % n:
            return False
    return True


def IsPrime2(number):

    if number < 2:
        raise Error('Invalid number: {}'.format(number))
    prime_itr = GetPrime()
    next_prime = prime_itr.next()
    max = int(math.sqrt(number)+1)
    while next_prime < max:
        if not number % next_prime:
            return False
        next_prime = prime_itr.next()
    return True


def IsPrime3(number):

    if number < 2:
        raise Error('Invalid number: {}'.format(number))
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        if number == prime:
            return True
        if not number % prime:
            return False
    for n in xrange(29, int(math.sqrt(number)+1), 2):
        if not number % n:
            return False
    return True


class TestPrime(unittest2.TestCase):

    def testInvalid(self):
        self.assertRaises(Error, IsPrime1, 1)
        self.assertRaises(Error, IsPrime2, 0)
        self.assertRaises(Error, IsPrime3, 1)

    def testPrimes10(self):
        prime_itr = GetPrime()
        prime_list = [prime_itr.next() for _ in xrange(10)]
        self.assertEqual([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], prime_list)

    def testTwo(self):
        self.assertTrue(IsPrime1(2))
        self.assertTrue(IsPrime2(2))
        self.assertTrue(IsPrime3(2))

    def testPrime1(self):
        prime_itr = GetPrime()
        prime_list = [prime_itr.next() for _ in xrange(10)]
        for prime in prime_list:
            self.assertTrue(IsPrime1(prime))
            self.assertTrue(IsPrime2(prime))
            self.assertTrue(IsPrime3(prime))
        for not_prime in set(range(2, 30)) - set(prime_list):
            self.assertFalse(IsPrime1(not_prime))
            self.assertFalse(IsPrime2(not_prime))
            self.assertFalse(IsPrime3(not_prime))

    def testPrime2(self):
        prime_list = [3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517]
        for prime in prime_list:
            self.assertTrue(IsPrime1(prime))
            self.assertTrue(IsPrime2(prime))
            self.assertTrue(IsPrime3(prime))
        for not_prime in set(range(3430, 3520)) - set(prime_list):
            self.assertFalse(IsPrime1(not_prime))
            self.assertFalse(IsPrime2(not_prime))
            self.assertFalse(IsPrime3(not_prime))

    def testRandom(self):
        trials = 1000
        max = 1000000
        for _ in xrange(trials):
            num = random.randint(2, max)
            p1, p2, p3 = [func(num) for func in (IsPrime1, IsPrime2, IsPrime3)]
            self.assertEqual(p1, p2)
            self.assertEqual(p1, p3)

    def testTime(self):
        trials = 1000
        max = 1000000
        atimes = [0] * 3
        for _ in xrange(trials):
            num = random.randint(0, max)
            t1 = time.time()
            p1 = IsPrime1(num)
            t2 = time.time()
            p2 = IsPrime2(num)
            t3 = time.time()
            p3 = IsPrime3(num)
            t4 = time.time()
            atimes[0] += t2 - t1
            atimes[1] += t3 - t2
            atimes[2] += t4 - t3
        print 'avg1: {:.3}, avg2: {:.3}, avg3: {:.3}'.format(
            *(atimes[i]/trials for i in xrange(3)))


if __name__ == '__main__':
    unittest2.main()
