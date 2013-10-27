# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage_root_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])

    assert inspect(staff).get_parentage().root is staff
    assert inspect(tuplet).get_parentage().root is staff
    assert inspect(staff.select_leaves()[0]).get_parentage().root is staff
    assert inspect(staff.select_leaves()[1]).get_parentage().root is staff
    assert inspect(staff.select_leaves()[2]).get_parentage().root is staff
