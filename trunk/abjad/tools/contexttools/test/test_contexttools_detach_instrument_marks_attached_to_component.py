from abjad import *


def test_contexttools_detach_instrument_marks_attached_to_component_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    instrument_mark = contexttools.InstrumentMark('Violin', 'Vn.')
    instrument_mark.attach(staff)

    detached_instrument_marks = contexttools.detach_instrument_marks_attached_to_component(staff)

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
    }
    '''

    assert detached_instrument_marks[0] is instrument_mark
    assert staff.format == "\\new Staff {\n\tc'4\n\td'4\n\te'4\n\tf'4\n}"
