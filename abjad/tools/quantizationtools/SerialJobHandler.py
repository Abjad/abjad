from abjad.tools.quantizationtools.JobHandler import JobHandler


class SerialJobHandler(JobHandler):
    r'''Serial job-handler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        r'''Calls serial job handler.

        Returns `jobs`.
        '''
        for job in jobs:
            job()
        return jobs
