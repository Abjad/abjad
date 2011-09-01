from abjad import *


def test_marktools_detach_noncontext_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 4))(staff[0])
    marktools.Articulation('staccato')(staff[0])

    r'''
    \new Staff {
        \time 2/4
        c'8 -\staccato
        d'8
        e'8
        f'8
    }
    '''

    marktools.detach_noncontext_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        \time 2/4
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\time 2/4\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
