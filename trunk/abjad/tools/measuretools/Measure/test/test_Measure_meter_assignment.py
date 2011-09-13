from abjad import *


def test_Measure_meter_assignment_01():
    '''Measures allow meter reassignment.'''

    t = Measure((4, 8), "c'8 d'8 e'8 f'8")

    r'''
    {
        \time 4/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    t.pop()
    contexttools.detach_time_signature_marks_attached_to_component(t)
    contexttools.TimeSignatureMark((3, 8))(t)

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"
