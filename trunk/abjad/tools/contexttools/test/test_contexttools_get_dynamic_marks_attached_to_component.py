from abjad import *


def test_contexttools_get_dynamic_marks_attached_to_component_01():

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

    dynamic_marks = contexttools.get_dynamic_marks_attached_to_component(staff[0])

    assert dynamic_mark in dynamic_marks
    assert len(dynamic_marks) == 1
