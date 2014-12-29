#!/usr/bin/python


import collections
import itertools
import operator
import unittest2


class Error(Exception):
    """Base error class."""


class UnionFind(object):

    def __init__(self):
        self.groups = {}
        self.leaders = collections.defaultdict(set)
        
    def Add(self, items):
        if items is None:
            raise Error('Invalid items: {}'.format(items))
        if not isinstance(items, list):
            items = [items]
        for item in items:
            self.Find(item)

    def Find(self, item):
        if not isinstance(item, collections.Hashable):
            raise Error('Invalid item: {}'.format(item))
        if item not in self.groups:
            self.groups[item] = item
            self.leaders[item].add(item)
            return item
        return self.groups[item]

    def Join(self, from_leader, to_leader):
        for item in self.leaders[from_leader]:
            self.groups[item] = to_leader
            self.leaders[to_leader].add(item)
        del self.leaders[from_leader]

    def Union(self, item1, item2):
        leader1, leader2 = [self.Find(item) for item in (item1, item2)]
        if leader1 == leader2:
            return
        if len(self.leaders[leader1]) <= len(self.leaders[leader2]):
            self.Join(leader1, leader2)
        else:
            self.Join(leader2, leader1)


class Cluster1(object):

    def __init__(self, k):
        if not isinstance(k, int):
            raise Error('Invalid k: {}'.format(k))
        self.k = k
        self.uf = UnionFind()
        self.edges = []
        
    def Add(self, node1, node2, cost):
        if not isinstance(cost, int):
            raise Error('Invalid cost: {}'.format(cost))
        if not isinstance(node1, int):
            node1 = int(node1)
        if not isinstance(node2, int):
            node2 = int(node2)
        node1, node2 = sorted([node1, node2])
        self.uf.Add([node1, node2])
        self.edges.append((cost, node1, node2))

    def GetClusters(self):
        sorted_edges = sorted(self.edges, reverse=True)
        while len(self.uf.leaders) > self.k:
            _, node1, node2 = sorted_edges.pop()
            self.uf.Union(node1, node2)
        return sorted_edges

    def GetMaxSpacing(self):
        sorted_edges = self.GetClusters()
        results = {'skip_same_cluster': 0}
        max_spacing = None
        while sorted_edges:
            cost, node1, node2 = sorted_edges.pop()
            # Skip if both nodes are in the same cluster.
            if self.uf.Find(node1) == self.uf.Find(node2):
                results['skip_same_cluster'] += 1
                continue
            max_spacing = cost
            break
        results['max_spacing'] = max_spacing
        return results


class BigCluster(object):
    # Convert hamming label to integer/binary.  This is ~10x faster.

    def __init__(self, label_size, min_distance):
        self.uf = UnionFind()
        self.labels = set()
        self.min_distance = min_distance
        self.label_size = label_size

    def Add(self, unused_node, label):
        self.labels.add(self.GetIntLabel(label))

    def GetIntLabel(self, label):
        label_list = label.split()
        result = 0
        for i in label_list:
            result <<= 1
            result += int(i)
        return result

    def GetAllLabelsDistance1(self, label):
        results = []
        for position in range(self.label_size):
            position_bit = 1 << (self.label_size-1-position)
            # Add candidate label if it is larger than the original one.
            # This will avoid duplicate check between (smaller, larger) &
            # (larger, smaller).
            if not (label & position_bit):
                results.append(label | position_bit)
        return results

    def GetAllLabelsDistance2(self, label):
        results = []
        cbs = itertools.combinations(range(self.label_size), 2)
        for position1, position2 in cbs:
            position_bit = 1 << (self.label_size-1-position1)
            # Add candidate label if it is larger than the original one.
            # This will avoid duplicate check between (smaller, larger) &
            # (larger, smaller).
            if label & position_bit:
                continue
            d_label = label
            # Flip the first bit.  The bit in this position is 0.
            d_label |= position_bit
            # Flip second position bit.
            position_bit = 1 << (self.label_size-1-position2)
            if d_label & position_bit:
                d_label -= position_bit
            else:
                d_label |= position_bit
            results.append(d_label)
        return results

    def GetMaxK(self):
        for label in self.labels:
            self.uf.Add(label)
        for get_labels_distance in (self.GetAllLabelsDistance1,
                                   self.GetAllLabelsDistance2):
            self.JoinLabelDistance(get_labels_distance)
        return len(self.uf.leaders)

    def JoinLabelDistance(self, get_labels_distance):
        for label in self.labels:
            for d_label in get_labels_distance(label):
                if d_label in self.labels:
                    self.uf.Union(label, d_label)


class UnionFindTest(unittest2.TestCase):

    def testInvalidFindItem(self):
        with self.assertRaises(Error):
            UnionFind().Find([])

    def testAddInvalidItems(self):
        with self.assertRaises(Error):
            UnionFind().Add(None)

    def testAddSingleItem(self):
        uf = UnionFind()
        item = 1
        uf.Add(item)
        self.assertEqual(uf.Find(item), item)

    def testAddItems(self):
        uf = UnionFind()
        r1 = range(10)
        uf.Add(r1)
        for item in r1:
            self.assertEqual(uf.Find(item), item)

    def testUnionSameGroup(self):
        uf = UnionFind()
        items = [1, 2]
        uf.Union(*items)
        self.assertEqual(uf.Find(items[0]), uf.Find(items[1]))

    def testUnionDiffGroups(self):
        uf = UnionFind()
        uf.Union(1, 2)
        leader = uf.Find(1)
        item = 3
        uf.Union(2, item)
        self.assertEqual(leader, uf.Find(item))
        item = 4
        uf.Union(item, 3)
        self.assertEqual(leader, uf.Find(item))


class Cluster1Test(unittest2.TestCase):
    K = 4

    def testInvalidK(self):
        with self.assertRaises(Error):
            Cluster1(None)

    def testInvalidAddCost(self):
        with self.assertRaises(Error):
            Cluster1(2).Add(1, 2, None)

    def testMaxSpacing1(self):
        c1 = Cluster1(self.K)
        inputs = [(1, 2, 1), (1, 3, 1), (1, 4, 2), (1, 5, 2), (1, 6, 2),
                  (2, 3, 1), (2, 4, 2), (2, 5, 2), (2, 6, 2),
                  (3, 4, 2), (3, 5, 2), (3, 6, 2),
                  (4, 5, 2), (4, 6, 2),
                  (5, 6, 2)]
        for input in inputs:
            c1.Add(*input)
        self.assertEqual(2, c1.GetMaxSpacing()['max_spacing'])

    def testMaxSpacing2(self):
        c1 = Cluster1(self.K)
        inputs = [(1, 2, 91), (1, 3, 6), (1, 4, 31), (1, 5, 53), (1, 6, 15),
                  (1, 7, 35), (1, 8, 83), (1, 9, 69), (1, 10, 78),
                  (2, 3, 98), (2, 4, 58), (2, 5, 46), (2, 6, 52), (2, 7, 55),
                  (2, 8, 74), (2, 9, 3), (2, 10, 34),
                  (3, 4, 42), (3, 5, 4), (3, 6, 22), (3, 7, 84), (3, 8, 32),
                  (3, 9, 74), (3, 10, 4), 
                  (4, 5, 94), (4, 6, 46), (4, 7, 92), (4, 8, 16), (4, 9, 65),
                  (4, 10, 76),
                  (5, 6, 5), (5, 7, 71), (5, 8, 17), (5, 9, 21), (5, 10, 73),
                  (6, 7, 91), (6, 8, 36), (6, 9, 66), (6, 10, 59),
                  (7, 8, 47), (7, 9, 9), (7, 10, 13),
                  (8, 9, 51), (8, 10, 85),
                  (9, 10, 2)]
        for input in inputs:
            c1.Add(*input)
        self.assertEqual(9, c1.GetMaxSpacing()['max_spacing'])

    def testMaxSpacing3(self):
        c1 = Cluster1(self.K)
        inputs = ['1 2 3', '1 3 80', '1 4 88', '1 5 65', '1 6 92',
                  '1 7 50', '1 8 43', '1 9 79', '1 10 67', '1 11 98',
                  '1 12 70',
                  '2 3 23', '2 4 48', '2 5 27', '2 6 74', '2 7 6',
                  '2 8 54', '2 9 73', '2 10 78', '2 11 65', '2 12 6',
                  '3 4 28', '3 5 6', '3 6 38', '3 7 88', '3 8 13',
                  '3 9 25', '3 10 40', '3 11 42', '3 12 52',
                  '4 5 32', '4 6 61', '4 7 23', '4 8 40', '4 9 56',
                  '4 10 36', '4 11 98', '4 12 41',
                  '5 6 23', '5 7 53', '5 8 72', '5 9 97', '5 10 12',
                  '5 11 7', '5 12 33',
                  '6 7 43', '6 8 58', '6 9 75', '6 10 9', '6 11 48',
                  '6 12 53', 
                  '7 8 84', '7 9 72', '7 10 63', '7 11 77', '7 12 76',
                  '8 9 95', '8 10 93', '8 11 84', '8 12 64',
                  '9 10 47', '9 11 51', '9 12 84',
                  '10 11 58', '10 12 21',
                  '11 12 86']
        for input in inputs:
            node1, node2, cost = input.split()
            c1.Add(node1, node2, int(cost))
        results = c1.GetMaxSpacing()
        self.assertEqual(21, results['max_spacing'])

    def testMaxSpacing4(self):
        c1 = Cluster1(self.K)
        inputs = ['1 2 4', '2 3 8', '3 4 7', '4 5 9', '5 6 10',
                  '6 3 4', '6 7 2', '7 8 1', '8 1 8', '8 2 11',
                  '8 9 7', '9 3 2', '9 7 6']
        for input in inputs:
            node1, node2, cost = input.split()
            c1.Add(node1, node2, int(cost))
        results = c1.GetMaxSpacing()
        self.assertEqual(7, results['max_spacing'])

    def testMaxSpacing5(self):
        c1 = Cluster1(3)
        inputs = ['1 2 1', '1 3 10', '1 4 30', '1 5 40',
                  '2 3 1', '2 4 25', '2 5 50',
                  '3 4 60', '3 5 70',
                  '4 5 80']
        for input in inputs:
            node1, node2, cost = input.split()
            c1.Add(node1, node2, int(cost))
        results = c1.GetMaxSpacing()
        self.assertEqual(25, results['max_spacing'])

    def testMaxSpacing6(self):
        c1 = Cluster1(self.K)
        inputs = ['1 2 1', '2 3 4', '3 4 1', '4 5 7', '5 6 1',
                  '6 7 3', '7 8 1', '7 9 2', '8 9 1', '8 1 5']
        for input in inputs:
            node1, node2, cost = input.split()
            c1.Add(node1, node2, int(cost))
        results = c1.GetMaxSpacing()
        self.assertEqual(3, results['max_spacing'])


class Cluster1HWTest(unittest2.TestCase):
    K = 4

    def setUp(self):
        with open('clustering1.txt', 'r') as fd:
            num_nodes = int(fd.readline())
            self.inputs = []
            while True:
                try:
                    node1, node2, cost = fd.readline().split()
                except (StopIteration, ValueError):
                    break
                self.inputs.append((node1, node2, int(cost)))

    def test(self):
        c1 = Cluster1(self.K)
        for input in self.inputs:
            c1.Add(*input)
        results = c1.GetMaxSpacing()
        self.assertEqual(106, results['max_spacing'])


class BigClusterTest(unittest2.TestCase):
    MIN_DISTANCE = 3

    def testCluster1(self):
        with open('test_cluster1.txt', 'r') as fd:
            nodes, label_size = fd.readline().split()
            bc = BigCluster(int(label_size), self.MIN_DISTANCE)
            for i in range(int(nodes)):
                bc.Add(i, fd.readline())
        self.assertEqual(4, bc.GetMaxK())

    def testCluster2(self):
        with open('test_cluster2.txt', 'r') as fd:
            nodes, label_size = fd.readline().split()
            bc = BigCluster(int(label_size), self.MIN_DISTANCE)
            for i in range(int(nodes)):
                bc.Add(i, fd.readline())
        self.assertEqual(45, bc.GetMaxK())

    def testCluster3(self):
        with open('test_cluster3.txt', 'r') as fd:
            nodes, label_size = fd.readline().split()
            bc = BigCluster(int(label_size), self.MIN_DISTANCE)
            for i in range(int(nodes)):
                bc.Add(i, fd.readline())
        self.assertEqual(1, bc.GetMaxK())


class BigClusterHWTest(unittest2.TestCase):
    MIN_DISTANCE = 3

    def test(self):
        with open('clustering_big.txt', 'r') as fd:
            nodes, label_size = fd.readline().split()
            bc = BigCluster(int(label_size), self.MIN_DISTANCE)
            for i in range(int(nodes)):
                bc.Add(i, fd.readline())
        self.assertEqual(6118, bc.GetMaxK())


if __name__ == '__main__':
    unittest2.main()
