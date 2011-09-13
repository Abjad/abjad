from abjad.tools.componenttools._Component import _Component
from abjad.tools.spannertools.get_spanners_contained_by_components import get_spanners_contained_by_components
from abjad.tools.spannertools.get_spanners_covered_by_components import get_spanners_covered_by_components


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

    .. versionchanged:: 2.0
        renamed ``spannertools.get_crossing()`` to
        ``spannertools.get_spanners_that_cross_components()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    all_components = set(componenttools.iterate_components_forward_in_expr(components, _Component))
    contained_spanners = get_spanners_contained_by_components(components)
    crossing_spanners = set([])
    for spanner in contained_spanners:
        spanner_components = set(spanner[:])
        if not spanner_components.issubset(all_components):
            crossing_spanners.add(spanner)

    return crossing_spanners
