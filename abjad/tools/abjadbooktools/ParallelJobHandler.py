# -*- encoding: utf-8 -*-
import multiprocessing
import pickle
from abjad.tools import abctools
from abjad.tools import systemtools


class ParallelJobHandler(abctools.AbjadObject):
    r'''Processes jobs in parallel, based on the number of CPUs available.
    '''

    ### INITIALIZER ###

    def __init__(self, message=None):
        self.message = message

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        r'''Calls parallel job handler.
        '''
        from abjad.tools import abjadbooktools
        finished_jobs = []
        total = len(jobs)
        job_queue = multiprocessing.JoinableQueue()
        result_queue = multiprocessing.Queue()
        workers = [abjadbooktools.ParallelJobHandlerWorker(
            job_queue, result_queue)
            for i in range(multiprocessing.cpu_count() * 2)]
        for worker in workers:
            worker.start()
        for job in jobs:
            job_queue.put(pickle.dumps(job, protocol=0))

        if self.message is not None:
            progress_indicator = systemtools.ProgressIndicator(
                message=self.message,
                total=total,
                )
            with progress_indicator:
                for i in range(len(jobs)):
                    finished_jobs.append(pickle.loads(result_queue.get()))
                    progress_indicator.advance()
        else:
            for i in range(len(jobs)):
                finished_jobs.append(pickle.loads(result_queue.get()))

        for worker in workers:
            job_queue.put(None)
        job_queue.join()
        result_queue.close()
        job_queue.close()
        for worker in workers:
            worker.join()
        return finished_jobs