from abjad import *


def test_componenttools_sum_prolated_duration_of_components_01( ):
   '''Sum of prolated durations of components in list.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))

   assert componenttools.sum_prolated_duration_of_components(t.leaves) == Rational(2, 8)
