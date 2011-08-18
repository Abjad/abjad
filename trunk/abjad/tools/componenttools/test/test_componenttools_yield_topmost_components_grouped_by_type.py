from abjad import *


def test_componenttools_yield_topmost_components_grouped_by_type_01():

    staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
    t = list(componenttools.yield_topmost_components_grouped_by_type(staff.leaves))

    assert t == [(staff[0], staff[1], staff[2]), (staff[3], staff[4]),
        (staff[5], staff[6])]
