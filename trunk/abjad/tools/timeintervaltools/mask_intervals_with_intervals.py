# -*- encoding: utf-8 -*-
def mask_intervals_with_intervals(masked_intervals, mask_intervals):
    r'''Clip or remove all intervals in `masked_intervals` outside of the bounds
    defined in `mask_intervals`, while maintaining `masked_intervals`' payload
    contents:
    
    ::

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

    start_offset = min(mask_tree.start_offset, masked_tree.start_offset)
    stop_offset = max(mask_tree.stop_offset, masked_tree.stop_offset)
    not_mask_tree = mask_tree.compute_logical_not(
        bounding_interval=timeintervaltools.TimeInterval(
            start_offset, stop_offset))

    if not not_mask_tree:
        return masked_tree

    not_mask_tree_bounds = not_mask_tree.all_unique_bounds
    split_masked_tree = timeintervaltools.TimeIntervalTree(
        masked_tree.split_at_rationals(*not_mask_tree_bounds))

    for interval in not_mask_tree:
        starts = set(split_masked_tree.find_intervals_starting_within_interval(
            interval))
        stops = set(split_masked_tree.find_intervals_stopping_within_interval(
            interval))
        intersection = set(starts).intersection(set(stops))
        split_masked_tree = timeintervaltools.TimeIntervalTree(
            list(set(split_masked_tree).difference(intersection)))

    return split_masked_tree
