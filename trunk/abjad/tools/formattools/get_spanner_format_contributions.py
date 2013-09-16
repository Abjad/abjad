# -*- encoding: utf-8 -*-


def get_spanner_format_contributions(component):
    r'''Gets spanner format contributions for `component`.

    Dictionary keys equal to format slot;
    dictionary values equal to format contributions.
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

    if isinstance(component, containertools.Container):
        before_contributions = result['before']
        after_contributions = result['after']
    else:
        before_contributions = result['opening']
        after_contributions = result['closing']
    stop_contributions = []
    other_contributions = []

    for spanner in component._get_parentage()._get_spanners():

        # override contributions (in before slot)
        if spanner._is_my_first_leaf(component):
            for contribution in \
                spanner.override._list_format_contributions(
                'override', is_once=False):
                before_contributions.append((spanner, contribution, None))

        # contributions for before slot
        for contribution in spanner._format_before_leaf(component):
            before_contributions.append((spanner, contribution, None))

        # contributions for after slot
        contributions = spanner._format_after_leaf(component)
        for contribution in contributions:
            after_contributions.append((spanner, contribution, None))

        # revert contributions (in after slot)
        if spanner._is_my_last_leaf(component):
            for contribution in \
                spanner.override._list_format_contributions('revert'):
                triple = (spanner, contribution, None)
                if triple not in after_contributions:
                    after_contributions.append(triple)

        # contributions for right slot
        contributions = spanner._format_right_of_leaf(component)
        if contributions:
            if spanner._is_my_last_leaf(component):
                for contribution in contributions:
                    stop_contributions.append((spanner, contribution, None))
            else:
                for contribution in contributions:
                    other_contributions.append((spanner, contribution, None))

    result['right'] = stop_contributions + other_contributions

    for key in result.keys():
        if not result[key]:
            del(result[key])
        else:
            result[key].sort(key=lambda x: x[0].__class__.__name__)
            result[key] = [x[1] for x in result[key]]

    return result
