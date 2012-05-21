from abc import ABCMeta
from abjad.tools.pitchtools._Diatonic import _Diatonic
from abjad.tools.pitchtools.PitchObject import PitchObject


class _DiatonicPitch(PitchObject, _Diatonic):
    '''.. versionadded:: 2.0

    Diatonic pitch base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._number

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
