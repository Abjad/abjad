from abc import ABCMeta
from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class _PitchClassSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Pitch-class segment base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
