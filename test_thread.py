#!/usr/bin/python


import Queue
import random
import sys
import time
import threading


DEFAULT_NUMBER_THREADS = 3
DEFAULT_NUMBER_TASKS = 6


class Worker(threading.Thread):
    """"Worker thread."""

    def __init__(self, name, queue):
        """Initialize this worker."""
        super(Worker, self).__init__()
        self.name = name
        self.queue = queue

    def run(self):
        """Run the thread."""
        while True:
            stime = self.queue.get()
            ctime = time.asctime(time.localtime())
            sys.stdout.write('%s: %s is sleeping for %s sec.\n' % (
                    ctime, self.name, stime))
            time.sleep(stime)
            self.queue.task_done()


def main():
    """"Main function."""
    num_threads = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_NUMBER_THREADS
    queue = Queue.Queue()
    threads = {}
    for num in range(num_threads):
        name = 't%s' % num
        threads[name] = Worker(name, queue)
        threads[name].setDaemon(True)
        threads[name].start()
    for _ in range(DEFAULT_NUMBER_TASKS):
        queue.put(random.randint(1, 5))
    queue.join()
    for _ in range(DEFAULT_NUMBER_TASKS):
        queue.put(random.randint(1, 5))
    queue.join()


if __name__ == '__main__':
    main()
