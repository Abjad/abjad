from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark


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
        TimeSignatureMark(4, 8)(|4/8, c'8, d'8, e'8, f'8|)

    Return time signature mark.

    Raise missing mark error when no time signature mark attaches to `component`.
    '''

    result = [ ]
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, TimeSignatureMark):
            result.append(mark)

    if len(result) == 0:
        raise MissingMarkError
    if 1 < len(result):
        raise ExtraMarkError

    result = result[0]

    return result


