from itertools import groupby
from abjad.tools.quantizationtools.QGridRhythmTree import QGridRhythmTree
from abjad.tools.quantizationtools._QGridQuantizer import _QGridQuantizer
from abjad.tools.quantizationtools.compare_timepoints_to_q_grid \
   import compare_timepoints_to_q_grid
from abjad.tools.quantizationtools.group_timepoints_by_beatspan \
   import group_timepoints_by_beatspan
from abjad.tools.quantizationtools.sort_rhythm_trees_by_error_relative_timepoint_group \
   import sort_rhythm_trees_by_error_relative_timepoint_group
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class NaiveQGridQuantizer(_QGridQuantizer):

   ## PUBLIC METHODS ##

   def quantize_ms_to_tempo(self, timepoints, verbose = False):
      lookup = self.search_tree.build_tempo_lookup(self.tempo, self.beatspan)
      grouped_unquantized_timepoints = group_timepoints_by_beatspan(timepoints, self.beatspan_ms)

      # find the best Q-grid / rhythm_tree for each group of unquantized timepoints,
      # and calculate the closest quantized rhythms for those timepoints,
      # within an "un-positioned" beatspan.
      best_q_grids = { }
      for beatspan_number in grouped_unquantized_timepoints:
         print beatspan_number, grouped_unquantized_timepoints[beatspan_number]
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
               print '\t%s\t%s\t%s' % (beatspan_number, best_error, best_rhythm_tree.definition)
               if best_error == 0:
                  break
         best_q_grids[beatspan_number] = (best_rhythm_tree, best_points)

      # now, find the absolute position of those quantized timepoints,
      # by taking their beatspan-number into account.
      quantized_timepoints = [ ]
      for beatspan_number in best_q_grids:
         beatspan_offset = self.beatspan * beatspan_number
         for i, quantized_timepoint in enumerate(best_q_grids[beatspan_number][1]): # quantized points
            quantized_timepoints.append([
               quantized_timepoint + beatspan_offset, # non-modulo, quantized timepoint
               grouped_unquantized_timepoints[beatspan_number][i], # original timepoint
               best_q_grids[beatspan_number][0] # rhythm tree
            ])

      quantized_timepoint_groups = group_timepoints_by_beatspan(
         quantized_timepoints, self.beatspan, subscript = 0)

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
