# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_change_tuplets_to_fixed_duration_tuplets_01():

    staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { c'8 d'8 e'8 }")
    assert all(type(x) is Tuplet for x in staff)

    tuplets = selectiontools.select_tuplets(staff)
    tuplets.change_tuplets_to_fixed_duration_tuplets()
    assert all(isinstance(x, tuplettools.FixedDurationTuplet) for x in staff)
