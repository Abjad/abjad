from abc import ABCMeta
from abjad.tools.pitchtools._Segment import _Segment


class _PitchClassSegment(_Segment):
    '''.. versionadded:: 2.0

    Pitch-class segment base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
