# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_change_fixed_duration_tuplets_to_tuplets_01():

    staff = Staff(2 * tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8"))
    assert all(isinstance(x, tuplettools.FixedDurationTuplet) for x in staff)

    tuplets = selectiontools.select_tuplets(staff)
    tuplets.change_fixed_duration_tuplets_to_tuplets()
    assert all(type(x) is Tuplet for x in staff)
