# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import ImmutableAbjadObject


class Set(frozenset, ImmutableAbjadObject):
    '''Music-theoretic set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
