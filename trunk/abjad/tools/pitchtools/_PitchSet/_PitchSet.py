from abc import ABCMeta
from abjad.tools.pitchtools.PitchObjectSet import PitchObjectSet


class _PitchSet(PitchObjectSet):
    '''.. versionadded:: 2.0

    Pitch set base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
