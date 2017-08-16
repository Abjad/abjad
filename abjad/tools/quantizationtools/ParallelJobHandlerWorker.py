import multiprocessing
import pickle


class ParallelJobHandlerWorker(multiprocessing.Process):
    r'''Parallel job-handler worker.

    Worker process which runs ``QuantizationJobs``.

    Not composer-safe.

    Used internally by ``ParallelJobHandler``.
    '''

    ### INITIALIZER ###

    def __init__(self, job_queue=None, result_queue=None):
        multiprocessing.Process.__init__(self)
        job_queue = job_queue or ()
        result_queue = result_queue or ()
        self.job_queue = job_queue
        self.result_queue = result_queue

    ### PUBLIC METHODS ###

    def run(self):
        r'''Runs parallel job handler worker.

        Returns none.
        '''
        while True:
            job = self.job_queue.get()
            if job is None:
                # poison pill causes worker shutdown
                #print '{}: Exiting'.format(process_name)
                self.job_queue.task_done()
                break
            #print '{}: {!r}'.format(process_name, job)
            job = pickle.loads(job)
            job()
            self.job_queue.task_done()
            self.result_queue.put(pickle.dumps(job, protocol=0))
        return
