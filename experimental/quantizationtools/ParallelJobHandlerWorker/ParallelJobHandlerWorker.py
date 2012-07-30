from abjad.tools import abctools
import multiprocessing


class ParallelJobHandlerWorker(multiprocessing.Process, abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self, job_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.job_queue = job_queue
        self.result_queue = result_queue

    ### PUBLIC METHODS ###

    def run(self):
        proc_name = self.name
        while True:
            job = self.job_queue.get( )
            if job is None:
                # poison pill causes worker shutdown
                # print '%s: Exiting' % proc_name
                self.job_queue.job_done( )
                break
            # print '%s: %s %d' % (proc_name, job, job.offset)
            job()
            self.job_queue.job_done( )
            self.result_queue.put(job)
        return

