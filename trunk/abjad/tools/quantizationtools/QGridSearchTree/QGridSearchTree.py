import copy
from itertools import groupby
from abjad import Fraction
from abjad.core import _Immutable
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import is_binary_rational
from abjad.tools.mathtools import divisors
from abjad.tools.mathtools import integer_to_binary_string
from abjad.tools.seqtools import yield_outer_product_of_sequences
from abjad.tools.quantizationtools.QGridRhythmTree import QGridRhythmTree
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class QGridSearchTree(_Immutable):
   '''A model of a Q-grid search tree, which defines the permissible divisions 
   in a set of Q-grid rhythm trees.'''

   __slots__ = ('_definition', '_rhythm_trees',)

   def __init__(self, *args):
      if len(args):
         if isinstance(args[0], self.__class__):
            definition = copy.copy(args[0]._definition)
         elif self._is_valid_q_grid_search_tree_definition(args[0]):
            definition = copy.copy(args[0])
         else:
            raise ValueError('Bad instantiation arguments: "%s"' % args)
      else:
         definition = self._make_nauert_q_grid_search_tree_definition( )

      object.__setattr__(self, '_definition', definition)
      object.__setattr__(self, '_rhythm_trees', None) # lazy load

   ## OVERRIDES ##

   def __contains__(self, item):
      if isinstance(item, QGridRhythmTree):
         if item in self.rhythm_trees:
            return True
      return False

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
      return ' '

   ## PRIVATE METHODS ##

   def _expand_q_grid_search_tree_to_q_grid_rhythm_trees(self, search_tree):
      assert isinstance(search_tree, self.__class__)

      def recurse(subtree):
         results = [ ]
         for key in subtree:
            if subtree[key] is None:
               # if no subtree, just add the result to results
               results.append((key,))
            else:
               # get all compositions, then sort them
               compositions = self._yield_all_grouped_binary_compositions_of_integer(key)
               compositions = self._sort_grouped_binary_compositions(compositions)
               # get the results for the subtree below this key
               subsubtree_result = recurse(subtree[key])
               # initialize the count of insertion points, and the outer_product
               # of our none_count * [subsubtree_result]
               none_count = 0
               outer_product = None
               # loop through the compositions, update as we go (and cache!)
               for composition in compositions:
                  current_none_count = len(filter(lambda x: x is None, composition))
                  if not current_none_count: # skip if nothing
                     results.append(tuple(composition))
                     continue
                  if none_count != current_none_count:
                     none_count = current_none_count
                     outer_product = [x for x in yield_outer_product_of_sequences(
                        none_count * [subsubtree_result])] # this might fail, so test!
                  for op in outer_product: # replace each None with outer_product subtree
                     count = 0
                     result = list(composition)
                     for idx, item in enumerate(result):
                        if item is None:
                           result[idx] = op[count]
                           count += 1
                     results.append(tuple(result))
         return tuple(results)

      return [QGridRhythmTree(x) for x in recurse(search_tree.definition)]

   def _is_valid_q_grid_search_tree_definition(self, definition):
      if not isinstance(definition, dict):
         return False
      def recurse(n):
         results = [ ]
         for key in n:
            if not isinstance(key, int) or \
               not 0 < key or \
               not divisors(key) == [1, key]:
               results.append(False)
            elif not isinstance(n[key], (dict, type(None))):
               results.append(False)
            elif isinstance(n[key], dict) and not recurse(n[key]):
               results.append(False)
            else:
               results.append(True)
         return results
      return all(recurse(definition))
     
   def _make_nauert_q_grid_search_tree_definition(self):
      return {
         2: {              # 1/2
            2: {           # 1/4
               2: {        # 1/8
                  2: None, # 1/16
               },
               3: None,    # 1/12
            },
            3: None,       # 1/6
            5: None,       # 1/10
            7: None,       # 1/14
         },
         3: {              # 1/3
            2: {           # 1/6
               2: None,    # 1/12
            },
            3: None,       # 1/9
            5: None,       # 1/15
         },
         5: {              # 1/5
            2: None,       # 1/10
            3: None,       # 1/15
         },
         7: {              # 1/7
            2: None,       # 1/14
         },
         11: None,         # 1/11
         13: None,         # 1/13
      }

   def _sort_grouped_binary_compositions(self, compositions):
      return list(sorted(compositions,
         key = lambda x: (filter(lambda y: y is None, x), len(x))))      

   def _yield_all_grouped_binary_compositions_of_integer(self, n):
      assert isinstance(n, int) and 0 < n
      x = 0
      string_length = n
      while x < 2 ** n:
         result = [ ]
         string = integer_to_binary_string(x)
         string = string.zfill(string_length)
         l = [int(c) for c in list(string)]
         g = groupby(l, lambda x: x)
         for value, group in g:
            if value:
               result.extend([None] * len(list(group)))
            else:
               result.append(len(list(group)))
         x += 1
         yield result

   ## PUBLIC ATTRIBUTES ##

   @property
   def definition(self):
      return copy.copy(self._definition)

   @property
   def rhythm_trees(self):
      if self._rhythm_trees is None:
         object.__setattr__(self, '_rhythm_trees',
            self._expand_q_grid_search_tree_to_q_grid_rhythm_trees(self))
      return self._rhythm_trees

   ## PUBLIC METHODS ##

   def prune(self, tempo, threshold, beatspan = Fraction(1, 4)):
      assert isinstance(tempo, TempoMark)
      assert 0 < threshold
      assert is_binary_rational(beatspan)
      if isinstance(beatspan, Fraction):
         assert beatspan.numerator == 1

      def recurse(old_node, prev_div):
         new_node = { }
         for key in old_node:
            div = Fraction(1, key)
            dur = tempo_scaled_rational_to_milliseconds(prev_div * div, tempo)
            if threshold <= dur:
               if old_node[key] is None:
                  new_node[key] = None
               else:
                  new_node[key] = recurse(old_node[key], div)
         if not new_node:
            return None
         return new_node

      return QGridSearchTree(recurse(self.definition, beatspan))
