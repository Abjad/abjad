def move_parentage_and_spanners_from_components_to_components(donors, recipients):
    '''.. versionadded:: 1.1

    Move parentage and spanners from `donors` to `recipients`.

    Give everything from donors to recipients.
    Almost exactly the same as container setitem logic.
    This helper works with orphan donors.
    Container setitem logic can not work with orphan donors.
    Return donors.

    .. versionchanged:: 2.0
        renamed ``scoretools.bequeath()`` to
        ``componenttools.move_parentage_and_spanners_from_components_to_components()``.
    '''
    from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components import _give_spanners_that_dominate_donor_components_to_recipient_components
    from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import _withdraw_components_in_expr_from_crossing_spanners
    from abjad.tools import componenttools

    assert componenttools.all_are_contiguous_components_in_same_parent(donors)
    assert componenttools.all_are_contiguous_components_in_same_parent(recipients)

    if len(donors) == 0:
        return donors

    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(donors)
    if parent:
        parent[start:stop+1] = recipients
        return donors
    else:
        _give_spanners_that_dominate_donor_components_to_recipient_components(donors, recipients)
        _withdraw_components_in_expr_from_crossing_spanners(donors)

    return donors
