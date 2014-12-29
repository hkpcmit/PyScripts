#!/usr/bin/python
#
# Two 10M-line files, (no duplicated lines within each file). There are 800 lines
# appear in both 1% random sample from file A and 1% random sample from file B.
# Estimate how many lines appear in both original files.


import numpy
import random


DUPLICATES = 8000000 
TEN_MILLIONS = 10000000
SAMPLE_SIZE = 100000
NUMBER_TRIALS = 10


def main():
    f1 = range(TEN_MILLIONS)
    f2 = range(DUPLICATES - TEN_MILLIONS, DUPLICATES)
    dup_samples = []
    for _ in xrange(NUMBER_TRIALS):
        sample1, sample2 = [set(random.sample(population, SAMPLE_SIZE))
                            for population in (f1, f2)]
        dup = sample1.intersection(sample2)
        dup_samples.append(len(dup))
    print 'Mean number of duplicates:', numpy.mean(dup_samples)
    print 'Median number of duplicates:', numpy.median(dup_samples)


if __name__ == '__main__':
    main()
