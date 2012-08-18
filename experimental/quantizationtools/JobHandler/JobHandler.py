from abc import abstractmethod
from abjad.tools import abctools


class JobHandler(abctools.AbjadObject):
    '''Abstact job handler class from which concrete job handlers inherit.

    JobHandlers control how QuantizationJob instances are processed by the Quantizer,
    either serially or in parallel.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self, jobs):
        raise NotImplemented
