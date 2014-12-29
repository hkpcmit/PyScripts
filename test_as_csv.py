#!/usr/bin/python


import collections
import re
import unittest2


RE_AS = re.compile(r'AS(\d)\s+(\d+)')
RE_LOC = re.compile(r'([A-Z]{3})')


class Error(Exception):
    """Error class."""


class LocationData(object):

    def __init__(self, locations=None, max_as_num=0):
        if not locations:
            locations = collections.OrderedDict()
        self.locations = locations
        self.max_as_num = max_as_num


def GetLocationData(file_name):

    data = LocationData()
    loc_dict = {}
    with open(file_name, 'r') as fd:
        for line in fd:
            line.rstrip()
            if not line:
                continue
            loc_res = RE_LOC.search(line)
            if loc_res:
                loc_dict = {}
                data.locations[loc_res.group(1)] = loc_dict
                continue
            as_res = RE_AS.search(line)
            if as_res:
                as_num = int(as_res.group(1))
                loc_dict[as_num] = as_res.group(2)
                if as_num > data.max_as_num:
                    data.max_as_num = as_num
    return data


def GetCsvList(location_data):

    output = []
    for loc, loc_dict in location_data.locations.iteritems():
        loc_list = [loc]
        loc_list.extend(['0'] * location_data.max_as_num)
        for idx, value in loc_dict.iteritems():
            loc_list[idx] = value
        output.append(','.join(loc_list))
    return output


def ToCsv(file_name):

    if not isinstance(file_name, basestring):
        raise Error('Invalid file_name: {}'.format(file_name))
    location_data = GetLocationData(file_name)
    return GetCsvList(location_data)


class TestAsCsv(unittest2.TestCase):
    
    def testInvalidFileName(self):
        self.assertRaises(Error, ToCsv, None)

    def testToCsv(self):
        file_name = 'AsInput.txt'
        expect = ['IAD,912157,54230,0,0,0',
                  'LGA,168827,0,0,0,0',
                  'DFW,986305,0,381136,0,0',
                  'MIA,362312,0,0,822294,634742']
        self.assertListEqual(expect, ToCsv(file_name))



if __name__ == '__main__':
    unittest2.main()
