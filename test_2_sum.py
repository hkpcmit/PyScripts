#!/usr/bin/python


import bisect
import collections
import unittest2


class Error(Exception):
    """Base error class."""


class TwoSum(object):

    def __init__(self):
        self.numbers = set()

    def Add(self, number):
        if not isinstance(number, int):
            raise Error('Invalid number: {}'.format(number))
        self.numbers.add(number)

    def Has2Sum(self, target):
        if not isinstance(target, int):
            raise Error('Invalid target: {}'.format(target))
        for number in self.numbers:
            complement = target - number
            if complement == number:
                continue
            if complement in self.numbers:
                return True
        return False


class TwoSumTargets(object):

    def __init__(self, min_target, max_target):
        if min_target >= max_target:
            raise Error('Invalid min/max_targets: {}/{}'.format(min_target, max_target))
        self.min_target = min_target
        self.max_target = max_target
        self.target_range = max_target - min_target
        self.numbers = collections.defaultdict(set)

    def Add(self, number):
        if not isinstance(number, int):
            raise Error('Invalid number: {}'.format(number))
        self.numbers[self.Hash(number)].add(number)

    def TargetSet(self):
        result = {
            'Number of buckets': len(self.numbers),
            'Max bucket size': max(
                len(numbers) for numbers in self.numbers.values())}
        total_numbers, total_sums, total_complement_hashes = 0, 0, 0
        numbers = self.numbers.copy()
        targets = set()
        for hsh in numbers.keys():
            number_set = numbers[hsh]
            for number in number_set:
                total_numbers += 1
                # Compute low and upper bounds of the complement.
                complement_low = self.min_target - number
                complement_high = self.max_target - number
                for complement_hash in range(
                    self.Hash(complement_low), self.Hash(complement_high)+1):
                    total_complement_hashes += 1
                    # Skip if no bucket for complement exists.
                    if complement_hash not in numbers:
                        continue
                    for complement in numbers[complement_hash]:
                        # Skip duplicate pairs.
                        if number == complement:
                            continue
                        t = number + complement
                        total_sums += 1
                        if self.min_target <= t <= self.max_target:
                            targets.add(t)
            # This number set has been checked and can be skipped in future comparison.
            del numbers[hsh]
        result['Number of targets'] = len(targets)
        result['Total numbers'] = total_numbers
        result['Avg sums'] = round(float(total_sums)/total_numbers, 2)
        result['Avg complement hashes'] = round(
            float(total_complement_hashes)/total_numbers, 2)
        return result

    def Hash(self, number):
        return number // self.target_range
                

class TwoSumTest(unittest2.TestCase):
    
    def testAddInvalidNumber(self):
        with self.assertRaises(Error):
            TwoSum().Add(None)            
    
    def testHas2SumInvalidTarget(self):
        with self.assertRaises(Error):
            TwoSum().Has2Sum(None)

    def testHasSum1(self):
        ts = TwoSum()
        for number in range(2):
            ts.Add(number)
        self.assertFalse(ts.Has2Sum(2))

    def testHasSum2(self):
        ts = TwoSum()
        for number in xrange(10):
            ts.Add(number)
        self.assertTrue(ts.Has2Sum(10))

    def testHasSum3(self):
        ts = TwoSum()
        for number in xrange(100):
            ts.Add(number)
        self.assertFalse(ts.Has2Sum(-2))

    def testHasSum4(self):
        ts = TwoSum()
        for number in xrange(-100, 1):
            ts.Add(number)
        self.assertFalse(ts.Has2Sum(32))

    def testHasSum5(self):
        ts = TwoSum()
        for number in xrange(-100, 101):
            ts.Add(number)
        self.assertTrue(ts.Has2Sum(0))


class HWTest(unittest2.TestCase):

    def setUp(self):
        self.ts = TwoSum()
        with open('algo1_programming_prob_2sum.txt', 'r') as fd:
            for line in fd:
                self.ts.Add(int(line))

    def test(self):
        target_list = [target for target in xrange(-10000, 10001)
                       if self.ts.Has2Sum(target)]
        print 'Number of targets: {}'.format(len(target_list))
        

class TwoSumTargetsTest(unittest2.TestCase):

    def test(self):
        self.ts = TwoSumTargets(-10000, 10000)
        with open('algo1_programming_prob_2sum.txt', 'r') as fd:
            for line in fd:
                self.ts.Add(int(line))
        print 'Result: {}'.format(self.ts.TargetSet())
        

class TwoSumSortTest(unittest2.TestCase):
    MIN_TARGET = -10000
    MAX_TARGET = 10000

    def test(self):
        with open('algo1_programming_prob_2sum.txt', 'r') as fd:
            input_set = set(int(line) for line in fd)
        sort_list = sorted(input_set)
        total_numbers = len(sort_list)
        result = {'Total numbers': total_numbers}
        targets = set()
        max_complement_range, total_complement_ranges, total_sums = 0, 0, 0
        for number in sort_list:
            # Compute lower and upper bounds of complements based on min/max
            # targets.
            min_complement = self.MIN_TARGET - number
            max_complement = self.MAX_TARGET - number
            # Find min_idx such that min_complement <= sort_list[min_idx]. In
            # other words, consider valid possible complements starting from
            # sort_list[min_idx].
            min_idx = bisect.bisect_left(sort_list, min_complement)
            max_idx = bisect.bisect_right(sort_list, max_complement)
            complement_range = max_idx - min_idx
            max_complement_range = max(max_complement_range, complement_range)
            total_complement_ranges += complement_range
            # Iterate over valid possible complements within input set.
            for idx in range(min_idx, max_idx):
                # sort_list[idx] is a candidate complement.  Skip duplicate pair.
                if sort_list[idx] == number:
                    continue
                target = number + sort_list[idx]
                total_sums += 1
                targets.add(target)
        result['Number of targets'] = len(targets)
        result['Avg complement range'] = round(
            float(total_complement_ranges)/total_numbers, 2)
        result['Max complement range'] = max_complement_range
        result['Avg sums'] = round(float(total_sums)/total_numbers, 2)
        print 'Result: {}'.format(result)


if __name__ == '__main__':
    unittest2.main()
