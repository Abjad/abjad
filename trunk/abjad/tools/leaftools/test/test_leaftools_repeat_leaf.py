from abjad import *


def test_leaftools_repeat_leaf_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    leaftools.repeat_leaf(staff[0], total=3)

    r'''
    \new Staff {
        c'8 [
        c'8
        c'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tc'8\n\td'8\n\te'8\n\tf'8 ]\n}"
