from experimental.quantizationtools.JobHandler import JobHandler


class SerialJobHandler(JobHandler):

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        for job in jobs:
            job()
        return jobs        
