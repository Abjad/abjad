from abjad import *


def test_componenttools_component_to_score_depth_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])

    assert componenttools.component_to_score_depth(staff) == 0
    assert componenttools.component_to_score_depth(tuplet) == 1
    assert componenttools.component_to_score_depth(staff.leaves[0]) == 2
