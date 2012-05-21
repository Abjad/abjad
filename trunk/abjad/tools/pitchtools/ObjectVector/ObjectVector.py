from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.datastructuretools import ImmutableDictionary


class ObjectVector(ImmutableDictionary):
    '''.. versionadded:: 2.0

    Music theoretic vector base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
