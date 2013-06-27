from abjad import *


def test_tuplettools_change_fixed_duration_tuplets_in_expr_to_tuplets_01():

    staff = Staff(2 * tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8"))
    assert all(isinstance(x, tuplettools.FixedDurationTuplet) for x in staff)

    tuplettools.change_fixed_duration_tuplets_in_expr_to_tuplets(staff)
    assert all(type(x) is Tuplet for x in staff)
