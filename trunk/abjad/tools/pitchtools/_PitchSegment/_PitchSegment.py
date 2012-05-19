from abc import ABCMeta
from abjad.tools.pitchtools.PitchObjectSegment import PitchObjectSegment


class _PitchSegment(PitchObjectSegment):
    '''.. versionadded:: 2.0

    Pitch segment base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
