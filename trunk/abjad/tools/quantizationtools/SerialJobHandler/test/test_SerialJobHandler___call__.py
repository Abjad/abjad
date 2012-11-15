from abjad.tools import quantizationtools
from abjad.tools.quantizationtools.JobHandler._Job import _Job


def test_SerialJobHandler___call___01():

    jobs = [_Job(x) for x in range(1, 11)]
    job_handler = quantizationtools.SerialJobHandler()
    finished_jobs = job_handler(jobs)
