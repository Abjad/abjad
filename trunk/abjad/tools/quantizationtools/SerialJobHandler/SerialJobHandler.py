from abjad.tools.quantizationtools.JobHandler import JobHandler


class SerialJobHandler(JobHandler):
    '''Processes ``QuantizationJob`` instances sequentially.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        for job in jobs:
            job()
        return jobs
