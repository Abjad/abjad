from abjad.tools import iterate
from abjad.tools import listtools
from abjad.tools.pitchtools.PitchArray import PitchArray
from abjad.tools.pitchtools.get_pitches import get_pitches


def _leaf_iterables_to_pitch_array(leaf_iterables, populate = True):
   r'''.. versionadded:: 1.1.2
   '''

   from abjad.tools import leaftools
   from abjad.tools import partition

   time_intervals = leaftools.get_composite_offset_difference_series(
      leaf_iterables)
   array_width = len(time_intervals)
   array_depth = len(leaf_iterables)
   pitch_array = PitchArray(array_depth, array_width)

   tokens = leaftools.make_quarter_notes_with_lilypond_multipliers([0], time_intervals)
   for leaf_iterable, pitch_array_row in zip(leaf_iterables, pitch_array.rows):
      durations = leaftools.get_durations_prolated(leaf_iterable)
      parts = partition.unfractured_by_durations(tokens, durations)
      part_lengths = [len(part) for part in parts]
      cells = pitch_array_row.cells
      grouped_cells = listtools.partition_by_lengths(cells, part_lengths)
      for group in grouped_cells:
         pitch_array_row.merge(group)
      leaves = iterate.leaves_forward_in_expr(leaf_iterable)
      if populate:
         for cell, leaf in zip(pitch_array_row.cells, leaves):
            cell.pitches.extend(get_pitches(leaf))

   return pitch_array
