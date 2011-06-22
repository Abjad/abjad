from collections import Iterable
from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import is_binary_rational
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.quantizationtools.QGridRhythmTree import QGridRhythmTree


def sort_rhythm_trees_by_error_relative_timepoint_group(
   timepoints,
   rhythm_trees, 
   tempo = TempoMark(Fraction(1, 4), 60), 
   beatspan = Fraction(1, 4)):
   '''This function is provided outside of the QGridQuantizer classes
   in order to provide an easier import for multiprocessing operations.'''

   assert isinstance(timepoints, Iterable) and len(timepoints)
   assert isinstance(rhythm_trees, Iterable) and len(rhythm_trees) and \
      all([isinstance(x, QGridRhythmTree) for x in rhythm_trees])
   assert isinstance(tempo, (TempoMark, type(None)))
   assert is_binary_rational(beatspan) and 0 < beatspan

   beatspan_ms = tempo_scaled_rational_to_milliseconds(beatspan, tempo)
   lookup = { } # tempo lookup
   results = [ ]
   for rhythm_tree in rhythm_trees:

      q_grid = rhythm_tree.q_grid * beatspan # scale from 0-1 to 0-beatspan
      group_points = [ ]
      group_error = 0
      
      for timepoint in [x % beatspan_ms for x in timepoints]:

         # check first Q-grid point against timepoint
         # this simplifies the logic of checking current_error against best_error
         # as we do not have to do "if best_error is None ... else" or similar
         q = q_grid[0]
         best_point = q
         try:
            best_error = abs(lookup[q] - timepoint)
         except KeyError:
            lookup[q] = tempo_scaled_rational_to_milliseconds(q, tempo)
            best_error = int(abs(lookup[q] - timepoint))

         # check the other Q-grid points
         for q in q_grid[1:]:
            try:
               curr_error = abs(lookup[q] - timepoint)
            except:
               lookup[q] = tempo_scaled_rational_to_milliseconds(q, tempo)
               curr_error = abs(lookup[q] - timepoint)
            if curr_error < best_error:
               best_point = q
               best_error = curr_error

         # add error of closest point to total
         group_points.append(best_point)
         group_error += int(best_error)

      # create our package
      results.append((group_error, rhythm_tree, tuple(group_points)))

   # sort by error
   return tuple(sorted(results, key = lambda x: x[0]))
