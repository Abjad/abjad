def mask_intervals_with_intervals(masked_intervals, mask_intervals):
    '''Clip or remove all intervals in `masked_intervals` outside of the bounds
    defined in `mask_intervals`, while maintaining `masked_intervals`' payload contents ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(0, 10, {'a': 1})
        >>> b = TimeInterval(5, 15, {'b': 2})
        >>> tree = TimeIntervalTree([a, b])
        >>> mask = TimeInterval(4, 11)
        >>> timeintervaltools.mask_intervals_with_intervals(tree, mask)
        TimeIntervalTree([
            TimeInterval(Offset(4, 1), Offset(10, 1), {'a': 1}),
            TimeInterval(Offset(5, 1), Offset(11, 1), {'b': 2})
        ])

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    masked_tree = timeintervaltools.TimeIntervalTree(masked_intervals)
    mask_tree = timeintervaltools.TimeIntervalTree(mask_intervals)

    if not masked_tree or not mask_tree:
        return timeintervaltools.TimeIntervalTree([])

    start = min(mask_tree.start, masked_tree.start)
    stop = max(mask_tree.stop, masked_tree.stop)
    not_mask_tree = timeintervaltools.compute_logical_not_of_intervals_in_interval(
        mask_tree, timeintervaltools.TimeInterval(start, stop))

    if not not_mask_tree:
        return masked_tree

    not_mask_tree_bounds = timeintervaltools.get_all_unique_bounds_in_intervals(not_mask_tree)
    split_masked_tree = timeintervaltools.split_intervals_at_rationals(masked_tree, not_mask_tree_bounds)

    for interval in not_mask_tree:
        starts = set(split_masked_tree.find_intervals_starting_within_interval(interval))
        stops = set(split_masked_tree.find_intervals_stopping_within_interval(interval))
        intersection = set(starts).intersection(set(stops))
        split_masked_tree = timeintervaltools.TimeIntervalTree(
            list(set(split_masked_tree).difference(intersection)))

    return split_masked_tree
