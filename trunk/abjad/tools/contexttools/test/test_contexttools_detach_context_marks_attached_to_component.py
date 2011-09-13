from abjad import *


def test_contexttools_detach_context_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef_mark = contexttools.ClefMark('treble')(staff)
    dynamic_mark = contexttools.DynamicMark('p')(staff[0])

    r'''
    \new Staff {
        \clef "treble"
        c'8 \p
        d'8
        e'8
        f'8
    }
    '''

    contexttools.detach_context_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        \clef "treble"
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\t\\clef "treble"\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'
