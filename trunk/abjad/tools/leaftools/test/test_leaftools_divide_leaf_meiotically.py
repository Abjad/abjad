from abjad import *


def test_leaftools_divide_leaf_meiotically_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.leaves)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    leaftools.divide_leaf_meiotically(staff[0], n = 4)


    r'''
    \new Staff {
        c'32 [
        c'32
        c'32
        c'32
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'32 [\n\tc'32\n\tc'32\n\tc'32\n\td'8\n\te'8\n\tf'8 ]\n}"
