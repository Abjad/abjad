from abjad import *


def test_tuplettools_change_tuplets_in_expr_to_fixed_duration_tuplets_01():

    staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { c'8 d'8 e'8 }") 
    assert all([x._class_name == 'Tuplet' for x in staff])

    tuplettools.change_tuplets_in_expr_to_fixed_duration_tuplets(staff)
    assert all([isinstance(x, tuplettools.FixedDurationTuplet) for x in staff])
