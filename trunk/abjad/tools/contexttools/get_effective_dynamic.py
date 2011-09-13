from abjad.tools.contexttools.DynamicMark import DynamicMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_dynamic(component):
    r'''.. versionadded:: 2.0

    Get effective dynamic of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.DynamicMark('f')(staff[0])
        DynamicMark('f')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    ::

        abjad> for note in staff:
        ...     print note, contexttools.get_effective_dynamic(note)
        ...
        c'8 DynamicMark('f')(c'8)
        d'8 DynamicMark('f')(c'8)
        e'8 DynamicMark('f')(c'8)
        f'8 DynamicMark('f')(c'8)

    Return dynamic mark or none.
    '''

    return get_effective_context_mark(component, DynamicMark)
