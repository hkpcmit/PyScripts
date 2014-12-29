#!/opt/local/bin/pypy


import collections
import test_dijkstra
import unittest2


class Error(Exception):
    """Base error class."""


class NegativeCycleError(Error):
    """Negative cycle error."""


class BellmanFord(object):

    def __init__(self):
        self.graph = collections.defaultdict(dict)
        # Track incoming edges.
        self.in_nodes = collections.defaultdict(list)
        self.prev_a, self.current_a = None, {}
        self.prev_pred, self.current_pred = None, {}

    def Add(self, node1, node2, cost):
        self.graph[node1][node2] = cost
        if node2 not in self.graph:
            self.graph[node2] = {}
        self.in_nodes[node2].append(node1)

    def GetNegativeCycle(self):
        start_node = None
        for node in self.current_a:
            if self.prev_a[node] != self.current_a[node]:
                repeat = set([node])
                start_node = node
                break
        # The start_node may not be part of the cycle.  Find the first node in
        # the cycle.
        node = start_node
        while self.current_pred[node] not in repeat:
            pred_node = self.current_pred[node]
            repeat.add(pred_node)
            node = pred_node
        start_node = node
        cycle_list = [start_node]
        cycle = set(cycle_list)
        cost = 0
        while self.current_pred[node] not in cycle:
            pred_node = self.current_pred[node]
            cycle.add(pred_node)
            cycle_list.append(pred_node)
            cost += self.graph[pred_node][node]
            node = pred_node
        cost += self.graph[self.current_pred[node]][node]
        return '<-'.join(str(node) for node in cycle_list), cost

    def ShortestPaths(self, source):
        self.current_a[source] = 0
        self.current_pred[source] = None
        for _ in range(1, len(self.graph)+1):
            self.prev_a, self.prev_pred = self.current_a, self.current_pred
            self.SPIteration(source)
            # Stop early if no change in this iteration.
            if self.prev_a == self.current_a:
                return self.current_a
        raise NegativeCycleError(
            'cycle: {}; cost: {}'.format(*self.GetNegativeCycle()))

    def SPIteration(self, source):
        self.current_a = {}
        for node in self.graph:
            try:
                cost_list = [(self.prev_a[node], self.prev_pred[node])]
            except KeyError:
                cost_list = []
            for in_node in self.in_nodes[node]:
                if in_node in self.prev_a:
                    cost_list.append(
                        (self.prev_a[in_node]+self.graph[in_node][node], in_node))
            if cost_list:
                self.current_a[node], self.current_pred[node] = min(cost_list)


class FloydWarshall(object):

    def __init__(self):
        self.nodes = set()
        self.current_a = collections.defaultdict(dict)

    def Add(self, node1, node2, cost):
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.current_a[node1][node1] = 0
        self.current_a[node2][node2] = 0
        self.current_a[node1][node2] = cost

    def GetSSP(self):
        self.ShortestPaths()
        return min(min(node_info.values())
                   for node_info in self.current_a.values())

    def ShortestPaths(self):
        for k in self.nodes:
            prev_a = self.current_a
            self.current_a = collections.defaultdict(dict) 
            for node1 in self.nodes:
                for node2 in self.nodes:
                    try:
                        costs = [prev_a[node1][node2]]
                    except KeyError:
                        costs = []
                    try:
                        costs.append(prev_a[node1][k]+prev_a[k][node2])
                    except KeyError:
                        pass
                    if costs:
                        self.current_a[node1][node2] = min(costs)


class ModifyFloydWarshall(FloydWarshall):
    # Assume directed graph in which every edge has length 1.
    # Use the recurrence A[i,j,k] = A[i,j,k-1] + A[i,k,k-1] * A[k,j,k-1].
    # For the base case, set A[i,j,0] = 1 if (i,j) is an edge and 0 otherwise.

    def ShortestPaths(self):
        for k in self.nodes:
            prev_a = self.current_a
            self.current_a = collections.defaultdict(dict) 
            for node1 in self.nodes:
                for node2 in self.nodes:
                    try:
                        self.current_a[node1][node2] = prev_a[node1][node2]
                    except KeyError:
                        self.current_a[node1][node2] = 0
                    try:
                        self.current_a[node1][node2] += (
                            prev_a[node1][k] * prev_a[k][node2])
                    except KeyError:
                        pass


class Johnson(object):
    BELLMAN_FORD_SOURCE = 0

    def __init__(self):
        self.graph = collections.defaultdict(dict)
        self.bf = BellmanFord()
        self.dk = test_dijkstra.Dijkstra()

    def Add(self, node1, node2, cost):
        self.graph[node1][node2] = cost
        self.bf.Add(node1, node2, cost)

    def GetSSP(self):
        # Compute shortest shortest path, i.e. all-pair shortest paths and return
        # the smallest one.  
        self.RunBellmanFord()
        return self.RunDijkstra()

    def RunBellmanFord(self):
        for node in self.graph:
            self.bf.Add(self.BELLMAN_FORD_SOURCE, node, 0)
        self.bf.ShortestPaths(self.BELLMAN_FORD_SOURCE)

    def RunDijkstra(self):
        bf_result = self.bf.current_a
        for node , node_info in self.graph.items():
            for neighbor, cost in node_info.items():
                # Add reweighted edges.
                self.dk.AddAdjacency(
                    node, neighbor, cost+bf_result[node]-bf_result[neighbor])
        distances = []
        for node in self.graph:
            res = self.dk.GetSP(node)
            # Get the min distance from this node.
            distances.append(min(res[dest].dist-bf_result[node]+bf_result[dest]
                                 for dest in res))
        return min(distances)


class BellmanFordTest(unittest2.TestCase):
    
    def testSingleEdge(self):
        bf = BellmanFord()
        bf.Add(1, 2, 1)
        self.assertEqual({1: 0, 2: 1}, bf.ShortestPaths(1))

    def testNegativeCycle1(self):
        bf = BellmanFord()
        bf.Add(1, 2, 1)
        bf.Add(2, 1, -2)
        with self.assertRaises(NegativeCycleError):
            bf.ShortestPaths(2)

    def testNegativeCycle2(self):
        bf = BellmanFord()
        edges = [(1, 2, 5), (1, 3, -2),
                 (2, 4, 1),
                 (3, 2, 2),
                 (4, 3, 2), (4, 5, -7), (4, 6, 3),
                 (5, 3, 3), (5, 6, 10)]
        for edge in edges:
            bf.Add(*edge)
        with self.assertRaises(NegativeCycleError):
            bf.ShortestPaths(1)

    def testGraph1(self):
        bf = BellmanFord()
        edges = [(1, 2, 2), (1, 3, 4),
                 (2, 3, 1), (2, 4, 2),
                 (3, 5, 4),
                 (4, 5, 2)]
        for edge in edges:
            bf.Add(*edge)
        expect = {1: 0, 2: 2, 3: 3, 4: 4, 5: 6}
        self.assertEqual(expect, bf.ShortestPaths(1))

    def testGraph2(self):
        bf = BellmanFord()
        edges = [(1, 2, 6), (1, 4, 7),
                 (2, 3, 5), (2, 4, 8), (2, 5, -4),
                 (3, 2, -2),
                 (4, 3, -3), (4, 5, 9),
                 (5, 1, 2), (5, 3, 7)]
        for edge in edges:
            bf.Add(*edge)
        expect = {1: 0, 2: 2, 3: 4, 4: 7, 5: -2}
        self.assertEqual(expect, bf.ShortestPaths(1))

    def testGraph3(self):
        bf = BellmanFord()
        edges = [(1, 2, 6), (1, 4, 7),
                 (2, 3, 5), (2, 4, 8), (2, 5, -4),
                 (3, 2, -2),
                 (4, 3, -3), (4, 5, 9),
                 (5, 1, 2), (5, 3, 7)]
        for edge in edges:
            bf.Add(*edge)
        expect = {1: -2, 2: 0, 3: 2, 4: 5, 5: -4}
        self.assertEqual(expect, bf.ShortestPaths(2))


class FloydWarshallTest(unittest2.TestCase):

    def testGraph1(self):
        fw = FloydWarshall()
        edges = [(1, 2, 2), (1, 3, 4),
                 (2, 3, 1), (2, 4, 2),
                 (3, 5, 4),
                 (4, 5, 2)]
        for edge in edges:
            fw.Add(*edge)
        self.assertEqual(0, fw.GetSSP())

    def testGraph2(self):
        fw = FloydWarshall()
        edges = [(1, 4, 2),
                 (2, 1, 6), (2, 3, 3),
                 (3, 1, 4), (3, 4, 5),
                 (4, 2, -7), (4, 3, -3)]
        for edge in edges:
            fw.Add(*edge)
        self.assertEqual(-7, fw.GetSSP())

    def testGraph2APSP(self):
        fw = FloydWarshall()
        edges = [(1, 2, 6), (1, 4, 7),
                 (2, 3, 5), (2, 4, 8), (2, 5, -4),
                 (3, 2, -2),
                 (4, 3, -3), (4, 5, 9),
                 (5, 1, 2), (5, 3, 7)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        expect = {1: 0, 2: 2, 3: 4, 4: 7, 5: -2}
        self.assertEqual(expect, fw.current_a[1])

    def testPS4_3Nodes(self):
        fw = FloydWarshall()
        edges = [(1, 2, -1), (1, 3, -1),
                 (2, 1, -1), (2, 3, -1),
                 (3, 1, -1), (3, 2, -1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print min([min(node_info.values()) for node_info in fw.current_a.values()])

    def testPS4_4Nodes(self):
        fw = FloydWarshall()
        edges = [(1, 2, -1), (1, 3, -1), (1, 4, -1),
                 (2, 1, -1), (2, 3, -1), (2, 4, -1),
                 (3, 1, -1), (3, 2, -1), (3, 4, -1),
                 (4, 1, -1), (4, 2, -1), (4, 3, -1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print min([min(node_info.values()) for node_info in fw.current_a.values()])

    def testPS4_5Nodes(self):
        fw = FloydWarshall()
        edges = [(1, 2, -1), (1, 3, -1), (1, 4, -1), (1, 5, -1),
                 (2, 1, -1), (2, 3, -1), (2, 4, -1), (2, 5, -1),
                 (3, 1, -1), (3, 2, -1), (3, 4, -1), (3, 5, -1),
                 (4, 1, -1), (4, 2, -1), (4, 3, -1), (4, 5, -1),
                 (5, 1, -1), (5, 2, -1), (5, 3, -1), (5, 4, -1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print min([min(node_info.values()) for node_info in fw.current_a.values()])


class ModifyFloydWarshallTest(unittest2.TestCase):

    def testPS3G1(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (1, 3, 1), (1, 4, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a

    def testPS3G2(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (2, 3, 1), (1, 4, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a

    def testPS3G3(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (2, 3, 1), (1, 3, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a

    def testPS3G4(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (2, 3, 1), (1, 3, 1),
                 (3, 4, 1),
                 (4, 5, 1), (5, 6, 1), (4, 6, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a

    def testPS3Cycle1(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (2, 1, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a

    def testPS3Cycle2(self):
        fw = ModifyFloydWarshall()
        edges = [(1, 2, 1), (2, 3, 1), (3, 1, 1)]
        for edge in edges:
            fw.Add(*edge)
        fw.ShortestPaths()
        print fw.current_a


class FloydWarshallHWTest(unittest2.TestCase):

    def AddGraph(self, filename):
        with open(filename, 'r') as fd:
            _, edges = fd.readline().split()
            edges = int(edges)
            fw = FloydWarshall()
            for _ in range(edges):
                fw.Add(*[int(i) for i in fd.readline().split()])
        return fw

    def testG3(self):
        fw = self.AddGraph('g3.txt')
        self.assertEqual(-19, fw.GetSSP())


class JohnsonTest(unittest2.TestCase):

    def testGraph1(self):
        js = Johnson()
        edges = [(1, 2, 2), (1, 3, 4),
                 (2, 3, 1), (2, 4, 2),
                 (3, 5, 4),
                 (4, 5, 2)]
        for edge in edges:
            js.Add(*edge)
        self.assertEqual(0, js.GetSSP())

    def testGraph2(self):
        js = Johnson()
        edges = [(1, 4, 2),
                 (2, 1, 6), (2, 3, 3),
                 (3, 1, 4), (3, 4, 5),
                 (4, 2, -7), (4, 3, -3)]
        for edge in edges:
            js.Add(*edge)
        self.assertEqual(-7, js.GetSSP())


class JohnsonHWTest(unittest2.TestCase):

    def AddGraph(self, filename):
        with open(filename, 'r') as fd:
            _, edges = fd.readline().split()
            edges = int(edges)
            js = Johnson()
            for _ in range(edges):
                js.Add(*[int(i) for i in fd.readline().split()])
        return js

    def testG1(self):
        js = self.AddGraph('g1.txt')
        with self.assertRaises(NegativeCycleError):
            js.GetSSP()

    def testG2(self):
        js = self.AddGraph('g2.txt')
        with self.assertRaises(NegativeCycleError):
            js.GetSSP()

    def testG3(self):
        js = self.AddGraph('g3.txt')
        self.assertEqual(-19, js.GetSSP())


if __name__ == '__main__':
    unittest2.main()
