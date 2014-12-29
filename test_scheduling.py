#!/usr/bin/python


import unittest2


class Error(Exception):
    """Base error class."""


class Job(object):

    def __init__(self, weight, length):
        self.weight = weight
        self.length = length


class Scheduling(object):

    def __init__(self, jobs):
        if not jobs:
            raise Error('Invalid jobs: {}'.format(jobs))
        if not isinstance(jobs, list):
            jobs = [jobs]
        for job in jobs:
            if not isinstance(job, Job):
                raise Error('Invalid job: {}'.format(job))
        self.jobs = jobs

    def GetSortList(self):
        raise NotImplementedError

    def GetCmpTime(self):
        cmp_time, total_cmp_time = 0, 0
        for job in self.GetSortList():
            cmp_time += job.length
            total_cmp_time += job.weight*cmp_time
        return total_cmp_time


class DifferenceScheduling(Scheduling):
    """Scheduling based on difference of job weight and length."""

    def GetSortList(self):
        # Dress each job to sort jobs based on difference of weight & length
        # and break tie using job weight.
        job_list = [(job.weight-job.length, job.weight, job)
                    for job in self.jobs]
        sort_list = sorted(job_list, reverse=True)
        return [tup[2] for tup in sort_list]


class OptimalScheduling(Scheduling):            
    """Scheduling based on sorted ratio of job weight to length."""

    def GetSortList(self):
        return sorted(self.jobs, reverse=True,
                      key=lambda job: float(job.weight)/job.length)


class DifferenceTest(unittest2.TestCase):

    def testInvalidJobs(self):
        with self.assertRaises(Error):
            DifferenceScheduling(None)

    def testInvalidJob(self):
        with self.assertRaises(Error):
            DifferenceScheduling([Job(1, 1), None])

    def testJobs1(self):
        jobs = [Job(3, 5), Job(1, 2)]
        sch = DifferenceScheduling(jobs)
        expect = 2 + 3*(2+5)
        self.assertEqual(sch.GetCmpTime(), expect)


class OptimalTest(unittest2.TestCase):

    def testJobs1(self):
        jobs = [Job(1, 3), Job(2, 2), Job(3, 1)]
        sch = OptimalScheduling(jobs)
        expect = 3*1 + 2*(1+2) + (1+2+3)
        self.assertEqual(sch.GetCmpTime(), expect)


class HWBase(unittest2.TestCase):

    def GetJobs(self, file_name):
        with open(file_name, 'r') as fd:
            n_jobs = int(fd.next())
            self.jobs = []
            for _ in xrange(n_jobs):
                weight, length = [
                    int(element) for element in fd.next().split()]
                self.jobs.append(Job(weight, length))

    def GetCmpTime(self, sch_class):
        sch = sch_class(self.jobs)
        return sch.GetCmpTime()


class HWTest(HWBase):

    def setUp(self):
        self.GetJobs('jobs.txt')

    def testDifference(self):
        print 'Difference: Weighted completion time:', self.GetCmpTime(
            DifferenceScheduling)

    def testOptimal(self):
        print 'Optimal: Weighted completion time:', self.GetCmpTime(
            OptimalScheduling)


class SampleTest(HWBase):

    def setUp(self):
        self.GetJobs('jobs1.txt')

    def testDifference(self):
        print 'Difference: Weighted completion time:', self.GetCmpTime(
            DifferenceScheduling)

    def testOptimal(self):
        print 'Optimal: Weighted completion time:', self.GetCmpTime(
            OptimalScheduling)


if __name__ == '__main__':
    unittest2.main()
