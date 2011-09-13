from abjad.tools.spannertools._withdraw_component_from_attached_spanners import _withdraw_component_from_attached_spanners

def _withdraw_components_from_attached_spanners(components):
    '''Withdraw `components` from attached spanners.

    Unspan every component in components.
    Does not navigate down into components; traverse shallowly.
    Return components.

    Note that you can leave noncontiguous notes spanned
    after apply unspan_components to components in the
    middle of some larger spanner.
    '''
    from abjad.tools import componenttools

    # check input
    assert componenttools.all_are_components(components)

    # detach spanners
    for component in components:
        #component.spanners._detach()
        _withdraw_component_from_attached_spanners(component)

    # return components
    return components
