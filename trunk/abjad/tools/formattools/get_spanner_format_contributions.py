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
    #spanners = list(spanners)
    #spanners = [x for x in spanners if not isinstance(x, spannertools.SlurSpanner)]
    #spanners.sort(key=lambda x: x.__class__.__name__)

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
            #before_contributions.extend(contributions)
            for contribution in contributions:
                before_contributions.append((spanner.__class__.__name__, contribution))
        #before_contributions.extend(spanner._format_before_leaf(component))
        contributions = spanner._format_before_leaf(component)
        for contribution in contributions:
            before_contributions.append((spanner.__class__.__name__, contribution))

        # after
        #after_contributions.extend(spanner._format_after_leaf(component))
        contributions = spanner._format_after_leaf(component)
        for contribution in contributions:
            after_contributions.append((spanner.__class__.__name__, contribution))
        if spanner._is_my_last_leaf(component):
            contributions = spanner.override._list_format_contributions('revert')
            #after_contributions.extend(contributions)
            for contribution in contributions:
                after_contributions.append((spanner.__class__.__name__, contribution))

        # right
        contributions = spanner._format_right_of_leaf(component)
        if contributions:
            if spanner._is_my_last_leaf(component):
                #stop_contributions.extend(contributions)
                for contribution in contributions:
                    stop_contributions.append((spanner.__class__.__name__, contribution))
            else:
                #other_contributions.extend(contributions)
                for contribution in contributions:
                    other_contributions.append((spanner.__class__.__name__, contribution))

    result['right'] = stop_contributions + other_contributions

    ### NEW ###
    for key, value in component._spanner_format_contributions.iteritems():
        for class_name, contribution in value:
            result[key].append(contribution)

    for key in result.keys():
        result[key].sort(key=lambda x: x[0])
        result[key] = [x[-1] for x in result[key]]

    for key in result.keys():
        if not result[key]:
            del(result[key])

    return result
