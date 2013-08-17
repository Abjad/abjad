# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class CounterpointIntervalClass(IntervalClass):
    '''Counterpoint interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta
    
    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
