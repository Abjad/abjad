from abjad.core import _Immutable


class _Pitch(_Immutable):
   '''.. versionadded:: 1.1.2

   Abstract pitch class from which concrete classes inherit.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))
