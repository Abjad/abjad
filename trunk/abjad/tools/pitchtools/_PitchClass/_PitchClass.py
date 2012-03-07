from abjad.mixins import _FlexEqualityComparator
from abjad.mixins import _Immutable


class _PitchClass(_Immutable, _FlexEqualityComparator):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    ### OVERLOADS ###

    def __hash__(self):
        return hash(repr(self))
