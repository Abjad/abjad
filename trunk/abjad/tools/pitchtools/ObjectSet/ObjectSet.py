from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools import ImmutableAbjadObject


class ObjectSet(frozenset, ImmutableAbjadObject):
    '''.. versionadded:: 2.0

    Music-theoretic set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(self):
        pass
