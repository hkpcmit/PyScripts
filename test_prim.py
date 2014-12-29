#!/usr/bin/python


import heapq
import unittest2


class Error(Exception):
    """Base error class."""


class Prim(object):

    def __init__(self):
        self.graph = {}
        self.edges = {}
        self.mst = {'edges': [], 'nodes': set(), 'total costs': 0,
                    'skip heappush': 0}
        self.heap = []
        self.heap_map = {}

    def Add(self, node1, node2, cost):
        if not node1 or not node2:
            raise Error(
                'Invalid node1/node2: {}/{}'.format(node1, node2))
        # Add to graph.
        node_map = {node1: node2, node2: node1}
        for node, neighbor in node_map.iteritems():
            if node not in self.graph:
                self.graph[node] = {'neighbors': []}
            self.graph[node]['neighbors'].append(neighbor)
        # Save edge info.
        self.edges[self.GetEdgeId(node1, node2)] = int(cost)

    def GetEdgeCost(self, node1, node2):
        return self.edges[self.GetEdgeId(node1, node2)]

    def GetEdgeId(self, node1, node2):
        return '-'.join(sorted([node1, node2]))

    def GetMstCost(self):
        all_nodes = self.graph.keys()
        init_node = all_nodes[0]
        non_tree_nodes = set(all_nodes[1:])
        self.mst['nodes'].add(init_node)
        while non_tree_nodes:
            self.SaveCutEdges(non_tree_nodes)
            cost, node, neighbor = self.GetMinCostNode()
            self.mst['edges'].append(self.GetEdgeId(node, neighbor))
            self.mst['nodes'].add(node)
            self.mst['total costs'] += cost
            non_tree_nodes = non_tree_nodes - set([node])
        result = {'total costs': self.mst['total costs'],
                  'skip heappush': self.mst['skip heappush']}
        return result
            
    def GetMinCostNode(self):
        while self.heap:
            cost, node, neighbor = heapq.heappop(self.heap)
            if node not in self.mst['nodes']:
                del self.heap_map[node]
                return cost, node, neighbor
            # Skip if this node is already in MST.
        raise Error('Cannot get node with min-cost that is not in MST.')

    def GetNodeMinCost(self, node):
        cost_list = []
        for neighbor in self.graph[node]['neighbors']:
            # Skip neighbor not in MST.
            if neighbor in self.mst['nodes']:
                # Save edge cost and neighbor so that min cost and the
                # corresponding neighbor will be returned.
                cost_list.append((self.GetEdgeCost(node, neighbor),
                                  neighbor))
        if cost_list:
            return min(cost_list)
        return

    def SaveCutEdges(self, non_tree_nodes):
        for node in non_tree_nodes:
            result = self.GetNodeMinCost(node)
            if result:
                cost, neighbor = result
                # Save and update the cost of this edge (node, neighbor)
                # in the heap only if its cost is lower than that within
                # the heap.  This can reduce the runtime by ~25%.
                if (node not in self.heap_map or
                    cost < self.heap_map[node]):
                    heapq.heappush(self.heap, (result[0], node, result[1]))
                    self.heap_map[node] = cost
                    continue
            self.mst['skip heappush'] += 1


class PrimTest(unittest2.TestCase):

    def testInvalidAdd(self):
        with self.assertRaises(Error):
            Prim().Add(None, None, 1)
            
    def testSample1(self):
        prim = Prim()
        # Edges with string costs are part of MST.
        edges = [('1', '2', '1'),
                 ('1', '4', 3),
                 ('1', '3', '4'),
                 ('2', '4', '2'),
                 ('3', '4', 5)]
        for edge in edges:
            prim.Add(*edge)
        self.assertEqual(prim.GetMstCost()['total costs'], 7)
            
    def testSample2(self):
        prim = Prim()
        edges = [('1', '2', '2'),
                 ('1', '4', 4),
                 ('2', '3', '4'),
                 ('2', '4', 4),
                 ('2', '5', '3'),
                 ('2', '6', '1'),
                 ('3', '6', 5),
                 ('4', '5', '2'),
                 ('5', '6', 5)]
        for edge in edges:
            prim.Add(*edge)
        self.assertEqual(prim.GetMstCost()['total costs'], 12)
            
    def testSample3(self):
        prim = Prim()
        edges = [('1', '2', '3'),
                 ('1', '6', '2'),
                 ('2', '3', 17),
                 ('2', '4', 16),
                 ('3', '4', '8'),
                 ('3', '9', 18),
                 ('4', '5', 11),
                 ('4', '9', '4'),
                 ('5', '6', '1'),
                 ('5', '7', '6'),
                 ('5', '8', '5'),
                 ('5', '9', '10'),
                 ('6', '7', 7),
                 ('7', '8', 15),
                 ('8', '9', 12),
                 ('8', '10', 13),
                 ('9', '10', '9')]
        for edge in edges:
            prim.Add(*edge)
        self.assertEqual(prim.GetMstCost()['total costs'], 48)


class HWTest(unittest2.TestCase):

    def test(self):
        prim = Prim()
        with open('edges.txt', 'r') as fd:
            n_nodes, n_edges = [
                int(num) for num in fd.next().split()]
            for _ in xrange(n_edges):
                prim.Add(*fd.next().split())
        self.assertEqual(-3612829, prim.GetMstCost()['total costs'])


if __name__ == '__main__':
    unittest2.main()
