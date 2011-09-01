from abjad.tools.marktools.StemTremolo import StemTremolo
from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError


def get_stem_tremolo_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get stem tremolo attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.StemTremolo(16)(staff[0])
        StemTremolo(16)(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 :16
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_stem_tremolo_attached_to_component(staff[0])
        StemTremolo(16)(c'8)

    Raise missing mark error when no stem tremolo attaches to `component`.

    Raise extra mark error when more than one stem tremolo attaches to `component`.

    Return stem tremolo.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, StemTremolo):
            result.append(mark)

    if len(result) == 0:
        raise MissingMarkError
    elif 1 < len(result) :
        raise ExtraMarkError
    else:
        return result[0]
