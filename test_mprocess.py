#!/usr/bin/python


import multiprocessing
import random
import sys
import time


DEFAULT_NUMBER_PROCESSES = 3
DEFAULT_NUMBER_TASKS = 6


class Error(Exception):
    """Base error class for this module."""


class Task(object):
    """Task object."""

    def __init__(self, tid, work, args=None):
        """Initialize this object.

        Args:
          tid: Task ID.
          work: Work function.
          args: Tuple of arguments for the work function.
        """
        if not callable(work):
            raise Error('work: %s is not callable' % work)
        self.tid = tid
        self.work = work
        if args is None:
            args = ()
        self.args = args


def Work(tid, stime):
    """Simulate work of task.

    Args:
      tid: Task ID.
      stime: Sleep time.
    """
    ctime = time.asctime(time.localtime())
    sys.stdout.write('%s: TID: %s sleeping %s sec\n' % (ctime, tid, stime))
    time.sleep(stime)


def RunTasks(task):
    """Run each task in the multiprocessing pool.

    Args:
      task: Instance of Task.
    """
    res = task.work(*task.args)
    return (task.tid, res)
    

def main():
    """"Main function."""
    num_processes = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_NUMBER_PROCESSES
    pool = multiprocessing.Pool(num_processes)
    task_list = [Task(tid, Work, (tid, random.randint(1, 5)))
                 for tid in range(DEFAULT_NUMBER_TASKS)]
    results = pool.map(RunTasks, task_list)
    pool.close()


if __name__ == '__main__':
    main()
