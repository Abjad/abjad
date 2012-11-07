from abjad import *


def test_containertools_delete_contents_of_container_starting_strictly_after_offset_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)
    containertools.delete_contents_of_container_starting_strictly_after_offset(staff, Duration(1, 8))

    r'''
    \new Staff {
        c'8 [
        d'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_after_offset_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)
    containertools.delete_contents_of_container_starting_strictly_after_offset(staff, Duration(3, 16))

    r'''
    \new Staff {
        c'8 [
        d'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_after_offset_03():
    '''Delete nothing when no contents start after prolated offset.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)
    containertools.delete_contents_of_container_starting_strictly_after_offset(staff, 99)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_after_offset_04():
    '''Delete all contents when all elements start after prolated offset.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)
    containertools.delete_contents_of_container_starting_strictly_after_offset(staff, -99)

    r'''
    \new Staff {
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == '\\new Staff {\n}'
