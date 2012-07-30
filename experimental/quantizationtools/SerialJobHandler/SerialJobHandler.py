from experimental.quantizationtools.JobHandler import JobHandler


class SerialJobHandler(JobHandler):

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        assert all([isinstance(job, QuantizationJob) for job in jobs])
        for job in jobs:
            job()
        return jobs        
