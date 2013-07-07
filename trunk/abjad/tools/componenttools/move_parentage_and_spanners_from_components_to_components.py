def move_parentage_and_spanners_from_components_to_components(
    donors, recipients):
    '''.. versionadded:: 1.1

    Move parentage and spanners from `donors` to `recipients`.

    Give everything from donors to recipients.

    Almost exactly the same as container setitem logic.

    This function works with orphan donors.

    Container setitem logic can not work with orphan donors.

    Return none.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools
    from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import \
        _withdraw_components_in_expr_from_crossing_spanners

    # check input
    assert componenttools.all_are_contiguous_components_in_same_parent(
        donors)
    assert componenttools.all_are_contiguous_components_in_same_parent(
        recipients)

    # coerce input
    if not isinstance(donors, selectiontools.Selection):
        donors = selectiontools.Selection(donors)

    # return donors unaltered when donors are empty
    if len(donors) == 0:
        return donors

    # give parentage and spanners to recipients
    parent, start, stop = donors.get_parent_and_start_stop_indices()
    if parent:
        parent.__setitem__(slice(start, stop + 1), recipients)
    else:
        donors._give_dominant_spanners_to_components(recipients)
        _withdraw_components_in_expr_from_crossing_spanners(donors)
