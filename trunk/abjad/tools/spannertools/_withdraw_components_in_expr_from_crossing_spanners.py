from abjad.tools.componenttools._Component import _Component
from abjad.tools.spannertools.get_spanners_that_cross_components import get_spanners_that_cross_components


def _withdraw_components_in_expr_from_crossing_spanners(components):
    '''This operation can leave score trees in a weird state.
    Operation should only be used in the middle of some other operation.
    Intended purpose is to strip components of crosssing spanners.
    Similar to stripping components of parentage.
    These two operations prepared components for reincorporation.
    Reincorporation means setting into some other score tree.
    Container setitem is probably primary consumer of this operation.
    Return None.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    crossing_spanners = get_spanners_that_cross_components(components)

    components_including_children = list(
        componenttools.iterate_components_forward_in_expr(components, _Component))

    for crossing_spanner in list(crossing_spanners):
        spanner_components = crossing_spanner._components[:]
        for component in components_including_children:
            if component in spanner_components:
                crossing_spanner._components.remove(component)
                #component.spanners._spanners.discard(crossing_spanner)
                component._spanners.discard(crossing_spanner)
