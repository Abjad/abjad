from abjad import *


def test_leaftools_list_written_durations_of_leaves_in_expr_01( ):

   staff = Staff(FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
   durations = leaftools.list_written_durations_of_leaves_in_expr(staff)

   assert durations == [Rational(1, 8), Rational(1, 8), Rational(1, 8), 
      Rational(1, 8), Rational(1, 8), Rational(1, 8)]
