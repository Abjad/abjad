from abjad.core import _Immutable
from abjad.core import _UnaryComparator


class _Pitch(_Immutable, _UnaryComparator):
   '''.. versionadded:: 1.1.2

   Abstract pitch class from which concrete classes inherit.
   '''

   __slots__ = ('_format_string', )

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)
