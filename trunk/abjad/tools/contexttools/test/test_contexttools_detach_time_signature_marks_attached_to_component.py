from abjad import *


def test_contexttools_detach_time_signature_marks_attached_to_component_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    time_signature_mark = contexttools.TimeSignatureMark((4, 4))(staff[0])

    result = contexttools.detach_time_signature_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
    }
    '''

    assert result[0] is time_signature_mark
    assert staff.format == "\\new Staff {\n\tc'4\n\td'4\n\te'4\n\tf'4\n}"
