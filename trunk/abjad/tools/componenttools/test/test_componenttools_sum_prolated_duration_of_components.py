from abjad import *


def test_componenttools_sum_prolated_duration_of_components_01( ):
   '''Sum of prolated durations of components in list.'''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))

   assert componenttools.sum_prolated_duration_of_components(t.leaves) == Rational(2, 8)
