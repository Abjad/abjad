from abjad import *


def test_PhrasingSlurSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.PhrasingSlurSpanner(staff.leaves, direction='up')

    r'''
    \new Staff {
        c'8 ^ \(
        d'8
        e'8
        f'8 \)
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 ^ \\(\n\td'8\n\te'8\n\tf'8 \\)\n}"


def test_PhrasingSlurSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.PhrasingSlurSpanner(staff.leaves, direction='down')

    r'''
    \new Staff {
        c'8 _ \(
        d'8
        e'8
        f'8 \)
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 _ \\(\n\td'8\n\te'8\n\tf'8 \\)\n}"
