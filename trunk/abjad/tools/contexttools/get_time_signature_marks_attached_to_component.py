from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_time_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get time signature marks attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.TimeSignatureMark((2, 4))(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \time 2/4
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_time_signature_marks_attached_to_component(staff)
        (TimeSignatureMark((2, 4))(Staff{4}),)

    Return tuple of zero or more time_signature marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(TimeSignatureMark,))
