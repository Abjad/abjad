from collections import Iterable
from itertools import groupby
from abjad import Container
from abjad import Fraction
from abjad import Rest
from abjad.tools.contexttools import TempoMark

from abjad.tools.leaftools import fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
from abjad.tools.mathtools import cumulative_sums_zero

from abjad.tools.quantizationtools.QGrid import QGrid
from abjad.tools.quantizationtools.QGridSearchTree import QGridSearchTree
from abjad.tools.quantizationtools.QGridTempoLookup import QGridTempoLookup
from abjad.tools.quantizationtools._Quantizer import _Quantizer

from abjad.tools.quantizationtools.is_valid_beatspan import is_valid_beatspan
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.seqtools import flatten_sequence
from abjad.tools.seqtools import iterate_sequence_pairwise_strict
from abjad.tools.seqtools import yield_outer_product_of_sequences
from abjad.tools.tietools import TieSpanner
from abjad.tools.tietools import get_tie_chain


class QGridQuantizer(_Quantizer):

   __slots__ = ('_beatspan', '_beatspan_ms', '_search_tree', '_tempo', '_tempo_lookup', '_threshold')

   def __init__(self,
      search_tree = None,
      beatspan = Fraction(1, 4),
      tempo = TempoMark(Fraction(1, 4), 60),
      threshold = None):

      assert isinstance(search_tree, (type(None), QGridSearchTree))
      if search_tree is None:
         search_tree = QGridSearchTree( )
      assert is_valid_beatspan(beatspan)
      assert isinstance(tempo, TempoMark)
      if threshold is not None:
         assert 0 < threshold
         search_tree = search_tree.prunt(beatspan, tempo, threshold)

      object.__setattr__(self, '_beatspan', beatspan)
      object.__setattr__(self, '_beatspan_ms', 
         tempo_scaled_rational_to_milliseconds(beatspan, tempo))
      object.__setattr__(self, '_search_tree', search_tree)
      object.__setattr__(self, '_tempo', tempo)
      object.__setattr__(self, '_tempo_lookup', QGridTempoLookup(search_tree, beatspan, tempo))
      object.__setattr__(self, '_threshold', threshold)

   ## PRIVATE METHODS ##

   def _compare_q_events_to_q_grid(self, offsets, q_events, q_grid):
      indices = [ ]
      error = 0

      for i, offset in enumerate(offsets):
         q = q_grid.offsets[0]
         best_index = 0
         best_error = abs(q - timepoint)

         for j, q in enumerate(q_grid.offsets[1:]):
            curr_error = abs(q - offset)
            if curr_error < best_error:
               best_index = j + 1
               best_error = curr_error

         best_index_contents = q_grid[best_index]
         if best_index_contents == 0:
            q_grid[best_index] = tuple(q_events[i],)
         elif isinstance(best_index_contents, tuple):
            new_contents = list(best_index_contents)
            new_contents.append(q_events[i])
            q_grid[best_index] = tuple(new_contents)
            
         error += best_error

      return error

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

   def _quantize(self, q_events, verbose = False):

      # group QEvents
      g = groupby(q_events, lambda x: divmod(x.offset, beatspan)[0])
      grouped_q_events = { }
      for value, group in g:
         grouped_q_events[value] = list(group)

      # find best Q-grids for each beatspan
      per_beatspan_q_grids = { }
      for beatspan_number in sorted(grouped_q_events.keys( )):

         # find modulo offsets
         mod_offsets = [Fraction(x.offset % self.beatspan_ms) / self.beatspan_ms \
            for x in grouped_q_events[beatspan_number]]

         # build Q-grid list
         per_beatspan_q_grids[beatspan_number] = [QGrid([0], 0)]
         for k in self.search_tree:
            grid = QGrid([0] * k, 0)
            per_beatspan_q_grids[beatspan_number].append(grid)
            per_beatspan_q_grids[beatspan_number].extend(self._divide_grid(grid, mod_offsets))

         # find error
         for i, q_grid in enumerate(per_beatspan_q_grids[beatspan_number]):
            error = self._compare_timepoints_to_q_grid( \
               mod_offsets, grouped_q_events[beatspan_number], q_grid)
            per_beatspan_q_grids[beatspan_number][i] = (error, q_grid)

         # sort by error, length of Q-grid (smaller is less complex)
         per_beatspan_q_grids[beatspan_number].sort(key = lambda x: (x[0], len(x[1])))

      assert len(per_beatspan_q_grids) == len(grouped_timepoints)

      # regroup
      carry = False # carry "next" into following Q-grid
      selected_q_grids = { }
      for beatspan_number in sorted(grouped_q_events.keys( )):
         selected = per_beatspan_q_grids[beatspan_number][0][1]
         if carry:
            selected[0] = 1
            carry = False
         selected_q_grids[beatspan_number] = selected
         if selected.next:
            if beatspan_number + 1 not in grouped_timepoints:
               selected_q_grids[beatspan_number + 1] = QGrid([1], 0)
            else:
               carry = True
            selected[-1] = 0

      # fill in gaps
      for i in range(sorted(selected_q_grids.keys( ))[-1]):
         if i not in selected_q_grids:
            selected_q_grids[i] = QGrid([0], 0)

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

   ## PUBLIC ATTRIBUTES ##

   @property
   def beatspan(self):
      return self._beatspan

   @property
   def beatspan_ms(self):
      return self._beatspan_ms

   @property
   def search_tree(self):
      return self._search_tree

   @property
   def tempo(self):
      return self._tempo

   @property
   def tempo_lookup(self):
      return self._tempo_lookup

   @property
   def threshold(self):
      return self._threshold
