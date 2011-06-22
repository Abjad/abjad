import copy
from abjad import Fraction
from abjad.core import _Immutable
from abjad.tools.durtools import is_binary_rational
from abjad.tools.mathtools import divisors
from abjad.tools.quantizationtools.QGrid import QGrid
from abjad.tools.quantizationtools.QGridDeletionTree import QGridDeletionTree


class QGridRhythmTree(_Immutable):
   '''A model of a Q-grid's nesting division structure.'''

   __slots__ = ('_deletion_tree', '_definition', '_q_grid',)

   def __init__(self, arg):
      if isinstance(arg, self.__class__):
         object.__setattr__(self, '_definition', arg.definition)
      elif self._is_valid_q_grid_rhythm_tree_definition(arg):
         object.__setattr__(self, '_definition', arg)
      else:
         raise ValueError('Bad argument: "%s"' % repr(arg))
      object.__setattr__(self, '_deletion_tree', None) # lazy load
      object.__setattr__(self, '_q_grid', None) # lazy load

   ## OVERRIDES ##

   def __eq__(self, other):
      if type(self) == type(other):
         if self.definition == other.definition:
            return True
      return False

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return self.definition

   ## PRIVATE METHODS ##

   def _expand_q_grid_rhythm_tree_to_q_grid(self, rhythm_tree):
      assert isinstance(rhythm_tree, self.__class__)
      def recurse(n, prev_div, prev_offset):
         results = [ ]
         div = Fraction(1, \
            sum(filter(lambda x: isinstance(x, int), n)) \
            + len(filter(lambda x: not isinstance(x, int), n))) \
            * prev_div
         idx = 0 # for counting
         for x in n:
            if isinstance(x, int):
               for j in range(idx, idx + x):
                  results.append((div * j) + prev_offset)
               idx += x
            else:
               results.extend(recurse(x, div, (div * idx) + prev_offset))
               idx += 1
         return tuple(results)
      expanded = list(recurse(rhythm_tree.definition, 1, 0))
      expanded.append(1)
      return QGrid(tuple(expanded))

   def _expand_q_grid_rhythm_tree_to_q_grid_deletion_tree(self, rhythm_tree):
      assert isinstance(rhythm_tree, self.__class__)
      def recurse(n):
         results = [ ]
         for x in n:
            if isinstance(x, int):
               results.extend([0] * x)
            else:
               results.append(recurse(x))
         return results
      return QGridDeletionTree(recurse(rhythm_tree.definition))


   def _is_valid_q_grid_rhythm_tree_definition(self, definition):
      def recurse(n):
         results = [ ]
         # every level should be a non-zero-length list
         if not isinstance(n, tuple) or not n:
            return [False]
         # all items at every level should be ints or more lists
         if not all([isinstance(x, (int, tuple)) for x in n]):
            return [False]
         # all int items should be greater than zero
         if not all([0 < x for x in filter(lambda y: isinstance(y, int), n)]):
            return [False]
         # the division at every level should be greater than zero and prime
         div = sum(filter(lambda x: isinstance(x, int), n)) \
            + len(filter(lambda x: not isinstance(x, int), n))
         if not set(divisors(div)) == set([1, div]):
            return [False]
         for x in n:
            if isinstance(x, tuple):
               results.extend(recurse(x))
            else:
               results.append(True)
         return results
      return all(recurse(definition))

   ## PUBLIC ATTRIBUTES ##

   @property
   def deletion_tree(self):
      if self._deletion_tree is None:
         object.__setattr__(self, '_deletion_tree',
            self._expand_q_grid_rhythm_tree_to_q_grid_deletion_tree(self))
      return copy.copy(self._deletion_tree) # Q-grid binary trees are semi-immutable

   @property
   def definition(self):
      return self._definition

   @property
   def q_grid(self):
      if self._q_grid is None:
         object.__setattr__(self, '_q_grid',
            self._expand_q_grid_rhythm_tree_to_q_grid(self))
      return self._q_grid
