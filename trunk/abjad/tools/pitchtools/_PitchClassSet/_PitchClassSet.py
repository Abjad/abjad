from abc import ABCMeta
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class _PitchClassSet(ObjectSet):
    '''.. versionadded:: 2.0

    Pitch-class set base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
