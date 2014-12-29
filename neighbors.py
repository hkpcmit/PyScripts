#!/usr/bin/python

SIZE = 3

class Error(Exception):
    """Base error class."""

class Position(object):

    def __init__(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise Error('Both x: %r and y: %r must be integers' % (x, y))
        self.x = x
        self.y = y

    def __str__(self):
        return ','.join([str(self.x), str(self.y)])
    
    def GetNeighbors(self):
        if self.x > 0:
            neigh_x = self.x - 1
            if self.y > 0:
                yield Position(neigh_x, self.y-1)
            yield Position(neigh_x, self.y)
            if self.y < SIZE - 1:
                yield Position(neigh_x, self.y+1)
        if self.y > 0:
            yield Position(self.x, self.y-1)
        if self.y < SIZE - 1:
            yield Position(self.x, self.y+1)
        if self.x < SIZE - 1:
            neigh_x = self.x + 1
            if self.y > 0:
                yield Position(neigh_x, self.y-1)
            yield Position(neigh_x, self.y)
            if self.y < SIZE - 1:
                yield Position(neigh_x, self.y+1)            


def main():
    current = Position(0, 0)
    for p in current.GetNeighbors():
        print 'Neighbor: %s' % p

if __name__ == '__main__':
    main()
