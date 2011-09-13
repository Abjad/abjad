from abjad.tools.componenttools._Component import _Component
from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


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
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components,
        allow_orphans = False)

    receipt = set([])

    if len(components) == 0:
        return receipt

    first, last = components[0], components[-1]

    start_components = first._navigator._contemporaneous_start_contents
    stop_components = set(last._navigator._contemporaneous_stop_contents)
    for component in start_components:
        #for spanner in component.spanners.attached:
        for spanner in get_spanners_attached_to_component(component):
            if set(spanner[:]) & stop_components != set([]):
                index = spanner.index(component)
                receipt.add((spanner, index))

    return receipt
