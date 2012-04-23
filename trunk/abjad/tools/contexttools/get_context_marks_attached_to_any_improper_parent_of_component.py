from abjad.tools.contexttools.Context import Context
from abjad.tools.contexttools.ContextMark import ContextMark


def get_context_marks_attached_to_any_improper_parent_of_component(component):


    r'''.. versionadded:: 2.0

    Get all context marks attached to any improper parent of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})
        abjad> contexttools.DynamicMark('f')(staff[0])
        DynamicMark('f')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8 \f
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_context_marks_attached_to_any_improper_parent_of_component(staff[0]) # doctest: +SKIP
        set([DynamicMark('f')(c'8), ClefMark('treble')(Staff{4})])

    Return unordered set of zero or more context marks.
    '''
    from abjad.tools import componenttools

    # changing result from a set to a list causes intermittently failing format in a few tests; why?
    # something to do with offset interface?
    result = set([])

    for component in componenttools.get_improper_parentage_of_component(component):
        for mark in component._marks_for_which_component_functions_as_start_component:
            if isinstance(mark, ContextMark):
                if mark not in result:
                    result.add(mark)

    return result
