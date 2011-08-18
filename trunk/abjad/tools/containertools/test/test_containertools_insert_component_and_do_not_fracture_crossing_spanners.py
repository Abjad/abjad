from abjad import *


def test_containertools_insert_component_and_do_not_fracture_crossing_spanners_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.leaves)
    containertools.insert_component_and_do_not_fracture_crossing_spanners(staff, 1, Note("cs'8"))

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\te'8\n\tf'8 ]\n}"
