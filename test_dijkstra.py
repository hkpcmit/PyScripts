#!/opt/local/bin/pypy


import collections
import heapq
import sys
import unittest2


class Error(Exception):
    """Error class for this module."""


class Adjacency(object):

    def __init__(self, neighbor, cost):
        self.neighbor = neighbor
        self.cost = cost


class SPInfo(object):

    def __init__(self, node, dist=sys.maxint, pred=None):
        self.node = node
        self.dist = dist
        self.pred = pred

    def __cmp__(self, that):
        this_info = (self.node, self.dist, self.pred)
        that_info = (that.node, that.dist, that.pred)
        return cmp(this_info, that_info)


class Dijkstra(object):
    
    def __init__(self):
        self.graph = collections.defaultdict(list)
        self.sp_info_map = {}
        self.heap = []
        self.shortest_distances = {}

    def AddAdjacency(self, node, neighbor=None, cost=None):
        if neighbor is None:
            self.graph[node] = []
            return
        self.graph[node].append(Adjacency(neighbor, cost))

    def GetSP(self, node):
        if node not in self.graph:
            raise Error('Invalid node: {}'.format(node))
        self.shortest_distances, self.sp_info_map = {}, {}
        self.sp_info_map[node] = SPInfo(node, dist=0)
        # Initialize the heap.
        self.heap = [(0, self.sp_info_map[node])]
        while self.heap:
            _, sp_info = heapq.heappop(self.heap)
            this_node = sp_info.node
            if this_node in self.shortest_distances:
                continue
            self.shortest_distances[this_node] = sp_info
            for adj in self.graph[this_node]:
                neighbor = adj.neighbor
                if neighbor in self.shortest_distances:
                    continue
                neighbor_dist = sp_info.dist + adj.cost
                if ((neighbor not in self.sp_info_map) or 
                    (neighbor_dist < self.sp_info_map[neighbor].dist)):
                    self.sp_info_map[neighbor] = SPInfo(
                        neighbor, dist=neighbor_dist, pred=this_node)
                    heapq.heappush(self.heap,
                                   (neighbor_dist, self.sp_info_map[neighbor]))
        return self.shortest_distances
                    
                            
class DijkstraTest(unittest2.TestCase):
    
    def testGetSPInvalidNode(self):
        with self.assertRaises(Error):
            Dijkstra().GetSP(None)

    def testSingleNode(self):
        dk = Dijkstra()
        dk.AddAdjacency(0)
        res = dk.GetSP(0)
        self.assertEqual(res[0], SPInfo(0, dist=0))

    def testSP1(self):
        dk = Dijkstra()
        dk.AddAdjacency(0, 1, 1)
        dk.AddAdjacency(1, 0, 1)
        dk.AddAdjacency(0, 2, 3)
        dk.AddAdjacency(2, 3, 3)
        dk.AddAdjacency(1, 2, 1)
        dk.AddAdjacency(2, 1, 1)
        res = dk.GetSP(0)
        self.assertEqual(res[0], SPInfo(0, dist=0))
        self.assertEqual(res[1], SPInfo(1, dist=1, pred=0))
        self.assertEqual(res[2], SPInfo(2, dist=2, pred=1))
        res = dk.GetSP(1)
        self.assertEqual(res[0], SPInfo(0, dist=1, pred=1))
        self.assertEqual(res[1], SPInfo(1, dist=0))
        self.assertEqual(res[2], SPInfo(2, dist=1, pred=1))
        res = dk.GetSP(2)
        self.assertEqual(res[0], SPInfo(0, dist=2, pred=1))
        self.assertEqual(res[1], SPInfo(1, dist=1, pred=2))
        self.assertEqual(res[2], SPInfo(2, dist=0))

    def testSP2(self):
        dk = Dijkstra()
        dk.AddAdjacency(0, 1, 1)
        dk.AddAdjacency(0, 2, 4)
        dk.AddAdjacency(1, 0, 1)
        dk.AddAdjacency(1, 2, 2)
        dk.AddAdjacency(1, 3, 5)
        dk.AddAdjacency(2, 0, 4)
        dk.AddAdjacency(2, 1, 2)
        dk.AddAdjacency(2, 3, 1)
        dk.AddAdjacency(3, 1, 5)
        dk.AddAdjacency(3, 2, 1)
        dk.AddAdjacency(10, 11, 1)
        dk.AddAdjacency(11, 10, 1)
        res = dk.GetSP(0)
        self.assertEqual(res[0], SPInfo(0, dist=0))
        self.assertEqual(res[1], SPInfo(1, dist=1, pred=0))
        self.assertEqual(res[2], SPInfo(2, dist=3, pred=1))
        self.assertEqual(res[3], SPInfo(3, dist=4, pred=2))
        for node in (10, 11):
            self.assertNotIn(node, res)
        res = dk.GetSP(1)
        self.assertEqual(res[0], SPInfo(0, dist=1, pred=1))
        self.assertEqual(res[1], SPInfo(1, dist=0))
        self.assertEqual(res[2], SPInfo(2, dist=2, pred=1))
        self.assertEqual(res[3], SPInfo(3, dist=3, pred=2))
        for node in (10, 11):
            self.assertNotIn(node, res)
        res = dk.GetSP(2)
        self.assertEqual(res[0], SPInfo(0, dist=3, pred=1))
        self.assertEqual(res[1], SPInfo(1, dist=2, pred=2))
        self.assertEqual(res[2], SPInfo(2, dist=0))
        self.assertEqual(res[3], SPInfo(3, dist=1, pred=2))
        for node in (10, 11):
            self.assertNotIn(node, res)
        res = dk.GetSP(3)
        self.assertEqual(res[0], SPInfo(0, dist=4, pred=1))
        self.assertEqual(res[1], SPInfo(1, dist=3, pred=2))
        self.assertEqual(res[2], SPInfo(2, dist=1, pred=3))
        self.assertEqual(res[3], SPInfo(3, dist=0))
        for node in (10, 11):
            self.assertNotIn(node, res)


    def testSP3(self):
        dk = Dijkstra()
        dk.AddAdjacency(1, 2, 7)
        dk.AddAdjacency(1, 3, 9)
        dk.AddAdjacency(1, 6, 14)
        dk.AddAdjacency(2, 1, 7)
        dk.AddAdjacency(2, 3, 10)
        dk.AddAdjacency(2, 4, 15)
        dk.AddAdjacency(3, 1, 9)
        dk.AddAdjacency(3, 2, 10)
        dk.AddAdjacency(3, 4, 11)
        dk.AddAdjacency(3, 6, 2)
        dk.AddAdjacency(4, 2, 15)
        dk.AddAdjacency(4, 3, 11)
        dk.AddAdjacency(4, 5, 6)
        dk.AddAdjacency(5, 4, 6)
        dk.AddAdjacency(5, 6, 9)
        dk.AddAdjacency(6, 1, 14)
        dk.AddAdjacency(6, 3, 2)
        dk.AddAdjacency(6, 5, 9)
        res = dk.GetSP(1)
        self.assertEqual(res[1], SPInfo(1, dist=0))
        self.assertEqual(res[2], SPInfo(2, dist=7, pred=1))
        self.assertEqual(res[3], SPInfo(3, dist=9, pred=1))
        self.assertEqual(res[4], SPInfo(4, dist=20, pred=3))
        self.assertEqual(res[5], SPInfo(5, dist=20, pred=6))
        self.assertEqual(res[6], SPInfo(6, dist=11, pred=3))

class HWTest(unittest2.TestCase):
    INFINITE = 1000000

    def setUp(self):
        self.dk = Dijkstra()
        with open('dijkstraData.txt', 'r') as fd:
            for line in fd:
                rec = line.split()
                node = int(rec[0])
                for adj in rec[1:]:
                    neighbor, cost = [int(e) for e in adj.split(',')]
                    self.dk.AddAdjacency(node, neighbor, cost)
        self.assertEqual(len(self.dk.graph), 200)

    def testHW(self):
        res = self.dk.GetSP(1)
        node_list = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
        dist_list = [str(res[node].dist if node in res else self.INFINITE)
                     for node in node_list]
        print 'Answer: {}'.format(','.join(dist_list))
            

if __name__ == '__main__':
    unittest2.main()
