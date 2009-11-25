from abjad.tools import listtools
from abjad.tools.pitchtools.PitchArray import PitchArray


def leaf_iterables_to_pitch_array_empty(leaf_iterables):
   r'''.. versionadded:: 1.1.2

   Return empty pitch array corresponding to `leaf_iterables`. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff(construct.scale(4)))
      abjad> score.append(Staff(construct.scale(2, Rational(1, 4))))
      abjad> score.append(Staff(FixedDurationTuplet((2, 8), construct.scale(3)) * 2))
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
              \new Staff {
                      c'4
                      d'4
              }
              \new Staff {
                      \times 2/3 {
                              c'8
                              d'8
                              e'8
                      }
                      \times 2/3 {
                              c'8
                              d'8
                              e'8
                      }
              }
      >>

   ::

      abjad> array = pitchtools.leaf_iterables_to_pitch_array(score)
      abjad> print array
      [     ] [     ] [     ] [     ]
      [             ] [             ]
      [ ] [     ] [ ] [ ] [     ] [ ]
   '''

   from abjad.tools import construct
   from abjad.tools import leaftools
   from abjad.tools import partition

   time_intervals = leaftools.composite_offset_difference_series(leaf_iterables)

   array_width = len(time_intervals)
   array_depth = len(leaf_iterables)

   pitch_array = PitchArray(array_depth, array_width)

   tokens = construct.quarter_notes_with_multipliers([0], time_intervals)
   for leaf_list, pitch_array_row in zip(leaf_iterables, pitch_array.rows):
      durations = leaftools.get_durations_prolated(leaf_list)
      parts = partition.unfractured_by_durations(tokens, durations)
      part_lengths = [len(part) for part in parts]
      cells = pitch_array_row.cells
      grouped_cells = listtools.partition_by_lengths(cells, part_lengths)
      for group in grouped_cells:
         pitch_array_row.merge(group)

   return pitch_array
