from abc import ABCMeta
from abjad.tools.abctools import FlexEqualityComparator
from abjad.tools.abctools import Immutable


class _PitchClass(Immutable, FlexEqualityComparator):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    __metaclass__ = ABCMeta

    ### OVERLOADS ###

    def __hash__(self):
        return hash(repr(self))
