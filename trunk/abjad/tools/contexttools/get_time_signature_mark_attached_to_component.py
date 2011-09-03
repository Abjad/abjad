from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark
from abjad.tools.contexttools.get_context_mark_attached_to_component import get_context_mark_attached_to_component


def get_time_signature_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get time signature mark attached to `component`::

        abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

    ::

        abjad> f(measure)
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_time_signature_mark_attached_to_component(measure)
        TimeSignatureMark((4, 8))(|4/8, c'8, d'8, e'8, f'8|)

    Return time signature mark.

    Raise missing mark error when no time signature mark attaches to `component`.
    '''

    return get_context_mark_attached_to_component(component, klasses=(TimeSignatureMark,))
