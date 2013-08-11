# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Segment(tuple, AbjadObject):
    '''Mix-in base class for ordered collections of pitch objects.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### CONSTRUCTOR ###

    @abc.abstractmethod
    def __new__(self):
        pass

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        return type(self)(tuple(self) + tuple(arg))

    def __getslice__(self, start, stop):
        return type(self)(tuple.__getslice__(self, start, stop))

    def __mul__(self, n):
        tmp = list(self)
        tmp *= n
        return type(self)(tmp)

    def __rmul__(self, n):
        return self * n
