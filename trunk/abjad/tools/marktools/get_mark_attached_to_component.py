from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.marktools.get_marks_attached_to_component import get_marks_attached_to_component


def get_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get exactly one mark attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Mark()(staff[0])
        Mark()(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_mark_attached_to_component(staff[0])
        Mark()(c'8)

    Return one mark.

    Raise missing mark error when no mark is attached.

    Raise extra mark error when more than one mark is attached.
    '''

    marks = get_marks_attached_to_component(component)
    if not marks:
        raise MissingMarkError
    elif 1 < len(marks):
        raise ExtraMarkError
    else:
        return marks[0]
