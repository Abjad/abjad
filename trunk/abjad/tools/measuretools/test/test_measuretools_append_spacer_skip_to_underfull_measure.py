from abjad import *


def test_measuretools_append_spacer_skip_to_underfull_measure_01():
    '''Handles measure prolation from nonbinary meter.'''

    t = Measure((4, 12), "c'8 d'8 e'8 f'8")
    contexttools.detach_time_signature_marks_attached_to_component(t)
    contexttools.TimeSignatureMark((5, 12))(t)
    assert t.is_underfull

    measuretools.append_spacer_skip_to_underfull_measure(t)


    r'''
    {
        \time 5/12
        \scaleDurations #'(2 . 3) {
            c'8
            d'8
            e'8
            f'8
            s1 * 1/8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\ts1 * 1/8\n\t}\n}"


def test_measuretools_append_spacer_skip_to_underfull_measure_02():
    '''Handles regular measure with no meter prolation.'''

    t = Measure((4, 8), "c'8 d'8 e'8 f'8")
    contexttools.detach_time_signature_marks_attached_to_component(t)
    contexttools.TimeSignatureMark((5, 8))(t)
    assert t.is_underfull

    measuretools.append_spacer_skip_to_underfull_measure(t)


    r'''
    {
        \time 5/8
        c'8
        d'8
        e'8
        f'8
        s1 * 1/8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\ts1 * 1/8\n}"
