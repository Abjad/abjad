from abjad import *


def test_tuplettools_get_first_tuplet_in_proper_parentage_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    tuplet = Tuplet(Fraction(2, 3), staff[:3])

    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(staff.leaves[0]) is tuplet
    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(staff.leaves[1]) is tuplet
    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(staff.leaves[2]) is tuplet
    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(staff.leaves[3]) is None

    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(tuplet) is None
    assert tuplettools.get_first_tuplet_in_proper_parentage_of_component(staff) is None
