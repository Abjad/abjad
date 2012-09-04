from abjad.tools import componenttools


def get_context_marks_attached_to_any_improper_parent_of_component(component):
    r'''.. versionadded:: 2.0

    Get all context marks attached to any improper parent of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})
        >>> contexttools.DynamicMark('f')(staff[0])
        DynamicMark('f')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8 \f
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_context_marks_attached_to_any_improper_parent_of_component(staff[0])
        (DynamicMark('f')(c'8), ClefMark('treble')(Staff{4}))

    Return tuple.
    '''
    from abjad.tools import contexttools

    result = []

    for component in componenttools.get_improper_parentage_of_component(component):
        for mark in component._marks_for_which_component_functions_as_start_component:
            if isinstance(mark, contexttools.ContextMark):
                result.append(mark)

    return tuple(result)
