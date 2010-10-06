from abjad.core import _FlexEqualityComparator
from abjad.tools.pitchtools._PitchClass import _PitchClass


class _NumericPitchClass(_PitchClass, _FlexEqualityComparator):
   '''.. versionadded:: 1.1.2

   Numeric pitch-class base class from which concrete classes inherit.
   '''

   __slots__ = ( )
