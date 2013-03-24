from abjad.tools import componenttools


def get_spanners_covered_by_components(components):
    '''.. versionadded:: 1.1

    Get spanners covered by `components`.

    Return unordered set of  spanners completely contained
    within the time bounds of thread-contiguous components.

    A spanner `p` is covered by timespan `t` when and only when
    ``t.start_ofset <= p.timespan.start_offset and p.timespan.stop_offset <= t.timespan.stop_offset``.
    '''
    from abjad.tools import spannertools

    assert componenttools.all_are_thread_contiguous_components(components)

    if not len(components):
        return set([])

    first, last = components[0], components[-1]
    components_begin = first.timespan.start_offset
    components_end = last.timespan.stop_offset

    result = spannertools.get_spanners_contained_by_components(components)
    for spanner in list(result):
        if spanner.timespan.start_offset < components_begin or components_end < spanner.timespan.stop_offset:
            result.discard(spanner)

    return result
