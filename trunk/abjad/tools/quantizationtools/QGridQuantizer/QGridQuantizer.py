from itertools import groupby
from abjad import Chord
from abjad import Container
from abjad import Fraction
from abjad import Rest
from abjad.tools.contexttools import TempoMark

from abjad.tools.leaftools import fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
from abjad.tools.marktools import Annotation

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
from abjad.tools.spannertools import MultipartBeamSpanner
from abjad.tools.tietools import TieSpanner
from abjad.tools.tietools import get_tie_chain
from abjad.tools.tietools import get_tie_chains_in_expr


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
         search_tree = search_tree.prune(beatspan, tempo, threshold)

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
         best_error = abs(q - offset)

         for j, q in enumerate(q_grid.offsets[1:], start = 1):
            curr_error = abs(q - offset)
            if curr_error < best_error:
               best_index = j
               best_error = curr_error

         best_index_contents = q_grid[best_index]
         if best_index_contents == 0:
            q_grid[best_index] = (q_events[i],)
         elif isinstance(best_index_contents, tuple):
            new_contents = list(best_index_contents)
            new_contents.append(q_events[i])
            q_grid[best_index] = tuple(new_contents)
            
         error += best_error

      return error

   def _divide_grid(self, grid, offsets):
      def recurse(grid, offsets):
         results = [ ]
         indices = grid.find_divisible_indices(offsets)
         divisors = [self.search_tree.find_subtree_divisibility(
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
            results.extend(recurse(results[-1], offsets))
         return results
      return recurse(grid, offsets)

   def _find_best_q_grid_foreach_q_event_group(self, q_event_groups):
      best_q_grids = { }

      for beatspan_number, group in q_event_groups.iteritems( ):

         errors = [ ]
         q_grids = [ ]

         mod_offsets = [Fraction(x.offset % self.beatspan_ms) / self.beatspan_ms for x in group]

         q_grids.append(QGrid([0], 0))
         for divisor in self.search_tree:
            q_grid = QGrid([0] * divisor, 0)
            q_grids.append(q_grid)
            q_grids.extend(self._divide_grid(q_grid, mod_offsets))

         for q_grid in q_grids:
            errors.append(self._compare_q_events_to_q_grid(mod_offsets, group, q_grid))
         
         pairs = zip(errors, q_grids)
         pairs.sort(key = lambda x: (x[0], len(x[1])))

         best_q_grids[beatspan_number] = pairs[0][1]

      return best_q_grids

   def _format_all_q_grids(self, best_q_grids):
      beatspan_numbers = sorted(best_q_grids.keys( ))

      # store indices of tie-chain starts
      indices = [ ]
      pitches = [ ]
      carry = 0
      for beatspan_number in beatspan_numbers:
         q_grid = best_q_grids[beatspan_number]
         for i, x in enumerate(q_grid):
            if isinstance(x, tuple):
               indices.append(i + carry)
               pcs = filter(lambda z: z is not None, flatten_sequence([y.value for y in x]))
               if len(pcs) == 0:
                  pcs = [None]
               pitches.append(pcs)
         carry += len(q_grid) - 1 # account of q_grid.next

      # remove terminating silence if it is the only event in the last grid
      final_grid = best_q_grids[beatspan_numbers[-1]]
      if len(final_grid) == 2:
         if len(final_grid[0]) == 1:
            best_q_grids.pop(beatspan_numbers[-1])
            beatspan_numbers.pop(-1)

      # make bare notation
      container = Container( )
      for beatspan_number in beatspan_numbers:
         q_grid = best_q_grids[beatspan_number]
         formatted = q_grid.format_for_beatspan(self.beatspan)
         if 1 < len(formatted):
            MultipartBeamSpanner(formatted)
         container.append(formatted)

      # add tie chains
      tie_chains = [ ]
      for i, pair in enumerate(iterate_sequence_pairwise_strict(indices)):
         leaves = container.leaves[pair[0]:pair[1]]
         pitch = pitches[i]
         if 1 < len(leaves) and pitch[0] is not None:
            tie_chains.append(get_tie_chain(TieSpanner(leaves)[0]))
         for leaf in leaves:
            parent = leaf._parentage.parent
            idx = parent.index(leaf)
            if len(pitch) == 1:
               if pitch[0] is None:
                  parent[idx] = Rest(leaf)
               else:
                  leaf.pitch = pitch[0]
            else:
               parent[idx] = Chord(leaf)
               parent[idx].pitches = pitch

      # rest any trailing, untied leaves
      trailing = container.leaves[indices[-1]:]
      if 1 < len(trailing):
         last_tie = TieSpanner(container.leaves[indices[-1]:])
         last_tie_chain = get_tie_chain(last_tie[0])
         last_tie_chain = fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(last_tie_chain)
         last_tie.clear( ) # detach
         for note in flatten_sequence(last_tie_chain):
            parent = note._parentage.parent
            parent[parent.index(note)] = Rest(note.duration.written)
      elif len(trailing) == 1:
         parent = trailing[0]._parentage.parent
         parent[parent.index(trailing[0])] = Rest(trailing[0].duration.written)

      # fuse tie chains
      for tie_chain in get_tie_chains_in_expr(container.leaves):
         if 1 < len(tie_chain):
            fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain)

      return container

   def _group_q_events_by_beatspan(self, q_events):
      g = groupby(q_events, lambda x: x.offset // self.beatspan_ms)
      grouped_q_events = { }
      for value, group in g:
         grouped_q_events[value] = list(group)
      return grouped_q_events

   def _regroup_and_fill_out_best_q_grids(self, best_q_grids):
      '''Shift events which have been quantized to the last offset
      of one Q-grid to the first offset of the subsequent grid.
      '''

      # events to be carried
      carried = None

      # cache keys, as the dictionary may be modified
      beatspan_numbers = sorted(best_q_grids.keys( ))
      for beatspan_number in beatspan_numbers:
         q_grid = best_q_grids[beatspan_number]

         ## rolling over the carried events
         if carried:
            if not q_grid[0]:
               q_grid[0] = carried
            else:
                zero = list(q_grid[0])
                zero.extend(carried)
                q_grid[0] = tuple(sorted(zero, key = lambda x: x.offset))
            carried = None

         # testing if events need to be carried
         if q_grid.next:
            # no grid follows, so create one
            if beatspan_number + 1 not in best_q_grids:
               best_q_grids[beatspan_number + 1] = QGrid([q_grid.next], 0)
            # another grid follows, so cache the carried events
            else:
               carried = q_grid.next
            q_grid[-1] = 0

      for i in range(sorted(best_q_grids.keys( ))[-1]):
         if i not in best_q_grids:
            best_q_grids[i] = QGrid([0], 0)

#      # if the terminating silence falls on the downbeat of the last Q-grid
#      # and it is the only Q-event there, remove the final Q-grid
#      if len(best_q_grids[beatspan_numbers[-1]]) == 2 and \
#         len(best_q_grids[beatspan_numbers[-1]][0]) == 1:
#         best_q_grids.pop(beatspan_numbers[-1])

      return best_q_grids

   def _quantize(self, q_events, verbose = False):

      grouped_q_events = self._group_q_events_by_beatspan(q_events)
      best_q_grids = self._find_best_q_grid_foreach_q_event_group(grouped_q_events)
      best_q_grids = self._regroup_and_fill_out_best_q_grids(best_q_grids)
      container = self._format_all_q_grids(best_q_grids)
      
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
