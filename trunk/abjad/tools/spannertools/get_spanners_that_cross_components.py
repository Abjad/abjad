from abjad.tools import componenttools


def get_spanners_that_cross_components(components):
    '''Assert thread-contiguous components.
    Collect spanners that attach to any component in 'components'.
    Return unordered set of crossing spanners.
    A spanner P crosses a list of thread-contiguous components C
    when P and C share at least one component and when it is the
    case that NOT ALL of the components in P are also in C.
    In other words, there is some intersection -- but not total
    intersection -- between the components of P and C.

    Compare 'crossing' spanners with 'covered' spanners.
    Compare 'crossing' spanners with 'dominant' spanners.
    Compare 'crossing' spanners with 'contained' spanners.
    Compare 'crossing' spanners with 'attached' spanners.

    Return spanners.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    assert componenttools.all_are_thread_contiguous_components(components)

    all_components = set(iterationtools.iterate_components_in_expr(components))
    contained_spanners = spannertools.get_spanners_contained_by_components(components)
    crossing_spanners = set([])
    for spanner in contained_spanners:
        spanner_components = set(spanner[:])
        if not spanner_components.issubset(all_components):
            crossing_spanners.add(spanner)

    return crossing_spanners
