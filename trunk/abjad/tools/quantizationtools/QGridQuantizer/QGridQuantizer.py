from collections import Iterable
from copy import copy
from itertools import groupby
from abjad import Container
from abjad import Fraction
from abjad import Rest
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import is_binary_rational
from abjad.tools.leaftools import fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.mathtools import divisors
from abjad.tools.quantizationtools._QGrid import _QGrid
from abjad.tools.quantizationtools._Quantizer import _Quantizer
from abjad.tools.quantizationtools.group_timepoints_by_beatspan \
   import group_timepoints_by_beatspan
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.seqtools import flatten_sequence
from abjad.tools.seqtools import iterate_sequence_pairwise_strict
from abjad.tools.seqtools import yield_outer_product_of_sequences
from abjad.tools.tietools import TieSpanner
from abjad.tools.tietools import get_tie_chain


class QGridQuantizer(_Quantizer):

   __slots__ = ('_beatspan', '_beatspan_ms', '_search_tree',
      '_tempo', '_tempo_lookup', '_threshold')

   def __init__(self,
      search_tree = None,
      beatspan = Fraction(1, 4),
      tempo = TempoMark(Fraction(1, 4), 60),
      threshold = None):

      ## CREATE DEFAULT SEARCH TREE IF NONE PROVIDED
      if search_tree is None:
         search_tree = self._make_standard_search_tree( )
      else:
         assert self._is_valid_search_tree_definition(search_tree)

      assert is_binary_rational(beatspan)
      if isinstance(beatspan, Fraction):
         assert beatspan.numerator == 1

      assert isinstance(tempo, TempoMark)

      ## PRUNE SEARCH TREE (OPTIONAL)
      if threshold is not None:
         assert 0 < threshold
         search_tree = self._prune_search_tree(search_tree, beatspan, tempo, threshold)

      ## SET ATTRS
      object.__setattr__(self, '_beatspan', beatspan)
      object.__setattr__(self, '_beatspan_ms', 
         tempo_scaled_rational_to_milliseconds(beatspan, tempo))
      object.__setattr__(self, '_q_grids', None) # lazy load
      object.__setattr__(self, '_search_tree', search_tree)
      object.__setattr__(self, '_search_tree_offsets', None) # lazy load
      object.__setattr__(self, '_tempo', tempo)
      object.__setattr__(self, '_tempo_lookup', None) # lazy load
      object.__setattr__(self, '_threshold', threshold)

   ## PRIVATE METHODS ##

   def _divide_grid(self, grid, timepoints):
      def recurse(grid, timepoints):
         results = [ ]
         indices = grid.find_divisible_indices(timepoints)
         divisors = [self._find_q_grid_parentage_divisibility(
            grid.find_parentage_of_index(index))
            for index in indices]
         filtered = filter(lambda x: x[1], zip(indices, divisors))
         if not filtered:
            return results
         indices = [x[0] for x in filtered]
         combinations = yield_outer_product_of_sequences([x[1] for x in filtered])
         for combination in combinations:
            zipped = zip(indices, combination)
            results.append(grid.subdivide_indices(zipped))
            results.extend(recurse(results[-1], timepoints))
         return results
      return recurse(grid, timepoints)

   def _find_q_grid_parentage_divisibility(self, parentage):
      node = self.search_tree[parentage[0]]
      for item in parentage[1:]:
         node = node[item]
         if node is None:
            return [ ]
      if node is None:
         return [ ]
      return node.keys( )

   def _is_valid_search_tree_definition(self, definition):
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

   def _make_standard_search_tree(self):
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

   def _prune_search_tree(self, search_tree, beatspan, tempo, threshold):
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
      return recurse(search_tree, beatspan)

   ## PUBLIC ATTRIBUTES ##

   @property
   def beatspan(self):
      return self._beatspan

   @property
   def beatspan_ms(self):
      return self._beatspan_ms

   @property
   def search_tree(self):
      return copy(self._search_tree)

   @property
   def search_tree_offsets(self):
      def recurse(n, prev_div, prev_offset):
         results = [ ]
         for k in n:
            div = Fraction(1, k) * prev_div
            for i in range(k):
               results.append(prev_offset + (i * div))
               if n[k] is not None:
                  results.extend(recurse(n[k], div, prev_offset + (i * div)))
         return results
      if self._search_tree_offsets is None:
         offsets = list(sorted(set(recurse(self.search_tree, 1, 0))))
         offsets.append(Fraction(1))
         object.__setattr__(self, '_search_tree_offsets', tuple(offsets))
      return self._search_tree_offsets

   @property
   def tempo(self):
      return self._tempo

   @property
   def tempo_lookup(self):
      if self._tempo_lookup is None:
         lookup = { }
         for offset in self.search_tree_offsets:
            new_offset = self.beatspan * offset
            lookup[offset] = tempo_scaled_rational_to_milliseconds(new_offset, self.tempo)
         object.__setattr__(self, '_tempo_lookup', lookup)
      return copy(self._tempo_lookup)

   @property
   def threshold(self):
      return self._threshold

   ## PUBLIC METHODS ##

   def quantize(self, *args, **kwargs):
      # validate input
      if len(args) == 1:
         assert all([isinstance(x, int) for x in args[0]])
         durations = args[0]
      elif 1 < len(args):
         assert all([isinstance(x, (int, Fraction)) for x in args[0]])
         assert isinstance(args[1], TempoMark)
         durations = [tempo_scaled_rational_to_milliseconds(x, args[1])
            for x in args[0]]
      if 'verbose' in kwargs:
         verbose = bool(kwargs['verbose'])
      else:
         verbose = False

      # calculate attack points
      offsets = cumulative_sums_zero([abs(x) for x in durations])[:-1]
      timepoints = zip(offsets, durations)
      if verbose:
         print 'TIMEPOINTS: %s' % offsets

      # group timepoints
      grouped_timepoints = group_timepoints_by_beatspan(timepoints, self.beatspan_ms, subscript = 0)

      # find best Q-grids for each beatspan
      if verbose:
         print 'Q-GRIDS:'
      per_beatspan_q_grids = { }
      for beatspan_number in sorted(grouped_timepoints.keys( )):
         mod_timepoints = [Fraction(x[0] % self.beatspan_ms) / self.beatspan_ms \
            for x in grouped_timepoints[beatspan_number]]
         # build Q-grid list
         per_beatspan_q_grids[beatspan_number] = [_QGrid([0], 0)]
         for k in self.search_tree:
            g = _QGrid([0] * k, 0)
            per_beatspan_q_grids[beatspan_number].append(g)
            per_beatspan_q_grids[beatspan_number].extend(self._divide_grid(g, mod_timepoints))
         # find error
         for i, q_grid in enumerate(per_beatspan_q_grids[beatspan_number]):
            error, points = _compare_timepoints_to_q_grid(mod_timepoints, q_grid)
            per_beatspan_q_grids[beatspan_number][i] = (error, points, q_grid)
         # sort by error, length of Q-grid (smaller is less complex)
         per_beatspan_q_grids[beatspan_number].sort(key = lambda x: (x[0], len(x[2])))
         if verbose:
            print '\t%d: %s' % (beatspan_number, grouped_timepoints[beatspan_number])
            for q in per_beatspan_q_grids[beatspan_number]:
               print '\t\t%0.4f %s' % (q[0], q[2])

      assert len(per_beatspan_q_grids) == len(grouped_timepoints)

      # regroup
      if verbose:
         print 'SELECTING:'
      carry = False # carry "next" into following Q-grid
      selected_q_grids = { }
      for beatspan_number in sorted(grouped_timepoints.keys( )):
         selected = per_beatspan_q_grids[beatspan_number][0][2]
         if carry:
            selected[0] = 1
            carry = False
         selected_q_grids[beatspan_number] = selected
         if selected.next:
            if beatspan_number + 1 not in grouped_timepoints:
               selected_q_grids[beatspan_number + 1] = _QGrid([1], 0)
            else:
               carry = True
            selected[-1] = 0
         if verbose:
            print '\t%d %s' % (beatspan_number, selected_q_grids[beatspan_number])

      # fill in gaps
      for i in range(sorted(selected_q_grids.keys( ))[-1]):
         if i not in selected_q_grids:
            selected_q_grids[i] = _QGrid([0], 0)

      # store indices of tie-chain starts
      indices = [ ]
      carry = 0
      for beatspan_number in sorted(selected_q_grids.keys( )):
         q_grid = selected_q_grids[beatspan_number]
         for i, x in enumerate(q_grid):
            if x == 1:
               indices.append(i + carry)
         carry += len(q_grid) - 1 # account of q_grid.next

      # make bare notation
      container = Container( )
      for beatspan_number in sorted(selected_q_grids.keys( )):
         q_grid = selected_q_grids[beatspan_number]
         container.append(q_grid.format_for_beatspan(self.beatspan))

      # add tie chains
      tie_chains = [ ]
      for pair in iterate_sequence_pairwise_strict(indices):
         leaves = container.leaves[pair[0]:pair[1]]
         if 1 < len(leaves):
            tie_chains.append(get_tie_chain(TieSpanner(leaves)[0]))

      # rest any trailing, untied leaves
      last_tie = TieSpanner(container.leaves[indices[-1]:])
      last_tie_chain = get_tie_chain(last_tie[0])
      last_tie_chain = fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(last_tie_chain)
      last_tie.clear( ) # detach
      for note in flatten_sequence(last_tie_chain):
         parent = note._parentage.parent
         parent[parent.index(note)] = Rest(note.duration.written)

      # fuse tie chains
      for tie_chain in reversed(tie_chains):
          fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain)

      return container

def _compare_timepoints_to_q_grid(timepoints, q_grid):
   # This will need to be rewritten for parallelization:
   # it should return error & indices, not error & points
   # and only the offsets should be provided, rather
   # than the entire Q-grid object itself.
   indices = [ ]
   points = [ ]
   error = 0
   for timepoint in timepoints:
      q = q_grid.offsets[0]
      best_index = 0
      best_point = q
      best_error = abs(q - timepoint)
      for i, q in enumerate(q_grid.offsets[1:]):
         curr_error = abs(q - timepoint)
         if curr_error < best_error:
            best_index = i + 1
            best_point = q
            best_error = curr_error
      q_grid[best_index] = 1
      points.append(best_point)
      error += best_error
   return error, points
