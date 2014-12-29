#!/usr/bin/python

import random
import sys


class Error(Exception):
    """Base error for this module."""


def isort(in_list):
    """Insersion sort.

    Args:
      in_list: Input list of integers to be sorted.
      
    Returns:
      Sorted list.
    """
    # TODO: Add more error checking.
    if not isinstance(in_list, list):
        raise Error('in_list: %s is not a list.' % in_list)
    if not in_list or len(in_list) == 1:
        return in_list
    for i in range(1, len(in_list)):
        ins_element = in_list[i]
        for j in range(i, -1, -1):
            if not j or in_list[j-1] < ins_element:
                break
            in_list[j] = in_list[j-1]
        in_list[j] = ins_element
    return in_list


def main():
    """Main function."""
    rand_100 = [random.randint(0, 1000) for _ in range(100)]
    rand_1000 = [random.randint(0, 10000) for _ in range(1000)]
    exp_results = [
        [[4, 3], [3, 4]],
        [[], []],
        [[3], [3]],
        [[1, 4, 3], [1, 3, 4]],
        [rand_100, sorted(rand_100)],
        [rand_1000, sorted(rand_1000)],
        ]
    for in_list, exp_result in exp_results:
        print 'Checking in_list: %s' % in_list
        res = isort(in_list)
        if res != exp_result:
            print '   FAIL.  Expect result: %s; find %s' % (exp_result, res)
            sys.exit(1)
        print '   PASS. Find %s\n' % res


if __name__ == '__main__':
    main()
