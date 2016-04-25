# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.JobHandler import JobHandler


class SerialJobHandler(JobHandler):
    r'''Processes ``QuantizationJob`` instances sequentially.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        r'''Calls serial job handler.

        Returns `jobs`.
        '''
        for job in jobs:
            job()
        return jobs
