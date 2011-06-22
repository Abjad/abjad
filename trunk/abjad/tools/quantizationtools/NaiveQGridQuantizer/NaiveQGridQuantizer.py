from itertools import groupby
from abjad.tools.quantizationtools.QGridRhythmTree import QGridRhythmTree
from abjad.tools.quantizationtools._QGridQuantizer import _QGridQuantizer
from abjad.tools.quantizationtools.group_timepoints_by_beatspan \
   import group_timepoints_by_beatspan
from abjad.tools.quantizationtools.sort_rhythm_trees_by_error_relative_timepoint_group \
   import sort_rhythm_trees_by_error_relative_timepoint_group
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class NaiveQGridQuantizer(_QGridQuantizer):

   ## PUBLIC METHODS ##

   def quantize_ms_to_tempo(self, timepoints, verbose = False):

      if verbose:
         print 'Grouping unquantized timepoints...'

      timepoint_groups = group_timepoints_by_beatspan(timepoints, self.beatspan_ms)

      # find best rhythm tree for each beatspan's timepoints

      if verbose:
         print 'Sorting rhythm trees...'

      q_grid_groups = { }
      for key in timepoint_groups:

         if verbose:
            print '\tGroup %d...' % key

         q_grid_groups[key] = sort_rhythm_trees_by_error_relative_timepoint_group(
            timepoint_groups[key], self.rhythm_trees,
            tempo = self.tempo, beatspan = self.beatspan)[0]

      # reorganize the results into a new list of tuples,
      # so we can then regroups all timepoints as some
      # should now be shifted to the beginning of the following Q-grid:
      # (quantized timepoint + beatspan offset, old timepoint, rhythm tree)

      if verbose:
         print 'Reorganizing timepoints...'

      quantized_timepoints = [ ]
      for key in q_grid_groups:
         beatspan_offset = self.beatspan * key
         for i, quantized_timepoint in enumerate(q_grid_groups[key][2]): # quantized points
            quantized_timepoints.append([
               quantized_timepoint + beatspan_offset, # non-modulo, quantized timepoint
               timepoint_groups[key][i], # original timepoint
               q_grid_groups[key][1] # rhythm tree
            ])

      # now, regroup by fractional beatspan

      if verbose:
         print 'Regrouping quantized timepoints...'

      quantized_timepoint_groups = group_timepoints_by_beatspan(
         quantized_timepoints, self.beatspan, subscript = 0)

      # if (quantized timepoint % beatspan) != (original timepoint % beatspan),
      # it will not have the correct associated rhythm tree as the other timepoints
      # in its group, so that must be discovered and overwritten

      if verbose:
         print 'Correcting quantized timepoint rhythm trees...'

      results = [ ]
      for key in quantized_timepoint_groups:
         for quantized_timepoint in quantized_timepoint_groups[key]:
            # if the quantized timepoint aligns to the beginning of the beatspan,
            # but the original timepoint does not, then it has been "shifted"
            # from an earlier beatspan to a later one during quantization,
            # and must have its rhythm tree point to the correct beatspan.
            if (quantized_timepoint[0] % self.beatspan == 0) and \
               (quantized_timepoint[1] % self.beatspan_ms != 0):
               # if there are other timepoints in the new group,
               # and they disagree about what the rhythm tree is,
               # take the reference from the later points.
               if 1 < len(quantized_timepoint_groups[key]) and \
                  quantized_timepoint_groups[key][-1][2] != quantized_timepoint[2]:
                  quantized_timepoint[2] = quantized_timepoint_groups[key][-1][2]
               # but, if there are no other points,
               # or all points align to the beginning of the beatspan,
               # set their rhythm tree to the simplest possible
               else:
                  quantized_timepoint[2] = QGridRhythmTree((1,))

            results.append(tuple(quantized_timepoint))

      if verbose:
         print '...done!'

      return results
