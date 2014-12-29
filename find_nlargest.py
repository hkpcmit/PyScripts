#!/usr/bin/python

import random
import sys


class Error(Exception):
    """Base error for this module."""

def rec_nlargest(input_list, n):
    """Recursive function to find first n-th largest numbers from the given list.

    Args:
      input_list: Input list.
      n: First n-th largest numbers.

    Returns:
      List of first n-th largest numbers.
    """
    if not isinstance(input_list, list):
        raise Error('input_list is not a list.')
    if not input_list or not n:
        return []
    if len(input_list) == 1:
        return input_list
    if n == 1:
        return [max(input_list)]
    #pivot = input_list[0]
    #partition_list = input_list[1:]
    pivot_position = random.randint(0, len(input_list)-1)
    partition_list = input_list[:pivot_position] + input_list[pivot_position+1:]
    pivot = input_list[pivot_position]
    greater = [element for element in partition_list if element > pivot]
    lesser = [element for element in partition_list if element <= pivot]
    if not greater:
        return [pivot] + rec_nlargest(lesser, n-1)
    greater_leng = len(greater)
    if (greater_leng + 1) < n:
        return rec_nlargest(greater, greater_leng) + [pivot] + rec_nlargest(lesser, n-1-greater_leng)
    if (greater_leng + 1) == n:
        return rec_nlargest(greater, greater_leng) + [pivot]
    if greater_leng == n:
        return rec_nlargest(greater, greater_leng)
    return rec_nlargest(greater, n)


def main():
    """Main function."""
    shuffle_60 = range(60)
    random.shuffle(shuffle_60)
    random_100 = [random.randint(1, 100) for _ in range(70)]
    exp_results = [[[], 100, []],
                   [[100], 0, []],
                   [[50], 500, [50]],
                   [range(50), 1, [49]],
                   [range(50), 10, range(49, 39, -1)],
                   [range(50, -1, -1), 10, range(50, 40, -1)],
                   [shuffle_60, 10, range(59, 49, -1)],
                   [[24] * 40, 12, [24] * 12],
                   [random_100, 36, sorted(random_100, reverse=True)[:36]]
                   ] 
    for input_list, n, exp_result in exp_results:
        print 'Checking input_list: %s, n: %s' % (input_list, n)
        res = rec_nlargest(input_list, n)
        if res != exp_result:
            print '   FAIL.  Expect result: %s; find %s' % (exp_result, res)
            sys.exit(1)
        print '   PASS.  Find %s\n' % res


if __name__ == '__main__':
    main()
