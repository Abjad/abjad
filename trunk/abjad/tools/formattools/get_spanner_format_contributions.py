def get_spanner_format_contributions(component):
    '''Get spanner format contributions for `leaf` as a dictionary 
    of format_slot:contributions key:value pairs.

    Return dict.
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
    spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))

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
            contributions = spanner.override._list_format_contributions('override', is_once = False)
            before_contributions.extend(contributions)
        if hasattr(spanner, '_format_before_leaf'):
            before_contributions.extend(spanner._format_before_leaf(component))
        else:
            before_contributions.extend(spanner._format._before(component))

        # after
        if hasattr(spanner, '_format_after_leaf'):
            after_contributions.extend(spanner._format_after_leaf(component))
        else:
            after_contributions.extend(spanner._format._after(component))
        if spanner._is_my_last_leaf(component):
            contributions = spanner.override._list_format_contributions('revert')
            after_contributions.extend(contributions)

        # right
        if hasattr(spanner, '_format_right_of_leaf'):
            contributions = spanner._format_right_of_leaf(component)
        else:
            contributions = spanner._format._right(component)
        if contributions:
            if spanner._is_my_last_leaf(component):
                stop_contributions.extend(contributions)
            else:
                other_contributions.extend(contributions)

    result['right'] = stop_contributions + other_contributions

    for key in result.keys():
        if not result[key]:
            del(result[key])

    return result

