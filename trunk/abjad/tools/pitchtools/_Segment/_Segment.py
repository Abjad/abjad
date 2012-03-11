from abc import ABCMeta
from abjad.tools.abctools import Immutable


class _Segment(tuple, Immutable):
    '''.. versionadded:: 2.0

    Mix-in base class for ordered collections of pitch objects.
    '''
    
    __metaclass__ = ABCMeta

    ### OVERLOADS ###

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
