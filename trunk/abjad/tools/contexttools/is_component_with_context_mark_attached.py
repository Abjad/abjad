from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def is_component_with_context_mark_attached(component, klasses = (ContextMark, )):
    r'''.. versionadded:: 2.0

    True when context mark of `klasses` attaches to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.TimeSignatureMark((4, 8))(staff[0])
        TimeSignatureMark((4, 8))(c'8)
        abjad> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
        abjad> contexttools.is_component_with_context_mark_attached(staff[0])
        True

    Otherwise false::

        abjad> contexttools.is_component_with_context_mark_attached(staff)
        False

    Return boolean.
    '''

    context_marks_attached = get_context_marks_attached_to_component(component, klasses = klasses)

    if 1 <= len(context_marks_attached):
        return True
    else:
        return False


