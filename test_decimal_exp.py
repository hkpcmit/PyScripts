#!/usr/bin/python
#
# Write a function which, given two integers (a numerator and a denominator), prints
# the decimal representation of the rational number "numerator/denominator". Since all
# rational numbers end with a repeating section, print the repeating section of digits
# inside parentheses.
#
# E.g.
# input: 1, 3 => 0.(3)
#        1, 2 => 0.5(0)
#        1, 7 => 0.(142857)
#        1, 30 => 0.0(3)


import unittest2


class Error(Exception):
    """Base error class."""


class DecimalExp(object):

    def __init__(self, numerator, denominator):
        if not isinstance(numerator, int):
            raise Error('Invalid numerator: {}'.format(numerator))
        if not isinstance(denominator, int) or not denominator:
            raise Error('Invalid denominator: {}'.format(denominator))
        self.numerator = numerator
        self.denominator = denominator

    def Expand(self, numerator):
        numerator_map = {}
        result = []
        position = 0
        while numerator not in numerator_map:
            numerator_map[numerator] = position
            position += 1
            numerator *= 10
            if numerator < self.denominator:
                result.append('0')
                continue
            result.append(str(numerator // self.denominator))
            numerator %= self.denominator
            # Return when there is no more remainder.
            if not numerator:
                return ''.join(result) + '(0)'
        repeat_position = numerator_map[numerator]
        non_repeat = ''.join(result[:repeat_position])
        return non_repeat + '({})'.format(''.join(result[repeat_position:]))

    def Get(self):
        if self.numerator > self.denominator:
            result = '{}.'.format(self.numerator // self.denominator)
        else:
            result = '0.'
        remainder = self.numerator % self.denominator
        if not remainder:
            return result + '(0)'
        return result + self.Expand(remainder)


class DecimalExpTest(unittest2.TestCase):

    def testInvalidNumerator(self):
        with self.assertRaises(Error):
            DecimalExp(None, None)

    def testInvalidDenominator(self):
        with self.assertRaises(Error):
            DecimalExp(1, None)

    def testZeroDenominator(self):
        with self.assertRaises(Error):
            DecimalExp(1, 0)

    def testZeroRepeat(self):
        de = DecimalExp(10, 2)
        self.assertEqual(de.Get(), '5.(0)')

    def testZeroRepeatDecimal(self):
        de = DecimalExp(1, 2)
        self.assertEqual(de.Get(), '0.5(0)')

    def testOneThird(self):
        de = DecimalExp(1, 3)
        self.assertEqual(de.Get(), '0.(3)')

    def test1Over30(self):
        de = DecimalExp(1, 30)
        self.assertEqual(de.Get(), '0.0(3)')

    def test61Over30(self):
        de = DecimalExp(61, 30)
        self.assertEqual(de.Get(), '2.0(3)')

    def testOneSeventh(self):
        de = DecimalExp(1, 7)
        self.assertEqual(de.Get(), '0.(142857)')

    def test35Over99(self):
        de = DecimalExp(35, 99)
        self.assertEqual(de.Get(), '0.(35)')

    def test1Over29(self):
        de = DecimalExp(1, 29)
        self.assertEqual(de.Get(), '0.(0344827586206896551724137931)')

    def test1Over97(self):
        de = DecimalExp(1, 97)
        self.assertEqual(de.Get(),
                         '0.(010309278350515463917525773195876288659793814432989'
                         '690721649484536082474226804123711340206185567)')

    def test1121001Over9990000(self):
        de = DecimalExp(1121001, 9990000)
        self.assertEqual(de.Get(), '0.1122(123)')


if __name__ == '__main__':
    unittest2.main()
