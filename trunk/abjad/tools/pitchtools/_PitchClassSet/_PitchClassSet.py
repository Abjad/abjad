from abc import ABCMeta
from abjad.tools.pitchtools.PitchObjectSet import PitchObjectSet


class _PitchClassSet(PitchObjectSet):
    '''.. versionadded:: 2.0

    Pitch-class set base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
