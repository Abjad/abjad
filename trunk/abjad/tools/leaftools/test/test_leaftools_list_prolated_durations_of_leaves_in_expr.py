from abjad import *


def test_leaftools_list_prolated_durations_of_leaves_in_expr_01():

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2)
    durations = leaftools.list_prolated_durations_of_leaves_in_expr(staff)

    assert durations == [Duration(1, 12), Duration(1, 12),
      Duration(1, 12), Duration(1, 12), Duration(1, 12), Duration(1, 12)]
