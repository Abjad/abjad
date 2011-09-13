from abjad.tools.pitchtools._Counterpoint import _Counterpoint
from abjad.tools.pitchtools._Interval import _Interval


class _CounterpointInterval(_Interval, _Counterpoint):
    '''..versionadded:: 2.0

    Counterpoint interval base class.
    '''

    ### OVERLOADS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    ### PUBLIC ATTRIBUTES ###

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        raise NotImplementedError
