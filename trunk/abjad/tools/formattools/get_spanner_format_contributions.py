def get_spanner_format_contributions(component):
    '''Get spanner format contributions for `component`.

    Return dictionary with format slot keys and format contributions values.
    '''
    from abjad.tools import containertools
    from abjad.tools import spannertools

    result = {
        'after': [],
        'before': [],
        'closing': [],
        'opening': [],
        'right': [],
    }

    spanners = spannertools.get_spanners_attached_to_any_improper_parent_of_component(component)
    spanners = list(spanners)
    #spanners = [x for x in spanners if not isinstance(x, spannertools.SlurSpanner)]
    spanners.sort(key=lambda x: x.__class__.__name__)

    if isinstance(component, containertools.Container):
        before_contributions = result['before']
        after_contributions = result['after']
    else:
        before_contributions = result['opening']
        after_contributions = result['closing']

    stop_contributions = []
    other_contributions = []

    for spanner in spanners:

        # before
        if spanner._is_my_first_leaf(component):
            contributions = spanner.override._list_format_contributions('override', is_once=False)
            before_contributions.extend(contributions)
        before_contributions.extend(spanner._format_before_leaf(component))

        # after
        after_contributions.extend(spanner._format_after_leaf(component))
        if spanner._is_my_last_leaf(component):
            contributions = spanner.override._list_format_contributions('revert')
            after_contributions.extend(contributions)

        # right
        contributions = spanner._format_right_of_leaf(component)
        if contributions:
            if spanner._is_my_last_leaf(component):
                stop_contributions.extend(contributions)
            else:
                other_contributions.extend(contributions)

    result['right'] = stop_contributions + other_contributions

    ### NEW ###

    for key, value in component._spanner_format_contributions.iteritems():
        result[key].extend(value)

    for key in result.keys():
        if not result[key]:
            del(result[key])

    return result
