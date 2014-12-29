#!/usr/bin/python


import sys


class Error(Exception):
    """Base error class for this module."""


def inc_int(int_list):
    """Increment integer digit list by 1.

    Args:
      int_list: List of integer digits.
      
    Returns:
      List of digits of incremented integer.
    """
    if not isinstance(int_list, list):
        raise Error('input_list: %s is not a list.' % input_list)
    carry_over = False
    for i in range(len(int_list) - 1, -1, -1):
        inc_digit = int(int_list[i]) + 1
        if inc_digit < 10:
            carry_over = False
            int_list[i] = str(inc_digit)
            break
        carry_over = True
        int_list[i] = '0'
    if carry_over:
        #result = ['1']
        #result.extend(int_list)
        #return result
        int_list[:0] = '1'
    return int_list


def main():
    """Main function."""
    exp_results = [
        [['1', '1', '9'], ['1', '2', '0']],
        [['2', '9', '9'], ['3', '0', '0']],
        [['9'], ['1', '0']],
        [['0'], ['1']],
        [['9', '9', '9'], ['1', '0', '0', '0']],
        ]
    for int_list, exp_result in exp_results:
        print 'Checking integer digit list: %s' % int_list
        res = inc_int(int_list)
        if res != exp_result:
            print '   FAIL.  Expect result: %s; find %s' % (exp_result, res)
            sys.exit(1)
        print '   PASS.  Find %s\n' % res


if __name__ == '__main__':
    main()
