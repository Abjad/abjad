from abjad.tools import componenttools


def get_spanners_that_dominate_components(components):
    '''Return Python list of (spanner, index) pairs.
    Each (spanner, index) pair gives a spanner which dominates
    all components in 'components' together with the start-index
    at which spanner first encounters 'components'.

    Use this helper to 'lift' any and all spanners temporarily
    from 'components', perform some action to the underlying
    score tree, and then reattach all spanners to new
    score components.

    This operation always leaves all expressions in tact.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_dominant()`` to
        ``spannertools.get_spanners_that_dominate_components()``.
    '''
    from abjad.tools import spannertools

    assert componenttools.all_are_thread_contiguous_components(components,
        allow_orphans = False)

    receipt = set([])

    if len(components) == 0:
        return receipt

    first, last = components[0], components[-1]

    start_components = componenttools.get_improper_descendents_of_component_that_start_with_component(first)
    stop_components = componenttools.get_improper_descendents_of_component_that_stop_with_component(last)
    stop_components = set(stop_components)
    for component in start_components:
        for spanner in spannertools.get_spanners_attached_to_component(component):
            if set(spanner[:]) & stop_components != set([]):
                index = spanner.index(component)
                receipt.add((spanner, index))

    return receipt
