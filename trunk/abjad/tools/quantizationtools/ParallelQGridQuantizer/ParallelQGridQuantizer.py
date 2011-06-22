from multiprocessing import Pool
from itertools import groupby
from abjad.tools.quantizationtools._QGridQuantizer import _QGridQuantizer
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class ParallelQGridQuantizer(_QGridQuantizer):

   ## PUBLIC METHODS ##

   def quantize_ms_to_tempo(self, timepoints, verbose = False):

      ## I need new private functions at quantizationtools module level:
      ##
      ## _group_unquantized_timepoints_by_beatspan
      ## _group_quantized_timepoints_by_beatspan
      ## _sort_qgrids_by_error_relative_timepoint_group
      ##
      ## Having module level private functions will assist parallelizing via
      ## multiprocessing.Pool.map_async( )

      quantized_results = [ ]
      g = groupby(timepoints, lambda x: divmod(x, self.beatspan_ms)[0])
      current_group = 0

      for value, group in g:
         # save original timepoint with its truncated counterpart
         timepoints = [(int(x - (value * self.beatspan_ms)), x) 
            for x in list(group)]

         # verbose update
         if verbose:
            current_group += 1
            print '\n[%d]:\t%s' % (current_group, [x[0] for x in timepoints])

         best_q_grid = self.q_grids[0]
         best_result = [ ]
         best_error = 0
         for timepoint in timepoints:
            point, error = self._find_nearest_q_grid_point_to_timepoint(
               timepoint[0], self.q_grids[0])
            result = [ # package everything
               point + (self.beatspan * value),
               timepoint[1],
               self.search_tree.rhythm_trees[0],
               value]
            best_result.append(result)
            best_error += error

         # verbose update
         if verbose:
            print '\t%s:\t%s' % (best_error, self.search_tree.rhythm_trees[0])

         for i, q_grid in enumerate(self.q_grids[1:]):
            current_result = [ ]
            current_error = 0
            for timepoint in timepoints:
               point, error = self._find_nearest_q_grid_point_to_timepoint(    
                  timepoint[0], q_grid)
               result = [point, timepoint[1]] # package minimum information
               current_result.append(result)
               current_error += error
            if current_error < best_error:
               best_q_grid = q_grid
               # only after confirming a new best result should we repackage
               for result in current_result:
                  result[0] += self.beatspan * value
                  result.append(self.search_tree.rhythm_trees[i + 1])
                  result.append(value)
               best_result = current_result
               best_error = current_error

               # verbose update
               if verbose:
                  print '\t%s:\t%s' % (best_error, self.search_tree.rhythm_trees[i + 1])

         quantized_results.extend(best_result)

      return quantized_results
