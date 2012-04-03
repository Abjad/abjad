from abc import ABCMeta
from abjad.tools.pitchtools._Counterpoint import _Counterpoint
from abjad.tools.pitchtools._IntervalClass import _IntervalClass


class _CounterpointIntervalClass(_IntervalClass, _Counterpoint):
    '''.. versionadded:: 2.0

    Counterpoint interval-class base class.
    '''

    ### CLASS ATTRIBUTES ###
    
    __metaclass__ = ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
