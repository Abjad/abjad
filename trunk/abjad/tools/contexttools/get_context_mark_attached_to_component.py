from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_context_mark_attached_to_component(component, klasses=(ContextMark,)):
    r'''.. versionadded:: 2.3

    Get context mark attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_context_mark_attached_to_component(staff)
        ClefMark('treble')(Staff{4})

    Return context mark.

    Raise missing mark error when no context mark attaches to `component`.
    '''

    context_marks = get_context_marks_attached_to_component(component, klasses = klasses)

    if len(context_marks) == 0:
        raise MissingMarkError
    elif 1 < len(context_marks):
        raise ExtraMarkError
    else:
        return context_marks[0]
