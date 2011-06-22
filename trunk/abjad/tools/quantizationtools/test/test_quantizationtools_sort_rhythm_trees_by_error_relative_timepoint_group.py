from random import shuffle
from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.quantizationtools import QGridRhythmTree
from abjad.tools.quantizationtools import group_timepoints_by_beatspan
from abjad.tools.quantizationtools import sort_rhythm_trees_by_error_relative_timepoint_group
from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds


def test_quantizationtools_sort_rhythm_trees_by_error_relative_timepoint_group_01( ):
   beatspan = Fraction(1, 4)
   tempo = TempoMark(beatspan, 60)
   beatspan_ms = tempo_scaled_rational_to_milliseconds(beatspan, tempo)
   timepoints = [5, 495, 505, 995, 1005, 1333, 1334, 1666, 1667, 1999, 2000, 2251, 2668, 2887]
   timepoint_groups = group_timepoints_by_beatspan(timepoints, beatspan_ms)

   rt_a = QGridRhythmTree( (2,) )
   rt_b = QGridRhythmTree( (3,) )
   rt_c = QGridRhythmTree( (1, (2,))) # given this timepoint set, (1, (2,)) is identical to (2,)
   rt_d = QGridRhythmTree( ((2,), (3,)) )
   rt_e = QGridRhythmTree( (11,) )
   rhythm_trees = [rt_a, rt_b, rt_c, rt_d, rt_e]

   results = { }
   for key in timepoint_groups:
      results[key] = sort_rhythm_trees_by_error_relative_timepoint_group(
         timepoint_groups[key], rhythm_trees, tempo = tempo, beatspan = beatspan)

   assert [x[1] for x in results[0]] == [rt_a, rt_c, rt_d, rt_e, rt_b]
   assert [x[1] for x in results[1]] == [rt_b, rt_e, rt_d, rt_c, rt_a]
   assert [x[1] for x in results[2]] == [rt_d, rt_e, rt_b, rt_c, rt_a]
