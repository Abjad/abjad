from abc import ABCMeta
from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class _PitchSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Pitch segment base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
