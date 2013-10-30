# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_SliceSelection_group_by_01():

    staff = Staff(scoretools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
    t = staff.select_leaves().group_by(type)

    assert t == [(staff[0], staff[1], staff[2]), (staff[3], staff[4]),
        (staff[5], staff[6])]
