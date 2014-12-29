#!/usr/bin/python
#
# Given two strings, s and t, determine whether any anagram of s occurs as a substring
# of t.


import collections
import unittest2


class Error(Exception):
    """Base error class."""


class AnagramSubStr(object):

    def __init__(self, s, t):
        if (not s or not t or
            not isinstance(s, basestring) or not isinstance(t, basestring)):
            raise Error('Invalid s/t: {}/{}'.format(s, t))
        self.s = s
        self.t = t
        self.s_map = collections.defaultdict(int)
        self.t_map = collections.defaultdict(int)
        self.extras = collections.defaultdict(int)

    def Check(self):
        s_length, t_length = len(self.s), len(self.t)
        if s_length > t_length:
            return False
        for c in self.s:
            self.s_map[c] += 1
        diff = self.GetInitDifference()
        if not diff:
            return True
        position = 1
        while position+s_length <= t_length:
            diff = self.UpdateDifference(position, diff)
            if not diff:
                return True
            position += 1
        return False

    def GetInitDifference(self):
        s_length = len(self.s)
        diff = -s_length
        for c in self.t[:s_length]:
            if c not in self.s_map:
                # Extra character not found in s.
                diff -= 1
                self.extras[c] += 1
            else:
                self.t_map[c] += 1
                if self.t_map[c] <= self.s_map[c]:
                    diff += 1
                else:
                    # Extra character found in s that is not desired.
                    diff -= 1
                    self.extras[c] += 1
        return diff

    def RemoveExtra(self, c):
        self.extras[c] -= 1
        if not self.extras[c]:
            del self.extras[c]

    def UpdateDifference(self, position, diff):
        s_length = len(self.s)
        exit_c = self.t[position-1]
        if exit_c in self.extras:
            diff += 1
            self.RemoveExtra(exit_c)
        else:
            # Exit character is in s.
            diff -= 1
            self.t_map[exit_c] -= 1
        enter_c = self.t[position+s_length-1]
        if enter_c in self.extras or enter_c not in self.s_map:
            # Extra character.
            diff -= 1
            self.extras[enter_c] += 1
        elif self.t_map[enter_c] < self.s_map[enter_c]:
            # Character needed to reduce the difference.
            diff += 1
            self.t_map[enter_c] += 1
        else:
            # Character not needed and is extra.
            diff -= 1
            self.extras[enter_c] += 1
        return diff
        

class AnagramSubStrTest(unittest2.TestCase):

    def testInvalid(self):
        with self.assertRaises(Error):
            AnagramSubStr(None, None)
        with self.assertRaises(Error):
            AnagramSubStr('', '')

    def testGreaterS(self):
        a = AnagramSubStr('12', '1')
        self.assertFalse(a.Check())

    def testSameLengths(self):
        a = AnagramSubStr('31', '13')
        self.assertTrue(a.Check())

    def testSameLengthsNoAnagram(self):
        a = AnagramSubStr('31', '43')
        self.assertFalse(a.Check())

    def testStartAnagram(self):
        a = AnagramSubStr('21', '123')
        self.assertTrue(a.Check())

    def testEndAnagram(self):
        a = AnagramSubStr('ab', '3ba')
        self.assertTrue(a.Check())

    def testEndAnagram(self):
        a = AnagramSubStr('2a', '31a2b')
        self.assertTrue(a.Check())

    def testExtra1(self):
        a = AnagramSubStr('2a2', '3122a2b')
        self.assertTrue(a.Check())

    def testExtra2(self):
        a = AnagramSubStr('2a2', '312aa2a2b')
        self.assertTrue(a.Check())

    def testExtra3(self):
        a = AnagramSubStr('2a2a', '31caa2a2b')
        self.assertTrue(a.Check())


if __name__ == '__main__':
    unittest2.main()
