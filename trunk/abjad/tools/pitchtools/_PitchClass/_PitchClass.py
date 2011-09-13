from abjad.core import _FlexEqualityComparator
from abjad.core import _Immutable


class _PitchClass(_Immutable, _FlexEqualityComparator):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    ### OVERLOADS ###

    def __hash__(self):
        return hash(repr(self))
