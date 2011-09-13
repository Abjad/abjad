from abjad.tools.pitchtools._Chromatic import _Chromatic
from abjad.tools.pitchtools._IntervalClass import _IntervalClass


class _ChromaticIntervalClass(_IntervalClass, _Chromatic):
    '''.. versionadded:: 2.0

    Chromatic interval-class base class.
    '''

    ### OVERLOADS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
