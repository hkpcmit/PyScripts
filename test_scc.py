#!/opt/local/bin/pypy


import collections
import sys
import unittest2


sys.setrecursionlimit(300000)


STACK_DFS = 1
STACK_POST_DFS = 2


class Error(Exception):
    """Base error class."""


class StackInfo(object):

    def __init__(self, op, node, neighbors=None):
        self.op = op
        self.node = node
        self.neighbors = neighbors


class SccGraph(object):

    def __init__(self):
        self.G = collections.defaultdict(set)
        self.Grev = collections.defaultdict(set)
        self.fin_times = {}

    def AddEdge(self, source, dest):
        self.G[source].add(dest)
        if dest not in self.G:
            self.G[dest] = set()
        self.Grev[dest].add(source)
        if source not in self.Grev:
            self.Grev[source] = set()

    def Dfs(self, graph, node, visited, label_func=None, scc_set=None):
        if not isinstance(visited, set):
            raise Error('Invalid visited: {}'.format(visited))
        visited.add(node)
        if scc_set is not None:
            scc_set.add(node)
        for neighbor in graph[node]:
            if neighbor in visited:
                continue
            self.Dfs(graph, neighbor, visited, label_func=label_func,
                     scc_set=scc_set)
        if label_func:
            label_func(node)

    def FirstPass(self):
        visited = set()
        self.fin_times = {}
        self.fin_time = self.length - 1

        def _Label(node):
            self.fin_times[self.fin_time] = node
            self.fin_time -= 1

        for node in self.Grev:
            if node not in visited:
                self.Dfs(self.Grev, node, visited, _Label)

    def SecondPass(self):
        visited = set()
        scc_list = []
        for i in xrange(self.length):
            node = self.fin_times[i]
            if node in visited:
                continue
            scc_set = set()
            self.Dfs(self.G, node, visited, scc_set=scc_set)
            scc_list.append(scc_set)
        return scc_list

    def GetSccList(self):
        self.FirstPass()
        return self.SecondPass()

    @property
    def length(self):
        return len(self.G)


class SccGraphStack(SccGraph):

    def DfsNeighbors(self, node, neighbors, stack, visited):
        if not neighbors:
            return False
        while neighbors:
            neighbor = neighbors.pop()
            if neighbor in visited: 
                continue
            stack.append(StackInfo(STACK_POST_DFS, node, neighbors=neighbors))
            stack.append(StackInfo(STACK_DFS, neighbor))
            return True

    def Dfs(self, graph, node, visited, label_func=None, scc_set=None):
        if not isinstance(visited, set):
            raise Error('Invalid visited: {}'.format(visited))
        stack = [StackInfo(STACK_DFS, node)]
        while stack:
            stack_info = stack.pop()
            this_node = stack_info.node
            if stack_info.op == STACK_DFS:
                visited.add(this_node)
                if scc_set is not None:
                    scc_set.add(this_node)
                neighbors = graph[this_node].copy()
                if self.DfsNeighbors(
                    this_node, graph[this_node].copy(), stack, visited):
                    # Need to DFS on a neighbor.  Proceed to the next stack info.
                    continue
            elif stack_info.op == STACK_POST_DFS:
                neighbors = stack_info.neighbors
                if self.DfsNeighbors(
                    this_node, stack_info.neighbors, stack, visited):
                    # Need to DFS on a neighbor.  Proceed to the next stack info.
                    continue
            if label_func:
                label_func(this_node)
                

class TestKosaraju(unittest2.TestCase):

    def testDfsInvalidVisited(self):
        graph = SccGraph()
        self.assertRaises(Error, graph.Dfs, None, None, None)

    def testK1(self):
        graph = SccGraph()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        expect_scc_list = [set([i]) for i in xrange(3)]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK2(self):
        graph = SccGraph()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(2, 1)
        expect_scc_list = [set([0]), set([1, 2])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK3(self):
        graph = SccGraph()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(0, 3)
        graph.AddEdge(3, 0)
        graph.AddEdge(1, 4)
        graph.AddEdge(4, 1)
        graph.AddEdge(2, 5)
        graph.AddEdge(5, 2)
        expect_scc_list = [set([0, 3]), set([1, 4]), set([2, 5])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK4(self):
        graph = SccGraph()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(1, 3)
        graph.AddEdge(2, 0)
        graph.AddEdge(2, 4)
        graph.AddEdge(2, 5)
        graph.AddEdge(3, 4)
        graph.AddEdge(3, 5)
        graph.AddEdge(4, 5)
        graph.AddEdge(5, 4)
        expect_scc_list = [set([0, 1, 2]), set([3]), set([4, 5])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)


class TestKosarajuStack(unittest2.TestCase):

    def testDfsInvalidVisited(self):
        graph = SccGraphStack()
        self.assertRaises(Error, graph.Dfs, None, None, None)

    def testK1(self):
        graph = SccGraphStack()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        expect_scc_list = [set([i]) for i in xrange(3)]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK2(self):
        graph = SccGraphStack()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(2, 1)
        expect_scc_list = [set([0]), set([1, 2])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK3(self):
        graph = SccGraphStack()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(0, 3)
        graph.AddEdge(3, 0)
        graph.AddEdge(1, 4)
        graph.AddEdge(4, 1)
        graph.AddEdge(2, 5)
        graph.AddEdge(5, 2)
        expect_scc_list = [set([0, 3]), set([1, 4]), set([2, 5])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)

    def testK4(self):
        graph = SccGraphStack()
        graph.AddEdge(0, 1)
        graph.AddEdge(1, 2)
        graph.AddEdge(1, 3)
        graph.AddEdge(2, 0)
        graph.AddEdge(2, 4)
        graph.AddEdge(2, 5)
        graph.AddEdge(3, 4)
        graph.AddEdge(3, 5)
        graph.AddEdge(4, 5)
        graph.AddEdge(5, 4)
        expect_scc_list = [set([0, 1, 2]), set([3]), set([4, 5])]
        for scc in graph.GetSccList():
            self.assertIn(scc, expect_scc_list)


class HWTest(unittest2.TestCase):

    def setUp(self):
        with open('SCC.txt', 'r') as fd:
            self.edges = [line.split() for line in fd]

    def testHW(self):
        graph = SccGraphStack()
        for edge in self.edges:
            graph.AddEdge(*edge)
        scc_list = graph.GetSccList()
        sort_list = sorted([len(scc) for scc in scc_list], reverse=True)
        self.assertEqual([434821, 968, 459, 313, 211], sort_list[:5])
        

if __name__ == '__main__':
    unittest2.main()
