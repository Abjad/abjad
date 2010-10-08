from abjad.core import _FlexEqualityComparator
from abjad.core import _Immutable


class _PitchClass(_Immutable, _FlexEqualityComparator):
   '''.. versionadded:: 1.1.2

   Abstract pitch-class class.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))
