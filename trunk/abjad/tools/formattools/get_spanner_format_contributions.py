def get_spanner_format_contributions(leaf):
    '''Get spanner format contributions for `leaf` as a dictionary 
    of format_slot:contributions key:value pairs.

    Return dict.
    '''

    from abjad.tools import spannertools

    result = {
        'before': [],
        'right': [],
        'after': [],
    }

    spanners = spannertools.get_spanners_attached_to_any_improper_parent_of_component(leaf)
    spanners = list(spanners)
    spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))

    before_contributions = result['before']
    after_contributions = result['after']
    stop_contributions = []
    other_contributions = []

    for spanner in spanners:

        # before
        if spanner._is_my_first_leaf(leaf):
            contributions = spanner.override._list_format_contributions('override', is_once = False)
            before_contributions.extend(contributions)
        if hasattr(spanner, '_format_before_leaf'):
            before_contributions.extend(spanner._format_before_leaf(leaf))
        else:
            before_contributions.extend(spanner._format._before(leaf))

        # after
        if hasattr(spanner, '_format_after_leaf'):
            after_contributions.extend(spanner._format_after_leaf(leaf))
        else:
            after_contributions.extend(spanner._format._after(leaf))
        if spanner._is_my_last_leaf(leaf):
            contributions = spanner.override._list_format_contributions('revert')
            after_contributions.extend(contributions)

        # right
        if hasattr(spanner, '_format_right_of_leaf'):
            contributions = spanner._format_right_of_leaf(leaf)
        else:
            contributions = spanner._format._right(leaf)
        if contributions:
            if spanner._is_my_last_leaf(leaf):
                stop_contributions.extend(contributions)
            else:
                other_contributions.extend(contributions)

    result['right'] = stop_contributions + other_contributions

    for key in result.keys():
        if not result[key]:
            del(result[key])

    return result
