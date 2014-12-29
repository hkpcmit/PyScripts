#!/opt/local/bin/pypy
#
# Traveling saleman problem.

import collections
import math
import sys
import unittest2


def nCr(n, r):
    if r < 0 or r > n:
        return 0
    ntor, rtor = 1, 1
    for t in xrange(1, min(r, n-r) + 1):
        ntor *= n
        rtor *= t
        n -= 1
    return ntor // rtor


class TableContent(object):

    def __init__(self, row_key, version, total_columns):
        self.row_key = row_key
        self.version = version
        self.columns = [None] * total_columns

    def __str__(self):
        return 'row_key: {}; columns: {}; version: {}'.format(
            self.row_key, self.columns, self.version)

    def ResetColumns(self):
        self.version += 1
        for i in range(len(self.columns)):
            self.columns[i] = None


class Table(object):

    def __init__(self, total_columns):
        self.total_columns = total_columns
        self.r = 1
        self.version = 0
        self.contents = self.InitContents()
        self.total_rows = 0
        self.max_index = 0
        self.index_base = None
        self.base_position = 0

    def InitContents(self):
        k = self.total_columns // 2
        if k*2 != self.total_columns:
            k += 1
        return [None] * nCr(self.total_columns, k)

    def GetContentOld(self, row_key):
        return self.contents[self.GetIndex(row_key)]

    def GetContent(self, row_key):
        content = self.contents[self.GetIndex(row_key)]
        if content and content.version == self.version: 
            return content
        return

    def GetIndexOld(self, row_key):
        bit = 1
        index, r = 0, 1
        for position in xrange(self.total_columns):
            if bit & row_key:
                index += nCr(position, r)
                r += 1
            bit <<= 1
        return index

    def GetIndex(self, row_key):
        if self.index_base is None:
            bit = 1
            index, r, init_position = 0, 1, 0
        else:
            bit = 1 << self.base_position
            index, init_position = self.index_base, self.base_position
            r = self.r
        for position in xrange(init_position, self.total_columns):
            if bit & row_key:
                index += nCr(position, r)
                r += 1
            bit <<= 1
        return index

    def GetMaxIndex(self):
        index = 0
        n = self.total_columns - self.r
        for r in xrange(1, self.r+1):
            index += nCr(n, r)
            n += 1
        return index

    def GetContents(self):
        for content in self.contents[:self.max_index+1]:
            if content and (content.version == self.version):
                yield content

    def SetIndexBase(self, key):
        self.index_base = 0
        self.base_position, r = 0, 1
        while key:
            if key % 2:
                self.index_base += nCr(self.base_position, r)
                r += 1
            self.base_position += 1
            key >>= 1

    def SetKey(self, row_key, column, value):
        index = self.GetIndex(row_key)
        if not self.contents[index]:
            content = TableContent(row_key, self.version, self.total_columns+1)
            content.columns[column] = value
            self.contents[index] = content
            self.total_rows += 1
            if index > self.max_index:
                self.max_index = index
        else:
            content = self.contents[index]
            # Check this is an old version.
            if content.version < self.version:
                content.ResetColumns()
                self.total_rows += 1
                if index > self.max_index:
                    self.max_index = index
            content.row_key = row_key
            content.columns[column] = value

    def SetR(self, r):
        self.r = r
        self.version += 1
        self.total_rows, self.max_index = 0, 0
        self.index_base, self.base_position = None, 0
        

class TSP(object):

    def __init__(self, x_list=None):
        # List of x coordinates that separate the cities into multiple groups.
        # Based on the city scatter plot, there should be two paths passing
        # through the groups[1:-1] in the shortest tour.
        self.x_list = x_list
        self.city_map = collections.defaultdict(list)
        self.current_a, self.prev_a = None, None
        if self.x_list is None:
            self.city_group = None
            self.first_city_in_group = None
        else:
            self.city_group = collections.defaultdict(set)
            self.first_city_in_group = []
        self.distance = collections.defaultdict(dict)

    def Add(self, city, x, y):
        self.city_map[city] = [x, y]
        if self.city_group is None:
            return
        for group, x_limit in enumerate(self.x_list):
            if x <= x_limit:
                self.city_group[group].add(city)
                if len(self.city_group[group]) == 1:
                    self.first_city_in_group.append(city)
                return
        self.city_group[len(self.x_list)].add(city)
        self.first_city_in_group.append(city)

    def Distance(self, city1, city2):
        if city1 > city2:
            city1, city2 = city2, city1
        try:
            return self.distance[city1][city2]
        except KeyError:
            pass
        city1_x, city1_y = self.city_map[city1]
        city2_x, city2_y = self.city_map[city2]
        self.distance[city1][city2] = math.sqrt(
            pow(city1_x-city2_x, 2) + pow(city1_y-city2_y, 2))
        return self.distance[city1][city2]

    def ExchangeA(self, size):
        self.prev_a, self.current_a = self.current_a, self.prev_a
        self.current_a.SetR(size)

    def GetCityBit(self, city):
        return 1 << (city-1)

    def GetCityGroup(self, city):
        for group, cities in self.city_group.items():
            if city in cities:
                return group

    def GetEndCities(self, city_set):
        if city_set == 1:
            return [1]
        return [city for city in range(2, self.total_cities+1)
                if city_set & self.GetCityBit(city)]

    def GetUnvisitCities(self, unvisit_cities):
        return [(city, self.GetCityBit(city))
                for city in range(2, self.total_cities+1)
                if unvisit_cities & self.GetCityBit(city)]

    def GetShortestCityPaths(self):
        for content in self.prev_a.GetContents():
            city_set = content.row_key
            unvisit_cities = self.all_cities - city_set
            for unvisit_city, unvisit_city_bit in self.GetUnvisitCities(
                unvisit_cities):
                cost_list = []
                for k, cost in enumerate(content.columns):
                    if cost is None:
                        continue
                    if self.JoinCities(k, unvisit_city, unvisit_cities):
                        cost_list.append(cost+self.Distance(k, unvisit_city))
                if cost_list:
                    new_city_set = city_set | unvisit_city_bit
                    self.current_a.SetKey(
                        new_city_set, unvisit_city, min(cost_list))

    def GetShortestTour(self):
        self.total_cities = len(self.city_map)
        # City set is represented as bit map.  The set of all cities is
        # represented as all-1's.
        self.all_cities = (1 << self.total_cities) - 1
        self.prev_a = Table(self.total_cities)
        self.current_a = Table(self.total_cities)
        self.current_a.SetKey(1, 1, 0.0)
        for size in range(2, self.total_cities+1):
            self.ExchangeA(size)
            self.GetShortestCityPaths()  
            print('Complete subproblem size: {}; current A size: {}'.format(
                    size, self.current_a.total_rows))
        content = self.current_a.GetContent(self.all_cities)
        return int(min(self.Distance(1, city) + cost
                       for city, cost in enumerate(content.columns)
                       if city and cost is not None))

    def GetUnvisitCityGroups(self, city1, city2, unvisit_cities, up_down):
        city1_x, city1_y = self.city_map[city1]
        city2_x, city2_y = self.city_map[city2]
        slope = None if city1_x == city2_x else (city2_y-city1_y) / (city2_x-city1_x)
        if not slope:
            return len(up_down)
        for city in range(city1+1, city2):
            city_bit = self.GetCityBit(city)
            # Skip visited city.
            if not (city_bit & unvisit_cities):
                continue
            city_x, city_y = self.city_map[city]
            if (city_y-city1_y) >= slope * (city_x-city1_x):
                up_down['up'].append(city)
            else:
                up_down['down'].append(city)
            if len(up_down) > 1:
                return 2
        return len(up_down)

    def JoinCities(self, city1, city2, unvisit_cities):
        if self.city_group is None:
            return True
        # Based on inspection of the city scatter plot, the optimal tour should
        # consist of non-intersecting paths connecting cities in the non-adjacent
        # groups.
        group1, group2 = [self.GetCityGroup(city) for city in (city1, city2)]
        last_group = len(self.city_group) - 1
        if (group1, group2) in [(0, last_group), (last_group, 0),
                                (0, last_group-1), (last_group-1, 0)]:
            return False
        if (group1 > 1) and (group1 == group2):
            return True
        # Check if the line connecting city1 and city2 will separate the
        # unvisited cities between them into 2 sets.  If so, don't join them.
        if self.UnvisitCityGroups(city1, city2, unvisit_cities) > 1:
            return False
        return True

    def UnvisitCityGroups(self, city1, city2, unvisit_cities):
        if city1 > city2:
            city1, city2 = city2, city1
        up_down = collections.defaultdict(list)
        groups = self.GetUnvisitCityGroups(
            city1, city2, unvisit_cities, up_down)
        if (groups > 1) or (city1 == 1):
            return groups
        prev_city = city1 - 1
        prev_city_bit = self.GetCityBit(prev_city)
        if prev_city_bit & unvisit_cities:
            groups = self.GetUnvisitCityGroups(
                prev_city-1, city1, unvisit_cities, up_down)
            if groups > 1:
                return groups
        return groups
            

class NewTSP(TSP):

    def GetShortestTour(self):
        self.total_cities = len(self.city_map)
        # City set is represented as bit map.  The set of all cities is
        # represented as all-1's.
        self.all_cities = (1 << self.total_cities) - 1
        self.prev_a = Table(self.total_cities)
        self.current_a = Table(self.total_cities)
        self.current_a.SetKey(1, 1, 0.0)
        # Compute shortest paths containing city size up to total cities // 2 + 1.
        # The current_a and prev_a can be used to fill the remaining unvisited
        # cities. 
        for size in range(2, self.total_cities//2+2):
            self.ExchangeA(size)
            self.GetShortestCityPaths()  
            print('Complete subproblem size: {}; current A size: {}'.format(
                    size, self.current_a.total_rows))
        if (self.total_cities % 2):
            return self.JoinRemainingPath(self.current_a)
        return self.JoinRemainingPath(self.prev_a)

    def JoinCities(self, city1, city2, unvisit_cities):
        if self.city_group is None:
            return True
        # Based on inspection of the city scatter plot, the optimal tour should
        # consist of non-intersecting paths connecting cities in the non-adjacent
        # groups.
        group1, group2 = [self.GetCityGroup(city) for city in (city1, city2)]
        last_group = len(self.city_group) - 1
        if (group1, group2) in [(0, last_group), (last_group, 0),
                                (0, last_group-1), (last_group-1, 0)]:
            return False
        if group1 == group2:
            return True
        # Check if the line connecting city1 and city2 will separate the
        # unvisited cities between them into 2 sets.  If so, don't join them.
        if self.UnvisitCityGroups(city1, city2, unvisit_cities) > 1:
            return False
        return True

    def JoinRemainingPath(self, remain_a):
        cost_list = []
        for content in self.current_a.GetContents():
            city_cost_list = []
            city_set = content.row_key
            remain_cities = self.all_cities - city_set
            # Add city 1 as source.
            remain_cities += 1
            remain_cities_content = remain_a.GetContent(remain_cities)
            if remain_cities_content is None:
                continue
            for k1, cost1 in enumerate(content.columns):
                if cost1 is None:
                    continue
                for k2, cost2 in enumerate(remain_cities_content.columns):
                    if cost2 is None:
                        continue
                    city_cost_list.append(cost1+cost2+self.Distance(k1, k2))
            cost_list.append(min(city_cost_list))
        return int(min(cost_list))


class TSPTest(unittest2.TestCase):
    
    def testG1(self):
        tsp = TSP()
        city_list = [(0.0, 0.0), (0.0, 1.0),
                     (2.0, 0.0), (2.0, 1.0)]
        for idx, (x, y) in enumerate(city_list):
            tsp.Add(idx+1, x, y)
        self.assertEqual(6, tsp.GetShortestTour())
    
    def testG2(self):
        tsp = TSP()
        city_list = [(0.0, 0.0), (0.0, 3.0),
                     (1.0, 0.0), (1.0, 3.0),
                     (5.0, 0.0)]
        for idx, (x, y) in enumerate(city_list):
            tsp.Add(idx+1, x, y)
        self.assertEqual(14, tsp.GetShortestTour())


class NewTSPTest(unittest2.TestCase):
    
    def testG1(self):
        tsp = NewTSP()
        city_list = [(0.0, 0.0), (0.0, 1.0),
                     (2.0, 0.0), (2.0, 1.0)]
        for idx, (x, y) in enumerate(city_list):
            tsp.Add(idx+1, x, y)
        self.assertEqual(6, tsp.GetShortestTour())
    
    def testG2(self):
        tsp = TSP()
        city_list = [(0.0, 0.0), (0.0, 3.0),
                     (1.0, 0.0), (1.0, 3.0),
                     (5.0, 0.0)]
        for idx, (x, y) in enumerate(city_list):
            tsp.Add(idx+1, x, y)
        self.assertEqual(14, tsp.GetShortestTour())


class TSPHWTest(unittest2.TestCase):

    def testHW(self):
        tsp = TSP([22000.0, 24000.00, 26000.00])
        with open('tsp.txt', 'r') as fd:
            total_cities = int(fd.readline())
            for city in range(1, total_cities+1):
                x, y = [float(e) for e in fd.readline().split()]
                tsp.Add(city, x, y)
        self.assertEqual(26442, tsp.GetShortestTour())


class NewTSPHWTest(unittest2.TestCase):

    def testHW(self):
        tsp = NewTSP([22000.0, 24000.00, 26000.00])
        with open('tsp.txt', 'r') as fd:
            total_cities = int(fd.readline())
            for city in range(1, total_cities+1):
                x, y = [float(e) for e in fd.readline().split()]
                tsp.Add(city, x, y)
        self.assertEqual(26442, tsp.GetShortestTour())


if __name__ == '__main__':
    unittest2.main()
