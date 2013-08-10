# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_covered_by_components(components):
    '''Get spanners covered by `components`.

    Return unordered set of  spanners completely contained
    within the time bounds of thread-contiguous components.

    A spanner `p` is covered by timespan `t` when and only when
    ``t.start_ofset <= more(p).get_timespan().start_offset and 
    more(p).get_timespan().stop_offset <= t.stop_offset``.
    '''
    from abjad.tools import spannertools

    assert componenttools.all_are_thread_contiguous_components(components)

    if not len(components):
        return set([])

    first, last = components[0], components[-1]
    components_begin = first._get_timespan().start_offset
    components_end = last._get_timespan().stop_offset

    result = spannertools.get_spanners_contained_by_components(components)
    for spanner in list(result):
        if spanner.get_timespan().start_offset < components_begin or \
            components_end < spanner.get_timespan().stop_offset:
            result.discard(spanner)

    return result
