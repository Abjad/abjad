from abjad import *


def test_leaftools_get_prolated_durations_from_leaves_in_expr_01( ):

   staff = Staff(FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
   durations = leaftools.get_prolated_durations_from_leaves_in_expr(staff)

   assert durations == [Rational(1, 12), Rational(1, 12), 
      Rational(1, 12), Rational(1, 12), Rational(1, 12), Rational(1, 12)]
