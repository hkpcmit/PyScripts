#!/opt/local/bin/pypy


import collections
import sys
import unittest2


sys.setrecursionlimit(300000)


class Knapsack(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = {}
        self.cache = collections.defaultdict(dict) 

    def Add(self, item, value, weight):
        self.items[item] = {'value': value, 'weight': weight}

    def MaxValue(self):
        return self.RecDP(len(self.items), self.capacity)

    def RecDP(self, item, capacity):
        # Implement optimal strategy:
        #   max(self.RecDP(item-1, current capacity),
        #       value(item) + self.RecDP(item-1), current capacity-capacity(item))
        if not item or not capacity:
            return 0
        try:
            return self.cache[item][capacity]
        except KeyError:
            pass
        max_value = self.RecDP(item-1, capacity)
        # Exclude computing the second subproblem if this weight cannot fit within
        # the current capacity. 
        if self.items[item]['weight'] <= capacity:
            max_value = max(max_value,
                            (self.items[item]['value'] +
                             self.RecDP(item-1,
                                        capacity-self.items[item]['weight'])))
        self.cache[item][capacity] = max_value
        return max_value


class KnapsackTest(unittest2.TestCase):

    def AddItems(self, filename):
        with open(filename, 'r') as fd:
            capacity, num_items = fd.readline().split()
            ks = Knapsack(int(capacity))
            for item in range(1, int(num_items)+1):
                value, weight = fd.readline().split()
                ks.Add(item, int(value), int(weight))
        return ks

    def test1(self):
        ks = self.AddItems('knapsack_test1.txt')
        self.assertEqual(8, ks.MaxValue())

    def test2(self):
        ks = self.AddItems('knapsack_test2.txt')
        self.assertEqual(12248, ks.MaxValue())

    def test3(self):
        ks = self.AddItems('knapsack_test3.txt')
        self.assertEqual(142156, ks.MaxValue())

    def testCPHW3(self):
        ks = self.AddItems('cf_hw3.txt')
        self.assertEqual(60, ks.MaxValue())

    def testHW1(self):
        ks = self.AddItems('knapsack1.txt')
        self.assertEqual(2493893, ks.MaxValue())

    def testHW2(self):
        ks = self.AddItems('knapsack_big.txt')
        self.assertEqual(4243395, ks.MaxValue())


if __name__ == '__main__':
    unittest2.main()
