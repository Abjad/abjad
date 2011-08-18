from abjad import *


def test_componenttools_component_to_score_root_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])

    assert componenttools.component_to_score_root(staff) is staff
    assert componenttools.component_to_score_root(tuplet) is staff
    assert componenttools.component_to_score_root(staff.leaves[0]) is staff
    assert componenttools.component_to_score_root(staff.leaves[1]) is staff
    assert componenttools.component_to_score_root(staff.leaves[2]) is staff
