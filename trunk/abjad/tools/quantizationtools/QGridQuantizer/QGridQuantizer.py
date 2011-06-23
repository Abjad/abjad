from collections import Iterable
from itertools import groupby
from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import is_binary_rational
from abjad.tools.quantizationtools._Quantizer import _Quantizer
from abjad.tools.quantizationtools.QGridSearchTree import QGridSearchTree
from abjad.tools.quantizationtools.QGridRhythmTree import QGridRhythmTree
from abjad.tools.quantizationtools.compare_timepoints_to_q_grid \
   import compare_timepoints_to_q_grid
from abjad.tools.quantizationtools.group_timepoints_by_beatspan \
   import group_timepoints_by_beatspan
from abjad.tools.quantizationtools.sort_rhythm_trees_by_error_relative_timepoint_group \
   import sort_rhythm_trees_by_error_relative_timepoint_group
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class QGridQuantizer(_Quantizer):

   __slots__ = ('_beatspan', '_beatspan_ms', '_q_grids',
      '_q_grid_tempo_lookup', '_search_tree', '_tempo', '_threshold')

   def __init__(self,
      search_tree = None,
      beatspan = Fraction(1, 4),
      tempo = TempoMark(Fraction(1, 4), 60),
      threshold = None):

      if search_tree is None:
         search_tree = QGridSearchTree( )
      else:
         assert isinstance(search_tree, QGridSearchTree)

      assert is_binary_rational(beatspan)
      if isinstance(beatspan, Fraction):
         assert beatspan.numerator == 1

      assert isinstance(tempo, TempoMark)

      if threshold is not None:
         assert 0 < threshold
         search_tree = search_tree.prune(tempo, threshold, beatspan)

      object.__setattr__(self, '_beatspan', beatspan)
      object.__setattr__(self, '_beatspan_ms', 
         tempo_scaled_rational_to_milliseconds(beatspan, tempo))
      object.__setattr__(self, '_q_grids', None) # lazy load
      object.__setattr__(self, '_q_grid_tempo_lookup', None) # lazy load
      object.__setattr__(self, '_search_tree', search_tree)
      object.__setattr__(self, '_tempo', tempo)
      object.__setattr__(self, '_threshold', threshold)

   ## PRIVATE METHODS ##

   def _find_nearest_q_grid_point_to_timepoint(self, timepoint, q_grid):
      best_point = q_grid[0]
      best_error = abs(self.q_grid_tempo_lookup[q_grid[0]] - timepoint)
      for q in q_grid[1:]:
         curr_error = abs(self.q_grid_tempo_lookup[q] - timepoint)
         if curr_error < best_error:
            best_point = q
            best_error = curr_error
      return best_point, best_error

   ## PUBLIC ATTRIBUTES ##

   @property
   def beatspan(self):
      return self._beatspan

   @property
   def beatspan_ms(self):
      return self._beatspan_ms

   @property
   def q_grids(self):
      if self._q_grids is None:
         object.__setattr__(self, '_q_grids',
            tuple([x.q_grid * self.beatspan
               for x in self.search_tree.rhythm_trees]))
      return self._q_grids

   @property
   def q_grid_tempo_lookup(self):
      if self._q_grid_tempo_lookup is None:
         q_grid_tempo_lookup = { }
         for q_grid in self.q_grids:
            for q in q_grid:
               if q not in q_grid_tempo_lookup:
                  q_grid_tempo_lookup[q] = \
                     int(tempo_scaled_rational_to_milliseconds(q, self.tempo))
         object.__setattr__(self, '_q_grid_tempo_lookup', q_grid_tempo_lookup)
      return self._q_grid_tempo_lookup

   @property
   def rhythm_trees(self):
      return self._search_tree.rhythm_trees

   @property
   def search_tree(self):
      return self._search_tree

   @property
   def tempo(self):
      return self._tempo

   @property
   def threshold(self):
      return self._threshold

   ## PUBLIC METHODS ##

   def quantize_milliseconds(self, durations):
      lookup = self.search_tree.build_tempo_lookup(self.tempo, self.beatspan)
      grouped_unquantized_timepoints = group_timepoints_by_beatspan(timepoints, self.beatspan_ms)

      # find the best Q-grid / rhythm_tree for each group of unquantized timepoints,
      # and calculate the closest quantized rhythms for those timepoints,
      # within an "un-positioned" beatspan.
      best_q_grids = { }
      for beatspan_number in grouped_unquantized_timepoints:
         timepoints = [x - (beatspan_number * self.beatspan_ms)
            for x in grouped_unquantized_timepoints[beatspan_number]]
         best_rhythm_tree = self.search_tree.rhythm_trees[0]
         best_error, best_points = compare_timepoints_to_q_grid(
            timepoints, self.search_tree.rhythm_trees[0].q_grid * self.beatspan, lookup)
         for rhythm_tree in self.search_tree.rhythm_trees[1:]:
            curr_error, curr_points = compare_timepoints_to_q_grid(
               timepoints, rhythm_tree.q_grid * self.beatspan, lookup)
            if curr_error < best_error:
               best_error = curr_error
               best_points = curr_points
               best_rhythm_tree = rhythm_tree
               if best_error == 0:
                  break

         best_q_grids[beatspan_number] = (best_rhythm_tree, best_points)

      # now, find the absolute position of those quantized timepoints,
      # by taking their beatspan-number into account,
      # and break them out of their dictionary into a list for regrouping
      quantized_timepoints = [ ]
      for beatspan_number in best_q_grids:
         beatspan_offset = self.beatspan * beatspan_number
         for i, quantized_timepoint in enumerate(best_q_grids[beatspan_number][1]): # quantized points
            quantized_timepoints.append([
               quantized_timepoint + beatspan_offset, # non-modulo, quantized timepoint
               grouped_unquantized_timepoints[beatspan_number][i], # original timepoint
               best_q_grids[beatspan_number][0] # rhythm tree
            ])

      # regroup the quantized timepoint, as some timepoints may have quantized to the
      # final Q in each Q-grid, necessitating being rewritten from a 1 to a 0,
      # and therefore having a different timepoint apply to them.
      grouped_quantized_timepoint = group_timepoints_by_beatspan(
         quantized_timepoints, self.beatspan, subscript = 0)

      # 
      results = [ ]
      for beatspan_number in quantized_timepoint_groups:
         quantized_timepoint_group = quantized_timepoint_groups[beatspan_number]
         for quantized_timepoint in quantized_timepoint_group:
            if (quantized_timepoint[0] % self.beatspan == 0) and \
               (quantized_timepoint[1] % self.beatspan_ms != 0):
               if 1 < len(quantized_timepoint_group) and \
                  quantized_timepoint_group[-1][2] != quantized_timepoint[2]:
                  quantized_timepoint[2] = quantized_timepoint_group[-1][2]
               else:
                  quantized_timepoint[2] = QGridRhythmTree((1,))
            results.append(tuple(quantized_timepoint))

      return results
