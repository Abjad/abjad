def _withdraw_component_from_attached_spanners(component):
    '''Withdraw `component` from all attached spanners.
    '''

    for spanner in component.spanners:
        spanner._remove(component)
