from abc import ABCMeta
from abjad.tools.pitchtools.PitchObjectSet import PitchObjectSet


class _IntervalSet(PitchObjectSet):
    '''.. versionadded:: 2.0

    Abstract interval set.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
