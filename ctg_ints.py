#!/usr/bin/python


import random
import time


class Error(Exception):
    pass


def findMaxMin(input_set, item, inc=1):
    m = item
    while True:
        nxt = m + inc
        if nxt not in input_set:
            break
        m = nxt
    return m


def ctgInts1(input):
    if not isinstance(input, list):
        raise Error('input: %s is not a list' % input)
    if len(input) < 2:
        return input
    input_set = set(input)
    best = []
    while input_set:
        item = input_set.pop()
        mx = findMaxMin(input_set, item)
        mn = findMaxMin(input_set, item, inc=-1)
        cur = range(mn, mx+1)
        if len(cur) > len(best):
            best = cur
        input_set = input_set - set(cur)
    return best


def ctgInts2(input):
    if not isinstance(input, list):
        raise Error('input: %s is not a list' % input)
    if len(input) < 2:
        return input
    input_set = set(input)
    best = []
    best_length = 0
    while input_set:
        item = input_set.pop()
        mx = findMaxMin(input_set, item)
        mn = findMaxMin(input_set, item, inc=-1)
        cur_length = mx - mn + 1
        if cur_length > best_length:
            best = [mn, mx]
            best_length = cur_length
        input_set = set(item for item in input_set if item < mn or item > mx)
    return range(best[0], best[1]+1)


def ctgInts3(input):
    if not isinstance(input, list):
        raise Error('input: %s is not a list' % input)
    if len(input) < 2:
        return input
    input_set = set(input)
    best = []
    best_length = 0
    start_end_map = {}
    end_start_map = {}
    while input_set:
        item = input_set.pop()
        is_lower_end = (item + 1) in start_end_map
        is_upper_end = (item - 1) in end_start_map
        if is_lower_end and is_upper_end:
            cur = [end_start_map[item-1], start_end_map[item+1]]
            start_end_map[cur[0]] = cur[1]
            del start_end_map[item+1]
            end_start_map[cur[1]] = cur[0]
            del end_start_map[item-1]
        elif is_lower_end:
            cur = [item, start_end_map[item+1]]
            start_end_map[item] = cur[1]
            del start_end_map[item+1]
            end_start_map[cur[1]] = item
        elif is_upper_end:
            cur = [end_start_map[item-1], item]
            start_end_map[cur[0]] = item
            end_start_map[item] = cur[0]
            del end_start_map[item-1]
        else:
            cur = [item, item]
            start_end_map[item] = item
            end_start_map[item] = item
        cur_length = cur[1] - cur[0] + 1
        if cur_length > best_length:
            best, best_length = cur, cur_length
    return range(best[0], best[1]+1)


def testInts(input, expect):
    output = ctgInts2(input)
    if output == expect:
        print 'input: %s => %s' % (input, output)
    else:
        print 'ERROR: input %s => %s, but expect: %s' % (
            input, output, expect)


def testFunc():
    testInts([], [])
    testInts([1], [1])
    testInts([1, 2], [1, 2])
    input = range(10000)
    expect = range(10000)
    random.shuffle(input)
    testInts(input, expect)
    testInts([1, 8, 10, 6, 12, 5, 13, 7, 20], [5, 6, 7, 8])


def testTime():
    input = range(100000)
    random.shuffle(input)
    t1 = time.time()
    ctgInts1(input)
    t2 = time.time()
    ctgInts2(input)
    t3 = time.time()
    ctgInts3(input)
    t4 = time.time()
    print 'Time difference1: %s' % (t2 - t1)
    print 'Time difference2: %s' % (t3 - t2)
    print 'Time difference3: %s' % (t4 - t3)


def main():
    # testFunc()
    testTime()


if __name__ == '__main__':
    main()
