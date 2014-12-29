#!/usr/bin/python


import collections
import copy
import random
import unittest2


class Error(Exception):
    """Base error class."""


class MinCutGraph(object):

    def __init__(self):
        # Original graph and edges.  This should not be modified and used
        # to get min cut.
        self.graph = collections.defaultdict(dict)
        self.all_edges = set()
        self.merged_graph = {}
        self.merge_map = {}
        self.edges = set()
        self.merge_number = 0

    def AddEdge(self, node, adjacencies):
        if not isinstance(adjacencies, list):
            raise Error('Invalid adjacencies: {}'.format(adjacencies))
        for neighbor in adjacencies:
            edge = self.MakeEdge(node, neighbor)
            try:
                self.graph[node]['edges'].add(edge)
            except KeyError:
                self.graph[node] = {
                    'nodes': set([node]), 'edges': set([edge])}
            self.all_edges.add(edge)

    def Contract(self, edge):
        node_list = edge.split('-')
        merged_nodes = [self.merge_map.get(node, node) for node in node_list]
        this_merged_node = 'm{}'.format(self.merge_number)
        self.merge_number += 1
        # Track the members of this merged node.
        nodes = self.merged_graph[merged_nodes[0]]['nodes']
        nodes = nodes.union(self.merged_graph[merged_nodes[1]]['nodes'])
        merge_info = {'nodes': nodes,
                      # Track edges that don't terminate at itself.
                      'edges': set()}
        self.merged_graph[this_merged_node] = merge_info
        for merged_node in merged_nodes:
            for node in self.merged_graph[merged_node]['nodes']:
                # Update the new merged node of which the node is a member.
                self.merge_map[node] = this_merged_node
            for edge in self.merged_graph[merged_node]['edges']:
                if self.IsSelfEdge(edge, this_merged_node):
                    # Remove edge that terminates at this merged node.
                    self.edges = self.edges - set([edge])
                else:
                    # Track outgoing edge.
                    merge_info['edges'].add(edge)
            del self.merged_graph[merged_node]

    def IsSelfEdge(self, edge, merged_node):
        nodes = set(edge.split('-'))
        return not (nodes - self.merged_graph[merged_node]['nodes'])
            
    def InitMergeGraph(self):
        self.merge_map = {}
        self.edges = self.all_edges.copy()
        self.merged_graph = copy.deepcopy(self.graph)

    def MakeEdge(self, node1, node2):
        return '-'.join(sorted([node1, node2]))

    def RandomCut(self):
        random.seed()
        self.InitMergeGraph()
        while len(self.merged_graph) != 2:
            edge_list = list(self.edges)
            edge = edge_list[random.randint(0, len(self.edges)-1)]
            self.Contract(edge)
        return self.edges.copy()

    def RandomMinCut(self, trials=100):
        min_cut = None
        for _ in xrange(trials):
            cut = self.RandomCut()
            if min_cut is None or len(cut) < len(min_cut):
                min_cut = cut
        return min_cut


class TestGraph(unittest2.TestCase):

    def testInvalidAdjacencies(self):
        graph = MinCutGraph()
        self.assertRaises(Error, graph.AddEdge, None, None)

    def testContract1(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1'])
        graph.AddEdge('1', ['0'])
        graph.InitMergeGraph()
        graph.Contract('0-1')
        self.assertEqual(len(graph.edges), 0)
        self.assertEqual(len(graph.merged_graph), 1)

    def testContract2(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1', '3'])
        graph.AddEdge('1', ['0', '2'])
        graph.AddEdge('2', ['1', '3'])
        graph.AddEdge('3', ['0', '2'])
        graph.InitMergeGraph()
        graph.Contract('0-1')
        self.assertEqual(graph.edges, set(['0-3', '1-2', '2-3']))
        self.assertEqual(len(graph.merged_graph), 3)
        graph.Contract('2-3')
        self.assertEqual(graph.edges, set(['0-3', '1-2']))
        self.assertEqual(len(graph.merged_graph), 2)
        graph.Contract('0-3')
        self.assertEqual(len(graph.edges), 0)
        self.assertEqual(len(graph.merged_graph), 1)

    def testContract3(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1', '3'])
        graph.AddEdge('1', ['0', '2', '3'])
        graph.AddEdge('2', ['1', '3'])
        graph.AddEdge('3', ['0', '1', '2'])
        graph.InitMergeGraph()
        graph.Contract('0-1')
        self.assertEqual(graph.edges, set(['0-3', '1-2', '1-3', '2-3']))
        self.assertEqual(len(graph.merged_graph), 3)
        graph.Contract('2-3')
        self.assertEqual(graph.edges, set(['0-3', '1-2', '1-3']))
        self.assertEqual(len(graph.merged_graph), 2)
        graph.Contract('0-3')
        self.assertEqual(len(graph.edges), 0)
        self.assertEqual(len(graph.merged_graph), 1)


class TestMinCut(unittest2.TestCase):

    def testRandomCut(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1', '3'])
        graph.AddEdge('1', ['0', '2', '3'])
        graph.AddEdge('2', ['1', '3'])
        graph.AddEdge('3', ['0', '1', '2'])
        cut = graph.RandomCut()
        self.assertEqual(len(graph.merged_graph), 2)
        self.assertTrue(2 <= len(cut) <= 3)

    def testRandomMinCut1(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1', '3'])
        graph.AddEdge('1', ['0', '2', '3'])
        graph.AddEdge('2', ['1', '3'])
        graph.AddEdge('3', ['0', '1', '2'])
        min_cut = graph.RandomMinCut()
        self.assertEqual(len(min_cut), 2)

    def testRandomMinCut2(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1'])
        graph.AddEdge('1', ['0', '2', '3'])
        graph.AddEdge('2', ['1', '4'])
        graph.AddEdge('3', ['1', '4', '5'])
        graph.AddEdge('4', ['2', '3', '5'])
        graph.AddEdge('5', ['3', '4'])
        min_cut = graph.RandomMinCut()
        self.assertEqual(len(min_cut), 1)

    def testRandomMinCut3(self):
        graph = MinCutGraph()
        graph.AddEdge('0', ['1', '2'])
        graph.AddEdge('1', ['0', '2', '3'])
        graph.AddEdge('2', ['0', '1', '4'])
        graph.AddEdge('3', ['1', '4', '5'])
        graph.AddEdge('4', ['2', '3', '5'])
        graph.AddEdge('5', ['3', '4'])
        min_cut = graph.RandomMinCut()
        self.assertEqual(len(min_cut), 2)

    def TestHomework(self):
        graph = MinCutGraph()
        with open('kargerMinCut.txt', 'r') as fd:
            for line in fd:
                node_list = line.split()
                graph.AddEdge(node_list[0], node_list[1:])
        min_cut = graph.RandomMinCut()
        print 'min_cut: {}'.format(min_cut)
        print 'min_cut length: {}'.format(len(min_cut))


if __name__ == '__main__':
    unittest2.main()

