from experimental.quantizationtools.Partitioner import Partitioner

class NullPartitioner(Partitioner):

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        pass
