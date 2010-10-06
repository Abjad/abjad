from abjad.core import _Immutable
from abjad.core import _StrictComparator


class _PitchClass(_Immutable, _StrictComparator):
   '''.. versionadded:: 1.1.2

   Abstract pitch-class class.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))
