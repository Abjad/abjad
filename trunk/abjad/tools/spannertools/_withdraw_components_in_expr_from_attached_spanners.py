from abjad.tools.componenttools._Component import _Component
from abjad.tools.spannertools._withdraw_component_from_attached_spanners import _withdraw_component_from_attached_spanners


def _withdraw_components_in_expr_from_attached_spanners(components):
    '''Find every spanner contained in 'components'.
    Withdraw all components in 'components' from spanners.
    Return 'components'.
    The operation may leave discontiguous spanners.
    '''
    from abjad.tools import componenttools

    # check components
    assert componenttools.all_are_thread_contiguous_components(components)

    # withdraw from contained spanners
    for component in componenttools.iterate_components_forward_in_expr(components, _Component):
        _withdraw_component_from_attached_spanners(component)

    # return components
    return components
