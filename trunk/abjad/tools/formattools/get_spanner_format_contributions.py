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
    #spanners.sort(key=lambda x: x.__class__.__name__)
    spanners_that_know_how_to_deposit_format_contributions = (
        spannertools.SlurSpanner,
        )

    if isinstance(component, containertools.Container):
        before_contributions = result['before']
        after_contributions = result['after']
    else:
        before_contributions = result['opening']
        after_contributions = result['closing']
    stop_contributions = []
    other_contributions = []

    for spanner in spanners:
        if isinstance(spanner, spanners_that_know_how_to_deposit_format_contributions):
            continue

        # override contributions (in before slot)
        if spanner._is_my_first_leaf(component):
            contributions = spanner.override._list_format_contributions('override', is_once=False)
            #before_contributions.extend(contributions)
            for contribution in contributions:
                before_contributions.append((spanner, contribution, None))

        # contributions for before slot
        #before_contributions.extend(spanner._format_before_leaf(component))
        contributions = spanner._format_before_leaf(component)
        for contribution in contributions:
            before_contributions.append((spanner, contribution, None))

        # contributions for after slot
        #after_contributions.extend(spanner._format_after_leaf(component))
        contributions = spanner._format_after_leaf(component)
        for contribution in contributions:
            after_contributions.append((spanner, contribution, None))

        # revert contributions (in after slot)
        if spanner._is_my_last_leaf(component):
            contributions = spanner.override._list_format_contributions('revert')
            #after_contributions.extend(contributions)
            for contribution in contributions:
                after_contributions.append((spanner, contribution, None))

        # contributions for right slot
        contributions = spanner._format_right_of_leaf(component)
        if contributions:
            if spanner._is_my_last_leaf(component):
                #stop_contributions.extend(contributions)
                for contribution in contributions:
                    stop_contributions.append((spanner, contribution, None))
            else:
                #other_contributions.extend(contributions)
                for contribution in contributions:
                    other_contributions.append((spanner, contribution, None))

    result['right'] = stop_contributions + other_contributions

    for format_slot_name, pairs in component._spanner_format_contributions.iteritems():
        result[format_slot_name].extend(pairs)

    # sort first by spanner class name;
    # sort next by spanner start offset; 
    # sort last by position of component within spanner
    def compare_contributions(contribution_1, contribution_2):
        left_class_name = contribution_1[0].__class__.__name__
        right_class_name = contribution_2[0].__class__.__name__
        if left_class_name == right_class_name:
            left_start_offset = getattr(contribution_1[0], 'start_offset', None)
            right_start_offset = getattr(contribution_2[0], 'start_offset', None)
            if left_start_offset == right_start_offset:
                if contribution_1[2] == contribution_2[2]:
                    return 0
                elif contribution_1[2] == 'first leaf in spanner':
                    return -1
                elif contribution_1[2] == 'last leaf in spanner':
                    return 1
                elif contribution_2[2] == 'first leaf in spanner':
                    return 1
                elif contribution_2[2] == 'last leaf in spanner':
                    return -1
                else:
                    return 0
            else:
                return cmp(left_start_offset, right_start_offset)
        else:
            return cmp(left_class_name, right_class_name)

    for key in result.keys():
        result[key].sort(cmp=compare_contributions)
        result[key] = [x[1] for x in result[key]]

    for key in result.keys():
        if not result[key]:
            del(result[key])

    return result
