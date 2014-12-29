#!/opt/local/bin/pypy
#
# Optimal binary tree:
#   Frequency:
#     W1: 0.05
#     W2: 0.4
#     W3: 0.08
#     W4: 0.04
#     W5: 0.1
#     W6: 0.1
#     W7: 0.23


import collections
import unittest2


class OBT(object):

    def __init__(self, freq):
        self.freq = freq
        self.a = collections.defaultdict(dict)

    def Compute(self):
        max_idx = len(self.freq) - 1
        for s in range(max_idx):
            for i in range(1, max_idx+1):
                if i+s > max_idx:
                    continue
                freq_sum = sum(self.freq[i:i+s+1])
                costs = []
                for root in range(i, i+s+1):
                    cost = freq_sum
                    try:
                        cost += self.a[i][root-1]
                    except KeyError:
                        pass
                    try:
                        cost += self.a[root+1][i+s]
                    except KeyError:
                        pass
                    costs.append(cost)
                self.a[i][i+s] = round(min(costs), 2)

    def GetMinCost(self, i, j):
        return self.a[i][j]


class OBTTest(unittest2.TestCase):
    
    def setUp(self):
        self.freq = [0, 0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
        self.obt = OBT(self.freq)
        self.obt.Compute()

    def test1(self):
        for i in range(1, len(self.freq)-1):
            self.assertEqual(self.freq[i], self.obt.GetMinCost(i, i))

    def test2(self):
        self.assertEqual(0.5, self.obt.GetMinCost(1, 2))

    def test3(self):
        self.assertEqual(0.43, self.obt.GetMinCost(6, 7))

    def test4(self):
        self.assertEqual(0.18, self.obt.GetMinCost(4, 5))

    def test5(self):
        self.assertEqual(2.18, self.obt.GetMinCost(1, 7))


class OBTFinalTest(unittest2.TestCase):
    
    def setUp(self):
        self.freq = [0, 0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25]
        self.obt = OBT(self.freq)
        self.obt.Compute()

    def test1(self):
        self.assertEqual(2.23, self.obt.GetMinCost(1, 7))


if __name__ == '__main__':
    unittest2.main()
