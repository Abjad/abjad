from abjad.tools.pitchtools._Diatonic import _Diatonic
from abjad.tools.pitchtools._Pitch import _Pitch


class _DiatonicPitch(_Pitch, _Diatonic):
    '''.. versionadded:: 2.0

    Diatonic pitch base class.
    '''

    ### OVERLOADS ###

    def __abs__(self):
        return self._number

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
