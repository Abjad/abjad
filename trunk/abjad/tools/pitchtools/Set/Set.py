# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Set(frozenset, AbjadObject):
    '''Music-theoretic set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
