import copy
from abjad import Container
from abjad import Fraction
from abjad import Note
from abjad import Rest
from abjad import Tuplet
from abjad.core import _Immutable
from abjad.tools.durtools import is_binary_rational
from abjad.tools.mathtools import divisors
from abjad.tools.mathtools import greatest_power_of_two_less_equal
from abjad.tools.seqtools import flatten_sequence


class QGridDeletionTree(_Immutable):
   '''A model of the nested division structure of a Q-grid,
   and of which timepoints have been deleted in that grid.

   A QGridDeletionTree is defined by a list of integers and lists,
   where each list is prime in length, all integer members are 0 or 1,
   and all sublists follow that same model.

   ::

      abjad> from abjad.tools.quantizationtools import QGridDeletionTree
      abjad> tree = QGridDeletionTree([0, [1, 0], [1, 0, 1]])

   ::

      abjad> tree[1] = 1
      abjad> tree[-1] = 0
      abjad> tree
      QGridDeletionTree([0, [1, 0], [1, 0, 0]])

   ::

      abjad> tree.format_for_beatspan(Fraction(1, 4))
      Tuplet(2/3, [r8, {c'16, r16}, {* 3:2 c'16, r16, r16 *}])

   Return newly constructed QGridDeletionTree.
   '''

   __slots__ = ('_definition',)

   def __init__(self, arg):
      if isinstance(arg, self.__class__):
         object.__setattr__(self, '_definition', copy.copy(arg.definition))
      elif self._is_valid_q_grid_deletion_tree_definition(arg):
         object.__setattr__(self, '_definition', copy.copy(arg))
      else:
         raise ValueError('Bad argument: "%s"' % repr(arg))

   ## OVERRIDES ##

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
      for x in flatten_sequence(self.definition):
         yield x

   def __len__(self):
      return len(flatten_sequence(self.definition))

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __setitem__(self, item, value):
      if not isinstance(item, int):
         raise ValueError('Index must be an int.')
      if item < 0:
         item = len(self) + item
      if item < 0 or len(self) <= item:
         raise Exception('Index out of bounds.')
      if value not in [0, 1]:
         raise ValueError('Can only set with 0 or 1')
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
      recurse(self._definition, item, value, 0)

   ## PRIVATE ATTRIBUTES

   @property
   def _format_string(self):
      return '%s' % self.definition

   ## PRIVATE METHODS ##

   def _is_valid_q_grid_deletion_tree_definition(self, definition):
      def recurse(n):
         if not isinstance(n, list) or \
            not all([isinstance(x, (int, list)) for x in n]) or \
            not all([x in [0, 1] for x in filter(lambda y: isinstance(y, int), n)]) or \
            not set(divisors(len(n))) == set([1, len(n)]):
            return [False]
         results = [ ]
         for x in n:
            if isinstance(x, int):
               if x in [0, 1]:
                  results.append(True)
               else:
                  results.append(False)
            else:
               results.extend(recurse(x))
         return results
      return all(recurse(definition))

   ## PUBLIC ATTRIBUTES ##

   @property
   def definition(self):
      '''The list structure which defines the deletion tree's
      nested division structure.'''

      return copy.deepcopy(self._definition)

   ## PUBLIC METHODS ##

   def format_for_beatspan(self, beatspan = Fraction(1, 4)):
      '''Create a score tree representation of the deletion tree's
      nested division structure ::

         abjad> tree = QGridDeletionTree([0, [1, 0], [1, 0, 1]])
         abjad> tree.format_for_beatspan( )
         Tuplet(2/3, [r8, {c'16, r16}, {* 3:2 c'16, r16, c'16 *}])

      Return newly constructed tuplet or container.
      '''
      
      assert is_binary_rational(beatspan)
      if isinstance(beatspan, Fraction):
         assert beatspan.numerator == 1

      def recurse(n, division):
         pow = greatest_power_of_two_less_equal(len(n))
         val = Fraction(1, pow) * division

         if divisors(len(n)) == [1, 2]: # we are in a duple container
            c = Container([ ])
         else: # we are in a non-2 prime container, hence tuplet
            c = Tuplet(Fraction(pow, len(n)), [ ])

         for x in n:
            if isinstance(x, int):
               if x == 0:
                  c.append(Rest(val))
               else:
                  c.append(Note(0, val))
            else:
               c.append(recurse(x, val))

         return c

      return recurse(self.definition, beatspan)
