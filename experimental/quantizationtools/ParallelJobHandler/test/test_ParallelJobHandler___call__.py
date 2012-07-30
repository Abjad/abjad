from experimental import quantizationtools
from experimental.quantizationtools.JobHandler._Job import _Job


def test_ParallelJobHandler___call___01():

    jobs = [_Job(x) for x in range(1, 11)]
    job_handler = quantizationtools.ParallelJobHandler()
    finished_jobs = job_handler(jobs)
