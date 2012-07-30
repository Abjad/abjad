from abc import abstractmethod
from abjad.tools import abctools


class JobHandler(abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self, jobs):
        raise NotImplemented
