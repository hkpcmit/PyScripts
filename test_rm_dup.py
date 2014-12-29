#!/usr/bin/python


def RmDup(in_list):
    """Test interview response."""
    end = 1
    for i in range(len(in_list)):
        for j in range(i, end):
            if in_list[i] == in_list[j]: break
        if j == end:
            in_list[end] = in_list[i]
            end += 1
    return in_list

def main():
    """Test interview response."""
    input = [
        [1, 2],
        [1, 1, 3],
        ]
    for in_list in input:
        res = RmDup(in_list)
        print 'in_list: {0}; res: {1}'.format(in_list, res)


if __name__ == '__main__':
    main()
