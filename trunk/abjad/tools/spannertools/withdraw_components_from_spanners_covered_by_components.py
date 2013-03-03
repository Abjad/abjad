from abjad.tools import componenttools


def withdraw_components_from_spanners_covered_by_components(components):
    '''Find every spanner covered by 'components'.
    Withdraw all components in 'components' from covered spanners.
    Return 'components'.
    The operation always leaves all score trees in tact.

    Return components.
    '''
    from abjad.tools import spannertools

    # check components
    assert componenttools.all_are_thread_contiguous_components(components)

    # withdraw from covered spanners
    for spanner in spannertools.get_spanners_covered_by_components(components):
        spanner.clear()

    # return components
    return components
