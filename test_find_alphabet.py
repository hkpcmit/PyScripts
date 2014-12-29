#!/usr/bin/python


import collections
import itertools
import unittest2


class Error(Exception):
    """Base error class."""


class AlphabetGraph(object):

    def __init__(self):
        self.graph = collections.defaultdict(dict)
        self.visit = set()
        self.reverse_list = []

    def InitInfo(self, node):
        self.graph[node]['neighbors'] = set()
        self.graph[node]['in_edges'] =  False

    def Add(self, lesser, greater):
        arg_map = {'lesser': lesser, 'greater': greater}
        for arg, value in arg_map.iteritems():
            if not isinstance(value, basestring):
                raise Error('Invalid {}: {}'.format(arg, value))
        for node in (lesser, greater):
            if node not in self.graph:
                self.InitInfo(node)
        self.graph[lesser]['neighbors'].add(greater)
        self.graph[greater]['in_edges'] = True

    def Dfs(self, node):
        self.visit.add(node)
        neighbors = self.graph[node]['neighbors']
        for neighbor in neighbors:
            if neighbor in self.visit:
                continue
            self.Dfs(neighbor)
        self.reverse_list.append(node)

    def Sort(self):
        sources = [node for node in self.graph if not self.graph[node]['in_edges']]
        sources_length = len(sources)
        if not sources_length or sources_length > 1:
            raise Error('Invalid source number in sources: {}'.format(sources))
        self.visit = set()
        self.reverse_list = []
        self.Dfs(sources[0])
        self.reverse_list.reverse()
        return self.reverse_list


def FindAlphabet(input_list):
    if not isinstance(input_list, list) or not input_list:
        raise Error('Invalid input_list: {}'.format(input_list))
    input_length = len(input_list)
    if input_length == 1:
        return input_list
    graph = AlphabetGraph()
    for i, element in enumerate(input_list[:input_length-1]):
        next = input_list[i+1]
        for e, n in itertools.izip(element, next):
            if e == n:
                continue
            graph.Add(e, n)
            break
    return graph.Sort()


class TestFindAlphabet(unittest2.TestCase):

    def testAlphabetGraphAddInvalid(self):
        graph = AlphabetGraph()
        self.assertRaises(Error, graph.Add, None, None)
        self.assertRaises(Error, graph.Add, 'a', None)

    def testAlphabetGraphAdd(self):
        graph = AlphabetGraph()
        graph.Add('a', 'b')
        expect_graph = {'a': {'neighbors': set(['b']), 'in_edges': False},
                        'b': {'neighbors': set(), 'in_edges': True}}
        self.assertDictEqual(expect_graph, graph.graph)
        graph.Add('b', 'c')
        expect_graph = {'a': {'neighbors': set(['b']), 'in_edges': False},
                        'b': {'neighbors': set(['c']), 'in_edges': True},
                        'c': {'neighbors': set(), 'in_edges': True}}
        self.assertDictEqual(expect_graph, graph.graph)
        graph.Add('a', 'd')
        expect_graph = {'a': {'neighbors': set(['b', 'd']), 'in_edges': False},
                        'b': {'neighbors': set(['c']), 'in_edges': True},
                        'c': {'neighbors': set(), 'in_edges': True},
                        'd': {'neighbors': set(), 'in_edges': True}}
        self.assertDictEqual(expect_graph, graph.graph)

    def testAlphabetGraphSortError(self):
        graph = AlphabetGraph()
        graph.Add('a', 'b')
        graph.Add('c', 'd')
        self.assertRaises(Error, graph.Sort)

    def testAlphabetGraphSort1(self):
        graph = AlphabetGraph()
        graph.Add('a', 'b')
        graph.Add('b', 'c')
        expect_list = ['a', 'b', 'c']
        self.assertEqual(expect_list, graph.Sort())

    def testAlphabetGraphSort2(self):
        graph = AlphabetGraph()
        graph.Add('a', 'c')
        graph.Add('b', 'c')
        graph.Add('b', 'a')
        self.assertEqual(['b', 'a', 'c'], graph.Sort())

    def testAlphabetGraphSort3(self):
        graph = AlphabetGraph()
        graph.Add('b', 'a')
        graph.Add('b', 'c')
        graph.Add('b', 'd')
        graph.Add('a', 'd')
        graph.Add('a', 'c')
        graph.Add('c', 'd')
        self.assertEqual(['b', 'a', 'c', 'd'], graph.Sort())

    def testFindAlphabetError(self):
        self.assertRaises(Error, FindAlphabet, None)
        self.assertRaises(Error, FindAlphabet, [])

    def testFindSingleAlphabet(self):
        expect_list = ['a']
        self.assertEqual(expect_list, FindAlphabet(expect_list))

    def testFindAlphabet(self):
        input_list = ['baa', 'bac', 'cb', 'ca']
        self.assertEqual(['b', 'a', 'c'], FindAlphabet(input_list))


if __name__ == '__main__':
    unittest2.main()
