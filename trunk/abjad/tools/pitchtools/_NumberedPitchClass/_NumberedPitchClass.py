from abjad.tools.pitchtools._Numbered import _Numbered
from abjad.tools.pitchtools._PitchClass import _PitchClass


#class _NumberedPitchClass(_PitchClass, _Numbered, _FlexEqualityComparator):
class _NumberedPitchClass(_PitchClass, _Numbered):
    '''.. versionadded:: 2.0

    Numbered pitch-class base class.
    '''

    __slots__ = ()
