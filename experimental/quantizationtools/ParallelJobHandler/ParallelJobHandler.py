from experimental.quantizationtools.JobHandler import JobHandler
from experimental.quantizationtools.ParallelJobHandlerWorker import ParallelJobHandlerWorker
import multiprocessing


class ParallelJobHandler(JobHandler):

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        assert all([isinstance(job, QuantizationJob) for job in jobs])

        finished_jobs = []
        job_queue = multiprocessing.JoinableQueue( )
        result_queue = multiprocessing.Queue( )
        workers = [ParallelJobHandlerWorker(job_queue, result_queue)
            for i in range(multiprocessing.cpu_count( ) * 2)]
        for worker in workers:
            worker.start( )
        for job in jobs:
            job_queue.put(job)
        for i in xrange(len(jobs)):
            finished_jobs.append(result_queue.get( ))
        for worker in workers:
            job_queue.put(None)
        job_queue.join( )
        result_queue.close( )
        job_queue.close( )
        for worker in workers:
             worker.join( )

        return finished_jobs

