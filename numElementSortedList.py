#!/usr/bin/python


import bisect


class Error(Exception):
    """Base error for this module."""


def numElements(input_list, element):
    if not isinstance(input_list, list):
        raise Error('{} is not a list.'.format(input_list))
    if not input_list:
        return 0
    position = bisect.bisect(input_list, element)
    if input_list[position-1] != element:
        return 0
    lower_end = bisect.bisect(input_list, element-1, hi=position)
    return position - lower_end
    

def main():
    fail_unexp_num_fmt = 'FAIL: Number of {}: {} found in {}; Expect: {}'
    pass_not_found_fmt = 'PASS: {} is not found in {}'
    pass_num_fmt = 'PASS: Number of {}: {} found in {}'
    # Test 1.
    try:
        res = numElements(None, 0)
        print 'FAIL: {} produces {}'.format(None, res)
    except Error as err:
        if str(err) == 'None is not a list.':
            print 'PASS: {}'.format(err)
        else:
            print 'FAIL: {}'.format(err)
    # Test 2.
    input = []
    element = 10
    res = numElements(input, element)
    if res == 0:
        print pass_not_found_fmt.format(element, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 0)
    # Test 3.
    element = 30
    input = [element]
    res = numElements(input, element)
    if res == 1:
        print pass_num_fmt.format(element, res, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 1)
    # Test 4.
    input = [60]
    element = 30
    res = numElements(input, element)
    if res == 0:
        print pass_not_found_fmt.format(element, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 0)
    # Test 5.
    input = [60, 70]
    element = 80
    res = numElements(input, element)
    if res == 0:
        print pass_not_found_fmt.format(element, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 0)
    # Test 6.
    input = [60, 70]
    element = 30
    res = numElements(input, element)
    if res == 0:
        print pass_not_found_fmt.format(element, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 0)
    # Test 7.
    element = 30
    input = [element, element]
    res = numElements(input, element)
    if res == 2:
        print pass_num_fmt.format(element, res, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 2)
    # Test 8.
    element = 30
    input = [0, element, element, element, 100]
    res = numElements(input, element)
    if res == 3:
        print pass_num_fmt.format(element, res, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 3)
    # Test 9.
    element = 0
    input = [element, 10, 20, 100]
    res = numElements(input, element)
    if res == 1:
        print pass_num_fmt.format(element, res, input)
    else:
        print fail_unexp_num_fmt.format(element, res, input, 1)


if __name__ == '__main__':
    main()
