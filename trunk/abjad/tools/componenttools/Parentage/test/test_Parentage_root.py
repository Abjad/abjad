from abjad import *


def test_Parentage_root_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])

    assert staff.parentage.root is staff
    assert tuplet.parentage.root is staff
    assert staff.leaves[0].parentage.root is staff
    assert staff.leaves[1].parentage.root is staff
    assert staff.leaves[2].parentage.root is staff
