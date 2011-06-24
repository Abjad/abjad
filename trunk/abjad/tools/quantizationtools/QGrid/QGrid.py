from collections import Iterable
from abjad import Fraction
from abjad.core import _Immutable


class QGrid(_Immutable):
   '''A model of a Q-grid: an ordered set of rationals.

   While Q-grids are generally bounded by 0 and 1, this implementation
   allows for multiplication by ints and Fractions for easy scaling
   against beatspans.

   ::

      abjad> from abjad import Fraction
      abjad> from abjad.tools.quantizationtools import QGrid
      abjad> q_grid = QGrid([0, Fraction(1, 5), 1])
      abjad> q_grid
      QGrid((0, Fraction(1, 5), 1))
      abjad> q_grid * Fraction(1, 2)
      QGrid((Fraction(0, 1), Fraction(1, 10), Fraction(1, 2)))

   Return QGrid.
   '''

   __slots__ = ('_values',)

   def __init__(self, arg):
      assert isinstance(arg, Iterable)
      assert all([isinstance(x, (int, Fraction)) for x in arg])
      object.__setattr__(self, '_values', tuple(sorted(set(arg))))

   ## OVERRIDES ##

   def __contains__(self, item):
      if item in self._values:
         return True
      return False

   def __eq__(self, other):
      if type(self) == type(other):
         if self._values == other._values:
            return True
      return False

   def __getitem__(self, key):
      return self._values[key]

   def __getslice(self, start, stop):
      return self._values[start:stop]

   def __iter__(self):
      for x in self._values:
         yield x

   def __len__(self):
      return len(self._values)

   def __mul__(self, other):
      if isinstance(other, (int, Fraction)) and 0 < other:
         return QGrid([x * other for x in self])
      raise ValueError("Can't multiply QGrid with %s" % repr(other))

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __rmul__(self, other):
      return self.__mul__(other)

   ## PRIVATE METHODS ##
   
   @property
   def _format_string(self):
      return self._values
