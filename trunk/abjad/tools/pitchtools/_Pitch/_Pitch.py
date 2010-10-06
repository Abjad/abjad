from abjad.core import _Immutable
from abjad.core import _StrictComparator


class _Pitch(_Immutable, _StrictComparator):
   '''.. versionadded:: 1.1.2

   Abstract pitch class from which concrete classes inherit.
   '''

   __slots__ = ( )

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg
