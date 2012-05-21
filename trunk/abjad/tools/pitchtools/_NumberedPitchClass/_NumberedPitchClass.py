from abc import ABCMeta
from abjad.tools.pitchtools._Numbered import _Numbered
from abjad.tools.pitchtools.PitchClassObject import PitchClassObject


class _NumberedPitchClass(PitchClassObject, _Numbered):
    '''.. versionadded:: 2.0

    Numbered pitch-class base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
