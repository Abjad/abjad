from abc import abstractmethod
from abjad.tools import abctools


class Partitioner(abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self, expr):
        raise NotImplemented
