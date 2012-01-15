from abjad.tools.spannertools.get_spanners_covered_by_components import get_spanners_covered_by_components


def withdraw_components_from_spanners_covered_by_components(components):
    '''Find every spanner covered by 'components'.
    Withdraw all components in 'components' from covered spanners.
    Return 'components'.
    The operation always leaves all score trees in tact.

    .. versionchanged:: 2.0
        renamed ``spannertools.withdraw_from_covered()`` to
        ``spannertools.withdraw_components_from_spanners_covered_by_components()``.
    '''
    from abjad.tools import componenttools

    # check components
    assert componenttools.all_are_thread_contiguous_components(components)

    # withdraw from covered spanners
    for spanner in get_spanners_covered_by_components(components):
        spanner.clear()

    # return components
    return components
