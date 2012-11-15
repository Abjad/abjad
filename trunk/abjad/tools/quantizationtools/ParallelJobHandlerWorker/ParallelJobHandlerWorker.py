import multiprocessing
import pickle
from abjad.tools.abctools import AbjadObject


class ParallelJobHandlerWorker(multiprocessing.Process, AbjadObject):
    '''Worker process which runs ``QuantizationJobs``.

    Not composer-safe.

    Used internally by ``ParallelJobHandler``.

    Return ``ParallelJobHandlerWorker`` instance.
    '''

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
                #print '{}: Exiting'.format(proc_name)
                self.job_queue.task_done( )
                break
            #print '{}: {!r}'.format(proc_name, job)
            job = pickle.loads(job)
            job()
            self.job_queue.task_done( )
            self.result_queue.put(pickle.dumps(job, protocol=0))
        return
