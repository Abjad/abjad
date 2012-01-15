from abjad.tools.spannertools.get_spanners_attached_to_any_improper_child_of_component import get_spanners_attached_to_any_improper_child_of_component


def get_spanners_contained_by_components(components):
    '''Return unordered set of spanners contained within
    any component in list of thread-contiguous components.
    Getter for t.spanners.contained across thread-contiguous components.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_contained()`` to
        ``spannertools.get_spanners_contained_by_components()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    result = set([])
    for component in components:
        result.update(get_spanners_attached_to_any_improper_child_of_component(component))
    return result
