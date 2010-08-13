from abjad.core import _Immutable


class _PitchClass(_Immutable):
   '''.. versionadded:: 1.1.2

   Abstract pitch-class class.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))
