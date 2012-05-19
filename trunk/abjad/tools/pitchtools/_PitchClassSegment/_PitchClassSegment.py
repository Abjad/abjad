from abc import ABCMeta
from abjad.tools.pitchtools.PitchObjectSegment import PitchObjectSegment


class _PitchClassSegment(PitchObjectSegment):
    '''.. versionadded:: 2.0

    Pitch-class segment base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
