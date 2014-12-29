#!/usr/bin/python

import time

s1 = ['test']
s2 = s1[:]
r1 = range(1000)

t1 = time.time()
for i in r1:
    s1.append('i: %s' % i)
print 'time1: %s' % (time.time() - t1)

t2 = time.time()
s2.extend('i: %s' % i for i in r1)
print 'time2: %s' % (time.time() - t1)
