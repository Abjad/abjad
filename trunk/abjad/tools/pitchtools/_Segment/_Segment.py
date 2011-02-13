from abjad.core import _Immutable


class _Segment(tuple, _Immutable):
   '''.. versionadded:: 1.1.2

   Mix-in base class for ordered collections of pitch objects.
   '''

   ## OVERLOADS ##

   def __getslice__(self, start, stop):
      return type(self)(tuple.__getslice__(self, start, stop))   
