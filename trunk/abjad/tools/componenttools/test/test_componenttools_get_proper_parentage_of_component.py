from abjad import *


def test_componenttools_get_proper_parentage_of_component_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    staff = Staff([tuplet])
    note = staff.leaves[0]

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
    }
    '''

    proper_parentage = componenttools.get_proper_parentage_of_component(note)
    assert len(proper_parentage) == 2
    assert proper_parentage[0] is tuplet
    assert proper_parentage[1] is staff
