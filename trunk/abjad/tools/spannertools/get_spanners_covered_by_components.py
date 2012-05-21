from abjad.tools.spannertools.get_spanners_contained_by_components import get_spanners_contained_by_components


def get_spanners_covered_by_components(components):
    '''Return unordered set of  spanners completely contained
        within the time bounds of thread-contiguous components.

        Compare 'covered' spanners with 'contained' spanners.
        Compare 'covered' spanners with 'dominant' spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_covered()`` to
        ``spannertools.get_spanners_covered_by_components()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    if not len(components):
        return set([])

    first, last = components[0], components[-1]
    components_begin = first.start_offset
    components_end = last.stop_offset

    result = get_spanners_contained_by_components(components)
    for spanner in list(result):
        if spanner.start_offset < components_begin or components_end < spanner.stop_offset:
            result.discard(spanner)

    return result
