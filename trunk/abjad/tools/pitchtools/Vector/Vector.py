import abc

from abjad.tools.datastructuretools import ImmutableDictionary


class Vector(ImmutableDictionary):
    '''.. versionadded:: 2.0

    Music theoretic vector base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
