# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage_root_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])
    leaves = select(staff).by_leaf()

    assert inspect_(staff).get_parentage().root is staff
    assert inspect_(tuplet).get_parentage().root is staff
    assert inspect_(leaves[0]).get_parentage().root is staff
    assert inspect_(leaves[1]).get_parentage().root is staff
    assert inspect_(leaves[2]).get_parentage().root is staff
