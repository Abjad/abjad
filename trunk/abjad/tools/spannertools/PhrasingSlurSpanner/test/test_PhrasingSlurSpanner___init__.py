from abjad import *


def test_PhrasingSlurSpanner___init___01():
    '''Init empty phrasing slur.
    '''

    phrasing_slur = spannertools.PhrasingSlurSpanner()
    assert isinstance(phrasing_slur, spannertools.PhrasingSlurSpanner)


def test_PhrasingSlurSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.PhrasingSlurSpanner(staff.leaves)


    r'''
    \new Staff {
        c'8 \(
        d'8
        e'8
        f'8 \)
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 \\(\n\td'8\n\te'8\n\tf'8 \\)\n}"
