from abjad.tools.contexttools.get_time_signature_marks_attached_to_component import get_time_signature_marks_attached_to_component


def detach_time_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach time signature marks attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> contexttools.TimeSignatureMark((4, 4))(staff[0])
        TimeSignatureMark((4, 4))(c'4)

    ::

        abjad> f(staff)
        \new Staff {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_time_signature_marks_attached_to_component(staff[0])
        (TimeSignatureMark((4, 4)),)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more time signature marks.
    '''

    marks = []
    for mark in get_time_signature_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)    
