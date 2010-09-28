from abjad import *


def test_leaftools_list_prolated_durations_of_leaves_in_expr_01( ):

   staff = Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
   durations = leaftools.list_prolated_durations_of_leaves_in_expr(staff)

   assert durations == [Fraction(1, 12), Fraction(1, 12), 
      Fraction(1, 12), Fraction(1, 12), Fraction(1, 12), Fraction(1, 12)]
