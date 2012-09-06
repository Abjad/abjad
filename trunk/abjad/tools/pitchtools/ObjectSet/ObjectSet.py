import abc
from abjad.tools.abctools import ImmutableAbjadObject


class ObjectSet(frozenset, ImmutableAbjadObject):
    '''.. versionadded:: 2.0

    Music-theoretic set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
