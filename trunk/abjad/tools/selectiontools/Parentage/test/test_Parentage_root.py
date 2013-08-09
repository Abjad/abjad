# -*- encoding: utf-8 -*-
from abjad import *


def test_Parentage_root_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])

    assert more(staff).select_parentage().root is staff
    assert more(tuplet).select_parentage().root is staff
    assert more(staff.select_leaves()[0]).select_parentage().root is staff
    assert more(staff.select_leaves()[1]).select_parentage().root is staff
    assert more(staff.select_leaves()[2]).select_parentage().root is staff
