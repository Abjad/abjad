from collections import Iterable
from copy import copy
from abjad import Fraction
from abjad.core import _Immutable
from abjad.tools.mathtools import divisors
from abjad.tools.seqtools import all_are_numbers
from abjad.tools.seqtools import flatten_sequence


class _QGrid(_Immutable):

   __slots__ = ('_definition', '_next', '_offsets')

   def __new__(klass, definition, next):
      self = object.__new__(klass)
      if not self._is_valid_grid_definition(definition):
         raise ValueError('Invalid _QGrid definition: %s' % repr(definition))
      if not isinstance(next, int):
         raise ValueError('"Next" value must be an int, got %s' % repr(next))
      object.__setattr__(self, '_definition', definition)
      object.__setattr__(self, '_next', next)
      object.__setattr__(self, '_offsets', self._expand_offsets( ))
      return self
   
   def __getnewargs__(self):
      return self._definition, self._next

   ## OVERRIDES ##

   def __eq__(self, other):
      if type(self) == type(other) and \
         self._definition == other._definition and \
         self._next == other._next:
         return True
      return False

   def __getitem__(self, item):
      if not isinstance(item, int):
         return None
      if item < 0:
         item = len(self) + item
      if item < 0 or len(self) <= item:
         return None

      for i, x in enumerate(self):
         if i == item:
            return x

   def __iter__(self):
      seq = flatten_sequence(self.definition)
      seq.append(self._next)
      for x in seq:
         yield x

   def __len__(self):
      return len(self.offsets)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __setitem__(self, item, value):
      def recurse(n, item, value, prev_count):
         count = prev_count
         for i, x in enumerate(n):
            if isinstance(x, list):
               count = recurse(x, item, value, count)
            else:
               if count == item:
                  n[i] = value
               count += 1
         return count

      if not isinstance(item, int):
         raise ValueError('Index must be an int.')
      if item < 0:
         item = len(self) + item
      if item < 0 or len(self) <= item:
         raise Exception('Index out of bounds.')
      if not isinstance(value, int):
         raise ValueError

      if item == len(self) - 1:
         object.__setattr__(self, '_next', item)
      else:
         recurse(self._definition, item, value, 0)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return '%s, %s' % (self._definition, self._next)

   ## PRIVATE METHODS ##

   def _expand_offsets(self):
      def recurse(n, prev_div, prev_offset):
         results = [ ]
         this_div = Fraction(1, len(n)) * prev_div
         for i, x in enumerate(n):
            this_offset = (i * this_div) + prev_offset
            if isinstance(x, int):
               results.append(this_offset)
            else:
               results.extend(recurse(x, this_div, this_offset))
         return results
      expanded = list(recurse(self._definition, 1, 0))
      expanded.append(1)
      return tuple(expanded)

   def _is_valid_grid_definition(self, definition):
      def recurse(n):
         if not isinstance(n, list) or \
            not all([isinstance(x, (int, list)) for x in n]) or \
            not set(divisors(len(n))) == set([1, len(n)]):
            return [False]
         results = [ ]
         for x in n:
            if isinstance(x, int):
               results.append(True)
            else:
               results.extend(recurse(x))
         return results
      return all(recurse(definition))

   ## PUBLIC ATTRIBUTES ##

   @property
   def definition(self):
      return copy(self._definition)

   @property
   def next(self):
      return self._next

   @property
   def offsets(self):
      return self._offsets

   ## PUBLIC METHODS ##

   def find_parentage_of_index(self, index):
      '''Return a tuple of the lengths of each container containing `index`,
      from the topmost to the bottommost.'''
      if index < 0:
         index = len(self) + index
      if index < 0 or len(self) <= index:
         return None
      if index == len(self) - 1:
         return None
      def recurse(n, index, prev_count):
         results = [ ]
         count = prev_count
         for i, x in enumerate(n):
            if isinstance(x, list):
               subcount, subresults = recurse(x, index, count)
               count = subcount
               if subresults:
                  results = [len(n)]
                  results.extend(subresults)
                  return count, results
            else:
               if index == count:
                  return count, [len(n)]
               count += 1
         return count, results
      return tuple(recurse(self.definition, index, 0)[1])

   def find_divisible_indices(self, points, multiplier = 1):
      '''Given a list of numbers 0 <= n <= 1, return a list of indices in self
      which "countain" those points, as though they were segments.'''
      assert all_are_numbers(points)
      assert isinstance(multiplier, (int, Fraction)) and 0 < multiplier
      points = filter(lambda x: 0 <= x <= multiplier, points)
      if multiplier != 1:
         offsets = [x * multiplier for x in self.offsets]
      else:
         offsets = self.offsets
      indices = [ ]
      for i in range(len(offsets) - 1):
         filtered = filter(lambda x: offsets[i] < x < offsets[i + 1], points)
         if filtered:
            indices.append(i)
      return indices

   def subdivide_indices(self, pairs):
      '''Given a list of 2-tuples, where for each tuple t,
      t[0] is a valid index into self, and t[1] is a prime integer
      greater than 1, return a new _QGrid with those indices subdivided.'''
      # add some validation here
      assert isinstance(pairs, Iterable) and \
         all([isinstance(x, Iterable) and len(x) == 2 for x in pairs]) and \
         all([0 <= x[0] < len(self) - 1 for x in pairs]) and \
         all([set(divisors(x[1])) == set([1, x[1]]) for x in pairs])
      pairs = sorted(pairs, key = lambda x: x[0])
      def recurse(n, prev_count):
         count = prev_count
         for i, x in enumerate(n):
            if isinstance(x, list):
               count = recurse(x, count)
            else:
               for pair in filter(lambda x: x[0] == count, pairs):
                  n[i] = [0] * pair[1]
                  pairs.pop(pairs.index(pair))
               count += 1
         return count
      definition = copy(self.definition)
      recurse(definition, 0)
      return _QGrid(definition, self.next)
